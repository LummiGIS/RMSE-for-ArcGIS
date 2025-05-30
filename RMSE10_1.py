try:
    import arcpy, exceptions, math, traceback, sys
    
    def GBGAddField(in_table, field_name, field_type, field_precision = None, field_scale = None, field_length = None, field_alias = None, field_is_nullable = None, field_domain = None):   
    #Adds a new field to a feature class or table.  If the table already exists, this function will end
    #gracefully and not crash your script.  Parameters 1,2 and 3 are required, all else are optional.
        fieldList = arcpy.ListFields(in_table)
        fieldList2 = []
        for field in fieldList:
            fieldList2.append(field.name)
        if field_name not in fieldList2:
            arcpy.AddField_management(in_table, field_name, field_type, field_precision, field_scale, field_length, field_alias, field_is_nullable, field_domain)
        else:
            print "Field already exists"
        

 
    #################        SET PARAMETERS HERE  ####################################
    
    TheFeatureClassOfPoints = r"RMSEtest"
    InterpolatedValueField = r"dronez"
    SurveyedValue = r"LiDARz"
    RMSEField = r"RMSE"


    ##################################################################################

    
    SquaredValues = []
    
    
    print "Start cursor"
    rows = arcpy.SearchCursor(TheFeatureClassOfPoints)
    for row in rows:
    #while row:
        i = row.getValue(InterpolatedValueField)
        s = row.getValue(SurveyedValue)
        SquaredValues.append(pow((i - s), 2))

    
    del rows    
    
    n = len(SquaredValues)
    
    SumOfSquares = sum(SquaredValues)
    
    x = SumOfSquares/n
    
    rmse = str(pow(x, .5))
    print "rmse =", rmse
    print "Add field."
    
   
    GBGAddField(TheFeatureClassOfPoints, RMSEField, "DOUBLE")
    print "Calculating field."
    arcpy.CalculateField_management(TheFeatureClassOfPoints, RMSEField, rmse, "VB")
    
   
    print "Finished"
    
except arcpy.ExecuteError: 
    # Get the tool error messages 
    msgs = arcpy.GetMessages(2) 
    # Return tool error messages for use with a script tool 
    arcpy.AddError(msgs) 
    # Print tool error messages for use in Python/PythonWin 
    print msgs
except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # Concatenate information together concerning the error into a message string
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    # Return python error messages for use in script tool or Python Window
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)
    # Print Python error messages for use in Python / Python Window
    print pymsg + "\n"
    print msgs
