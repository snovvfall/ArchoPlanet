import re, os, bpy, bge, xlrd3

controllerCurrent = bge.logic.getCurrentController()
objectCurrent = controllerCurrent.owner
objectCurrent.playAction('backlightOn', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)