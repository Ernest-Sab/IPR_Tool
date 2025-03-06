"""
IPRescue UI Script
=====================

Description:
------------
This script provides a user interface for the IPRescue tool in Autodesk Maya. 
It includes functionalities for creating and managing deformers such as superDelta and Pull-Push.

Modules:
--------
- maya.cmds
- maya.api.OpenMaya
- maya.mel
- maya.app.general.mayaMixin
- PySide2.QtCore
- PySide2.QtWidgets
- PySide2.QtGui

Custom Modules:
---------------
- Resources.maya_utils
- Resources.UI_utils
- easy_deform_prog

Classes:
--------
- superDelta: A dialog for creating and managing the superDelta deformer.
- PullPush: A dialog for creating and managing the Pull-Push deformer.
- ToolsUI: The main UI class that integrates the superDelta and Pull-Push dialogs.

Author:
-------
Ernesto Sabato

Date:
-----
March 5, 2025

Version:
--------
1.0.0
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.mel as mel
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtCore, QtWidgets, QtGui

import os
import sys

from Resources.maya_utils import get_maya_main_window, delete_workspace_control
from Resources.UI_utils import DropMenu, DynamicMenuBar, Sliders

import IPRescue_prog as cl_pr

# Global variable for the version
TOOL_VERSION = '1.0.0'

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'): 
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) 
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'): 
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    
class superDelta(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(superDelta, self).__init__(parent)

        self.setObjectName('superDelta_UI')
        self.setFixedSize(450, 130)
        
        self.setStyleSheet('#superDelta_UI {border: 3px solid rgb(90,90,90);'
            'border-radius: 5px;'
            'background-color: rgb(72,72,72);}'
        )

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        # Import Slider
        self.iterations_slider = Sliders('Iteration')
        self.paint_smooth_slider = Sliders('Paint Smooth Value', value={'min':0, 'max':10, 'decimal': 0, 'default':2, 'interval':1})

        # Apply button
        self.apply_superDelta_btn = QtWidgets.QPushButton('Create superDelta')
        self.apply_superDelta_btn.setStyleSheet(
            'QPushButton {font-weight: bold;'
            'font-size: 12px;'
            'background-color: rgb(0,122,44);'
            'border-radius: 5px;}'
            
            'QPushButton:hover {'
            'background-color: rgb(0,130,50);'
            'border-radius: 10px;}'

            'QPushButton:pressed {'
            'color: yellow;'
            'background-color: rgb(0,135,55);'
            'border-radius: 15px;}'
        )
        
        self.apply_superDelta_btn.setFixedHeight(30)
        
        # Help button
        self.info = QtWidgets.QStyle.SP_MessageBoxInformation
        self.info_image = self.style().standardIcon(self.info)  

        self.help_btn = QtWidgets.QPushButton()
        self.help_btn.setIcon(self.info_image)
        self.help_btn.setFixedWidth(30)
        self.help_btn.setFixedHeight(30)
        self.help_btn.setStyleSheet(
            '''
            QPushButton {
            border-radius: 2px;}

            QPushButton:hover {
            background-color: rgb(100,100,110);}
            '''
        )

    def create_layout(self):
        sliders_lay = QtWidgets.QVBoxLayout()
        sliders_lay.addWidget(self.iterations_slider)
        sliders_lay.addWidget(self.paint_smooth_slider)

        buttons_lay = QtWidgets.QHBoxLayout()
        buttons_lay.addWidget(self.apply_superDelta_btn)
        buttons_lay.addWidget(self.help_btn, QtCore.Qt.AlignBottom)

        master_lay = QtWidgets.QVBoxLayout(self)
        master_lay.addLayout(sliders_lay)
        master_lay.addLayout(buttons_lay)
        master_lay.addStretch()

    def create_connections(self):
        self.help_btn.clicked.connect(self.message)
        self.apply_superDelta_btn.clicked.connect(self.execute)

    def message(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowTitle('How to use the superDelta tool')
        messageBox.setText('The DeltaMush is a useful deformer when it comes to cleaning IP through geometries.\n'
                            'The superDelta will automatize some processes that are fundamental in making the deformer work properly.'
                            '\nFor example, it automatically always creates the deformer at the beginning of your timeline.'
                            '\n\n How to use:\n'
                            '1. SELECT THE GEOMETRY IN OBJECT MODE: applying the deltaMush through Object selection will create a normal deltaMush, but all the influences will be painted to 0%.'
                            'It will automatically go into Paint Mode to let you paint the influence where you want it.\n\n'
                            '2. SELECT COMPONENTS: Applying the deltaMush through Component selection will create a deltaMush and paint the influence just in the area'
                            'you specified. You can increase or decrease the smooth area around the deltaMush with the Paint Smooth Value.'
                            'Other than that, this option will create the deformer with some custom settings in the attribute to speed-up the clean-up process.'
        )
        
        messageBox.exec_()

    def execute(self):
        self.geo, self.geo_type, self.vtxSel = cl_pr.selection_check()

        # Take Values from Slider
        self.iteration_value = self.iterations_slider.value_text()
        self.paint_smooth_value = self.paint_smooth_slider.value_text()

        try:
            mc.undoInfo(openChunk=True)

            # Turn off viewport
            mel.eval("paneLayout -e -manage false $gMainPane")

            # Go to the first frame
            currentFrame = mc.currentTime(q=1)
            currentFirstFrame = mc.playbackOptions(minTime=1, q=1)

            mc.currentTime(currentFirstFrame, edit=1)
            
            self.deltaMush_deformer = cl_pr.deltaMush(self.geo, self.vtxSel, int(self.iteration_value))
            cl_pr.paint_mode(self.geo, self.vtxSel, int(self.paint_smooth_value), 'deltaMush', self.deltaMush_deformer)
            
            # Go back to the original frame
            mc.currentTime(currentFrame, edit=1)
            mc.playbackOptions(minTime=1, q=1)

            # Turn on viewport
            mel.eval("paneLayout -e -manage true $gMainPane")

            mc.undoInfo(closeChunk=True)
        
        except Exception as e:
            mel.eval("paneLayout -e -manage true $gMainPane")
            mc.undoInfo(closeChunk=True)
            QtWidgets.QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

class PullPush(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PullPush, self).__init__(parent)

        self.setObjectName('push_pull_UI')
        self.setFixedSize(450, 130)

        self.setStyleSheet('#push_pull_UI {border: 3px solid rgb(90,90,90);'
            'border-radius: 5px;'
            'background-color: rgb(72,72,72);}'
        )

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        # Import Sliders
        self.strength_slider = Sliders('Strength', value={'min':1, 'max':50, 'decimal': 0, 'default':1, 'interval':1})
        self.paint_smooth_slider = Sliders('Smooth Iterations', value={'min':0, 'max':10, 'decimal': 0, 'default':2, 'interval':1})

        # Apply buttons
        self.pull_btn = QtWidgets.QPushButton('Create Pull')
        self.pull_btn.setStyleSheet(
            'QPushButton {font-weight: bold;'
            'font-size: 12px;'
            'background-color: rgb(0,122,44);'
            'border-radius: 5px;}'
            
            'QPushButton:hover {'
            'background-color: rgb(0,130,50);'
            'border-radius: 10px;}'

            'QPushButton:pressed {'
            'color: yellow;'
            'background-color: rgb(0,135,55);'
            'border-radius: 15px;}'
        )
        self.pull_btn.setFixedHeight(30)

        self.push_btn = QtWidgets.QPushButton('Create Push')
        self.push_btn.setStyleSheet(
            'QPushButton {font-weight: bold;'
            'font-size: 12px;'
            'background-color: rgb(0,122,44);'
            'border-radius: 5px;}'
            
            'QPushButton:hover {'
            'background-color: rgb(0,130,50);'
            'border-radius: 10px;}'

            'QPushButton:pressed {'
            'color: yellow;'
            'background-color: rgb(0,135,55);'
            'border-radius: 15px;}'
        )
        self.push_btn.setFixedHeight(30)
        
        # Help button
        self.info = QtWidgets.QStyle.SP_MessageBoxInformation
        self.info_image = self.style().standardIcon(self.info)  

        self.help_btn = QtWidgets.QPushButton()
        self.help_btn.setFixedWidth(30)
        self.help_btn.setFixedHeight(30)
        self.help_btn.setIcon(self.info_image)
        self.help_btn.setStyleSheet(
            '''
            QPushButton {
            border-radius: 2px;}

            QPushButton:hover {
            background-color: rgb(100,100,110);}
            '''
        )

    def create_layout(self):
        sliders_lay = QtWidgets.QVBoxLayout()
        sliders_lay.addWidget(self.strength_slider)
        sliders_lay.addWidget(self.paint_smooth_slider)

        buttons_lay = QtWidgets.QHBoxLayout()
        buttons_lay.addWidget(self.pull_btn)
        buttons_lay.addWidget(self.push_btn)
        buttons_lay.addWidget(self.help_btn, QtCore.Qt.AlignBottom)
        buttons_lay.setContentsMargins(0, 0, 0, 0)

        master_lay = QtWidgets.QVBoxLayout(self)
        master_lay.addLayout(sliders_lay)
        master_lay.addLayout(buttons_lay)
        master_lay.addStretch()

    def create_connections(self):
        self.help_btn.clicked.connect(self.message)
        self.pull_btn.clicked.connect(self.execute_pull)
        self.push_btn.clicked.connect(self.execute_push)
        
    def message(self):
        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowTitle('How to use the Pull-Push tool')
        messageBox.setText('The Texture Deformer is a useful deformer when it comes to cleaning IP through geometries.\n'
                            'The Pull-Push will automatize some settings based on your needs.\n\n\n'
                            'PULL BUTTON: The Pull button will set the deformer so that the geo will be moved outside following its normals.\n\n'
                            'PUSH BUTTON: The Push button will set the deformer so that the geo will be moved inside following its normals.\n'
                            '\n\n How to use:\n'
                            '1. SELECT THE GEOMETRY IN OBJECT MODE: applying the Pull-Push through Object selection will create a Texture Defomer with the settings based on which button you pressed,' 
                            'but all the influences will be painted to 0%.'
                            'It will automatically go into Paint Mode to let you paint the influence where you want it.\n\n'
                            '2. SELECT COMPONENTS: Applying the Pull-Push through Component selection will create a Texture-Deformer with the settings based on which button you pressed,'
                            'and paint the influence just in the specified area'
                            'You can increase or decrease the smooth area around the selected one with the Paint Smooth Value.'
        )
        
        messageBox.exec_()

    def check_sliders_values(self):
        self.geo, self.geo_type, self.vtxSel = cl_pr.selection_check()
        
        # Take Values from Slider
        self.strength_value = self.strength_slider.value_text()
        self.paint_smooth_value = self.paint_smooth_slider.value_text()
    
    def execute_pull(self):
        self.name = '{}_Pull'.format(self.geo)
        self.check_sliders_values()

        self.tex_def = cl_pr.texture_deformer(self.geo, self.vtxSel, 1, self.strength_value, self.name)
        cl_pr.paint_mode(self.geo, self.vtxSel, int(self.paint_smooth_value), 'textureDeformer', self.tex_def)

    def execute_push(self):
        self.geo, self.geo_type, self.vtxSel = cl_pr.selection_check()
        name = '{}_Push'.format(self.geo)
        self.check_sliders_values()

        try:
            mc.undoInfo(openChunk=True)
            
            # Turn off viewport
            mel.eval("paneLayout -e -manage false $gMainPane") 

            self.tex_def = cl_pr.texture_deformer(self.geo, self.vtxSel, -1, self.strength_value*-1, name)
            cl_pr.paint_mode(self.geo, self.vtxSel, self.paint_smooth_value, 'textureDeformer', self.tex_def)

            mel.eval("paneLayout -e -manage true $gMainPane")

            mc.undoInfo(closeChunk=True)
        except Exception as e:
            mel.eval("paneLayout -e -manage true $gMainPane")
            mc.undoInfo(closeChunk=True)
            QtWidgets.QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

class ToolsUI(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    _dock_control = 'toolsUI_Dock' # Unique name for docking in Maya

    def __init__(self, parent=get_maya_main_window(QtWidgets.QDialog)):
        delete_workspace_control(self._dock_control+'WorkspaceControl')

        super(ToolsUI, self).__init__(parent)

        self.setObjectName(self.__class__._dock_control)

        self.setWindowTitle('IPRescue Tools')
        self.setStyleSheet('#toolsUI_Dock {border: 0.5 solid rgb(72,75,75);'
            'border-radius: 10px;'
            'width: 467px;'
            'min-width: 467px;'
            'background-color: rgb(58,60,60);}'
            'QMenuBar {background-color: rgb(58,60,60);}'
        )

        self.btn_images()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def btn_images(self):
        # Arrow pictures
        self.arrow_down = QtWidgets.QStyle.SP_ArrowDown
        self.arrow_right = QtWidgets.QStyle.SP_ArrowRight
        self.icon_arrow_down = self.style().standardIcon(self.arrow_down)  
        self.icon_arrow_right = self.style().standardIcon(self.arrow_right) 

    def create_widgets(self):
        # Menu bar
        self.menu_bar = DynamicMenuBar(items={'Info': ['About', 'Contacts'],
                                              'Help': ['Documentation', 'Updates']})
        self.menu_bar.get_action('Documentation').triggered.connect(self.open_readme)
        self.menu_bar.get_action('Contacts').triggered.connect(self.contacts)
        self.menu_bar.get_action('About').triggered.connect(self.about)

        # self.menu_bar.get_action('Apply to a Secondary Mesh').setCheckable(True)

        # Super-delta drop-down
        self.superDelta_drop = DropMenu('    SuperDelta', image={'open': self.icon_arrow_down,
                                                                 'close': self.icon_arrow_right})
        self.superDelta_open_btn, self.superDelta_close_btn = self.superDelta_drop.btn_return()

        # Push-Pull drop-down
        self.push_pull_drop = DropMenu('    Push-Pull', image={'open': self.icon_arrow_down,
                                                               'close': self.icon_arrow_right})
        self.push_pull_open_btn, self.push_pull_close_btn = self.push_pull_drop.btn_return()

        self.superDeltaUI = superDelta()
        self.pushPullUI = PullPush()

        self.tool_version = QtWidgets.QLabel(TOOL_VERSION)
        self.tool_version.setStyleSheet('color: lightGray; font-size: 10px; font-style: italic;')
        self.tool_version.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

    def create_layout(self):
        deformer_creation_lay = QtWidgets.QVBoxLayout()
        deformer_creation_lay.addWidget(self.superDelta_drop)
        deformer_creation_lay.addWidget(self.superDeltaUI)
        deformer_creation_lay.addWidget(self.push_pull_drop)
        deformer_creation_lay.addWidget(self.pushPullUI)
        deformer_creation_lay.addStretch()

        self.master_lay = QtWidgets.QVBoxLayout(self)
        self.master_lay.addWidget(self.menu_bar)
        self.master_lay.addWidget(QtWidgets.QFrame(frameShape=QtWidgets.QFrame.HLine, frameShadow=QtWidgets.QFrame.Sunken))
        self.master_lay.addLayout(deformer_creation_lay)
        self.master_lay.addWidget(self.tool_version)
        self.setLayout(self.master_lay)

    def create_connections(self):
        self.superDelta_close_btn.clicked.connect(self.show_delta_elem)
        self.superDelta_open_btn.clicked.connect(self.hide_delta_elem)

        self.push_pull_close_btn.clicked.connect(self.show_pull_push_elem)
        self.push_pull_open_btn.clicked.connect(self.hide_pull_push_elem)        

    def open_readme(self):
        try:
            script_dir = os.path.dirname(__file__)
            readme_path = os.path.join(script_dir, '..', 'README.md')
            if os.path.exists(readme_path):
                os.startfile(readme_path)
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'README.md file not found.')
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', f'Could not open README.md: {e}')

    def contacts(self):
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setWindowTitle('Contacts')
        messageBox.setTextFormat(QtCore.Qt.RichText)
        messageBox.setText(
            'For any questions or issues, please contact: <br><br>'
            '<b>Ernesto Sabato</b><br><br>'
            'Email: <b>   g.ernestosabato@gmail.com</b></div>'
        )
        messageBox.exec_()

    def about(self):
        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setWindowTitle('About')
        messageBox.setTextFormat(QtCore.Qt.RichText)
        messageBox.setText(
            '<div align="center">'
            '<b>IPRESCUE TOOL</b><br><br>'
            'Version: <b>{}</b><br><br>'
            'Author: <b>Ernesto Sabato</b><br><br>'
            'Last Date Updated: <b>March 5, 2025</b></div>'.format(TOOL_VERSION)
        )
        messageBox.exec_()
    
    def hide_delta_elem(self):
        # Hide UI
        self.superDeltaUI.hide()
    
    def show_delta_elem(self):
        # Show UI
        self.superDeltaUI.show()

    def hide_pull_push_elem(self):
        # Hide UI
        self.pushPullUI.hide()
    
    def show_pull_push_elem(self):
        # Show UI
        self.pushPullUI.show()

if __name__ == '__main__':
    mainUi = ToolsUI()
    mainUi.show(dockable=True)