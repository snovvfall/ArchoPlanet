import re, os, bpy, bge, xlrd3, GameLogic

def openCityWorkbook(cityWorkbookPath):
    workbookCurrent = xlrd3.open_workbook(cityWorkbookPath + "\\City\\Irkutsk\\" + "Irkutsk.xls")
    "%s\\Irkutsk.xls" % cityWorkbookPath
    workbookCurrent.sheet_names()
    
    #Parse sheetStreets column names
    sheetStreets = workbookCurrent.sheet_by_name('Streets')
    for sheetStreetsColumn in range(sheetStreets.ncols):
        if sheetStreets.cell(0,sheetStreetsColumn).value == 'Length':
            sheetStreetsColumnLength = sheetStreets.cell(0,sheetStreetsColumn).value
        if sheetStreets.cell(0,sheetStreetsColumn).value == 'Sections':
            sheetStreetsColumnSections = sheetStreets.cell(0,sheetStreetsColumn).value
        if sheetStreets.cell(0,sheetStreetsColumn).value == 'District':
            sheetStreetsColumnDistrict = sheetStreets.cell(0,sheetStreetsColumn).value
    
    #Parse sheetStreetsParts column names
    sheetStreetsParts = workbookCurrent.sheet_by_name('StreetsParts')
    for sheetStreetsPartsColumn in range(sheetStreetsParts.ncols):
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Directions':
            sheetStreetsPartsColumnDirections = sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Length':
            sheetStreetsPartsColumnLength = sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'TrafficCars':
            sheetStreetsPartsColumnTrafficCars = sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'TrafficPeople':
            sheetStreetsPartsColumnTrafficPeople = sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Routes':
            sheetStreetsPartsColumnRoutes = sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Height':
            sheetStreetsPartsColumnHeight = sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'District':
            sheetStreetsPartsColumnDistrict = sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Street':
            sheetStreetsPartsColumnStreet = sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Route1':
            sheetStreetsPartsColumnRoute1 = sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value
    
    #Parse sheetBuildings column names
    sheetBuildings = workbookCurrent.sheet_by_name('Buildings')
    for sheetBuildingsColumn in range(sheetBuildings.ncols):
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Height':
            sheetBuildingsColumnHeight = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Administrative':
            sheetBuildingsColumnAdministrative = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Trade':
            sheetBuildingsColumnTrade = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Entertainment':
            sheetBuildingsColumnEntertainment = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Cultural':
            sheetBuildingsColumnCultural = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Residential':
            sheetBuildingsColumnResidential = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Education':
            sheetBuildingsColumnEducation = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Medicine':
            sheetBuildingsColumnMedicine = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Sport':
            sheetBuildingsColumnSport = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Industrial':
            sheetBuildingsColumnIndustrial = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Age':
            sheetBuildingsColumnAge = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Damage':
            sheetBuildingsColumnDamage = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'District':
            sheetBuildingsColumnDistrict = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Street1':
            sheetBuildingsColumnStreet1 = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Street2':
            sheetBuildingsColumnStreet2 = sheetBuildings.cell(0,sheetBuildingsColumn).value
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Quarter':
            sheetBuildingsColumnQuarter = sheetBuildings.cell(0,sheetBuildingsColumn).value

'''#Find street which name is equal to objectClicked's name
def streetBelongingBuildings:
    for sheetStreetsPartsRow in range(sheetStreetsParts.nrows):
        if sheetStreetsParts.cell(sheetStreetsPartsRow,0).value == objectClicked.name:
            #Find building in sheetBuildings which belongs to the street named objectClicked
            for sheetBuildingsRow in range(sheetBuildings.nrows):
                if sheetBuildings.cell(sheetBuildingsRow,13).value == objectClicked.name:
                    #Backlight buildings which belong to street
                    objectAction = sceneIrkutsk.objects[sheetBuildings.cell(sheetBuildingsRow,0).value]
                    objectAction.playAction('backlightOn', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PING_PONG)'''

openCityWorkbook('D:\\Dropbox\\2Current\\ArchoPlanet')

#Iterate through all objects in all scenes and perform backlightOff action
scenes = bge.logic.getSceneList()
for i in scenes:
    if i.name == 'Irkutsk':
        sceneIrkutsk = i
    if i.name == 'Interface':
        sceneInterface = i
sceneIrkutskObjects = sceneIrkutsk.objects
for objectIterate in sceneIrkutskObjects:
    objectIterate.playAction('backlightOff', 1, 24, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
sceneInterfaceObjects = sceneInterface.objects
for objectIterate in sceneIrkutskObjects:
    objectIterate.playAction('backlightOff', 1, 24, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)

'''if mouseSensor.getButtonStatus(bge.events.LEFTMOUSE) == bge.logic.KX_INPUT_JUST_ACTIVATED:
    objectClicked = bge.logic.getCurrentController().sensors["MouseOverAny"].hitObject
    if 'Irkutsk' in objectClicked.name:
        if 'Street' in objectClicked.name:
            if ',' in objectClicked.name:
        if 'Quarter' in objectClicked.name:
        if 'Building' in objectClicked.name:
    else:
        '''