# -*- coding: utf-8 -*-
"""
Módulo para unir los archivos .pdf de una carpeta en un solo archivo .pdf
"""

from UTILERIAS.UTILERIAS_PDF import pdf_join

# Proceso para inicializar cuadros de diálogo
import Tkinter as tk
import tkFileDialog
root = tk.Tk()
root.withdraw()

carp_mapas="Y:"

carpeta_cliente = tkFileDialog.askdirectory(initialdir=carp_mapas, title=u"Selecciona la carpeta destino de los mapas") + "/"
archivo="UnionPDF"
print(carpeta_cliente)

print(pdf_join(carpeta_cliente,archivo))