import bge, mathutils, xlrd3

#Find scenes
scenes = bge.logic.getSceneList()
for sceneIterate in scenes:
    if 'Interface' in sceneIterate.name:
        sceneInterface = sceneIterate
    if 'City' in sceneIterate.name:
        sceneCity = sceneIterate

#Only on first script launch dim all objects except landscape
if sceneCity.objects['action'].localPosition == mathutils.Vector((-10000.0, -10000.0, 0.0)):
    for objectIterate in sceneCity.objects:
        if 'Irkutsk' in objectIterate.name:
            sceneCity.objects['action'].localPosition = mathutils.Vector((-10001.0, -10000.0, 0.0))
            objectIterate.playAction('CityStartup', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)