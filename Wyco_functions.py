import arcpy
import numpy as np
import os

#Inputs

input_gdb = os.path.join(r"C:\Users\psullivan\OneDrive - Wyco Field Services\Desktop\GIS\ArcPro\UDM_Extracts\Wyco_DenverCO_Bulk_2021-05-06_20-30-38.gdb")

#clip = os.path.join(r"C:\Users\psullivan\Desktop\Field_Data\Study_Area\Study_Area.gdb\Hwy_85_Crossing")
#Intermedary_GDB = os.path.join(r"C:\Users\psullivan\Desktop\Field_Data\Projects\Hwy_85_Crossing\Intermediary.gdb")
#out_folder_shp = os.path.join(r"C:\Users\psullivan\Desktop\Field_Data\Projects\Hwy_85_Crossing\Shapefiles")
#out_foulder_pics = os.path.join(r"C:\Users\psullivan\Desktop\Field_Data\Projects\Hwy_85_Crossing\Photos")

projection = os.path.join(r"C:\Users\psullivan\OneDrive - Wyco Field Services\Desktop\GIS\ArcPro\GIS_Projects\Spatial_Data\Projections\Colorado_State_Central_Projection.prj")

compare1 = os.path.join(r"C:\Users\psullivan\OneDrive - Wyco Field Services\Desktop\GIS\ArcPro\UDM_Extracts\Wyco_DenverCO_Bulk_2021-03-28_20-30-37.gdb\fiberCable")
compare2 = os.path.join(r"C:\Users\psullivan\OneDrive - Wyco Field Services\Desktop\GIS\ArcPro\UDM_Extracts\Wyco_DenverCO_Bulk_2021-05-06_20-30-38.gdb\fiberCable")

#out_file = os.path.join(r"C:\Users\psullivan\Desktop\Python\selection_output.txt")

#Activate necessary ArcGIS work environments
arcpy.env.workspace = input_gdb
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(projection)

#Grab lists for future iterative arrays
fcList = arcpy.ListFeatureClasses()
tables = arcpy.ListTables()

class geoprocessing():

    def __init__(self,input_gdb,clip,out_folder_shp,fcList,Intermedary_GDB,out_foulder_pics,tables,compare1,compare2,out_file):

        #Attributes for all of the inputs
        self.input_gdb = input_gdb
        self.clip = clip
        self.out_folder_shp = out_folder_shp
        self.fcList = fcList
        self.Intermedary_GDB = Intermedary_GDB
        self.out_foulder_pics = out_foulder_pics
        self.tables = tables
        self.compare1 = compare1
        self.compare2 = compare2
        self.out_file = out_file

    #This function clips the data and exports the feature classes as shapefiles. 
    def field_data_clip(self):

        #By iterating through the names of the feature classes, you can preform processes per feature class in the GDB
        for fc in self.fcList:

            # Process: Select Layer By Location (Select Layer By Location) 
            select_extract = arcpy.SelectLayerByLocation_management(in_layer= self.input_gdb + "\\" + str(fc), 
                                                                    overlap_type="INTERSECT", 
                                                                    select_features= self.clip, 
                                                                    search_distance="", 
                                                                    selection_type="NEW_SELECTION", 
                                                                    invert_spatial_relationship="NOT_INVERT")

            #Process: Copy Features (Copy Features) exports selected features to intermediary GDB
            arcpy.CopyFeatures_management(in_features=select_extract, 
                                        out_feature_class= self.Intermedary_GDB + "\\" + str(fc), 
                                        config_keyword="", 
                                        spatial_grid_1=None, 
                                        spatial_grid_2=None, 
                                        spatial_grid_3=None)

            # Process: Feature Class To Shapefile (Feature Class To Shapefile) 
            arcpy.FeatureClassToShapefile_conversion( self.Intermedary_GDB + "\\" + str(fc), 
                                                    self.out_folder_shp )

    #This function exports the photos from the field data
    def photo_extraction(self):

        #This for loop iterates through the table attachments from the IKE fielding equipment
        #ANY GEOPROCESSING DISRUPTS THE PHOTO DATA STORED ON THE GEODATABASE. 
        for table in self.tables:

            table_path = self.input_gdb + "\\" + str(table) 
            #"DATA" is where the photo data is stored. The rest of the attributes create the photos in the correct order. 
            with arcpy.da.SearchCursor(table_path, ['DATA','ATT_NAME', 'REL_GLOBALID']) as photo:

                for row in photo:
                    
                    photo_make = row[0]
                    filename = "{0}_{1}_{2}".format(table,row[2], row[1])
                    #The "tobytes()" function call creates a photo from the photo data input. 
                    open(self.out_foulder_pics + os.sep + filename, 'wb').write(photo_make.tobytes())
                    del row
                    del filename
                    del photo_make

    def find_different_fqnids(self):
        """
        This method compares the fields of 2 feature classes and then grabs the differences between the fields. 
        It is intended to keep track of how FQNIDs are deleted over a period of time. 
        """

        field1 = 'FQN_ID'
        field2 = 'FQN_ID'

        compare_list1 = []
        compare_list2 = []
        selection = []

        with arcpy.da.SearchCursor(self.compare1, [field1]) as cursor1:
            for row1 in cursor1:
                compare_list1.append(row1[0]) 

        with arcpy.da.SearchCursor(self.compare2, [field2]) as cursor2:
            for row2 in cursor2:
                compare_list2.append(row2[0]) 

        for i_fc1 in compare_list1:
            if i_fc1 not in compare_list2:
                selection.append(i_fc1)

        for i_fc2 in compare_list2:
            if i_fc2 not in compare_list1:
                selection.append(i_fc2)         

        return selection

    def get_fqnids(self,selection): 
        """
        This method will eventually grab the dates associated with the .find_different_fqnids() selection.  
        Its purpose is to find when each FQNID was created. 
        """

        str_selection = "'" + "', '".join(selection) + "'"
        SQL = "FQN_ID IN (" + str_selection + ")"

        arcpy.SelectLayerByAttribute_management(self.compare2, "NEW_SELECTION", SQL)


    def write_csv(self,transform_list):
        """
        This method is used to output the list from .find_different_fqnids() in a csv format
        """

        out_file = open(self.out_file, "w")
        out_file.write('FQNIDs' + ',' + '\n')

        for fqnid in transform_list:
            out_file.write( str(fqnid) + ',' + '\n')

        out_file.close()
    
    def write_txt(self,transform_list):
        """
        This method is used to output the list from .find_different_fqnids() in a txt format
        """

        out_file = open(self.out_file, "w")
        
        for fqnid in transform_list:
            out_file.write("'" + str(fqnid) + "'," + "\n")
        
        out_file.close()

generator = geoprocessing(input_gdb,clip,out_folder_shp,fcList,Intermedary_GDB,out_foulder_pics,tables,compare1,compare2,out_file)

#generator.photo_extraction()

#generator.field_data_clip()

#selection = generator.find_different_fqnids()

selection = generator.find_different_fqnids()

generator.get_fqnids(selection)
