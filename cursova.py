from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
from config import host, user,db_name
import pymsgbox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.db()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(510, 330)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.AddButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddButton.setGeometry(QtCore.QRect(250, 65, 101, 31))
        self.AddButton.setObjectName("AddButton")
        self.AddButton.clicked.connect(self.AddButtFun)
        self.book_id_label = QtWidgets.QLabel(self.centralwidget)
        self.book_id_label.setGeometry(QtCore.QRect(10, 65, 55, 16))
        self.book_id_label.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.book_id_label.setObjectName("book_id_label")
        self.Client_id_Lable = QtWidgets.QLabel(self.centralwidget)
        self.Client_id_Lable.setGeometry(QtCore.QRect(10, 100, 55, 16))
        self.Client_id_Lable.setObjectName("Client_id_Lable")
        self.Order_date_label = QtWidgets.QLabel(self.centralwidget)
        self.Order_date_label.setGeometry(QtCore.QRect(10, 135, 61, 20))
        self.Order_date_label.setObjectName("Order_date_label")
        self.End_ord_date_label = QtWidgets.QLabel(self.centralwidget)
        self.End_ord_date_label.setGeometry(QtCore.QRect(4, 170, 91, 16))
        self.End_ord_date_label.setObjectName("End_ord_date_label")
        self.Order_start_data = QtWidgets.QDateEdit(self.centralwidget)
        self.Order_start_data.setGeometry(QtCore.QRect(75, 135, 110, 22))
        self.Order_start_data.setObjectName("Order_start_data")
        self.Order_end_data = QtWidgets.QDateEdit(self.centralwidget)
        self.Order_end_data.setGeometry(QtCore.QRect(100, 165, 110, 22))
        self.Order_end_data.setObjectName("Order_end_data")
        self.booksList = QtWidgets.QComboBox(self.centralwidget)
        self.booksList.setGeometry(QtCore.QRect(75, 65, 100, 22))
        self.booksList.setObjectName("booksList")
        self.clientsList = QtWidgets.QComboBox(self.centralwidget)
        self.clientsList.setGeometry(QtCore.QRect(75, 100, 100, 22))
        self.clientsList.setObjectName("clientsList")
        self.WorkerList = QtWidgets.QComboBox(self.centralwidget)
        self.WorkerList.setGeometry(QtCore.QRect(250, 10, 141, 22))
        self.WorkerList.setObjectName("WorkerList")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(15)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.dbViver=QtWidgets.QTextEdit(self.centralwidget)
        self.dbViver.setObjectName("dvViver")
        self.dbViver.setGeometry(0, 190, 500, 131)

        self.setData()
        self.data_update()
        MainWindow.setCentralWidget(self.centralwidget)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Library"))
        self.AddButton.setText(_translate("MainWindow", "Внести дані"))
        self.book_id_label.setText(_translate("MainWindow", "Book id"))
        self.Client_id_Lable.setText(_translate("MainWindow", "Сlient id"))
        self.Order_date_label.setText(_translate("MainWindow", "Order data"))
        self.End_ord_date_label.setText(_translate("MainWindow", "End order data"))
        self.label_3.setText(_translate("MainWindow", "Взяти книгу"))

    def data_update(self):
        self.dbViver.clear()
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT * FROM order_list ")
            rows = cursor.fetchall()
            text=''
            all_date_dist=[]
            for row in rows:
                all_date_dist.append(row)
                temp_text=f"{self.dbViver.toPlainText()}\n{row['orderID']},{row['book_id']},{row['client_id']}," \
                     f"{row['worker_id']},{row['order_date']},{row['end_order_date']}\n"
                text+=temp_text
            all_date_text=''
            for row in all_date_dist:
                all_date_text+=f'{row}\n'
            self.dbViver.setText(all_date_text)#text-чистые данные all_date_text-не чистые данные




    def setData(self):
        #workers
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT * FROM worker")
            rows=cursor.fetchall()
            for row in rows:
                worker=str(row["workerID"])+" "+row["name"]
                self.WorkerList.addItem(str(worker))
        #clients
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT * FROM client")
            rows=cursor.fetchall()
            for row in rows:
                client=str(row["clientID"])+" "+row["name"]
                self.clientsList.addItem(str(client))
        #books
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT * FROM book")
            rows=cursor.fetchall()
            for row in rows:
                book=str(row["bookID"])+" "+row["book_name"]
                self.booksList.addItem(str(book))
        # black_list
        with self.connect.cursor() as cursor:
            cursor.execute("SELECT person_id FROM `black_list`")
            rows = cursor.fetchall()
            self.blak_list=[]
            for row in rows:
                self.blak_list.append(row["person_id"])
                print(self.blak_list)

    def AddButtFun(self):
        with self.connect.cursor() as cursor:
            temp=self.Order_start_data.text().split(sep=".")
            startData=f"{temp[2]}-{temp[1]}-{temp[0]}"
            temp = self.Order_end_data.text().split(sep=".")
            endData = f"{temp[2]}-{temp[1]}-{temp[0]}"
            values={"book_id":int(self.booksList.currentText()[0]),
                    "client_id":int(self.clientsList.currentText()[0]),
                    "worker_id":int(self.WorkerList.currentText()[0]),
                    "order_date":startData,
                    "end_order_date":endData}
            if values["client_id"] in self.blak_list:
                if pymsgbox.confirm(title="Зауважте",text="Данний читач знаходится у чорному списку",buttons=['Продовжити','Відміна']) =="Відміна":
                    pymsgbox.alert(text="Операція відмінена")
                    return

            ins=f"INSERT INTO order_list (book_id,client_id,worker_id,order_date,end_order_date) VALUES ({values['book_id']},{values['client_id']}," \
                f"{values['worker_id']},'{values['order_date']}','{values['end_order_date']}')"
            cursor.execute(ins)
            self.connect.commit()
        self.data_update()


    def db(self):
        try:
            self.connect = pymysql.connect(host=host, port=3306, user=user, database=db_name,
                                           cursorclass=pymysql.cursors.DictCursor)
        except Exception as ex:
            print(ex)
            pymsgbox.alert(title="ERROR",text="Невозможно подключится к базе данных")
            sys.exit()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
