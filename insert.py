from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector as mc
 
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("VEHICLE REGISTRATION")
        Form.resize(919, 507)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditEmaul = QtWidgets.QLineEdit(Form)
        self.lineEditEmaul.setObjectName("lineEditEmaul")
        self.horizontalLayout.addWidget(self.lineEditEmaul)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEditPass = QtWidgets.QLineEdit(Form)
        self.lineEditPass.setObjectName("lineEditPass")
        self.horizontalLayout_2.addWidget(self.lineEditPass)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEditPlate = QtWidgets.QLineEdit(Form)
        self.lineEditPlate.setObjectName("lineEditPlate")
        self.horizontalLayout_3.addWidget(self.lineEditPlate)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        
        #connected clicked signal of button with insert_data method
        self.pushButton.clicked.connect(self.insert_data)
        self.verticalLayout.addWidget(self.pushButton)
        self.labelResult = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        fonts = QtGui.QFont()
        fonts.setPointSize(10)
        fonts.setBold(True)
        fonts.setWeight(20)
        self.labelResult.setFont(font)
        self.label.setFont(fonts)
        self.label_2.setFont(fonts)
        self.label_3.setFont(fonts)
        self.labelResult.setText("")
        self.labelResult.setObjectName("labelResult")
        self.verticalLayout.addWidget(self.labelResult)
 
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
 
 
 
#inserting data to codeloop database in wampserver
    def insert_data(self):
        try:
            mydb = mc.connect(
 
                host="localhost",
                user="root",
                password="",
                database="vehiclerecognition"
            )
 
            mycursor = mydb.cursor()
 
            user = self.lineEditEmaul.text()
            phone =self.lineEditPass.text()
            plate =self.lineEditPlate.text()
 
            sql = "INSERT INTO user (name, phone, plate) VALUES (%s, %s, %s)"
            val = (user, phone, plate)
 
            mycursor.execute(sql, val)
 
            mydb.commit()
            self.labelResult.setText("Data Inserted")
 
        except mc.Error as e:
            self.labelResult.setText("Error Inserting Data")
 
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "VEHICLE REGISTRATION"))
        self.label.setText(_translate("Form", "Full Name :"))
        self.label_2.setText(_translate("Form", "Phone Number :"))
        self.label_3.setText(_translate("Form", "Vehicle Plate Number :"))
        self.pushButton.setText(_translate("Form", "Insert"))
 
 
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Form = QtWidgets.QWidget()
#     ui = Ui_Form()
#     ui.setupUi(Form)
#     Form.show()
#     sys.exit(app.exec_())
