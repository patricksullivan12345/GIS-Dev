import pandas as pd
import numpy as np
import os
import arcpy

class quarterly_reporting():

    def __init__(self):

        #Attributes for all of the inputs
        self.csv_path = os.path.join("C:\\Users\\psullivan\\OneDrive - Mastec\\Desktop\\GIS\\ArcPro\\GIS_Projects\\Spatial_Data\\Quarterly_Reports\\Q3_2021\\Reports\\Q3_CSV.csv")
        self.text_output = os.path.join("C:\\Users\\psullivan\\OneDrive - Mastec\\Desktop\\GIS\\ArcPro\\GIS_Projects\\Spatial_Data\\Quarterly_Reports\\Q3_2021\\output_span.txt")
        self.root_gdb = os.path.join("C:\\Users\\psullivan\\OneDrive - Mastec\\Desktop\\GIS\\ArcPro\\GIS_Projects\\Spatial_Data\\Quarterly_Reports\\Q3_2021\\Q3_Report.gdb")
        self.excel_output = os.path.join("C:\\Users\\psullivan\\OneDrive - Mastec\\Desktop\\GIS\\ArcPro\\GIS_Projects\\Spatial_Data\\Quarterly_Reports\\Q3_2021\\Reports\\Ouput.xlsx")
        self.root_gdb = arcpy.env.workspace

    def txt_SQL(self):

        tracker_csv = pd.read_csv(self.csv_path)

        #print(tracker_csv.columns)

        #CHANGE THE TITLE OF THE COLUMN WORK ORDER NFIDs TO WORK_ORDER_NFIDs IN THE CSV

        work_orders = tracker_csv.WorkOrderNFIDs.to_list()

        np_work_orders = np.array(work_orders)

        #Removal of elements of 'data junk' that might cause an error.
        np_work_orders = np_work_orders[np_work_orders!='nan']
        np_work_orders = np_work_orders[np_work_orders!= 'not adding to 3-gis']
        np_work_orders = np_work_orders[np_work_orders!= '`']

        #print(np_work_orders)

        with open(self.text_output, 'w') as file:

            file.write('CREATEWORKORDERID IN ( ')

            counter = 1

            for ewo in np_work_orders:

                if counter != len(np_work_orders):

                    file.write("'" + str(ewo) + "'," + "\n")

                    #file.write(str(counter) + "Not there yet \n")

                    counter = counter + 1

                else:

                    file.write("'" + str(ewo) + "' ")

                    #file.write(str(counter) + "Done \n")

            file.write(' )')

        file.close()

        with open (self.text_output, "r") as SQL_file:

            SQL_select = SQL_file.read()
            SQL_file.close()

            return SQL_select

    def layer_select(self): 

        SQL = report.txt_SQL()

        select_to_export = arcpy.SelectLayerByAttribute_management("Span", "NEW_SELECTION", SQL)

        return select_to_export

    def layer_export(self):

        export_select = layer_select()

        export = arcpy.management.CopyFeatures("Span","Span_export")

        return export

    def export_selection_to_excel(self):

        temp_table = arcpy.conversion.TableToTable("Span_export", self.root_gdb, "Span_Table")

        quarterlyReport = arcpy.conversion.TableToExcel(temp_table,self.excel_output,"ALIAS")

        return quarterlyReport

report = quarterly_reporting()

report.layer_select()