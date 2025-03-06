"""
IPRescue Program
===================

Description:
------------
This module provides core functionalities for the IPRescue tool in Autodesk Maya. 
It includes functions for checking selections, applying paint modes, and creating deformers such as deltaMush and texture deformers.

Functions:
----------
- selection_check(): Checks the current selection in Maya and returns the geometry, its type, and selected vertices.
- paint_mode(geo, vtx, smooth_value, deformer_type, deformer_name): Applies paint mode to the specified geometry and vertices.
- deltaMush(geo, vtx, iteration_value): Creates a deltaMush deformer on the specified geometry with the given iteration value.
- texture_deformer(geo, vtx, offset, strength_value, name): Creates a texture deformer on the specified geometry with the given offset and strength value.

Modules:
--------
- maya.cmds
- maya.mel
- maya.api.OpenMaya

Usage:
------
Import this module and use the provided functions to create and manage deformers in Maya:
    from IPRescue_prog import selection_check, paint_mode, deltaMush, texture_deformer

Author:
-------
Ernesto Sabato

Date:
-----
March 5, 2025
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import maya.cmds as mc
import maya.mel as mel
import maya.api.OpenMaya as om

def selection_check():
    geo = mc.ls(sl=True, o=True)[0]
    geo_type = mc.ls(sl=True, fl=True)
    vtxSel = []

    if len(geo_type) > 0:
        for item in geo_type:
            if '.vtx' in item:
                vtxSel.append(item)

            # convert face\edge into vertex
            elif '.e' in item:
                eConv = mc.polyListComponentConversion(geo_type, fe=1, tv=1)
                for i in eConv:
                    vtxSel.append(i)

            elif '.f' in item:
                fConv = mc.polyListComponentConversion(geo_type, ff=1, tv=1)
                for i in fConv:
                    vtxSel.append(i)

    return geo, geo_type, vtxSel

def paint_mode(geo, vtx, smooth_value, deformer_type, deformer_name):
    try:
        mc.select(geo, af=1)
        mc.percent(deformer_name, v=0)
        mel.eval('ArtPaintBlendShapeWeightsTool')
        mel.eval('artSetToolAndSelectAttr( "artAttrCtx", "{}.{}.weights" );'.format(deformer_type, deformer_name))

        if vtx:
            mc.select(vtx)
            mel.eval('artAttrPaintOperation artAttrCtx Replace;')
            mel.eval('artAttrCtx -e -value 1 `currentCtx`;')
            mel.eval('artAttrCtx -e -clear `currentCtx`;')

            mc.select(vtx)
            mel.eval('invertSelection;')
            for _ in range(smooth_value):
                mc.GrowPolygonSelectionRegion()

            mel.eval('artAttrPaintOperation artAttrCtx Smooth;')
            mel.eval('artAttrCtx -e -value 1 `currentCtx`;')
            for _ in range(smooth_value):
                mel.eval('artAttrCtx -e -clear `currentCtx`;')

            mc.select(vtx)
    except Exception as e:
        print('Error in paint_mode: {}'.format(e))

def deltaMush(geo, vtx, iteration_value):
    name_suffix = 'superDelta'

    if mc.objectType(geo) == 'mesh':
        geo_transform = mc.listRelatives(geo, parent=True)[0]

        delta_mush_deformer = mc.deltaMush(
            geo_transform, name = '{}_{}'.format(geo_transform, name_suffix), ss=1, si=iteration_value
        )[0]

        mc.setAttr('{}.displacement'.format(delta_mush_deformer), 0)
    else:
        delta_mush_deformer = mc.deltaMush(geo, name = '{}_{}'.format(geo, name_suffix), si=iteration_value)[0]

    return delta_mush_deformer

def texture_deformer(geo, vtx, offset, strength_value, name):
    name_suffix = 'texDef'

    tex_def, handle = mc.textureDeformer(geo, n='{}_{}'.format(name, name_suffix), en=1, s=strength_value, d="Normal", pointSpace="UV", o=offset)
    mc.setAttr("{}.texture".format(tex_def), 1,1,1, type='double3')
    mc.setAttr('{}.hiddenInOutliner'.format(handle), True)

    return tex_def