import re, os, bpy, xlrd3

def sheet(sheet_path):
    wb = xlrd3.open_workbook(sheet_path + "\\" + "irkutsk.xls")
    "%s\\irkutsk.xls" % sheet_path
    wb.sheet_names()
    sh = wb.sheet_by_index(0)
    cellRow = 1
    for cellRow from 1 to 99999:
        bpy.context.scene.frame_set(100)
        ob = bpy.data.objects[sh.cell(rowx=cellRow,colx=0)]
        bpy.context.scene.objects.active = ob
        ob.modifiers[0].thickness = sh.cell(rowx= cellRow,colx=1)
        ob.modifiers[0].keyframe_insert(data_path="thickness")
        cellRow = cellRow + 1

sheet('D:\\Dropbox\\2Current\\ISTU\\Project')