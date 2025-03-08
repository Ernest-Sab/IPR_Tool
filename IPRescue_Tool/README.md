# IPRescue Tool

## Author
Ernesto Sabato

## Date
March 5, 2025

## Version
1.0.0

## Description

The IPRescue is a user-friendly tool for Autodesk Maya that provides functionalities for creating and managing deformers to cleanup IPs in shots.
This tool is a mix of multiple tools built initially for the CFX or Tech Anim department to speed-up the Cleanup process of Pre or Post simulation, but it can be used everywhere it is necessary to deform and clean IPs.

## Features

- **SuperDelta Deformer**: Automates the creation and management of deltaMush deformers.
- **Pull-Push Deformer**: Automates the creation and management of texture deformers for pulling and pushing geometries.

## Installation

1. Download the folder into your local Maya scripts folder (..\user\Documents\maya\scripts\) or somewhere on your local machine.
2. If you choose the second option, ensure that the repository is added to your Python path in Maya.

## Usage

### Opening the IPRescue UI

To open the IPRescue UI in Autodesk Maya, run the following command in the Maya script editor using the Python tab:

```python
from IPRescue_Tool import open_IPRescue as ipr

if __name__ == '__main__':
    ipr.open_IPRescue_ui()
```

You can also create a shelf button by dragging the code into the shelf.

### SuperDelta Deformer
The SuperDelta Tool is based on the DeltaMush native Maya Deformer.
The SuperDelta will automitize some processes that are fundamental in making the deformer work properly,
as, for example, appling it to the correct frame in the timeline.

The tool can be used in 2 modes:
- **Object Mode**: Select the geometry in object mode and apply the deltaMush deformer. 
Applying the deltaMush through Object selection will create a normal deltaMush, 
but all the influences will be painted to 0%.
- **Component Mode**: Select components and apply the deltaMush deformer. 
The influence will be painted in the specified area, and you can adjust the smooth area with the Paint Smooth Value.

### Pull-Push Deformer
The Pull-Push Tool is based on the Texture Deformer native Maya Deformer.
This tool will automatize some settings based on your needs to cover the purpose of cleaning IP in shots.

The tool can be used in 2 modes:
1. **Object Mode**: Select the geometry in object mode and apply the Pull or Push deformer. 
The influences will be painted to 0%, and you can paint the influence where needed.
2. **Component Mode**: Select components and apply the Pull or Push deformer. 
The influence will be painted in the specified area, and you can adjust the smooth area with the Paint Smooth Value.

- **PULL BUTTON**: The Pull button will set the deformer so that the geo will be moved outside following its normals.
- **PUSH BUTTON**: The Push button will set the deformer so that the geo will be moved inside following its normals.

## Compatibility
The scripts are compatible with both Python 2 and Python 3.

## Files

[Open IPR Tool](../IPRescue_Tool/open_IPRescue.py)

This script imports and opens the Easy Deform UI in Autodesk Maya.

[IPR UI](../IPRescue_Tool/Scripts/IPRescue_UI.py)

This script provides the main user interface for the Easy Deform tool. 
It includes classes for creating and managing the SuperDelta and Pull-Push deformers.

[IPR Program File](../IPRescue_Tool/Scripts/IPRescue_prog.py)

This module provides core functionalities for the Easy Deform tool. 
It includes functions for checking selections, applying paint modes, and creating deformers such as deltaMush and texture deformers.

[Maya Utilities](..\IPRescue_Tool/Scripts/Resources/maya_utils.py)

This module provides utility functions for working with Autodesk Maya. 
It includes functions to get the Maya main window and delete workspace controls.

[UI Utilities](../IPRescue_Tool/Scripts/Resources/UI_utils.py)

This module provides utility classes and functions for creating and managing UI components using PySide2. 
It includes classes for sliders, checkboxes, combo boxes, line edits, drop-down menus, and dynamic menu bars.
