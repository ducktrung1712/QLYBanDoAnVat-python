import pyodbc
import bcrypt

# Thông số kết nối cơ sở dữ liệu
server = 'LUCIFER\\LUCIFER'
database = 'QLyBanDoAnVat'
db_username = 'sa'
db_password = 'dtvn2003'

connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=' + server + ';'
    'DATABASE=' + database + ';'
    'UID=' + db_username + ';'
    'PWD=' + db_password
)

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

# Kết nối tới cơ sở dữ liệu
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Tạo lại các bảng
cursor.execute('''
IF OBJECT_ID('OrderDetails', 'U') IS NOT NULL DROP TABLE OrderDetails;
IF OBJECT_ID('Shipment', 'U') IS NOT NULL DROP TABLE Shipment;
IF OBJECT_ID('Orders', 'U') IS NOT NULL DROP TABLE Orders;
IF OBJECT_ID('Products', 'U') IS NOT NULL DROP TABLE Products;
IF OBJECT_ID('Categories', 'U') IS NOT NULL DROP TABLE Categories;
IF OBJECT_ID('Employees', 'U') IS NOT NULL DROP TABLE Employees;
IF OBJECT_ID('Account', 'U') IS NOT NULL DROP TABLE Account;

CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Description NVARCHAR(100)
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Description NVARCHAR(100),
    Price DECIMAL(10, 2) NOT NULL CHECK (Price >= 0),
    PriceOld DECIMAL(10, 2) CHECK (PriceOld >= 0),
    StockQuantity INT NOT NULL CHECK (StockQuantity >= 0),
    CategoryID INT,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    Position NVARCHAR(50)
);

CREATE TABLE Account (
    UserName NVARCHAR(50) PRIMARY KEY,
    Displayname NVARCHAR(50) NOT NULL,
    Password NVARCHAR(100) NOT NULL DEFAULT 0,
    Type INT NOT NULL DEFAULT 0
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY IDENTITY(1,1),
    OrderDate DATE NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    Status NVARCHAR(50) NOT NULL
);

CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY IDENTITY(1,1),
    OrderID INT FOREIGN KEY REFERENCES Orders(OrderID),
    ProductID NVARCHAR(50) NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10, 2) NOT NULL,
    TotalPrice DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Shipment (
    ShipmentID INT PRIMARY KEY IDENTITY(1,1),
    OrderID INT FOREIGN KEY REFERENCES Orders(OrderID),
    CustomerName NVARCHAR(255) NOT NULL,
    Address NVARCHAR(255) NOT NULL,
    Phone NVARCHAR(50) NOT NULL,
    ShippingDate DATE NOT NULL,
    DeliveryDate DATE NOT NULL
);
''')
conn.commit()

# Chèn dữ liệu mẫu vào bảng Categories
categories = [
    ('Beverages', 'Drinks and beverages'),
    ('Snacks', 'Light snacks and bites'),
    ('Dairy', 'Milk and dairy products'),
    ('Bakery', 'Bread and baked goods'),
    ('Produce', 'Fresh fruits and vegetables')
]

for category in categories:
    cursor.execute("INSERT INTO Categories (Name, Description) VALUES (?, ?)", category)
conn.commit()

# Chèn dữ liệu mẫu vào bảng Products
products = [
    ('Coke', 'Coca-Cola soft drink', 1.50, 1.20, 100, 1),
    ('Chips', 'Potato chips', 2.00, 1.80, 150, 2),
    ('Milk', 'Whole milk', 3.00, 2.50, 200, 3),
    ('Bread', 'Whole grain bread', 2.50, 2.20, 50, 4),
    ('Apple', 'Fresh apple', 0.80, 0.70, 300, 5)
]

for product in products:
    cursor.execute("INSERT INTO Products (Name, Description, Price, PriceOld, StockQuantity, CategoryID) VALUES (?, ?, ?, ?, ?, ?)", product)
conn.commit()

