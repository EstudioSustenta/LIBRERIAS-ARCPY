# import arcpy
from arcpy.mapping import MapDocument as map
from arcpy.mapping import ListDataFrames as dataf
from arcpy import RefreshActiveView as rf
from arcpy.mapping import AddLayer as carga

mapa="Y:/0_SIG_PROCESO/PLANTILLA.mxd"
mxd=map(mapa)
df=dataf(mxd)[0]

mxd.defaultView = "Layout"
# mxd.defaultView = "DataFrame"
print(mxd.defaultView)
print(df.name)