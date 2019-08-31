from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import pymysql as MySQLdb
from PyQt5.uic import loadUiType

ui, _ = loadUiType('library.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()
        self.Dark_Orange_Theme()
        self.Show_Author()
        self.Show_Category()
        self.Show_Publisher()
        self.Show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()




    def Handle_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)
    def Handle_Buttons(self):
        self.pushButton_5.clicked.connect(self.Show_Themes)
        # self.pushButton_21.clicked.connect(self.Hiding_Themes)
        self.pushButton_26.clicked.connect(self.Hiding_Themes)
        self.pushButton.clicked.connect(self.Open_Day_To_Day_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_21.clicked.connect(self.Open_Clients_Tab)
        self.pushButton_3.clicked.connect(self.Open_Users_Tab)
        self.pushButton_4.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_9.clicked.connect(self.Search_Books)
        self.pushButton_8.clicked.connect(self.Edit_Books)

        self.pushButton_16.clicked.connect(self.Add_Category)
        self.pushButton_15.clicked.connect(self.Add_Author)
        self.pushButton_14.clicked.connect(self.Add_Publisher)
        self.pushButton_10.clicked.connect(self.Delete_Books)

        self.pushButton_11.clicked.connect(self.Add_New_User)
        self.pushButton_12.clicked.connect(self.Login)
        self.pushButton_13.clicked.connect(self.Edit_User)

        self.pushButton_22.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_23.clicked.connect(self.Dark_Gray_Theme)
        self.pushButton_24.clicked.connect(self.Dark_Orange_Theme)
        self.pushButton_25.clicked.connect(self.QDark_Theme)

        self.pushButton_17.clicked.connect(self.Add_New_Client)
        self.pushButton_19.clicked.connect(self.Search_Client)
        self.pushButton_18.clicked.connect(self.Edit_Client)
        self.pushButton_20.clicked.connect(self.Delete_Client)

    def Show_Themes(self):
        self.groupBox_5.show()

    def Hiding_Themes(self):
        self.groupBox_5.hide()

    ################################################
    ######### Opening Tabs #########################
    def Open_Day_To_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(4)

    ################################################
    ######### Books #########################
    def Add_New_Book(self):
        self.db = MySQLdb.connect(host='localhost' , user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit_3.text()
        book_category = self.comboBox_3.currentIndex()
        book_author = self.comboBox_4.currentIndex()
        book_publisher = self.comboBox_5.currentIndex()
        book_price = self.lineEdit_4.text()

        self.cur.execute('''
            INSERT INTO book (book_name, book_description, book_code,  book_category, book_author, book_publisher, book_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price ))
        self.db.commit()
        self.statusBar().showMessage('New Book Added')
        self.lineEdit_2.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_3.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText('')

    def Search_Books(self):
        self.db = MySQLdb.connect(host='localhost' , user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()
        book_title = self.lineEdit_7.text()

        sql = ''' SELECT * FROM book WHERE book_name=%s'''
        self.cur.execute(sql, [(book_title)])

        data = self.cur.fetchone()
        print(data)
        self.lineEdit_8.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_6.setText(data[3])
        self.comboBox_8.setCurrentIndex(data[4])
        self.comboBox_6.setCurrentIndex(data[5])
        self.comboBox_7.setCurrentIndex(data[6])
        self.lineEdit_5.setText(str(data[7]))
    def Edit_Books(self):
        self.db = MySQLdb.connect(host='localhost' , user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_8.text()
        book_description = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_6.text()
        book_category = self.comboBox_8.currentIndex()
        book_author = self.comboBox_6.currentIndex()
        book_publisher = self.comboBox_7.currentIndex()
        book_price = self.lineEdit_5.text()

        search_book_title = self.lineEdit_7.text()

        self.cur.execute('''
            UPDATE book SET book_name = %s, book_description = %s, book_code = %s, book_category = %s, book_author = %s, book_publisher = %s, book_price = %s 
            WHERE book_name = %s                           
        ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price, search_book_title))

        self.db.commit()
        self.statusBar().showMessage('Book Updated')
    def Delete_Books(self):
        self.db = MySQLdb.connect(host='localhost' , user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_7.text()
        warning = QMessageBox.warning(self, 'Delete Book', "Are you sure you want to delete this book", QMessageBox.Yes | QMessageBox.No)

        if warning == QMessageBox.Yes:
            sql = ''' DELETE FROM book WHERE book_name=%s '''
            self.cur.execute(sql, [(book_title)])
            self.db.commit()
            self.statusBar().showMessage('Book Deleted')

    ################################################
    ######### users #########################
    def Add_New_Client (self):

        self.db = MySQLdb.connect(host='localhost' , user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()
        client_name = self.lineEdit_22.text()
        client_email = self.lineEdit_23.text()
        client_id = self.lineEdit_24.text()

        self.cur.execute('''
            INSERT INTO clients(client_name, client_email, client_id)
            VALUES (%s, %s, %s)
        ''', (client_name, client_email, client_id))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('New Client Added')

    def Show_All_Client(self):
        pass
    
    def Edit_Client(self):
        pass


    def Search_Client(self):
        pass

    def Delete_Client(self):
        pass

    ################################################
    ######### users #########################
    def Add_New_User(self):
        self.db = MySQLdb.connect(host='localhost' , user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_9.text()
        email = self.lineEdit_10.text()
        password = self.lineEdit_11.text()
        password_2 = self.lineEdit_12.text()

        if password == password_2:
            self.cur.execute('''
                INSERT INTO users(user_name, user_email, user_password)
                VALUES (%s, %s, %s)
            ''', (username, email, password))

            self.db.commit()
            self.statusBar().showMessage('New User Added')
        else:
            self.label_30.setText('Please enter a valid password again')


    def Login(self):
        self.db = MySQLdb.connect(host='localhost' , user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_13.text()
        password = self.lineEdit_14.text()

        sql: str = ''' SELECT * FROM users '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                print('user match')
                self.statusBar().showMessage('Valid Username & Password')
                self.groupBox_4.setEnabled(True)

                self.lineEdit_15.setText(row[1])
                self.lineEdit_17.setText(row[2])
                self.lineEdit_16.setText(row[3])

    def Edit_User(self):
        username = self.lineEdit_13.text()
        email = self.lineEdit_17.text()
        password = self.lineEdit_16.text()
        password_2 = self.lineEdit_18.text()
        username_new = self.lineEdit_15.text()

        if password == password_2:
            self.db = MySQLdb.connect(host='localhost', user='root', password='d33ps3curity', db='library')
            self.cur = self.db.cursor()
            self.cur.execute('''
                UPDATE users SET user_name = %s, user_email = %s, user_password = %s WHERE user_name = %s
            ''', (username_new, email, password, username))

            self.db.commit()
            self.statusBar().showMessage('User Data Updated Successfully')


        else:
            print('Make Sure You Enter Your Password Correctly')

    ################################################
    ######### settings #########################
    def Add_Category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        category_name = self.lineEdit_21.text()
        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (%s)
        ''', (category_name,))

        self.db.commit()
        self.statusBar().showMessage('New Category Added ')
        self.lineEdit_21.setText('')
        self.Show_Category()
        self.Show_Category_Combobox()

    def Show_Category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category ''')
        data = self.cur.fetchall()
        # print(data)
        # self.tableWidget_4.insertRow(0)
        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)
    def Add_Author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        author_name = self.lineEdit_20.text()
        self.cur.execute('''
        INSERT INTO author (author_name) VALUES (%s)
        ''', (author_name, ))

        self.db.commit()
        self.lineEdit_20.setText('')
        self.statusBar().showMessage('New Author Added ')
        self.Show_Author()
        self.Show_Author_Combobox()

    def Show_Author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM author ''')
        data = self.cur.fetchall()
        # self.tableWidget_4.insertRow(0)
        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    def Add_Publisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        publisher_name = self.lineEdit_19.text()
        self.cur.execute('''
        INSERT INTO publisher (publisher_name) VALUES (%s)
        ''', (publisher_name, ))

        self.db.commit()
        self.lineEdit_19.setText('')
        self.statusBar().showMessage('New Publisher Added ')
        self.Show_Publisher()
        self.Show_Publisher_Combobox()

    def Show_Publisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()
        # self.tableWidget_4.insertRow(0)
        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

    ################################################
    ######### show settings data in UI #########################

    def Show_Category_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category ''')
        data = self.cur.fetchall()

        # print(data)
        self.comboBox_3.clear()
        for category in data:
            self.comboBox_3.addItem(category[0])
            self.comboBox_8.addItem(category[0])

    def Show_Author_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()
        self.cur.execute(''' SELECT author_name FROM author ''')
        data = self.cur.fetchall()
        self.comboBox_4.clear()
        for author in data:
            self.comboBox_4.addItem(author[0])
            self.comboBox_6.addItem(author[0])
    def Show_Publisher_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='d33ps3curity', db='library')
        self.cur = self.db.cursor()
        self.cur.execute(''' SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()
        self.comboBox_5.clear()
        for publisher in data:
            self.comboBox_5.addItem(publisher[0])
            self.comboBox_7.addItem(publisher[0])

    ################################################
    ######### UI Themes #########################

    def Dark_Blue_Theme(self):
        style = open('themes/darkblue.css')
        style = style.read()
        self.setStyleSheet(style)


    def Dark_Gray_Theme(self):
        style = open('themes/darkgray.css')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Orange_Theme(self):
        style = open('themes/darkorange.css')
        style = style.read()
        self.setStyleSheet(style)

    def QDark_Theme(self):
        style = open('themes/qdarkstyle.css')
        style = style.read()
        self.setStyleSheet(style)
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
