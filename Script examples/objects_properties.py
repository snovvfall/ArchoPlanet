import re, os, bpy, xlrd3

def sheet(sheet_path):
    wb = xlrd3.open_workbook(sheet_path + "\\" + "Irkutsk.xls")
    "%s\\Irkutsk.xls" % sheet_path
    wb.sheet_names()
    sh = wb.sheet_by_index(0)
    for rownumber in range(1,99999):
        ob = bpy.data.objects[sh.cell(rownumber,0).value]
        bpy.context.scene.objects.active = ob
        bpy.context.scene.frame_set(100)
        ob.modifiers[0].thickness = sh.cell(rownumber,1).value
        ob.modifiers[0].keyframe_insert(data_path="thickness")
        bpy.context.scene.frame_set(200)
        ob.modifiers[0].thickness = sh.cell(rownumber,2).value
        ob.modifiers[0].keyframe_insert(data_path="thickness")
        
sheet('D:\\Dropbox\\2Current\\ArchoPlanet')