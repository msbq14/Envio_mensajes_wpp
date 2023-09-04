import sys
import os
import tkinter as tk
from PyQt6.QtWidgets import QWidget, QFileDialog, QApplication, QMessageBox, QAbstractItemView, QDialogButtonBox
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QScreen, QPixmap, QMouseEvent
from PyQt6.QtCore import Qt
from vista.ventana import Ventana
from vista.vista_previa import VentanaEmergente
from modelo.manejoMensajes import *

class Controlador(QWidget):

    def __init__(self):

        super().__init__()
        # instancio la ventana
        self.app = QtWidgets.QApplication(sys.argv)
        self.vista = Ventana()
        self.centrarVentana()
        self.tabla=None
        
        #----------------------
        self.modelo=Mensajes()
        
        #---------------------------------------------------------------------------------
        self.vista.ui.btnSeleccionarImagen.clicked.connect(self.seleccionarImagen)
        self.vista.ui.btnSeleccionarArchivo.clicked.connect(self.seleccionarArchivo)
        self.vista.ui.btnSeleccionarImagen.setEnabled(False)
        self.vista.ui.checkBox.stateChanged.connect(self.checkbox_cambiado)
        self.vista.ui.tblNombreTelefono.setModel(None)
        self.vista.ui.listEncabezados.itemClicked.connect(self.limitar_seleccion_lista)
        self.vista.ui.btnEnviarMensaje.clicked.connect(self.enviarMensaje)
        self.vista.ui.txtAreaMensaje.mousePressEvent=self.mouse_clic
        self.setModeloTabla()
        

    def centrarVentana(self):
        # obtener la geometría de la pantalla
        screen_geometry = QApplication.primaryScreen().geometry()

        # obtener el tamaño de la ventana
        window_size = self.vista.geometry()

        # calcular la posición central de la ventana
        x = int((screen_geometry.width() - window_size.width()) / 2)
        y = int((screen_geometry.height() - window_size.height()) / 2)

        # mover la ventana a la posición central
        self.vista.move(x, y)

    def mouse_clic(self, event:QMouseEvent):
        if event.button()==Qt.MouseButton.LeftButton:
            self.vista.ui.txtAreaMensaje.setText("")

    def checkbox_cambiado(self, estado):
        if estado ==2:
            self.vista.ui.btnSeleccionarImagen.setEnabled(True)
            style = """
            QPushButton {
                background-color: rgb(20, 180, 183);
                border-color: rgb(20, 180, 183);
                color: rgb(255,255,255);

            }
        """
            self.vista.ui.btnSeleccionarImagen.setStyleSheet(style)
            
        else:
            self.vista.ui.btnSeleccionarImagen.setEnabled(False)
            self.cambiarAparienciaBotonDeshabilitado()
            self.vista.ui.lblImagen.clear()
            

    def cambiarAparienciaBotonDeshabilitado(self):
        style = """
            QPushButton {
                background-color: #ccc; 
                color: #888;  
                border: 1px solid #aaa; 
            }
        """
        self.vista.ui.btnSeleccionarImagen.setStyleSheet(style)

    def seleccionarImagen(self):

        self.imagen, ok=QFileDialog.getOpenFileName(self, "Seleccionar imagen", r"<Default dir>", "Archivos de imágenes (*.jpg *.png)")
        #imagen es la direccion de la imagen

        #si la imagen ha sido seleccionada
        if self.imagen:
            self.imagen=os.path.relpath(self.imagen, os.getcwd()) #tome la ruta relativa de la imagen

            if ok:
                tamanio_original=QtGui.QPixmap(self.imagen)
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

        self.vista.ui.listEncabezados.clear()
        self.tabla.setRowCount(0)
        archivo, ok = QFileDialog.getOpenFileName(self, "Seleccionar archivo", r"<Default dir>", "Archivos excel (*.xlsx *.csv)")
        if ok:
            encabezados=self.modelo.obtenerCabeceras(archivo)
            self.setModeloLista(encabezados)
            self.setModeloTabla()

    def limitar_seleccion_lista(self):
        
        lista_items = self.vista.ui.listEncabezados.selectedItems()
        longitud = len(self.vista.ui.listEncabezados.selectedItems())
        if longitud > 2:
            lista_items[longitud - 1].setSelected(False)
        elif longitud ==2:
            lista_textos = [item.text() for item in lista_items] #convierte el lista_items que es de tipo QListWidgetItem a list
            datos=self.modelo.obtenerElementosDadasLasCabeceras(lista_textos[0],lista_textos[1])
            self.llenarTabla(datos)


    def setModeloTabla(self):
        self.tabla=QStandardItemModel()
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
                background-color: #14b4b7;  
                color: #ffffff;  
                font-weight: bold;  

            }

        """

        style_sheet = """
        QTableView::item:selected {
                background-color: rgba(20,180,183,0.3);
                color: black;
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
    

    def llenarTabla(self, data):
        

        for i in range(len(data)):
            for j in range(len(data[i])):
                self.tabla.setItem(i,j,QStandardItem(str(data[i][j])))


    def enviarMensaje(self):
        #mostrar la vista previa en otra ventana puede ser mejor idea 
        mensaje = "¿Está seguro de que desea enviar el mensaje a los números telefónicos que aparecen en la tabla?"
        mensaje += "\nMensaje: "+self.vista.ui.txtAreaMensaje.toPlainText()
        
        #si no se va a enviar una imagen
        if not self.vista.ui.checkBox.isChecked():
            respuesta = QMessageBox.question(self, "Confirmación", mensaje, QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
            if self.vista.ui.txtAreaMensaje.toPlainText().strip() and respuesta == 16384:

                self.modelo.mandarMensaje(self.obtenerSegundaColumna(),self.vista.ui.txtAreaMensaje.toPlainText())
            else:
                QMessageBox.information(self,"Aviso", "No se enviaron los mensajes") 

        else:
            mensaje = "¿Está seguro de que desea enviar el mensaje con la imagen a los números telefónicos que aparecen en la tabla?"
            respuesta = QMessageBox.question(self, "Confirmacion", mensaje, QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
            
            if self.vista.ui.txtAreaMensaje.toPlainText().strip() and respuesta == 16384:
                self.modelo.mandarImagenConMensaje(self.obtenerSegundaColumna(), self.vista.ui.txtAreaMensaje.toPlainText(), self.imagen)
            else:
                QMessageBox.information(self,"Aviso", "No se enviaron los mensajes")
            

    def aceptar(self):
        self.modelo.mandarImagenConMensaje(self.obtenerSegundaColumna(), self.vista.ui.txtAreaMensaje.toPlainText(), self.imagen)
    def cancelar(self):
        QMessageBox.information(self,"Aviso", "No se enviaron los mensajes") 

    def manejarVentanaEmergente(self, mensaje):
        # respuesta = QMessageBox.question(self, "Confirmacion", mensaje, QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)

        tamanio_original=QtGui.QPixmap(self.imagen)
        ancho_original=tamanio_original.width()
        alto_original=tamanio_original.height()

        #obtengo el tamanio del label que contendra la imagen en la ventana
        ancho_label=self.emergente.ui.lblImagenVistaPrevia.width() 

        #redimensiono el ancho y largo de la imagen manteniendo las proporciones originales de la misma
        relacion_aspecto=ancho_label/ancho_original 
        alto_deseado=int(alto_original*relacion_aspecto)
    
        self.emergente.ui.lblImagenVistaPrevia.setMinimumSize(QtCore.QSize(251,291))
        self.emergente.ui.lblImagenVistaPrevia.setMaximumSize(QtCore.QSize(251,291))
        #escalo la imagen original al tamanio del label
        redimensionada=tamanio_original.scaled(ancho_label, alto_deseado, Qt.AspectRatioMode.KeepAspectRatio)
        self.emergente.ui.lblImagenVistaPrevia.setPixmap(redimensionada)
        self.emergente.ui.lblMensajeVistaPrevia.setText(mensaje)
        
    def obtenerSegundaColumna(self):
        segunda_columna = []
        for fila in range(self.tabla.rowCount()):
            item = self.tabla.item(fila, 1)  # 1 representa la segunda columna
            if item:
                segunda_columna.append(item.text())

        return segunda_columna
    

    def verificarTablaNoVacia(self):
        for fila in range(self.tabla.rowCount()):
            for columna in range(self.tabla.columnCount()):
                item = self.tabla.item(fila, columna)
                if item and not item.text().strip() == "":
                    return True 
                
        
        return False

        