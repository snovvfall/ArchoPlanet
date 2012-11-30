import re, os, bpy, bge, xlrd3

def workbookOpen(sheet_path):
    workbookCurrent = xlrd3.open_workbook(sheet_path + "\\City\\Irkutsk\\" + "Irkutsk.xls")
    "%s\\Irkutsk.xls" % sheet_path
    workbookCurrent.sheet_names()
	sheetStreets = workbookCurrent.sheet_by_index(0)
	sheetBuildings = workbookCurrent.sheet_by_index(1)
	
workbookOpen('D:\\Dropbox\\2Current\\ArchoPlanet')