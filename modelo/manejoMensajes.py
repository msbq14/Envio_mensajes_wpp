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

    def obtenerElementosDadasLasCabeceras(self, cabecera1, cabecera2, archivo):
        nombres=self.df[self.df[cabecera1]]
        print(nombres)
        telefonos=self.df[self.df[cabecera2]]
        print(telefonos)



#df = pd.read_excel('C:/Users/mari1/Escritorio/pasantias-NewBest/empresas.xlsx')
#df = df[df['telefonosEmpresa'].str.startswith('09') == True].reset_index()
#df = df['telefonosEmpresa']                                                           
#df 

mensaje = "Recuerdas quién nos puso una cárcel de máxima seguridad en Cuenca? https://vm.tiktok.com/ZM2EVhEnp/"

#for i in df: 
#    pywhatkit.sendwhatmsg_instantly('+593'+str(i),mensaje, 15, True )