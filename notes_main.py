from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QRadioButton,
QPushButton,QButtonGroup,QGridLayout,QGroupBox,QMessageBox,QInputDialog,
QLabel, QVBoxLayout, QHBoxLayout,QTextEdit,QLineEdit,QListWidget)
import json

'''with open('questions.json', 'r', encoding='utf-8') as file:
    json.dump(z_list_json, file, ensure_ascii=False, sort_keys=True)'''
try:
    with open('z_list_json.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except:
    data = {}

def update_json():
    with open('z_list_json.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, sort_keys=True)

def show_z():
    name = z_list.selectedItems()[0].text()
    create_z.setText(data[name]['текст'])
    t_list.clear()
    t_list.addItems(data[name]['теги'])

def add_t(): 
    if z_list.selectedItems():
        t_dialog = QInputDialog(main_win)
        t_dialog.setWindowTitle('Добавить тег')
        t_dialog.resize(400,300)
        if t_dialog.exec():
            t_name = t_dialog.textValue()
            name = z_list.selectedItems()[0].text()
            if t_name != '' and t_name not in data[name]['теги']: 
                data[name]['теги'].append(t_name)
                t_list.addItem(t_name) 
                update_json()  

def add_z():
    z_name , ok = QInputDialog.getText(
        main_win,'добавте заметку','Ввод названия заметки'
    )
    if ok and z_name != '' and z_name not in data:
        data[z_name] = {'текст':'','теги':['Новая']}
        z_list.addItem(z_name)
        update_json()

def save_z():
    if z_list.selectedItems():
        name = z_list.selectedItems()[0].text()
        data[name]['текст']=create_z.toPlainText()
        update_json()


def del_z():
    if z_list.selectedItems():
        name = z_list.selectedItems()[0].text()
        create_z.clear()
        del data[name]
        t_list.clear()
        z_list.clear()
        z_list.addItems(data)
        update_json()

def del_t():
    if z_list.selectedItems() and t_list.selectedItems():
        name_t = t_list.selectedItems()[0].text()
        name_z = z_list.selectedItems()[0].text()
        t_list.clear()
        data[name_z]['теги'].remove(name_t)
        t_list.addItems(data[name_z]['теги'])
        update_json()

def search_t():
    note={}
    t_dialog = QInputDialog(main_win)
    t_dialog.setWindowTitle('искать заметку по тегу')
    t_dialog.resize(400,300)
    if t_dialog.exec():
        t_name = t_dialog.textValue()
        z_list.clear()
        for note_name in data. keys():
            if t_name in data[note_name] ['теги']:
                note[note_name] = data[note_name]
        z_list.addItems(note)
        t_list.clear()
        create_z.clear()

def cancel_search_t():
    z_list.clear()
    t_list.clear()
    create_z.clear()
    z_list.addItems(data)

app = QApplication([])
main_win =QWidget()
main_win.setWindowTitle('умные заметки')
main_win.resize(1000,700)

lable_z = QLabel('список заметок')
lable_t = QLabel('список тегов')
vbl1 = QVBoxLayout()
vbl2 = QVBoxLayout()
hbl = QHBoxLayout()
hbl.addLayout(vbl1)
hbl.addLayout(vbl2)
main_win.setLayout(hbl)

b_add_z=QPushButton('создать заметку')
b_del_z=QPushButton('удалить замтку')
b_save_z=QPushButton('сохранить заметку')
b_add_t=QPushButton('добавить тег')
b_del_t=QPushButton('удалить тег')
b_search_t=QPushButton('искать по тегу')
b_cancel_search_t=QPushButton('отменить поиск')

create_z = QTextEdit()
t_list = QListWidget()
z_list = QListWidget()

z_list.addItems(data)

vbl2.addWidget(create_z)
vbl2.addWidget(b_add_z)
vbl2.addWidget(b_del_z)
vbl2.addWidget(b_save_z)
vbl2.addWidget(lable_t)
vbl2.addWidget(t_list)
vbl2.addWidget(b_add_t)
vbl2.addWidget(b_del_t)
vbl2.addWidget(b_search_t)
vbl2.addWidget(b_cancel_search_t)
vbl1.addWidget(lable_z)
vbl1.addWidget(z_list)

b_add_t.clicked.connect(add_t)
b_add_z.clicked.connect(add_z)
b_save_z.clicked.connect(save_z)
b_del_z.clicked.connect(del_z)
b_del_t.clicked.connect(del_t)
b_search_t.clicked.connect(search_t)
b_cancel_search_t.clicked.connect(cancel_search_t)

z_list.itemClicked.connect(show_z)

app.setStyleSheet("""
    QWidget {
        background-color: #121212;
        color: #FFFFFF;
    }
    QPushButton {
        background-color: #333333;
        border: 1px solid #555555;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #444444;
    }
    QTextEdit {
        font-size: 24px;   
    }
""")

main_win.show()
app.exec_()
