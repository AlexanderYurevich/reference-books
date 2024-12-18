import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import tkinter as tk
from sqlalchemy import text
from tkinter import ttk, messagebox
from tkcalendar import DateEntry


# Информация об авторе
AUTHOR_INFO = "\nФИО: Юревич А.Н.\nКурс: 3\nГруппа: 11\nГод: 2024"

# Параметры подключения к базе данных
DB_CONNECTION_STRING = "mssql+pyodbc://@DESKTOP-MTF3688\SQLEXPRESS/CSAB?driver=ODBC+Driver+17+for+SQL+Server"

# SQL запросы
QUERIES = {
    "Order": "SELECT ID, CreateAt, CustomerName, CustomerEmail, DeliveryType, Rate FROM [Order]",
    "Product": "SELECT ID, ProductName, Price, Quantity, OrderID FROM Product"
}

# Создание подключения к базе данных
with create_engine(DB_CONNECTION_STRING).connect() as engine:
    
    def fetch_data(table_name):
        """Получение данных из указанного справочника."""
        try:
            query = QUERIES[table_name]
            data = pd.read_sql(query, engine)
            return data
        except SQLAlchemyError as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные: {e}")
            return pd.DataFrame()
    
    def sort_table(data, column, ascending):
        """Сортировка таблицы по указанной колонке."""
        if column == "CreateAt":
            data[column] = pd.to_datetime(data[column], format="%Y-%m-%d")
        return data.sort_values(by=column, ascending=ascending)
    
    def display_table(table_name):
        """Отображение данных справочника с выпадающим списком для ID (только при редактировании)."""
        data = fetch_data(table_name)
        if data.empty:
            return
    
        def sort_and_refresh(col):
            nonlocal data
            ascending = col not in sort_and_refresh.sorted or not sort_and_refresh.sorted[col]
            sort_and_refresh.sorted[col] = ascending
            sorted_data = sort_table(data, col, ascending)
            refresh_table(sorted_data)
    
        sort_and_refresh.sorted = {}
    
        def refresh_table(data):
            for item in tree.get_children():
                tree.delete(item)
            for _, row in data.iterrows():
                tree.insert("", "end", values=[row[col] for col in data.columns])
    
        def update_id_combobox():
            """Обновление списка ID в выпадающем списке."""
            nonlocal data
            data = fetch_data(table_name)
    
        def add_record():
            add_window = tk.Toplevel(root)
            add_window.title("Добавление записи")
    
            fields = list(data.columns)
            entries = {}
    
            for i, field in enumerate(fields):
                label = tk.Label(add_window, text=field, font=("Arial", 12))
                label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
    
                if field == "ID":
                    entry = tk.Entry(add_window)  # Поле для ручного ввода ID
                elif field == "CreateAt":
                    entry = DateEntry(add_window, date_pattern='yyyy/mm/dd')
                elif field in ["Rate", "Price"]:
                    entry = tk.Entry(add_window, validate="key", validatecommand=(add_window.register(lambda val: val.replace('.', '', 1).isdigit()), '%P'))
                elif field in ["DeliveryType"]:
                    entry = ttk.Combobox(add_window, values=["Курьер", "Самовывоз"], state="readonly")
                else:
                    entry = tk.Entry(add_window)
    
                entry.grid(row=i, column=1, padx=10, pady=5)
                entries[field] = entry
    
            def save():
                record = {field: entries[field].get() for field in fields}
                try:
                    insert_query = f"INSERT INTO [{table_name}] (" + ", ".join(fields) + ") VALUES (" + ", ".join(f":{col}" for col in fields) + ")"
                    engine.execute(text(insert_query), record)
                    refresh_table(fetch_data(table_name))
                    engine.commit()
                    update_id_combobox()  # Обновление списка ID после добавления
                    add_window.destroy()
                except SQLAlchemyError as e:
                    messagebox.showerror("Ошибка", f"Не удалось сохранить запись: {e}")
    
            save_button = tk.Button(add_window, text="Сохранить", command=save)
            save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)
    
        def edit_record(item_id):
            edit_window = tk.Toplevel(root)
            edit_window.title("Редактирование записи")
    
            fields = list(data.columns)
            entries = {}
    
            for i, field in enumerate(fields):
                label = tk.Label(edit_window, text=field, font=("Arial", 12))
                label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
    
                if field == "ID":
                    # Выпадающий список для ID
                    id_combo = ttk.Combobox(edit_window, values=list(fetch_data(table_name)["ID"]), state="readonly")
                    id_combo.grid(row=i, column=1, padx=10, pady=5)
                    entries[field] = id_combo
                elif field == "CreateAt":
                    entry = DateEntry(edit_window, date_pattern='yyyy/mm/dd')
                elif field in ["Rate", "Price"]:
                    entry = tk.Entry(edit_window, validate="key", validatecommand=(edit_window.register(lambda val: val.replace('.', '', 1).isdigit()), '%P'))
                elif field in ["DeliveryType"]:
                    entry = ttk.Combobox(edit_window, values=["Курьер", "Самовывоз"], state="readonly")
                else:
                    entry = tk.Entry(edit_window)
    
                if field != "ID":
                    entry.grid(row=i, column=1, padx=10, pady=5)
                    entries[field] = entry
    
            def save():
                record = {field: entries[field].get() for field in fields}
                try:
                    update_query = f"UPDATE [{table_name}] SET " + ", ".join(f"{col} = :{col}" for col in fields) + " WHERE ID = :ID"
                    print(update_query)
                    #record["ID"] = item_id
                    print(record)
                    engine.execute(text(update_query), record)
                    engine.commit()
                    refresh_table(fetch_data(table_name))
                    edit_window.destroy()
                except SQLAlchemyError as e:
                    messagebox.showerror("Ошибка", f"Не удалось сохранить запись: {e}")
    
            save_button = tk.Button(edit_window, text="Сохранить", command=save)
            save_button.grid(row=len(fields), column=0, columnspan=2, pady=10)
    
        def delete_record():
            delete_window = tk.Toplevel(root)
            delete_window.title("Удаление записи")
    
            label = tk.Label(delete_window, text="Выберите поле для удаления:", font=("Arial", 12))
            label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    
            field_combo = ttk.Combobox(delete_window, values=list(data.columns), state="readonly")
            field_combo.grid(row=0, column=1, padx=10, pady=5)
    
            value_label = tk.Label(delete_window, text="Введите значение:", font=("Arial", 12))
            value_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    
            value_entry = tk.Entry(delete_window)
            value_entry.grid(row=1, column=1, padx=10, pady=5)
    
            def confirm_delete():
                field = field_combo.get()
                value = value_entry.get()
                if not field or not value:
                    messagebox.showwarning("Предупреждение", "Пожалуйста, выберите поле и введите значение.")
                    return
    
                try:
                    delete_query = f"DELETE FROM [{table_name}] WHERE {field} = :value"
                    engine.execute(text(delete_query), {"value": value})
                    engine.commit()
                    refresh_table(fetch_data(table_name))
                    update_id_combobox()  # Обновление списка ID после удаления
                    delete_window.destroy()
                except SQLAlchemyError as e:
                    messagebox.showerror("Ошибка", f"Не удалось удалить запись: {e}")
    
            delete_button = tk.Button(delete_window, text="Удалить", command=confirm_delete)
            delete_button.grid(row=2, column=0, columnspan=2, pady=10)
    
        def view_record():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Предупреждение", "Выберите запись для просмотра.")
                return
    
            item_id = tree.item(selected_item[0])['values'][0]
            record = data[data['ID'] == item_id]
            view_window = tk.Toplevel(root)
            view_window.title("Просмотр записи")
    
            for i, (col, value) in enumerate(record.iloc[0].items()):
                label = tk.Label(view_window, text=f"{col}: {value}", font=("Arial", 12))
                label.pack(anchor=tk.W, padx=10, pady=5)
    
        top = tk.Toplevel(root)
        top.title(f"Справочник: {table_name}")
    
        tree = ttk.Treeview(top, columns=list(data.columns), show="headings")
        for col in data.columns:
            tree.heading(col, text=col, command=lambda c=col: sort_and_refresh(c))
            tree.column(col, anchor=tk.W)
        tree.pack(expand=True, fill=tk.BOTH)
    
        refresh_table(data)
    
        button_frame = tk.Frame(top)
        button_frame.pack(pady=10)
    
        add_button = tk.Button(button_frame, text="Добавить", command=add_record)
        add_button.pack(side=tk.LEFT, padx=5)
    
        edit_button = tk.Button(button_frame, text="Редактировать", command=lambda: edit_record(tree.item(tree.selection()[0])['values'][0] if tree.selection() else None))
        edit_button.pack(side=tk.LEFT, padx=5)
    
        delete_button = tk.Button(button_frame, text="Удалить", command=delete_record)
        delete_button.pack(side=tk.LEFT, padx=5)
    
        view_button = tk.Button(button_frame, text="Просмотр", command=view_record)
        view_button.pack(side=tk.LEFT, padx=5)
    # Основной интерфейс приложения
    root = tk.Tk()
    root.title("Приложение для работы со справочниками")
    root.geometry("600x400")
    
    title_label = tk.Label(root, text="Приложение для работы со справочниками", font=("Arial", 16))
    title_label.pack(pady=10)
    
    info_label = tk.Label(root, text=AUTHOR_INFO, font=("Arial", 10), justify=tk.LEFT)
    info_label.pack(pady=5)
    
    frame = tk.Frame(root)
    frame.pack(pady=20)
    
    select_label = tk.Label(frame, text="Выберите справочник:", font=("Arial", 12))
    select_label.grid(row=0, column=0, padx=10)
    
    selected_table = tk.StringVar()
    
    combo = ttk.Combobox(frame, textvariable=selected_table, values=list(QUERIES.keys()), state="readonly")
    combo.grid(row=0, column=1, padx=10)
    combo.current(0)
    
    def show_selected_table():
        table_name = selected_table.get()
        if table_name:
            display_table(table_name)
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите справочник из списка.")
    
    show_button = tk.Button(frame, text="Показать", command=show_selected_table)
    show_button.grid(row=0, column=2, padx=10)
    
    root.mainloop()