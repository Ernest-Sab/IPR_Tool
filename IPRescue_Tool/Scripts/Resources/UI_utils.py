"""
UI Utilities
============

Description:
------------
This module provides utility classes and functions for creating and managing UI components using PySide2. 
It includes classes for sliders, checkboxes, combo boxes, line edits, drop-down menus, and dynamic menu bars.

Classes:
--------
- Sliders: A class for creating slider widgets with associated labels and text fields.
- CheckBox: A class for creating checkbox widgets with associated labels.
- ComboBox: A class for creating combo box widgets with a list of items.
- LineEditNum: A class for creating line edit widgets for numerical input with validation.
- DropMenu: A class for creating drop-down menu buttons with open and close states.
- DynamicMenuBar: A class for creating dynamic menu bars with customizable actions.

Modules:
--------
- PySide2.QtCore
- PySide2.QtWidgets
- PySide2.QtGui

Usage:
------
Import this module and use the provided classes to create and manage UI components:
    from Resources.UI_utils import Sliders, CheckBox, ComboBox, LineEditNum, DropMenu, DynamicMenuBar

Author:
-------
Ernesto Sabato

Date:
-----
March 5, 2025
"""

from PySide2 import QtCore, QtWidgets, QtGui

class Sliders(QtWidgets.QDialog):

    def __init__(self, name, value={'min':1, 'max':100, 'decimal': 0, 'default':10, 'interval':1}, parent=None):
        super(Sliders, self).__init__(parent)

        self.slider_group(name, value)
        self.create_layout()
        self.create_connections()
        self.def_value = value['default']

    def slider_group(self, name, value):

        if value['decimal'] == 0:
            validator = QtGui.QIntValidator(value['min'],value['max'], self)
        elif value['decimal'] > 0:
            validator = QtGui.QDoubleValidator(value['min'],value['max'], value['decimal'], self)
        else:
            raise TypeError('Number not supported')

        #Label Name        
        self.label = QtWidgets.QLabel('{}    '.format(name))
        self.label.setStyleSheet(
            'font-size: 12px;'
        )
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)

        #Number Edit
        self.num_text = QtWidgets.QLineEdit()
        self.num_text.setStyleSheet(
        'background-color: rgb(54,54,54);'
        'font-size: 11px;')
        self.num_text.setFixedWidth(80)
        self.num_text.setFixedHeight(25)
        self.num_text.setText(str(value['default']))
        self.num_text.setValidator(validator)

        #Slider
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(value['min'])
        self.slider.setMaximum(value['max'])
        self.slider.setValue(value['default'])
        self.slider.setTickInterval(value['interval'])
        self.slider.setFixedWidth(200)

    def value_text(self):
        self.txt_value = self.num_text.text()

        return float(self.txt_value)
        
    def create_layout(self):
        iterations_lay = QtWidgets.QHBoxLayout(self)
        iterations_lay.addWidget(self.label)
        iterations_lay.addWidget(self.num_text, QtCore.Qt.AlignRight)
        iterations_lay.addWidget(self.slider, QtCore.Qt.AlignRight)

        iterations_lay.setContentsMargins(0, 0, 0, 0)

    def create_connections(self):
        self.slider.valueChanged.connect(self.print_txt)
        self.num_text.textEdited.connect(self.change_slider)
        self.num_text.textEdited.connect(self.change_label_font)
        self.slider.valueChanged.connect(self.change_label_font)

    def print_txt(self):
        sliderValue = self.slider.value()
        self.num_text.setText(str(sliderValue))

    def change_slider(self):
        txt_value = self.num_text.text()
        self.slider.setValue(float(txt_value))

    def change_label_font(self):
        txt_value = self.value_text()

        if txt_value != self.def_value:
            self.label.setStyleSheet(
                'font-size: 11px;'
                'font-weight: bold;'
            )
        else:
            self.label.setStyleSheet(
                'font-size: 11px;'
            )

