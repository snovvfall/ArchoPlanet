import re, os, bpy, bge, xlrd3, GameLogic

sheet_path = 'D:\\Dropbox\\2Current\\ArchoPlanet'
workbookCurrent = xlrd3.open_workbook(sheet_path + "\\City\\Irkutsk\\" + "Irkutsk.xls")
"%s\\Irkutsk.xls" % sheet_path
workbookCurrent.sheet_names()
sheetStreets = workbookCurrent.sheet_by_name(u'Streets')
sheetBuildings = workbookCurrent.sheet_by_name(u'Buildings')

#objectCurrent is owner of controllerCurrent
controllerCurrent = bge.logic.getCurrentController()
objectCurrent = controllerCurrent.owner
sceneCurrent = GameLogic.getCurrentScene()

#Find street which name is equal to objectCurrent's name
for sheetStreetsRowNumber in range(sheetStreets.nrows):
    if sheetStreets.cell(sheetStreetsRowNumber,0).value == objectCurrent.name:
		#Find building in sheetBuildings which belongs to the street named objectCurrent
		for sheetBuildingsRowNumber in range(sheetBuildings.nrows):
			if sheetBuildings.cell(sheetBuildingsRowNumber,13).value == objectCurrent.name:
				#Backlight buildings which belong to street
				objectAction = sceneCurrent.objects[sheetBuildings.cell(sheetBuildingsRowNumber,0).value]
				objectAction.playAction('backlightOn', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PING_PONG)