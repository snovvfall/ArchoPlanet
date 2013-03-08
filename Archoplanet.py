import bge, mathutils, os, imp

def WorkbookSheet(WorkbookPath, SheetName):
    Workbook = xlrd3.open_workbook(os.path.join(os.path.abspath(''), WorkbookPath))
    Workbook.sheet_names()
    Sheet = Workbook.sheet_by_name(SheetName)
    return Sheet

def WorkbookSheetColumnNumber(Sheet, SheetColumn):
    for SheetColumnIterate in range(Sheet.ncols):
        if Sheet.cell(0,SheetColumnIterate).value == SheetColumn:
            SheetColumnNumber = SheetColumnIterate
    return SheetColumnNumber

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

# Import xlrd3 module from ArchoPlanet directory
xlrd3 = imp.load_source('xlrd3', os.path.join(os.path.abspath(''), 'xlrd3', '__init__.py'))

# Find scenes
scenes = bge.logic.getSceneList()
for sceneIterate in scenes:
    if 'Interface' in sceneIterate.name:
        sceneInterface = sceneIterate
    if 'Earth' in sceneIterate.name:
        sceneEarth = sceneIterate
    if 'Cities' in sceneIterate.name:
        sceneCity = sceneIterate

# Dim all objects except landscape and text
if sceneInterface.objects['Level1 City Parent'].localPosition == mathutils.Vector((0.1, -0.11, 0.0)):
    for objectIterate in sceneInterface.objects:
        if not 'Text' in objectIterate.name:
            sceneInterface.objects['Level1 City Parent'].localPosition = mathutils.Vector((0.1, -0.1, 0.0))
            objectIterate.playAction('InterfaceClickedOff', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
        else:
            objectIterate.playAction('InterfaceText', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)

# If left mouse button clicked
if bge.logic.mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_JUST_ACTIVATED:
    objectClicked = bge.logic.getCurrentController().sensors['MouseOverAny'].hitObject
    
    # Python scene management, not finished
    '''if objectClicked.name == 'CityIrkutsk':
        sceneEarth.end
        bge.logic.addScene(CityIrkutsk, overlay=0)
        if sceneCity.objects['action'].localPosition == mathutils.Vector((-10000.0, -10000.0, 0.0)):
            for objectIterate in sceneCity.objects:
                if 'Irkutsk' in objectIterate.name:
                    sceneCity.objects['action'].localPosition = mathutils.Vector((-10001.0, -10000.0, 0.0))
                    objectIterate.playAction('CityStartup', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)'''
    
   # Assign current clicked and visible objects as fake object to avoid 'referenced before assignment' errors
    Level1ClickedCurrent = sceneInterface.objects['Action']
    Level2Current = sceneInterface.objects['Action']
    Level2ClickedCurrent = sceneInterface.objects['Action']
    Level3Current = sceneInterface.objects['Action']
    Level3ClickedCurrent = sceneInterface.objects['Action']
    Level4Current = sceneInterface.objects['Action']
    Level4ClickedCurrent = sceneInterface.objects['Action']
    
    # Assign colors which will be used later
    ColorClickedOn = mathutils.Vector((0.5, 0.5, 0.5, 0.7))
    
    # Find current clicked and visible objects
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
    
    # If clicked interface Level 1
    if 'Level1' in objectClicked.name:     
        level1Clear()
        level2Clear()
        level3Clear()
        level4Clear()
    
    # If clicked interface Level 2
    if 'Level2' in objectClicked.name:
        level2Clear()
        level3Clear()
        level4Clear()
        
        if objectClicked.name == 'Level2 Buildings Height':
            
            # Show buildings height x25
            WorkbookPath = os.path.join('Cities', 'Irkutsk', 'Irkutsk.xls')
            SheetName = 'Buildings'
            WorkbookSheet(WorkbookPath, SheetName)
            
            Sheet = WorkbookSheet(WorkbookPath, SheetName)
            SheetColumn = 'Height'
            WorkbookSheetColumnNumber(Sheet, SheetColumn)
            SheetColumnNumber = WorkbookSheetColumnNumber(Sheet, SheetColumn)
            
            # Iterate all lines in sheet, 'for SheetRow in range(Sheet.nrows):' will not work, I don't know why
            for SheetRow in range(1, 99999):
                ObjectCurrentName = Sheet.cell(SheetRow,0).value
                if ObjectCurrentName in sceneCity.objects:
                    objectCurrent = sceneCity.objects[ObjectCurrentName]
                    
                    # Convert cell value which was read from workbook from float to string, remove 'text:' and '.0' from it, play action
                    actionCurrent = 'ScaleZ1-' + str(Sheet.cell(SheetRow,SheetColumnNumber).value).replace('text:', '').replace('.0', '')
                    objectCurrent.playAction(actionCurrent, 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
    
    # If clicked interface Level 3
    if 'Level3' in objectClicked.name:
        level3Clear()
        level4Clear()
    
    # If clicked interface Level 4
    if 'Level4' in objectClicked.name:
        level4Clear()
    
    # Highlight clicked item and show its inside next level items
    sceneInterface.objects[objectClicked.name + ' Parent'].playAction('Visible', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)
    objectClicked.playAction('InterfaceClickedOn', 1, 12, layer = 0, play_mode = bge.logic.KX_ACTION_MODE_PLAY)