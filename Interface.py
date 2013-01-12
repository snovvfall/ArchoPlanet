import bge, mathutils, xlrd3

def level1Clear():
    Level1ClickedCurrent.playAction('InterfaceClickedOff', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
    Level2Current.playAction('Invisible', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
    
def level2Clear():
    Level2ClickedCurrent.playAction('InterfaceClickedOff', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
    Level3Current.playAction('Invisible', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
    
def level3Clear():
    Level3ClickedCurrent.playAction('InterfaceClickedOff', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
    Level4Current.playAction('Invisible', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
    
def level4Clear():
    Level4ClickedCurrent.playAction('InterfaceClickedOff', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)    

#Find scenes
scenes = bge.logic.getSceneList()
for sceneIterate in scenes:
    if 'Interface' in sceneIterate.name:
        sceneInterface = sceneIterate
    if 'City' in sceneIterate.name:
        sceneCity = sceneIterate

#Only on first script launch dim all objects except text
if sceneInterface.objects['Level1 City Parent'].localPosition == mathutils.Vector((0.1, -0.11, 0.0)):
    for objectIterate in sceneInterface.objects:
        if not 'Text' in objectIterate.name:
            sceneInterface.objects['Level1 City Parent'].localPosition = mathutils.Vector((0.1, -0.1, 0.0))
            objectIterate.playAction('InterfaceClickedOff', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
        else:
            objectIterate.playAction('InterfaceText', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
        
#If left mouse button clicked
if bge.logic.mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_ACTIVATED:
    objectClicked = bge.logic.getCurrentController().sensors['MouseOverAny'].hitObject
    
   #Assign current clicked and visible objects as fake object to avoid 'referenced before assignment' errors
    Level1ClickedCurrent = sceneInterface.objects['Action']
    Level2Current = sceneInterface.objects['Action']
    Level2ClickedCurrent = sceneInterface.objects['Action']
    Level3Current = sceneInterface.objects['Action']
    Level3ClickedCurrent = sceneInterface.objects['Action']
    Level4Current = sceneInterface.objects['Action']
    Level4ClickedCurrent = sceneInterface.objects['Action']
    
    #Assign colors which will be used later
    ColorClickedOn = mathutils.Vector((0.5, 0.5, 0.5, 0.7))
    
    #Find current clicked and visible objects
    for objectIterate in sceneInterface.objects:
        if objectIterate.color == ColorClickedOn and 'Level1' in objectIterate.name:
            Level1ClickedCurrent = objectIterate
        if objectIterate.localPosition == mathutils.Vector((2.1, -0.1, 0.0)):
            Level2Current = objectIterate
        if objectIterate.color == ColorClickedOn and 'Level2' in objectIterate.name:
            Level2ClickedCurrent = objectIterate
        if objectIterate.localPosition == mathutils.Vector((4.1, -0.1, 0.0)):
            Level3Current = objectIterate
        if objectIterate.color == ColorClickedOn and 'Level3' in objectIterate.name:
            Level3ClickedCurrent = objectIterate
        if objectIterate.localPosition == mathutils.Vector((6.1, -0.1, 0.0)):
            Level4Current = objectIterate
        if objectIterate.color == ColorClickedOn and 'Level4' in objectIterate.name:
            Level4ClickedCurrent = objectIterate
    
    #Open workbook whick stores information about city's objects
    workbookCity = xlrd3.open_workbook('D:\\Dropbox\\ArchoPlanet' + "\\City\\" + "Irkutsk.xls")
    workbookCity.sheet_names()
    
    #Parse sheetStreets column names
    sheetStreets = workbookCity.sheet_by_name('Streets')
    for sheetStreetsColumn in range(sheetStreets.ncols):
        if sheetStreets.cell(0,sheetStreetsColumn).value == 'Length':
            sheetStreetsColumnLength = sheetStreetsColumn
        if sheetStreets.cell(0,sheetStreetsColumn).value == 'Sections':
            sheetStreetsColumnSections = sheetStreetsColumn
        if sheetStreets.cell(0,sheetStreetsColumn).value == 'District':
            sheetStreetsColumnDistrict = sheetStreetsColumn
    
    #Parse sheetStreetsParts column names
    sheetStreetsParts = workbookCity.sheet_by_name('StreetsParts')
    for sheetStreetsPartsColumn in range(sheetStreetsParts.ncols):
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Directions':
            sheetStreetsPartsColumnDirections = sheetStreetsPartsColumn
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Length':
            sheetStreetsPartsColumnLength = sheetStreetsPartsColumn
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'TrafficCars':
            sheetStreetsPartsColumnTrafficCars = sheetStreetsPartsColumn
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'TrafficPeople':
            sheetStreetsPartsColumnTrafficPeople = sheetStreetsPartsColumn
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Routes':
            sheetStreetsPartsColumnRoutes = sheetStreetsPartsColumn
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Height':
            sheetStreetsPartsColumnHeight = sheetStreetsPartsColumn
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'District':
            sheetStreetsPartsColumnDistrict = sheetStreetsPartsColumn
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Street':
            sheetStreetsPartsColumnStreet = sheetStreetsPartsColumn
        if sheetStreetsParts.cell(0,sheetStreetsPartsColumn).value == 'Route1':
            sheetStreetsPartsColumnRoute1 = sheetStreetsPartsColumn
    
    #Parse sheetBuildings column names
    sheetBuildings = workbookCity.sheet_by_name('Buildings')
    for sheetBuildingsColumn in range(sheetBuildings.ncols):
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Height':
            sheetBuildingsColumnHeight = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Administrative':
            sheetBuildingsColumnAdministrative = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Trade':
            sheetBuildingsColumnTrade = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Food':
            sheetBuildingsColumnFood = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Entertainment':
            sheetBuildingsColumnEntertainment = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Cultural':
            sheetBuildingsColumnCultural = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Residential':
            sheetBuildingsColumnResidential = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Education':
            sheetBuildingsColumnEducation = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Medicine':
            sheetBuildingsColumnMedicine = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Sport':
            sheetBuildingsColumnSport = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Industrial':
            sheetBuildingsColumnIndustrial = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Age':
            sheetBuildingsColumnAge = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Damage':
            sheetBuildingsColumnDamage = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'District':
            sheetBuildingsColumnDistrict = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Street1':
            sheetBuildingsColumnStreet1 = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Street2':
            sheetBuildingsColumnStreet2 = sheetBuildingsColumn
        if sheetBuildings.cell(0,sheetBuildingsColumn).value == 'Quarter':
            sheetBuildingsColumnQuarter = sheetBuildingsColumn 
    
    #If clicked interface Level 1
    if 'Level1' in objectClicked.name:     
        level1Clear()
        level2Clear()
        level3Clear()
        level4Clear()
    
    #If clicked interface Level 2
    if 'Level2' in objectClicked.name:
        level2Clear()
        level3Clear()
        level4Clear()
        
        if objectClicked.name == 'Level2 Buildings Height':
        
            #for sheetBuildingsRow in range(sheetBuildings.nrows): will not work, I don't know why
            for sheetBuildingsRow in range(1, 99999):
                objectCurrent = sceneCity.objects[sheetBuildings.cell(sheetBuildingsRow,0).value]
                
                #Convert cell value which was read from workbook from float to string and remove 'text:' and '.0' from it
                actionCurrent = 'scaleZ1-' + str(sheetBuildings.cell(sheetBuildingsRow,sheetBuildingsColumnHeight).value).replace('text:', '').replace('.0', '')
                objectCurrent.playAction(actionCurrent, 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
            
    #If clicked interface Level 3
    if 'Level3' in objectClicked.name:
        level3Clear()
        level4Clear()
    
    #If clicked interface Level 4
    if 'Level4' in objectClicked.name:
        level4Clear()
        
    sceneInterface.objects[objectClicked.name + ' Parent'].playAction('Visible', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
    objectClicked.playAction('InterfaceClickedOn', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)