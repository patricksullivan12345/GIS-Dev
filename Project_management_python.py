import arcpy
import os

input_gdb = os.path.join(r"C:\Users\psullivan\OneDrive - Mastec\Desktop\GIS\ArcPro\Project_Managment\Data_House.gdb")

fibercable = arcpy.GetParameterAsText(0)

arcpy.env.workspace = input_gdb

fields = arcpy.ListFields(fibercable,"*")

for field in fields:

    if field.name != "SHAPE_Length" and field.name != "SUBTYPECODE" and field.name != "SHAPE" and field.name != "OBJECTID" and field.name != "CALCULATEDLENGTH" and field.name != "FQN_ID" and field.name != "CREATEWORKORDERID" and field.name != "CONSTRUCTIONSTARTPLANNED" and field.name != "SPLICETESTACTUAL" and field.name != "CONSTRUCTIONSTARTACTUAL" and field.name != "SPLICETESTESTIMATED" and field.name != "CABLEPLACEDESTIMATED" and field.name != "CABLEPLACEDACTUAL":

	arcpy.DeleteField_management(fibercable, [field.name])
