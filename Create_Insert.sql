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
(101, '2024-12-01', '���� ������', 'ivan@example.com', '������', 150.75),
(103, '2024-12-02', '����� �������', 'maria@example.com', '���������', 0),
(105, '2024-12-03', '���� �������', 'petr@example.com', '������', 200.50),
(107, '2024-12-04', '���� �������', 'anna@example.com', '������', 120.00),
(109, '2024-12-05', '���� �������', 'oleg@example.com', '���������', 0);


INSERT INTO Product (ID, ProductName, Price, Quantity, OrderID)
VALUES 
(201, '�������', 45000.00, 1, 101),
(202, '����', 1200.50, 2, 103),
(204, '����������', 2500.99, 1, 105),
(206, '�������', 12000.00, 1, 107),
(208, '��������', 25000.00, 3, 109);