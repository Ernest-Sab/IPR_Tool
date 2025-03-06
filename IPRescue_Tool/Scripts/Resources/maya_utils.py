"""
Maya Utilities
==============

Description:
------------
This module provides utility functions for working with Autodesk Maya. 
It includes functions to get the Maya main window and delete workspace controls.

Functions:
----------
- get_maya_main_window(instance): Returns the Maya main window as a PySide2 QWidget instance.
- delete_workspace_control(ctrl): Deletes the specified workspace control if it exists.

Modules:
--------
- __future__
- shiboken2
- maya.cmds
- maya.OpenMayaUI
- logging

Author:
-------
Ernesto Sabato

Date:
-----
March 5, 2025
"""

from __future__ import absolute_import, division, print_function, unicode_literals
from shiboken2 import wrapInstance
import maya.cmds as mc
import maya.OpenMayaUI as omui
import logging

logger = logging.getLogger(__name__)

def get_maya_main_window(instance):
    ''' Return Maya main window as a PySide2 QWidget instance.'''
    try:
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(int(main_window_ptr), instance)
    except Exception as e:
        logger.error('Error getting Maya main window: {}'.format(e))
        return None

def delete_workspace_control(ctrl):
    try:
        if mc.workspaceControl(ctrl, q=True, exists=True):
            mc.workspaceControl(ctrl, e=True, close=True)
            mc.deleteUI(ctrl, control=True)
        logger.info('Workspace control {} deleted successfully.'.format(ctrl))
    except Exception as e:
        logger.error('Error deleting workspace control: {}'.format(e))