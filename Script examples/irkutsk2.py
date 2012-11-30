import re, os, bpy, xlrd3

def sheet(sheet_path):
    wb = xlrd3.open_workbook(sheet_path + "\\" + "irkutsk.xls")
    "%s\\irkutsk.xls" % sheet_path
    wb.sheet_names()
    sh = wb.sheet_by_index(0)
    cell_A2 = sh.cell(rowx=1,colx=0).value
    cell_B2 = sh.cell(rowx=1,colx=1).value
    ob = bpy.data.objects[cell_A2]
    bpy.context.scene.objects.active = ob
    ob.modifiers[0].thickness = cell_B2
    ob.modifiers[0].keyframe_insert(data_path="thickness")

sheet('D:\\Dropbox\\2Current\\ISTU\\Project')
