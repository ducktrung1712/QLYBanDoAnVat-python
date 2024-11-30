import sys
import bcrypt
import pyodbc
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import *
from PyQt6.uic.properties import QtCore
from QlyBanDoAnVat.btladmin import Ui_MainWindow
from Login import Ui_Form

class LoginWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loginButton.clicked.connect(self.handle_login)
        self.cancelButton.clicked.connect(self.close)

    def handle_login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        if self.check_credentials(username, password):
            QtWidgets.QMessageBox.information(self, 'Thông báo', 'Đăng nhập thành công!')
            self.open_main_window()
        else:
            QtWidgets.QMessageBox.warning(self, 'Thông báo', 'Đăng nhập thất bại. Vui lòng kiểm tra lại tên đăng nhập hoặc mật khẩu.')

    def check_credentials(self, username, password):
        # Connect to the database and check login information
        server = 'LUCIFER\\LUCIFER'
        database = 'QLyBanDoAnVat'
        db_username = 'sa'
        db_password = 'dtvn2003'

        connection_string_with_db = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=' + server + ';'
            'DATABASE=' + database + ';'
            'UID=' + db_username + ';'
            'PWD=' + db_password
        )

        conn = pyodbc.connect(connection_string_with_db)
        cursor = conn.cursor()
        cursor.execute("SELECT Password FROM Account WHERE UserName = ?", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            stored_password = result[0]
            return bcrypt.checkpw(password.encode(), stored_password.encode())
        return False

    def open_main_window(self):
        self.main_window = MainWindow(self)
        self.main_window.show()
        self.close()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, login_window):
        super().__init__()
        uic.loadUi('btladmin.ui', self)  # Load the btladmin UI file dynamically
        self.setWindowTitle('Trang chính')
        self.login_window = login_window
        # Connect the commandLinkButton to the method that will log out and return to login screen
        self.commandLinkButton.clicked.connect(self.logout)
        #loaddatacbbd
        for i in range(self.load_data_into_tableDanhmuc().__len__()):
            self.cbbdm.addItem(self.load_data_into_tableDanhmuc()[i][1])

        # Call the method to load data into the table
        self.load_data_into_tableSanpham()
        self.load_data_into_tableDanhmuc()
        self.load_data_into_tableNhanvien()
        self.load_data_into_tableorder()
        self.load_data_into_tableShipment()
        # Connect the buttons to the add, edit, and delete methods
        self.btnThem.clicked.connect(self.add_product)
        self.btnXoa.clicked.connect(self.delete_product)
        self.btnSua.clicked.connect(self.edit_product)
        self.btnThem_2.clicked.connect(self.add_category)
        self.btnSua_2.clicked.connect(self.edit_category)
        self.btnXoa_2.clicked.connect(self.delete_category)
        self.btnThem_3.clicked.connect(self.add_employee)
        self.btnSua_3.clicked.connect(self.edit_employee)
        self.btnXoa_3.clicked.connect(self.delete_employee)
        self.cbbdm.currentIndexChanged.connect(self.on_combobox_changed)
        self.btnExportOrders_2.clicked.connect(self.export_order_details_to_txt)
        self.btnAddOrder_2.clicked.connect(self.create_order)
        self.btnDeleteOrder_2.clicked.connect(self.delete_order)
        self.btnUpdateStatus_2.clicked.connect(self.update_order_status)
        self.btnSaveShipment.clicked.connect(self.add_shipment)
        self.btnXoaship.clicked.connect(self.delete_shipment)
        self.btSuaship.clicked.connect(self.edit_shipment)

        # Connect search button to search method
        self.btnOk.clicked.connect(self.search_products)
        self.btnOk_2.clicked.connect(self.search_Categories)
        self.btnOk_3.clicked.connect(self.search_employee)
        self.btnOkship.clicked.connect(self.search_shipment)
        # Connect table click event to the method
        self.tableSanpham.cellClicked.connect(self.display_product_details)
        self.tableDanhmuc.cellClicked.connect(self.display_category_details)
        self.tableNhanvien.cellClicked.connect(self.display_employee_details)
        self.tableWidgetOrders_2.cellClicked.connect(self.display_order_details)
        self.tableShip.cellClicked.connect(self.display_shipment_details)
        # Connect the print button to the export method
        self.btnIn.clicked.connect(self.export_to_txt)
        # Connect the add product button to the method
        self.btnAddProduct_2.clicked.connect(self.add_product_to_order_details)


    def get_db_connection(self):
        # Database connection parameters
        server = 'LUCIFER\\LUCIFER'
        database = 'QLyBanDoAnVat'
        db_username = 'sa'
        db_password = 'dtvn2003'

        connection_string_with_db = (
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=' + server + ';'
                                     'DATABASE=' + database + ';'
                                                              'UID=' + db_username + ';'
                                                                                     'PWD=' + db_password
        )

        return pyodbc.connect(connection_string_with_db)
    def logout(self):
        self.close()
        self.login_window.show()

    def load_data_into_tableSanpham(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        self.tableSanpham.setRowCount(0)  # Clear any existing rows in the table

        for row_number, row_data in enumerate(result):
            self.tableSanpham.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableSanpham.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    def load_data_into_tableDanhmuc(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Categories")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        self.tableDanhmuc.setRowCount(0)  # Clear any existing rows in the table

        for row_number, row_data in enumerate(result):
            self.tableDanhmuc.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableDanhmuc.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        return result
    def load_data_into_tableNhanvien(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Employees")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        self.tableNhanvien.setRowCount(0)  # Clear any existing rows in the table

        for row_number, row_data in enumerate(result):
            self.tableNhanvien.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableNhanvien.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    def load_data_into_tableShipment(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Shipment")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        self.tableShip.setRowCount(0)  # Clear any existing rows in the table

        for row_number, row_data in enumerate(result):
            self.tableShip.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableShip.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    def load_data_into_tableorder(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Orders")
        result = cursor.fetchall()
        self.tableWidgetOrders_2.setRowCount(result.__len__())
        self.tableWidgetOrders_2.setColumnCount(4)
        self.tableWidgetOrders_2.setHorizontalHeaderLabels(["OrderID", "OrderDate", "TotalAmount", "Status"])
        table_row = 0
        for row in result:
            sum = 0
            self.tableWidgetOrders_2.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            cursor.execute("SELECT * FROM OrderDetails WHERE OrderID = ?", (str(row[0]),))
            order_details = cursor.fetchall()
            self.tableWidgetOrders_2.setItem(table_row, 1, QTableWidgetItem(str(row[1])))
            for row1 in order_details:
                sum += row1[5]
            self.tableWidgetOrders_2.setItem(table_row, 2, QTableWidgetItem(str(sum)))
            self.tableWidgetOrders_2.setItem(table_row, 3, QTableWidgetItem(str(row[3])))
            table_row += 1

    def display_order_details(self, row, column):
        order_id = self.tableWidgetOrders_2.item(row, 0).text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM OrderDetails WHERE OrderID = ?", (order_id,))
        order_details = cursor.fetchall()
        cursor.close()
        conn.close()

        self.tableWidgetOrderDetails_2.setRowCount(0)
        for row_number, row_data in enumerate(order_details):
            self.tableWidgetOrderDetails_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidgetOrderDetails_2.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    def display_product_details(self, row, column):
        # Display product details in text fields and combobox when a row is clicked
        self.txtID.setText(self.tableSanpham.item(row, 0).text())
        self.txtTensp.setText(self.tableSanpham.item(row, 1).text())
        self.txtMota.setText(self.tableSanpham.item(row, 2).text())
        self.txtGianhap.setText(self.tableSanpham.item(row, 3).text())
        self.txtGiaban.setText(self.tableSanpham.item(row, 4).text())
        self.txtSoluong.setText(self.tableSanpham.item(row, 5).text())
        self.txtDanhmuc.setText(self.tableSanpham.item(row, 6).text())

    def display_shipment_details(self):

        row = self.tableShip.currentRow()


        orderid = self.tableShip.item(row, 1).text()
        customername = self.tableShip.item(row, 2).text()
        address = self.tableShip.item(row, 3).text()
        phone = self.tableShip.item(row, 4).text()
        shipdate = QDate.fromString(self.tableShip.item(row, 5).text(), "yyyy-MM-dd")
        deliverydate = QDate.fromString(self.tableShip.item(row, 6).text(), "yyyy-MM-dd")
        self.lineEdit_3.setText(orderid)
        self.lineEditCustomerName.setText(customername)
        self.lineEditAddress.setText(address)
        self.lineEditPhone.setText(phone)
        self.dateEditShippingDate.setDate(shipdate)
        self.dateEditDeliveryDate.setDate(deliverydate)

    def calculate_total_amount(self):
        # Tính tổng số tiền của đơn hàng
        total_amount = 0
        for row in range(self.tableWidgetOrderDetails_2.rowCount()):
            total_price = float(self.tableWidgetOrderDetails_2.item(row, 5).text())
            total_amount += total_price
        return total_amount
    def add_product(self):
        # Get the product details from the input fields
        name = self.txtTensp.text()
        description = self.txtMota.text()
        price = self.txtGiaban.text()
        price_old = self.txtGianhap.text()
        stockquantity = self.txtSoluong.text()
        categoryid = self.txtDanhmuc.text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Products ( Name, Description, Price, PriceOld, StockQuantity, CategoryID) VALUES (?, ?, ?, ?, ?, ?)",
            (name, description, price, price_old, stockquantity, categoryid))
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Thêm sản phẩm thành công!')
        self.load_data_into_tableSanpham()

    def edit_product(self):
        # Get the product details from the input fields
        product_id = self.txtID.text()
        name = self.txtTensp.text()
        description = self.txtMota.text()
        price = self.txtGiaban.text()
        price_old = self.txtGianhap.text()
        stockquantity = self.txtSoluong.text()
        categoryid = self.txtDanhmuc.text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Products SET Name = ?, Description = ?, Price = ?,PriceOld = ?, StockQuantity = ?, CategoryID = ? WHERE ProductID = ?",
            (name, description, price, price_old, stockquantity, categoryid, product_id))
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Cập nhật sản phẩm thành công!')
        self.load_data_into_tableSanpham()

    def delete_product(self):
        # Get the product ID from the input field
        product_id = self.txtID.text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Products WHERE ProductID = ?", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Xóa sản phẩm thành công!')
        self.load_data_into_tableSanpham()

    def search_products(self):
        search_text = self.txtTimkiem.text().strip()
        if search_text:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM Products WHERE Name LIKE ?"
            cursor.execute(query, ('%' + search_text + '%',))
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            self.tableSanpham.setRowCount(0)  # Clear any existing rows in the table

            for row_number, row_data in enumerate(result):
                self.tableSanpham.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableSanpham.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    def export_to_txt(self):
        # Đường dẫn mặc định khi mở file dialog
        default_dir = "C:/Users/daica/OneDrive/Documents/Python/QlyBanDoAnVat/In"

        # Mở file dialog để chọn nơi lưu file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", default_dir, "Text Files (*.txt);;All Files (*)")

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    row_count = self.tableSanpham.rowCount()
                    column_count = self.tableSanpham.columnCount()
                    for row in range(row_count):
                        row_data = []
                        for column in range(column_count):
                            item = self.tableSanpham.item(row, column)
                            row_data.append(item.text() if item else "")
                        file.write('\t'.join(row_data) + '\n')

                QMessageBox.information(self, 'Thông báo', 'Xuất dữ liệu thành công!')
            except Exception as e:
                QMessageBox.warning(self, 'Thông báo', f'Có lỗi xảy ra: {e}')
    def display_category_details(self, row, column):
        # Display
        self.txtID_2.setText(self.tableDanhmuc.item(row, 0).text())
        self.txtTenDM.setText(self.tableDanhmuc.item(row,1).text())
        self.txtota.setText(self.tableDanhmuc.item(row, 2).text())
    def add_category(self):
        # Get the category details from the input fields
        name = self.txtTenDM.text()
        description = self.txtota.text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Categories ( Name, Description) VALUES (?, ?)",
            (name, description))
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Thêm danh mục thành công!')
        self.load_data_into_tableDanhmuc()
    def edit_category(self):
        # Get the category details from the input fields
        category_id = self.txtID_2.text()
        name = self.txtTenDM.text()
        description = self.txtota.text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Categories SET Name = ?, Description = ? WHERE CategoryID = ?",
            (name, description, category_id))
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Chỉnh sửa danh mục thành công!')
        self.load_data_into_tableDanhmuc()
    def delete_category(self):
        # Get the product ID from the input field
        category_id = self.txtID_2.text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Categories WHERE CategoryID = ?", (category_id,))
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Xóa danh muc thành công!')
        self.load_data_into_tableDanhmuc()
    def search_Categories(self):
        search_text = self.txtTimkiem_2.text().strip()
        if search_text:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM Categories WHERE Name LIKE ?"
            cursor.execute(query, ('%' + search_text + '%',))
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            self.tableDanhmuc.setRowCount(0)  # Clear any existing rows in the table

            for row_number, row_data in enumerate(result):
                self.tableDanhmuc.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableDanhmuc.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def display_employee_details(self, row, column):
            # Display product details in text fields and combobox when a row is clicked
            self.txtID_3.setText(self.tableNhanvien.item(row, 0).text())
            self.txtHo.setText(self.tableNhanvien.item(row, 1).text())
            self.txtTen.setText(self.tableNhanvien.item(row, 2).text())
            self.txtEmail.setText(self.tableNhanvien.item(row, 3).text())
            self.txtSdt.setText(self.tableNhanvien.item(row, 4).text())
            self.txtVitri.setText(self.tableNhanvien.item(row, 5).text())

    def add_employee(self):
            # Get the product details from the input fields
            ho = self.txtHo.text()
            ten = self.txtTen.text()
            email = self.txtEmail.text()
            sdt = self.txtSdt.text()
            viTri = self.txtVitri.text()
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Employees ( FirstName, LastName, Email, Phone, Position) VALUES (?, ?, ?, ?, ?)",
                (ho, ten, email, sdt, viTri))
            conn.commit()
            cursor.close()
            conn.close()

            QtWidgets.QMessageBox.information(self, 'Thông báo', 'Thêm nhân viên thành công!')
            self.load_data_into_tableNhanvien()

    def edit_employee(self):
            # Get the product details from the input fields
            employee_id = self.txtID_3.text()
            ho = self.txtHo.text()
            ten = self.txtTen.text()
            email = self.txtEmail.text()
            sdt = self.txtSdt.text()
            viTri = self.txtVitri.text()
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Employees SET FirstName = ?, LastName = ?, Email = ?,Phone = ?, Position = ? WHERE EmployeeID = ?",
                (ho, ten, email, sdt, viTri, employee_id))
            conn.commit()
            cursor.close()
            conn.close()
            QtWidgets.QMessageBox.information(self, 'Thông báo', 'Cập nhật nhân viên thành công!')
            self.load_data_into_tableNhanvien()
    def delete_employee(self):
        # Get the product ID from the input field
        employee_id = self.txtID_3.text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Employees WHERE EmployeeID = ?", (employee_id,))
        conn.commit()
        cursor.close()
        conn.close()
        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Xóa nhân viên thành công!')
        self.load_data_into_tableNhanvien()

    def search_employee(self):
        search_text = self.txtTimkiem_3.text().strip()
        if search_text:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM Employees WHERE FirstName LIKE ? OR LastName LIKE ? OR EmployeeID LIKE ?"
            cursor.execute(query, ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            self.tableNhanvien.setRowCount(0)  # Clear any existing rows in the table

            for row_number, row_data in enumerate(result):
                self.tableNhanvien.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableNhanvien.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def create_order(self):
        order_date = self.dateEdit.date().toPyDate()
        total_amount = self.calculate_total_amount()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Orders (OrderDate, TotalAmount, Status) VALUES (?, ?, ?)",
                       (order_date, total_amount, 'Chua Thanh Toan'))
        order_id = cursor.execute("SELECT @@IDENTITY AS ID;").fetchone()[0]

        for row in range(self.tableWidgetOrderDetails_2.rowCount()):
            product_id = self.tableWidgetOrderDetails_2.item(row, 0).data(QtCore.Qt.UserRole)
            quantity = int(self.tableWidgetOrderDetails_2.item(row, 1).text())
            unit_price = float(self.tableWidgetOrderDetails_2.item(row, 2).text())
            total_price = float(self.tableWidgetOrderDetails_2.item(row, 3).text())

            cursor.execute(
                "INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice, TotalPrice) VALUES (?, ?, ?, ?, ?)",
                (order_id, product_id, quantity, unit_price, total_price))

        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Tạo đơn hàng thành công!')
        self.load_data_into_tableorder()
    def update_order_status(self):
        row = self.tableWidgetOrders_2.currentRow()
        order_id = self.tableWidgetOrders_2.item(row, 0).text()
        status = self.lineEdit.text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Orders SET Status = ? WHERE OrderID = ?", (status, order_id))
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Cập nhật trạng thái đơn hàng thành công!')

        self.load_data_into_tableorder()
    def delete_order(self):
        row = self.tableWidgetOrders_2.currentRow()
        order_id = self.tableWidgetOrders_2.item(row, 0).text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM OrderDetails WHERE OrderID = ?", (order_id,))
        cursor.execute("DELETE FROM Orders WHERE OrderID = ?", (order_id,))
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Xóa đơn hàng thành công!')
        self.load_data_into_tableorder()
    def export_order_details_to_txt(self):
        # Get the selected order ID from the orders table
        current_row = self.tableWidgetOrders_2.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self, 'Error', 'No order selected')
            return

        order_id_item = self.tableWidgetOrders_2.item(current_row, 0)
        if order_id_item is None:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Order ID not found')
            return

        order_id = int(order_id_item.text())

        default_dir = "C:/Users/daica/OneDrive/Documents/Python/QlyBanDoAnVat/In"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", default_dir, "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    conn = self.get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM OrderDetails WHERE OrderID = ?", (order_id,))
                    order_details = cursor.fetchall()
                    # Write the header
                    file.write('OrderDetailID\tOrderID\tProduct\tQuantity\tUnitPrice\tTotalPrice\n')
                    for detail in order_details:
                        file.write('\t'.join(map(str, detail)) + '\n')
                    cursor.close()
                    conn.close()
                QtWidgets.QMessageBox.information(self, 'Thông báo', 'Xuất dữ liệu thành công!')
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, 'Thông báo', f'Có lỗi xảy ra: {e}')

    def on_combobox_changed(self):
        selected_text = self.cbbdm.currentText()
        self.cbbsp.clear()
        products = self.LoadDataId(selected_text)
        print(products)  # For debugging: print the list of products

        for product in products:
            product_id = product[0]  # Assuming the product ID is in the first column
            product_name = product[1]  # Assuming the product name is in the second column
            self.cbbsp.addItem(product_name, product_id)  # Set both display text and data

        # For debugging: print the combo box items and their data
        for index in range(self.cbbsp.count()):
            print(f"Item {index}: {self.cbbsp.itemText(index)} with data {self.cbbsp.itemData(index)}")

    def LoadDataId(self, tensp):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        qr = ("SELECT p.ProductID, p.Name AS ProductName, p.Description AS ProductDescription, p.Price, p.PriceOld, "
              "p.StockQuantity, c.CategoryID, c.Name AS CategoryName, c.Description AS CategoryDescription "
              "FROM [QLyBanDoAnVat].[dbo].[Products] p "
              "JOIN [QLyBanDoAnVat].[dbo].[Categories] c ON p.CategoryID = c.CategoryID "
              "WHERE c.Name = ? "
              "ORDER BY p.Name;")
        cursor.execute(qr, (tensp,))
        rs = cursor.fetchall()
        conn.close()
        return rs

    def add_product_to_order_details(self):
        # Get the selected order ID from the orders table
        current_row = self.tableWidgetOrders_2.currentRow()
        if current_row == -1:
            QtWidgets.QMessageBox.warning(self, 'Error', 'No order selected')
            return

        order_id_item = self.tableWidgetOrders_2.item(current_row, 0)
        if order_id_item is None:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Order ID not found')
            return

        self.current_order_id = int(order_id_item.text())  # Set current_order_id here
        product_id = self.cbbsp.currentData()
        if product_id is None:
            QtWidgets.QMessageBox.warning(self, 'Error', 'No product selected')
            return

        product_name = self.cbbsp.currentText()  # Get the selected product name

        try:
            quantity = int(self.lineEdit_2.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid quantity')
            return

        unit_price = self.get_product_price(product_id)
        if unit_price is None:
            QtWidgets.QMessageBox.warning(self, 'Error', f'Could not find price for product ID {product_id}')
            return

        total_price = quantity * unit_price

        # Insert product details into the order details table in the UI
        row_count = self.tableWidgetOrderDetails_2.rowCount()
        self.tableWidgetOrderDetails_2.insertRow(row_count)
        self.tableWidgetOrderDetails_2.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(self.current_order_id)))
        self.tableWidgetOrderDetails_2.setItem(row_count, 2, QtWidgets.QTableWidgetItem(product_name))  # Use product name
        self.tableWidgetOrderDetails_2.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(quantity)))
        self.tableWidgetOrderDetails_2.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(unit_price)))
        self.tableWidgetOrderDetails_2.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(total_price)))

        # Save the details to the database
        self.save_order_detail_to_database(product_name, quantity, unit_price, total_price)
        self.load_data_into_tableorder()
        self.calculate_total_amount()

    def save_order_detail_to_database(self, product_name, quantity, unit_price, total_price):
        conn = self.get_db_connection()
        cursor = conn.cursor()

        try:
            # Use self.current_order_id directly
            cursor.execute(
                "INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice, TotalPrice) VALUES (?, ?, ?, ?, ?)",
                (self.current_order_id, product_name, quantity, unit_price, total_price)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            QtWidgets.QMessageBox.warning(self, 'Error', f'Failed to save order detail: {e}')
        finally:
            cursor.close()
            conn.close()
    def get_product_price(self, product_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT PriceOld FROM Products WHERE ProductID = ?", (product_id,))
        row = cursor.fetchone()
        price = row[0] if row else None  # Handle case where no price is found
        conn.close()

        return price
    def add_shipment(self):
        # Get the product details from the input fields
        orderid = self.lineEdit_3.text()
        customername = self.lineEditCustomerName.text()
        address = self.lineEditAddress.text()
        phone = self.lineEditPhone.text()
        shipdate = self.dateEditShippingDate.date().toPyDate()
        deliverydate = self.dateEditDeliveryDate.date().toPyDate()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Shipment ( OrderID, CustomerName, Address, Phone, ShippingDate, DeliveryDate) VALUES (?, ?, ?, ?, ?, ?)",
            (orderid, customername, address, phone, shipdate, deliverydate))
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Đặt ship thành công!')
        self.load_data_into_tableShipment()
    def delete_shipment(self):
        row = self.tableShip.currentRow()
        ship_id = self.tableShip.item(row, 0).text()
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Shipment WHERE ShipmentID = ?", (ship_id,))
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Xóa Ship thành công!')
        self.load_data_into_tableShipment()
    def search_shipment(self):
        search_text = self.txtTimkiemship.text().strip()
        if search_text:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM Shipment WHERE OrderID LIKE ? OR CustomerName LIKE ? "
            cursor.execute(query, ('%' + search_text + '%', '%' + search_text + '%',))
            result = cursor.fetchall()
            cursor.close()
            conn.close()

            self.tableShip.setRowCount(0)  # Clear any existing rows in the table

            for row_number, row_data in enumerate(result):
                self.tableShip.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableShip.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    def edit_shipment(self):
        # Get the current row
        row = self.tableShip.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Please select a shipment to edit.')
            return

        # Get the shipment ID from the selected row
        ship_id = self.tableShip.item(row, 0).text()

        # Get the updated details from the input fields
        orderid = self.lineEdit_3.text()
        customername = self.lineEditCustomerName.text()
        address = self.lineEditAddress.text()
        phone = self.lineEditPhone.text()
        shipdate = self.dateEditShippingDate.date().toPyDate()
        deliverydate = self.dateEditDeliveryDate.date().toPyDate()

        # Update the database with the new details
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Shipment SET OrderID = ?, CustomerName = ?, Address = ?, Phone = ?, ShippingDate = ?, DeliveryDate = ? WHERE ShipmentID = ?",
            (orderid, customername, address, phone, shipdate, deliverydate, ship_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        QtWidgets.QMessageBox.information(self, 'Thông báo', 'Cập nhật ship thành công!')
        self.load_data_into_tableShipment()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())
