"""
Open IPRescue UI
===================

Description:
------------
This script imports and opens the IPRescue UI in Autodesk Maya.

Usage:
------
To use this script, run the following command in the Maya script editor:
    import open_IPRescue
    open_IPRescue.open_IPRescue_ui()

You can also create a shelf button by dragging the code into the shelf.

Author:
-------
Ernesto Sabato

Date:
-----
March 5, 2025
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
import traceback

sys.path.append(r'C:\Users\ernes\Documents\Personal_projects\Cleanup_Tool_gumroad\free_version')
import IPRescue_UI

def open_easy_deform_ui():
    try:
        mainUi = IPRescue_UI.ToolsUI()
        mainUi.show(dockable=True)
    except Exception as e:
        traceback.print_exc()
        print('An error occurred: {}'.format(e))

if __name__ == '__main__':
    open_easy_deform_ui()