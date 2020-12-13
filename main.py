# -*- coding: utf-8 -*-
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, \
    QTableWidgetItem
from PyQt5.QtCore import QRect
from design import Ui_MainWindow
from form import Ui_Form
from registration import Ui_Form_2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui.setupUi(self)
        self.join = False
        self.con = sqlite3.connect('library.sqlite')
        self.cur = self.con.cursor()
        self.all_books = self.cur.execute('''SELECT name FROM [books]''').fetchall()
        self.all_books = [book[0] for book in self.all_books]
        self.all_registered_books = self.cur.execute('''SELECT name FROM [books]
                                                        WHERE status_id = 2''').fetchall()
        self.all_registered_books = [i[0] for i in self.all_registered_books]
        self.update_list_of_books()
        self.update_list_of_users()
        ui.join_btn_1.clicked.connect(member.show)
        ui.error_label_1.setText('Вы не вошли')
        ui.register_btn.clicked.connect(reg.show)
        ui.adding_book.clicked.connect(self.add_new_book)
        ui.remove_user_btn.clicked.connect(self.remove_user)
        ui.remove_book_btn.clicked.connect(self.remove_book)
        self.con.commit()
        self.con.close()

    def update_list_of_registered_books(self):
        self.con = sqlite3.connect('library.sqlite')
        self.cur = self.con.cursor()
        self.registered_books = self.cur.execute('''SELECT name FROM [books], [people]
                                                    WHERE [books].status_id=2 AND [books].person_id=[people].Id AND [people].nickname=?''',
                                                 (self.user,)).fetchall()
        self.registered_books = [i[0] for i in self.registered_books]
        ui.table_of_registered_books.setColumnCount(1)
        item = QTableWidgetItem()
        item.setText('name')
        ui.table_of_registered_books.setRowCount(len(self.registered_books))
        ui.table_of_registered_books.setHorizontalHeaderItem(0, item)
        ui.table_of_registered_books.setColumnWidth(0, 260)
        for i, elem in enumerate(self.registered_books):
            ui.table_of_registered_books.setItem(0, i, QTableWidgetItem(str(elem)))

    def add_registered_book(self):
        ui.error_label_1.setText('')
        self.con = sqlite3.connect('library.sqlite')
        self.cur = self.con.cursor()
        if len(self.registered_books) + 1 > 5:
            ui.error_label_1.setText('Вы не можете взять больше 5 книг')
        else:
            self.cur.execute('''UPDATE [books] SET status_id = 2, person_id = (SELECT Id FROM [people]
                                WHERE nickname = ?)
                                WHERE name=?''',
                             (self.user, self.all_books[ui.comboBox.currentIndex()]))
            if self.all_books[ui.comboBox.currentIndex()] in self.all_registered_books:
                ui.error_label_1.setText('Эта книга уже занята')
            else:
                self.registered_books.append(self.all_books[ui.comboBox.currentIndex()])
                self.all_registered_books.append(self.all_books[ui.comboBox.currentIndex()])
                self.con.commit()
                self.update_list_of_registered_books()
        self.con.close()

    def show_for_current_user(self, user):
        self.user = user
        self.update_list_of_registered_books()
        for _ in range(len(self.all_books)):
            ui.comboBox.removeItem(0)
        ui.comboBox.addItems(self.all_books)
        if not self.join:
            ui.take_book_btn.clicked.connect(self.add_registered_book)
            ui.back_book_btn.clicked.connect(dialog_1.show)
            self.join = True

    def add_new_book(self):
        ui.error_label_2.setText('')
        self.con = sqlite3.connect('library.sqlite')
        self.cur = self.con.cursor()
        try:
            if not ui.name_book_label.text():
                raise NameError
            elif not ui.author_label.text():
                raise AssertionError
            elif ui.name_book_label.text() in self.all_books:
                raise NotADirectoryError
            self.cur.execute('''INSERT INTO [books] (name, status_id, author)
                                VALUES (?, ?, ?)''',
                             (ui.name_book_label.text(), 1, ui.author_label.text()))
            self.con.commit()
            self.con.close()
            if self.join:
                ui.comboBox.addItems([ui.name_book_label.text()])
        except NameError:
            ui.error_label_2.setText('Вы не ввели название книги')
        except AssertionError:
            ui.error_label_2.setText('Вы не ввели имя автора книги')
        except NotADirectoryError:
            ui.error_label_2.setText('Такая книга уже есть')
        finally:
            self.con.close()
            self.update_list_of_books()

    def update_list_of_books(self):
        con = sqlite3.connect('library.sqlite')
        cur = con.cursor()
        result = cur.execute('''SELECT [books].name, [books].author, [people].nickname 
                                FROM [books], [people]
                                WHERE [books].status_id = [people].Id ''').fetchall()
        ui.table_all_books.setColumnCount(3)
        ui.table_all_books.setRowCount(len(result))
        for i, j in enumerate(['Название', 'Автор', 'Получатель']):
            item = QTableWidgetItem()
            item.setText(j)
            ui.table_all_books.setHorizontalHeaderItem(i, item)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                ui.table_all_books.setItem(i, j, QTableWidgetItem(str(val)))
        con.close()

    def update_list_of_users(self):
        con = sqlite3.connect('library.sqlite')
        cur = con.cursor()
        result = cur.execute('''SELECT nickname FROM [people]''').fetchall()
        result = [i[0] for i in result]
        ui.table_of_all_users.setColumnCount(1)
        ui.table_of_all_users.setRowCount(len(result))
        item = QTableWidgetItem()
        item.setText('Nickname')
        ui.table_of_all_users.setHorizontalHeaderItem(0, item)
        ui.table_of_all_users.setColumnWidth(0, 250)
        for i, elem in enumerate(result):
            ui.table_of_all_users.setItem(0, i, QTableWidgetItem(str(elem)))
        con.close()

    def remove_user(self):
        ui.error_label_2.setText('')
        con = sqlite3.connect('library.sqlite')
        cur = con.cursor()
        rows = list(set([i.row() for i in ui.table_of_all_users.selectedItems()]))
        ids = [ui.table_of_all_users.item(i, 0).text() for i in rows]
        if len(ids) > 1:
            ui.error_label_2.setText('Выберите только одного пользователя')
        else:
            print(ids[0])
            cur.execute('''UPDATE [books] SET status_id=1, person_id=NULL
                           WHERE person_id=(SELECT Id FROM [people]
                           WHERE nickname=?)''', (ids[0],))
            cur.execute('''DELETE FROM [people]
                           WHERE nickname=?''', (ids[0],))
            con.commit()
            self.update_list_of_users()
        con.close()

    def remove_book(self):
        ui.error_label_2.setText('')
        con = sqlite3.connect('library.sqlite')
        cur = con.cursor()
        rows = list(set([i.row() for i in ui.table_all_books.selectedItems()]))
        ids = [ui.table_all_books.item(i, 0).text() for i in rows]
        if len(ids) > 1:
            ui.error_label_2.setText('Выберите только одну книгу')
        else:
            cur.execute('''DELETE FROM [books]
                           WHERE name=?''', (ids[0],))
            con.commit()
            self.update_list_of_books()
        con.close()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Возвращение книги')
        self.resize(300, 150)
        self.label = QLabel(self)
        self.label.setText('Вы уверены что хотите вернуть эту книгу?')
        self.label.move(40, 25)
        self.btn = QPushButton(self)
        self.btn.setText('Да')
        self.btn.move(15, 100)
        self.btn_2 = QPushButton(self)
        self.btn_2.setText('Нет')
        self.btn_2.move(200, 100)
        self.btn_2.clicked.connect(self.closing)
        self.btn.clicked.connect(self.remove_book)

    def remove_book(self):
        con = sqlite3.connect('library.sqlite')
        cur = con.cursor()
        rows = list(set([i.row() for i in ui.table_of_registered_books.selectedItems()]))
        ids = [ui.table_of_registered_books.item(i, 0).text() for i in rows]
        if len(ids) > 1:
            ui.error_label_1.setText('Выберите только одну книгу')
        else:
            cur.execute('''UPDATE [books] SET status_id = 1
                                       WHERE name=?''', (ids[0],))
            window.registered_books.remove(ids[0])
            window.all_registered_books.remove(ids[0])
            con.commit()
            window.update_list_of_registered_books()
            self.closing()
        con.close()

    def closing(self):
        self.close()
        ui.error_label_1.setText('')