class CheckBox(QtWidgets.QDialog):

    def __init__(self, name, status=False, parent=None):
        super(CheckBox, self).__init__(parent)

        self.check_box(name, status)
        self.create_layout()
        self.init_state = status
        self.create_connections()

    def check_box(self, name, status):
        self.check_box = QtWidgets.QCheckBox(name)
        
        if status == True:
            self.check_box.setChecked(True)

    def create_layout(self):
        check_lay = QtWidgets.QGridLayout(self)
        check_lay.addWidget(self.check_box)

        check_lay.setContentsMargins(0, 0, 0, 0)
    
    def create_connections(self):
        self.check_box.stateChanged.connect(self.status_check)
        self.check_box.stateChanged.connect(self.change_font)

    def status_check(self):
        self.check_status = self.check_box.isChecked()
        return self.check_status

    def change_font(self):
        if self.status_check() != self.init_state:
            self.check_box.setStyleSheet(
                'font-weight: bold;'
            )
        else:
            self.check_box.setStyleSheet(
                'font-weight: normal;'
            )

class ComboBox(QtWidgets.QDialog):
    
    def __init__(self, items = {1: 'item_1',
                                2: 'item_2'}, default=0, parent=None):
        super(ComboBox, self).__init__(parent)

        self.create_widgets(items, default)
        self.create_layout()
        self.def_item = default
        self.create_connections()

    def create_widgets(self, items, default):
        self.box = QtWidgets.QComboBox()

        if len(items) < 2:
            raise TypeError("Not Enough items")
        else:
            for item in items.values():
                self.box.addItem(str(item))

        if default > len(items)-1:
            raise TypeError("Not Enough items to set this index as a default\n"
                            "The first index is equal to 0")
        else:
            self.box.setCurrentIndex(default)

    def create_layout(self):
        combo_lay = QtWidgets.QVBoxLayout(self)
        combo_lay.addWidget(self.box)

        combo_lay.setContentsMargins(0, 0, 0, 0)

    def create_connections(self):
        self.box.currentIndexChanged.connect(self.selected_item)
        self.box.currentIndexChanged.connect(self.change_font)

    def signal(self):
        return self.box

    def selected_item(self):
        self.item = self.box.currentIndex()
        return self.item

    def change_font(self):
        if self.selected_item() != self.def_item:
            self.box.setStyleSheet(
                'font-weight: bold;'
            )
        else:
            self.box.setStyleSheet(
                'font-weight: normal;'
            )

class LineEditNum(QtWidgets.QDialog):
    def __init__(self, name, value={'min': 0, 'max': 10, 'decimal': 0, 'default': 1}, parent=None):
        super(LineEditNum, self).__init__(parent)

        self.create_widgets(name, value)
        self.create_layout()
        self.create_connections()
        
        self.def_value = value['default']

    def create_widgets(self, name, value):
        if value['decimal'] == 0:
            validator = QtGui.QIntValidator(value['min'],value['max'], self)
        elif value['decimal'] > 0:
            validator = QtGui.QDoubleValidator(value['min'],value['max'], value['decimal'], self)
        else:
            raise TypeError('Number not supported')

        #Label Name        
        self.label = QtWidgets.QLabel('{}: '.format(name))
        self.label.setStyleSheet(
            'font-size: 12px;'
        )
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)

        #Number Edit
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setStyleSheet(
        'background-color: rgb(54,54,54);'
        'font-size: 11px;')
        self.line_edit.setFixedWidth(40)
        self.line_edit.setFixedHeight(25)
        self.line_edit.setText(str(value['default']))
        self.line_edit.setValidator(validator)
    
    def create_layout(self):
        line_edit_lay = QtWidgets.QHBoxLayout(self)
        line_edit_lay.addWidget(self.label)
        line_edit_lay.addWidget(self.line_edit)
        line_edit_lay.addStretch()

        line_edit_lay.setContentsMargins(0, 0, 0, 0)

    def create_connections(self):
        self.line_edit.textEdited.connect(self.text_number)
        self.line_edit.textEdited.connect(self.change_label_font)

    def text_number(self):
        self.txt_value = self.line_edit.text()
        return float(self.txt_value)
        
    def change_label_font(self):
        txt_value = self.text_number()

        if txt_value != self.def_value:
            self.label.setStyleSheet(
                'font-size: 11px;'
                'font-weight: bold;'
            )
        else:
            self.label.setStyleSheet(
                'font-size: 11px;'
            )

