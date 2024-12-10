CREATE TABLE [Order] (
    ID INT PRIMARY KEY,           
    CreateAt DATETIME NOT NULL,                 
    CustomerName NVARCHAR(255) NOT NULL,        
    CustomerEmail NVARCHAR(255) NOT NULL,       
    DeliveryType NVARCHAR(100) NOT NULL,        
    Rate DECIMAL(10, 2) NOT NULL                
);

CREATE TABLE Product (
    ID INT PRIMARY KEY,           
    ProductName NVARCHAR(255) NOT NULL,          
    Price DECIMAL(10, 2) NOT NULL,               
    Quantity INT NOT NULL,                       
    OrderID INT NOT NULL,                      
    CONSTRAINT FK_Product_Order FOREIGN KEY (OrderID) REFERENCES [Order](ID)
);

INSERT INTO [Order] (ID, CreateAt, CustomerName, CustomerEmail, DeliveryType, Rate)
VALUES 
(101, '2024-12-01', 'Иван Иванов', 'ivan@example.com', 'Курьер', 150.75),
(103, '2024-12-02', 'Мария Петрова', 'maria@example.com', 'Самовывоз', 0),
(105, '2024-12-03', 'Петр Смирнов', 'petr@example.com', 'Курьер', 200.50),
(107, '2024-12-04', 'Анна Козлова', 'anna@example.com', 'Курьер', 120.00),
(109, '2024-12-05', 'Олег Сидоров', 'oleg@example.com', 'Самовывоз', 0);


INSERT INTO Product (ID, ProductName, Price, Quantity, OrderID)
VALUES 
(201, 'Ноутбук', 45000.00, 1, 101),
(202, 'Мышь', 1200.50, 2, 103),
(204, 'Клавиатура', 2500.99, 1, 105),
(206, 'Монитор', 12000.00, 1, 107),
(208, 'Смартфон', 25000.00, 3, 109);