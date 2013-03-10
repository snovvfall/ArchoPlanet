ArchoPlanet
===========
Models
    Low-poly buildings
        Name same to one in corresponding workbook 'Name English' column
        Use '-' instead of '/' in names
        Use transliterated english letters for names, and names of additional parts of buildings too ('1a', '6b' for example)
        Material 'action'
        Flat mesh planes
        Solidify modifier with thickness 4 m
        Z scale - number of floors
    
Code
    Copy paste code in Archoplanet.blend internal notepad. I could have link it, but it wouldn't work on both Linux and Windows
    There are some problems with relative path behavior on different platforms, so better close Blender at all and then open ArchoPlanet.blend
    On Linux, if you need debug console opened while working with ArchoPlanet, in command line first cd to ArchoPlanet directory, then open Blender and Archoplanet as normal

TODO
    Data
        OpenStreetMap
        Parse .xls, assign variables by script, not one by one
        Python scene management
        Standalone application
        Database (MongoDB?) on remote server
    Interface
        Buttons icons
        Minimize buttons when too many selected
        Hide buttons when no user's actions for 10 seconds
        Touchscreen support
    Data representation
        Logical operations when selecting objects (for example, select all 3-storey buildings with 1 to 5 administrative value)
        Create parent which moves all city's objects to Earth's surface when this city's scene is being linked to Earth's scene
        Load only nearby objects
        50 km load districts and main roads
        2 km load quarters and streets
        500 m buildings
        Camera moves slower when near ground
        Smooth movements
    Python
        Names of all variables and functions should begin with capital letters
    Blender
        Actions
        Reload scene with same camera position
        Zombie objects
    Projects
        Parse
        Change existing objects
    Performance settings
        Display's resolution
        Texturing
        Shading
        GLSL/Solid view