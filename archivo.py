import json

class Eventos:
    '''Esta clase maneja el archivo de eventos'''

    def __init__(self,ruta):
        '''Constructor'''
        self.ruta=ruta

    def crear_eventos(self,datos):
        '''Este metodo crea y guarda los eventos en el archivo. Primero, mediante
        manejo de errores comprueba si existe el archivo, si existe agrega el
        evento al archivo, si no existe crea el archivo y guarda el evento'''
        if self.verificar_archivo():
            lista=[]
            lista.append(datos)
            with open(self.ruta,'w') as archivo:
                json.dump(lista,archivo,indent=2)
        else:
            with open(self.ruta) as archivo:
                lista=json.load(archivo)
            lista.append(datos)
            with open(self.ruta,'w') as archivo:
                json.dump(lista,archivo,indent=2)
    
    def modificar_evento(self, datosV, datosN):
        '''Este metodo modifica los datos de un evento pasado como parametro'''
        with open(self.ruta) as archivo:
            lista=json.load(archivo)
        for evento in lista:
            if datosV==evento:
                indice=lista.index(evento)
                lista[indice]=datosN
                break
        with open(self.ruta,'w') as archivo:
            json.dump(lista,archivo,indent=2)

    def eliminar_evento(self,datos):
        '''Este metodo elimina un evento'''
        with open(self.ruta) as archivo:
            lista=json.load(archivo)
        lista.remove(datos)
        with open(self.ruta,'w') as archivo:
            json.dump(lista,archivo,indent=2)

    def coincide_fecha_hora(self, fecha, hora):
        '''Este metodo controla la coincidencia de fecha y hora en el archivo'''
        with open(self.ruta) as archivo:
            lista=json.load(archivo)
        for evento in lista:
            if evento['fecha']==fecha and evento['hora']==hora:
                return True
        return False
            
    def verificar_archivo(self):
        '''Este metodo verifica la existencia del archivo, devuelve True si
        no existe y False si es que el archivo ya existe'''
        band=False
        try:
            archivo=open(self.ruta)
        except FileNotFoundError:
            band=True
        finally:
            if not band:
                archivo.close()
        return band
    
    def traer_datos(self):
        '''Este metodo devuelve una lista de diccionarios con los datos del
        archivo json, si el archivo no existe devuelve una lista vacia'''
        if not self.verificar_archivo():
            with open(self.ruta) as archivo:
                lista=json.load(archivo)
        else:
            lista=[]
        return lista