class DropMenu(QtWidgets.QDialog):
    def __init__(self, name, image = {'open': None,
                                      'close': None}, default='open', parent=None):
        super(DropMenu, self).__init__(parent)

        self.btn_images()
        self.create_widgets(name, image, default)
        self.create_layout()
        self.create_connections()

    def create_widgets(self, name, image, default):
        #Drop-down
        self.open_btn = QtWidgets.QPushButton(name)
        self.open_btn.setMinimumHeight(30)
        self.close_btn = QtWidgets.QPushButton(name)
        self.close_btn.setMinimumHeight(30)

        #Button Open
        if image['open']:
            self.btn_open_style(self.open_btn, image['open'])
        else:
            self.btn_open_style(self.open_btn, self.image_down)

        #Button Close
        if image['close']:
            self.btn_close_style(self.close_btn, image['close'])
        else:
            self.btn_close_style(self.close_btn, self.image_up)

        if default == 'open':
            self.close_btn.hide()
        elif default == 'close':
            self.open_btn.hide()
        else:
            raise TypeError('Invalid input')

    def create_layout(self):
        drop_lay = QtWidgets.QVBoxLayout(self)
        drop_lay.addWidget(self.open_btn)
        drop_lay.addWidget(self.close_btn)

        drop_lay.setContentsMargins(0, 0, 0, 0)

    def btn_images(self):
        #Arrow pictures
        self.arrow_up = QtWidgets.QStyle.SP_TitleBarShadeButton
        self.arrow_down = QtWidgets.QStyle.SP_TitleBarUnshadeButton
        self.image_down = self.style().standardIcon(self.arrow_up)  
        self.image_up = self.style().standardIcon(self.arrow_down)

    def btn_open_style(self, btn, image):
        btn.setIcon(image)
        btn.setStyleSheet(
            'QPushButton {text-align: left;'
            'font-weight: bold;'
            'font-size: 12px;'
            'border-radius: 5px;'
            'background-color: rgb(110, 110, 110);}'

            'QPushButton:hover {'
            'background-color: rgb(120, 120, 120);}'
        )

    def btn_close_style(self, btn, image):
        btn.setIcon(image)
        btn.setStyleSheet(
            'QPushButton {text-align: left;'
            'font-size: 12px;'
            'border-radius: 5px;'
            'background-color: rgb(90, 90, 90);}'

            'QPushButton:hover {'
            'background-color: rgb(100, 100, 100);}'
        )   

    def create_connections(self):
        self.open_btn.clicked.connect(self.hide_element)
        self.close_btn.clicked.connect(self.show_element)

    def hide_element(self):
        self.close_btn.setVisible(True)
        self.open_btn.setVisible(False)

    def show_element(self):
        self.close_btn.setVisible(False)
        self.open_btn.setVisible(True)

    def btn_return(self):
        return self.open_btn, self.close_btn

class DynamicMenuBar(QtWidgets.QDialog):
    def __init__(self, items, parent=None):
        super(DynamicMenuBar, self).__init__(parent)

        self.actions = {}
        self.create_widgets(items)
        self.create_layout()

    def create_widgets(self, items):
        self.menu_bar = QtWidgets.QMenuBar()
        self.menu_bar.setMinimumHeight(25)

        for key, value in items.items():
            menu = self.menu_bar.addMenu(key)
            for action_name in value:
                action = QtWidgets.QAction(action_name, self)
                menu.addAction(action)
                self.actions[action_name] = action

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setMenuBar(self.menu_bar)
        layout.setContentsMargins(0, 0, 0, 0)

    def get_action(self, action_name):
        return self.actions.get(action_name)

if __name__ == '__main__':
    ui = DynamicMenuBar()
    ui.show()