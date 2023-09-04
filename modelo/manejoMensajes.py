import pandas as pd
import pywhatkit
from datetime import datetime
import numpy as np

class Mensajes():
    def __init__(self) -> None:
        pass

    def obtenerCabeceras(self, ruta_archivo):
        try:
            try:
                self.df=pd.read_csv(ruta_archivo)
            except:
                self.df=pd.read_excel(ruta_archivo)

            cabeceras=self.df.columns.tolist()
            filtradas=[cabecera for cabecera in cabeceras if "Unnamed" not in cabecera]

            
            return filtradas
        except Exception as e:
            print("error al leer el archivo:", str(e))

    def obtenerElementosDadasLasCabeceras(self, cabecera1, cabecera2):
        nombres=self.df[cabecera1]
        print(nombres)
        telefonos=self.df[cabecera2]
        print(telefonos)
        data_filtrado=self.df.dropna(subset=[cabecera2]).copy() #filtra telefonos vacios con nombres correspondientes
        data_filtrado = data_filtrado[data_filtrado[cabecera2].str.startswith("09") | data_filtrado[cabecera2].str.startswith("'09")].reset_index()

        nombres_y_telefonos = data_filtrado[[cabecera1, cabecera2]]
        nombres_y_telefonos.loc[:, cabecera2] = nombres_y_telefonos[cabecera2].str.replace("'", "")

        lista_de_listas = nombres_y_telefonos.values.tolist()
        return lista_de_listas


    def mandarMensaje(self, numeros_telefonicos,mensaje):
        for numero in numeros_telefonicos:
            pywhatkit.sendwhatmsg_instantly('+593'+str(numero),mensaje, 15, True )

    def mandarImagenConMensaje(self, numeros_telefonicos, mensaje, imagen):
        for numero in numeros_telefonicos:
            
            pywhatkit.sendwhats_image('+593'+str(numero), imagen, mensaje, 10, True)
        