class Joining(QWidget):
    def __init__(self):
        super().__init__()
        self.ui_form = Ui_Form()
        self.join = False
        self.ui_form.setupUi(self)
        self.ui_form.pushButton_2.clicked.connect(self.is_existed)

    def is_existed(self):
        self.con = sqlite3.connect('library.sqlite')
        self.cur = self.con.cursor()
        users = self.cur.execute('''SELECT nickname, password FROM [people]''').fetchall()
        for i in users:
            if i[0] == self.ui_form.lineEdit_2.text() and i[1] == self.ui_form.lineEdit.text():
                ui.user_label.setText(f'Пользователь: {i[0]}')
                ui.error_label_1.setText('')
                self.join = True
                window.show_for_current_user(i[0])
                self.close()
        if not self.join:
            self.ui_form.label_3.setText('Неверный логин или пароль')
        self.con.close()


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        self.ui_form = Ui_Form_2()
        self.ui_form.setupUi(self)
        self.ui_form.pushButton.clicked.connect(self.check_login)

    def check_login(self):
        self.con = sqlite3.connect('library.sqlite')
        self.cur = self.con.cursor()
        self.all_logins = self.cur.execute('''SELECT nickname FROM [people]''').fetchall()
        self.all_logins = [i[0] for i in self.all_logins]
        try:
            if not self.ui_form.lineEdit.text():
                raise EOFError
            elif not self.ui_form.lineEdit_2.text():
                raise PermissionError
            elif self.ui_form.lineEdit.text() in self.all_logins:
                raise ArithmeticError
            else:
                self.cur.execute('''INSERT INTO [people] (nickname, password)
                                    VALUES (?, ?)''',
                                 (self.ui_form.lineEdit.text(), self.ui_form.lineEdit_2.text()))
                self.con.commit()
                self.con.close()
                self.close()
        except EOFError:
            self.ui_form.label.setText('Вы не ввели никнейм')
        except PermissionError:
            self.ui_form.label.setText('Вы не ввели пароль')
        except ArithmeticError:
            self.ui_form.label.setText('Такой логин уже существует')
        finally:
            window.update_list_of_users()
            self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    dialog_1 = Window()
    member = Joining()
    reg = Registration()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