# Chèn dữ liệu mẫu vào bảng Employees
employees = [
    ('John', 'Doe', 'john.doe@example.com', '1234567890', 'Manager'),
    ('Jane', 'Smith', 'jane.smith@example.com', '0987654321', 'Cashier'),
    ('Jim', 'Brown', 'jim.brown@example.com', '1122334455', 'Stock Clerk'),
    ('Jack', 'White', 'jack.white@example.com', '6677889900', 'Sales Associate'),
    ('Jill', 'Green', 'jill.green@example.com', '2233445566', 'Customer Service')
]

for employee in employees:
    cursor.execute("INSERT INTO Employees (FirstName, LastName, Email, Phone, Position) VALUES (?, ?, ?, ?, ?)", employee)
conn.commit()

# Chèn dữ liệu mẫu vào bảng Account
accounts = [
    ('admin', 'Administrator', hash_password('admin123'), 1),
    ('nv01', 'Nguyễn Văn A', hash_password('password1'), 0),
    ('nv02', 'Trần Thị B', hash_password('password2'), 0),
    ('nv03', 'Lê Văn C', hash_password('password3'), 0),
    ('nv04', 'Phạm Thị D', hash_password('password4'), 0),
    ('admin1', 'Administrator', 'admin1', 1)
]

for account in accounts:
    cursor.execute("INSERT INTO Account (UserName, Displayname, Password, Type) VALUES (?, ?, ?, ?)", account)
conn.commit()

# Chèn dữ liệu mẫu vào bảng Orders
orders = [
    ('2023-06-01', 150.00, 'Pending'),
    ('2023-06-02', 200.50, 'Shipped'),
    ('2023-06-03', 120.75, 'Delivered'),
    ('2023-06-04', 180.20, 'Pending'),
    ('2023-06-05', 210.40, 'Cancelled')
]

for order in orders:
    cursor.execute("INSERT INTO Orders (OrderDate, TotalAmount, Status) VALUES (?, ?, ?)", order)
conn.commit()

# Lấy OrderID cho các đơn hàng mới chèn
cursor.execute("SELECT OrderID FROM Orders")
order_ids = [row[0] for row in cursor.fetchall()]

# Chèn dữ liệu mẫu vào bảng OrderDetails
order_details = [
    (order_ids[0], 'P001', 2, 50.00, 100.00),
    (order_ids[0], 'P002', 1, 50.00, 50.00),
    (order_ids[1], 'P003', 3, 60.00, 180.00),
    (order_ids[1], 'P004', 1, 20.50, 20.50),
    (order_ids[2], 'P005', 4, 30.75, 123.00),
    (order_ids[3], 'P006', 2, 90.10, 180.20),
    (order_ids[4], 'P007', 5, 42.08, 210.40)
]

for order_detail in order_details:
    cursor.execute("INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice, TotalPrice) VALUES (?, ?, ?, ?, ?)", order_detail)
conn.commit()

# Chèn dữ liệu mẫu vào bảng Shipment
shipments = [
    (order_ids[0], 'Nguyen Van A', '123 Le Loi, TP.HCM', '0901234567', '2023-06-01', '2023-06-03'),
    (order_ids[1], 'Tran Thi B', '456 Tran Hung Dao, Ha Noi', '0907654321', '2023-06-02', '2023-06-05'),
    (order_ids[2], 'Le Van C', '789 Nguyen Trai, Da Nang', '0912345678', '2023-06-03', '2023-06-06'),
    (order_ids[3], 'Pham Thi D', '321 Hai Ba Trung, Hai Phong', '0918765432', '2023-06-04', '2023-06-08'),
    (order_ids[4], 'Hoang Van E', '654 Le Thanh Ton, Can Tho', '0923456789', '2023-06-05', '2023-06-09')
]

for shipment in shipments:
    cursor.execute("INSERT INTO Shipment (OrderID, CustomerName, Address, Phone, ShippingDate, DeliveryDate) VALUES (?, ?, ?, ?, ?, ?)", shipment)
conn.commit()

# Đóng kết nối
cursor.close()
conn.close()

print("Database setup and data insertion completed successfully.")
