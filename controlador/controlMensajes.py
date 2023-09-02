import sys
import os
import tkinter as tk
from PyQt6.QtWidgets import QWidget, QFileDialog, QApplication, QMessageBox, QListView, QAbstractItemView
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QScreen, QPixmap
from PyQt6.QtCore import Qt
from vista.ventana import Ventana
from modelo.manejoMensajes import *

class Controlador(QWidget):

    def __init__(self):

        super().__init__()
        # instancio la ventana
        self.app = QtWidgets.QApplication(sys.argv)
        self.vista = Ventana()
        self.tabla = None
        #----------------------
        self.modelo=Mensajes()
        
        #---------------------------------------------------------------------------------
        self.vista.ui.btnSeleccionarImagen.clicked.connect(self.seleccionarImagen)
        self.vista.ui.btnSeleccionarArchivo.clicked.connect(self.seleccionarArchivo)
        self.vista.ui.btnSeleccionarImagen.setEnabled(False)
        self.vista.ui.checkBox.stateChanged.connect(self.checkbox_cambiado)
        self.vista.ui.tblNombreTelefono.setModel(None)
        self.vista.ui.listEncabezados.itemClicked.connect(self.limitar_seleccion)
        self.setModeloTabla()
        # self.setModeloLista()

        
    def limitar_seleccion(self):
        for i in self.vista.ui.listEncabezados.selectedItems():
            print(i.text())
        lista_items = self.vista.ui.listEncabezados.selectedItems()
        longitud = len(self.vista.ui.listEncabezados.selectedItems())
        
        if longitud > 2:
            lista_items[longitud - 1].setSelected(False)
    def checkbox_cambiado(self, estado):
        if estado ==2:
            self.vista.ui.btnSeleccionarImagen.setEnabled(True)
        else:
            self.vista.ui.btnSeleccionarImagen.setEnabled(False)

    def seleccionarImagen(self):

        imagen, ok=QFileDialog.getOpenFileName(self, "Seleccionar imagen", r"<Default dir>", "Archivos de imágenes (*.jpg *.png)")
        #imagen es la direccion de la imagen

        #si la imagen ha sido seleccionada
        if imagen:
            imagen=os.path.relpath(imagen, os.getcwd()) #tome la ruta relativa de la imagen

            if ok:
                tamanio_original=QtGui.QPixmap(imagen)
                ancho_original=tamanio_original.width()
                alto_original=tamanio_original.height()

                #obtengo el tamanio del label que contendra la imagen en la ventana
                ancho_label=self.vista.ui.lblImagen.width()

                #redimensiono el ancho y largo de la imagen manteniendo las proporciones originales de la misma
                relacion_aspecto=ancho_label/ancho_original #251 es el ancho maximo que contiene a la imagen
                alto_deseado=int(alto_original*relacion_aspecto)
                self.vista.ui.lblImagen.setMinimumSize(QtCore.QSize(251,291))
                self.vista.ui.lblImagen.setMaximumSize(QtCore.QSize(251,291))
                #escalo la imagen original al tamanio del label
                redimensionada=tamanio_original.scaled(ancho_label, alto_deseado, Qt.AspectRatioMode.KeepAspectRatio)
                self.vista.ui.lblImagen.setPixmap(redimensionada)

        else:
            pass


    def seleccionarArchivo(self):

        
        archivo, ok = QFileDialog.getOpenFileName(self, "Seleccionar archivo", r"<Default dir>", "Archivos excel (*.xlsx *.csv)")
        if ok:
            encabezados=self.modelo.obtenerCabeceras(archivo)
            self.setModeloLista(encabezados)

            #self.vista.ui.listEncabezados.selectionModel().selectionChanged.connect(self.controlarSeleccion)
            #self.modelo.obtenerElementosDadasLasCabeceras()


    def controlarSeleccion(self, seleccion):
        seleccionados=seleccion.indexes()
        print(str(seleccionados))
        if len(seleccionados)>2:

            QMessageBox.warning(self, "Advertencia", "Solo se pueden seleccionar 2 elementos.")
            # Deseleccionar todos los elementos
            for idx in seleccionados:
                self.vista.ui.listEncabezados.selectionModel().select(idx, Qt.ItemSelectionModel.Deselect)


    def setModeloTabla(self):
        self.tabla = QStandardItemModel()
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Telefono"])
        self.vista.ui.tblNombreTelefono.setModel(self.tabla)
        self.tabla.setRowCount(12)
        
        ancho_tabla=self.vista.ui.tblNombreTelefono.width()
        cabecera = self.vista.ui.tblNombreTelefono.horizontalHeader()
        cabecera.resizeSection(0,int(ancho_tabla)-245)
        cabecera.resizeSection(1,230)
        cabecera.setFirstSectionMovable(False)
        header_style = """
            QHeaderView::section {
                background-color: #ff8b29; /* Color de fondo de la cabecera */
                color: #ffffff; /* Color del texto de la cabecera */
                font-weight: bold; /* Texto en negrita */

            }

        """

        style_sheet = """
        QTableView::item:selected {
                background-color: #ff8b29; 
                color: white;
        }"""

        self.vista.ui.tblNombreTelefono.horizontalHeader().setStyleSheet(header_style)
        self.vista.ui.tblNombreTelefono.setAlternatingRowColors(True)

        self.vista.ui.tblNombreTelefono.setStyleSheet(style_sheet)
        
    def setModeloLista(self, encabezados):
        
        self.vista.ui.listEncabezados.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        for i in encabezados:
            self.vista.ui.listEncabezados.addItem(i)


        # Establecer hoja de estilo para cambiar el color de texto a blanco
        style_sheet = """QListView { color: white; background-color: #14b4b7}
        QListView::item:selected {
                background-color: #999999; 
            }"""
    
        self.vista.ui.listEncabezados.setStyleSheet(style_sheet)
    


        