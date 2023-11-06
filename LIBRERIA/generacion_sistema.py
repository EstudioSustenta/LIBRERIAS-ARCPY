# -*- coding: utf-8 -*-


# ---------------------------------------------------------------------------
# borrame.py
# Created on: 2023-10-07 23:06:46.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: borrame <Expression> 
# Description: 
# ---------------------------------------------------------------------------

# Set the necessary product code
# import arcinfo


# Import arcpy module
import arcpy



def start(seleccion):

    arcpy.env.overwriteOutput = True
    # arcpy.env.addOutputsToMap = u"NONE"

    Expression = u"\"DESCRIP\" = '{}'".format(seleccion)
        
    # Local variables:
    PROYECTOS_shp__2_ = u"Y:\\0_SIG_PROCESO\\ORIGEN\\PROYECTOS.shp"
    PROYECTOS_shp = PROYECTOS_shp__2_
    SISTEMA_WGS_shp = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\SISTEMA_WGS.shp"
    SISTEMA_LAT_LON_shp = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\SISTEMA LAT-LON.shp"
    SISTEMA_LAT_LON_shp__2_ = SISTEMA_LAT_LON_shp
    SISTEMA_LAT_LON_shp__6_ = SISTEMA_LAT_LON_shp__2_
    SISTEMA_LAT_LON_shp__7_ = SISTEMA_LAT_LON_shp__6_
    SISTEMA_LAT_LON_shp__5_ = SISTEMA_LAT_LON_shp__7_
    SISTEMA_LAT_LON_shp__4_ = SISTEMA_LAT_LON_shp__5_
    SISTEMA_PROYECTADO_shp = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\SISTEMA_PROYECTADO.shp"
    SISTEMA_shp__3_ = SISTEMA_PROYECTADO_shp
    SISTEMA_PROYECTADO_shp__2_ = SISTEMA_shp__3_
    SISTEMA_PROYECTADO_shp__3_ = SISTEMA_PROYECTADO_shp__2_
    MUNICIPAL_CENSO_2020_DECRETO_185_shp__2_ = u"Y:\\0_SIG_PROCESO\\BASES DE DATOS\\00 MEXICO\\INEGI\\MUNICIPAL CENSO 2020 DECRETO 185.shp"
    SISTEMA_PROYECTADO_Identity1_shp = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\SISTEMA_PROYECTADO_Identity.shp"
    SISTEMA_PROYECTADO_Identity1_shp__2_ = SISTEMA_PROYECTADO_Identity1_shp
    LOCALIDADES_URBANAS_Y_RURALES_shp = u"Y:\\0_SIG_PROCESO\\BASES DE DATOS\\00 MEXICO\\INEGI\\LOCALIDADES_URBANAS_Y_RURALES.shp"
    SISTEMA_PROYECTADO_Identity2__shp = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\SISTEMA_PROYECTADO_Identity2_.shp"
    SISTEMA_PROYECTADO_Identity2__shp__2_ = SISTEMA_PROYECTADO_Identity2__shp
    COLONIAS_shp = u"Y:\\0_SIG_PROCESO\\BASES DE DATOS\\00 MEXICO\\NUMEROSLOCOS\\COLONIAS.shp"
    SISTEMA1_shp__2_ = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\SISTEMA1.shp"
    SISTEMA_shp__2_ = SISTEMA1_shp__2_
    SISTEMA_shp__5_ = SISTEMA_shp__2_
    Republica60_wgs84_tif = u"Y:\\GIS\\MEXICO\\VARIOS\\INEGI\\RASTER\\CEM 60M\\Republica60 wgs84.tif"
    SISTEMA2_shp = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\SISTEMA2.shp"
    Extract_SISTEMA1_shp__2_ = SISTEMA2_shp
    Extract_SISTEMA1_shp__3_ = Extract_SISTEMA1_shp__2_
    Extract_SISTEMA1_shp__4_ = Extract_SISTEMA1_shp__3_
    MARES_Y_OCEANOS_shp = u"Y:\\GIS\\MEXICO\\VARIOS\\00 PROPIOS\\GEOGRAFICOS\\MARES Y OCEANOS.shp"
    Extract_SISTEMA1_shp__5_ = Extract_SISTEMA1_shp__4_
    Extract_SISTEMA1_shp__7_ = Extract_SISTEMA1_shp__5_
    SISTEMA2_shp__2_ = Extract_SISTEMA1_shp__7_
    SISTEMA_URBANO_NACIONAL_shp = u"Y:\\0_SIG_PROCESO\\BASES DE DATOS\\00 MEXICO\\INEGI\\SISTEMA URBANO NACIONAL.shp"
    SISTEMA_shp = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\SISTEMA.shp"
    SISTEMA_shp__6_ = SISTEMA_shp
    DATOS_DE_UBICACION_GENERAL_xls = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\DATOS DE UBICACION GENERAL.xls"
    MULTIBUFFER_shp = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\MULTIBUFFER.shp"
    SISTEMA_SIMPLIFICADO_shp = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\SISTEMA_SIMPLIFICADO.shp"
    SISTEMA_SIMPLIFICADO__3_ = SISTEMA_SIMPLIFICADO_shp
    PROYECTOS_shp__4_ = PROYECTOS_shp
    PROYECTOS_XLS = u"Y:\\0_SIG_PROCESO\\00 GENERAL\\PROYECTOS.XLS"

    # Process: Select
    arcpy.Select_analysis(PROYECTOS_shp__2_, SISTEMA_WGS_shp, Expression)
    log.log(repet,u"Select_analysis")
    # Process: Project
    arcpy.Project_management(SISTEMA_WGS_shp, SISTEMA_LAT_LON_shp, "GEOGCS['GCS_NAD_1927_Definition_1976',DATUM['D_NAD_1927_Definition_1976',SPHEROID['Clarke_1866',6378206.4,294.9786982]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", u"", u"PROJCS['WGS_1984_UTM_Zone_13N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-105.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", u"NO_PRESERVE_SHAPE", u"", u"NO_VERTICAL")
    log.log(repet,u"Project_management")
    # Process: Add XY Coordinates (2)
    arcpy.AddXY_management(SISTEMA_LAT_LON_shp)
    log.log(repet,u"AddXY_management")
    # Process: Add Field
    arcpy.AddField_management(SISTEMA_LAT_LON_shp__2_, "LAT", u"DOUBLE", u"3", u"", u"", u"", u"NULLABLE", u"NON_REQUIRED", u"")
    log.log(repet,u"AddField_management")
    # Process: Calculate Field
    arcpy.CalculateField_management(SISTEMA_LAT_LON_shp__6_, "LAT", u"[POINT_Y]", u"VB", u"")
    log.log(repet,u"CalculateField_management")
    # Process: Add Field (2)
    arcpy.AddField_management(SISTEMA_LAT_LON_shp__7_, "LON", u"DOUBLE", u"3", u"", u"", u"", u"NULLABLE", u"NON_REQUIRED", u"")
    log.log(repet,u"AddField_management")
    # Process: Calculate Field (2)
    arcpy.CalculateField_management(SISTEMA_LAT_LON_shp__5_, "LON", u"[POINT_X]", u"VB", u"")
    log.log(repet,u"CalculateField_management")
    # Process: Project (2)
    arcpy.Project_management(SISTEMA_LAT_LON_shp__4_, SISTEMA_PROYECTADO_shp, "PROJCS['WGS_1984_UTM_Zone_13N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-105.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]", u"", u"GEOGCS['GCS_NAD_1927_Definition_1976',DATUM['D_NAD_1927_Definition_1976',SPHEROID['Clarke_1866',6378206.4,294.9786982]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]", u"NO_PRESERVE_SHAPE", u"", u"NO_VERTICAL")
    log.log(repet,u"Project_management")
    # Process: Add XY Coordinates
    arcpy.AddXY_management(SISTEMA_PROYECTADO_shp)
    log.log(repet,u"AddXY_management")
    # Process: Calculate Field (3)
    arcpy.CalculateField_management(SISTEMA_shp__3_, "POINT_X", u"[POINT_X]", u"VB", u"")
    log.log(repet,u"CalculateField_management")
    # Process: Calculate Field (4)
    arcpy.CalculateField_management(SISTEMA_PROYECTADO_shp__2_, "POINT_Y", u"[POINT_Y]", u"VB", u"")
    log.log(repet,u"CalculateField_management")
    # Process: Identity
    arcpy.Identity_analysis(SISTEMA_PROYECTADO_shp__3_, MUNICIPAL_CENSO_2020_DECRETO_185_shp__2_, SISTEMA_PROYECTADO_Identity1_shp, "ALL", u"", u"NO_RELATIONSHIPS")
    log.log(repet,u"Identity_analysis")
    # Process: Delete Field (2)
    # arcpy.DeleteField_management(SISTEMA_PROYECTADO_Identity1_shp, "FID_SISTEM;FID_MUNICI")
    # log.log(repet,u"13")
    # Process: Identity (2)
    arcpy.Identity_analysis(SISTEMA_PROYECTADO_Identity1_shp__2_, LOCALIDADES_URBANAS_Y_RURALES_shp, SISTEMA_PROYECTADO_Identity2__shp, "ALL", u"", u"NO_RELATIONSHIPS")
    log.log(repet,u"Identity_analysis")
    # Process: Identity (3)
    arcpy.Identity_analysis(SISTEMA_PROYECTADO_Identity2__shp__2_, COLONIAS_shp, SISTEMA1_shp__2_, "ALL", u"", u"NO_RELATIONSHIPS")
    log.log(repet,u"Identity_analysis")
    # Process: Add Field (3)
    arcpy.AddField_management(SISTEMA_shp__2_, "ALTITUD", u"SHORT", u"", u"", u"", u"", u"NULLABLE", u"NON_REQUIRED", u"")
    log.log(repet,u"AddField_management")
    # Process: Extract Values to Points
    arcpy.gp.ExtractValuesToPoints_sa(SISTEMA_shp__5_, Republica60_wgs84_tif, SISTEMA2_shp, "NONE", u"VALUE_ONLY")
    log.log(repet,u"gp.ExtractValuesToPoints_sa")
    # Process: Calculate Field (6)
    arcpy.CalculateField_management(SISTEMA2_shp, "ALTITUD", u"[RASTERVALU]", u"VB", u"")
    log.log(repet,u"CalculateField_management")
    # Process: Near (2)
    arcpy.Near_analysis(Extract_SISTEMA1_shp__3_, "'Y:\\GIS\\MEXICO\\VARIOS\\00 PROPIOS\\GEOGRAFICOS\\MARES Y OCEANOS.shp'", u"", u"NO_LOCATION", u"NO_ANGLE", u"PLANAR")
    log.log(repet,u"Near_analysis")
    # Process: Add Field (4)
    arcpy.AddField_management(Extract_SISTEMA1_shp__4_, "CONTINENTA", u"FLOAT", u"", u"", u"", u"", u"NULLABLE", u"NON_REQUIRED", u"")
    log.log(repet,u"AddField_management")
    # Process: Calculate Field (5)
    arcpy.CalculateField_management(Extract_SISTEMA1_shp__5_, "CONTINENTA", u"[NEAR_DIST] /1000", u"VB", u"")
    log.log(repet,u"CalculateField_management")
    # Process: Identity (4)
    arcpy.Identity_analysis(SISTEMA2_shp__2_, SISTEMA_URBANO_NACIONAL_shp, SISTEMA_shp, "ALL", u"", u"NO_RELATIONSHIPS")
    log.log(repet,u"Identity_analysis")
    # Process: Table To Excel
    # arcpy.TableToExcel_conversion(SISTEMA_shp__6_, DATOS_DE_UBICACION_GENERAL_xls, "NAME", u"CODE")
    # log.log(repet,u"TableToExcel_conversion")
    # Process: Multiple Ring Buffer
    # arcpy.MultipleRingBuffer_analysis(SISTEMA_shp__2_, MULTIBUFFER_shp, "50;100;200;500;1000", u"Meters", u"DISTANCIA", u"ALL", u"FULL")
    # log.log(repet,u"MultipleRingBuffer_analysis")
    # Process: Copy Features
    # arcpy.CopyFeatures_management(SISTEMA_PROYECTADO_shp__3_, SISTEMA_SIMPLIFICADO_shp, "", u"0", u"0", u"0")
    # log.log(repet,u"CopyFeatures_management")

    # # Process: Table To Excel (2)
    # arcpy.TableToExcel_conversion(PROYECTOS_shp__4_, PROYECTOS_XLS, "NAME", u"CODE")

    # arcpy.env.addOutputsToMap = u"CURRENT"

    log.log(repet,u"\n\nFin de proceso de selección de proyecto para :" + seleccion +"\n\n")

