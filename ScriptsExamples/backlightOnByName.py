import re, os, bpy, bge, xlrd3, GameLogic

sceneCurrent = GameLogic.getCurrentScene()
objectAction = sceneCurrent.objects['2 Buildings Height 02']
objectAction.playAction('backlightOn', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_LOOP)