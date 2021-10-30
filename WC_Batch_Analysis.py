import arcpy 
import os

"""
The feature class WC_BATCH_FQNIDs used a filter that only showed FQNIDs that had "WC_Batch" in the Last User field. 
"""

fiberCable_original = os.path.join("C:\\Users\\psullivan\\OneDrive - Mastec\\Desktop\\GIS\\ArcPro\\UDM_Extracts\\Denver\\Wyco_DenverCO_Bulk_2021-10-18_20-30-32.gdb\\fiberCable")
WC_Batch_fc = os.path.join("C:\\Users\\psullivan\\OneDrive - Mastec\\Desktop\\GIS\\ArcPro\\GIS_Projects\\KMZs_and_conversions\\KMZs.gdb\\WC_BATCH_FQNIDs")

output_csv =  os.path.join("C:\\Users\\psullivan\\OneDrive - Mastec\\Desktop\\GIS\\ArcPro\\Programming\\WC_Batch_Compare.csv")

FQNID_field = ['FQN_ID']

def FQNID_compare(FQNID_field,WC_Batch_fc,fiberCable_original):

    Original_FQNIDs = []
    WC_BATCH_FQNIDs = []
    Final_compare = []

    with arcpy.da.SearchCursor(fiberCable_original, FQNID_field) as cursor:
        for row in cursor:
            #print(u'{0}'.format(row[0]))
            Original_FQNIDs.append(str(row[0]))

    with arcpy.da.SearchCursor(WC_Batch_fc, FQNID_field) as cursor:
        for row in cursor:
            #print(u'{0}'.format(row[0]))
            WC_BATCH_FQNIDs.append(str(row[0]))

    for FQNID in Original_FQNIDs[:]:
        if FQNID in WC_BATCH_FQNIDs:
            Final_compare.append(FQNID)

    output_tuple = (Original_FQNIDs,Final_compare)

    return output_tuple

FQNIDs = FQNID_compare(FQNID_field,WC_Batch_fc,fiberCable_original)

#print(len(FQNIDs[1]))

percent_affected = (len(FQNIDs[1])/len(FQNIDs[0]))*100

out_file = open(output_csv, "w")

out_file.write("Original FQNIDs 10/18" + "," + "FQNIDs Affected by WC_Batch 10/25" + "," + "FQNIDs Affected by WC_Batch 10/18,\n")
out_file.write("Total of original FQNIDs: " +str(len(FQNIDs[0]))+ "," + "Total of affect FQNIDs: " + str(len(FQNIDs[1])) + "," + "Percentage of Denver Market Affected: " + str(percent_affected) +"%,\n")

for i in range(0,len(FQNIDs[0])):

        if i <= (len(FQNIDs[1])-1):
            out_file.write(str(FQNIDs[0][i]) + "," + str(FQNIDs[1][i]) + ",\n")

        elif i > (len(FQNIDs[1])-1):
            out_file.write(str(FQNIDs[0][i]) + ",\n")

out_file.close()
