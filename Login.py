from PyQt6 import QtCore, QtGui, QtWidgets
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)

        self.usernameLineEdit = QtWidgets.QLineEdit(Form)
        self.usernameLineEdit.setGeometry(QtCore.QRect(160, 100, 141, 22))
        self.usernameLineEdit.setObjectName("usernameLineEdit")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(70, 100, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.passwordLineEdit = QtWidgets.QLineEdit(Form)
        self.passwordLineEdit.setGeometry(QtCore.QRect(160, 150, 141, 22))
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(160, 40, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(40, 265, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.loginButton = QtWidgets.QPushButton(Form)
        self.loginButton.setGeometry(QtCore.QRect(90, 210, 93, 28))
        self.loginButton.setObjectName("loginButton")

        self.cancelButton = QtWidgets.QPushButton(Form)
        self.cancelButton.setGeometry(QtCore.QRect(240, 210, 93, 28))
        self.cancelButton.setObjectName("cancelButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Dialog"))
        self.label.setText(_translate("Form", "Username:"))
        self.label_2.setText(_translate("Form", "Password:"))
        self.label_3.setText(_translate("Form", "Đăng Nhập"))
        self.label_4.setText(_translate("Form", "Nếu không đăng nhập được liên hệ Admin"))
        self.loginButton.setText(_translate("Form", "Đăng Nhập"))
        self.cancelButton.setText(_translate("Form", "Cancel"))
