import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from archivo import Eventos

class App(tk.Frame):

    '''Clase principal de la app'''

    def __init__(self, parent):

        '''Constructor'''

        super().__init__(parent)
        self.parent=parent
        parent.title('Eventos')
        parent.geometry("1088x600")
        self.arch_evento=Eventos('Eventos.json')
        
        self.recordatorio() #Al ejecutar la aplicacion verifica los recordatorios de eventos

        
        '''El frame1 es el contenedor de la vista semanal'''

        self.frame1=ttk.Frame(self,width=1200,height=1200,padding=10,relief='solid')
        self.frame1.grid(row=0,column=0,sticky='nw')

        self.dias=['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
        hoy=datetime.now()
        self.inicio_semana=hoy-timedelta(days=hoy.weekday())

        self.etiqueta=ttk.Label(self.frame1,text='Semana: '+hoy.strftime("%W-%Y"), anchor='center',padding=10)
        self.etiqueta.grid(columnspan=9)
        
        self.lista_etiquetas=[]

        ttk.Button(self.frame1,text='<<', command=self.anterior).grid(row=2)

        for i,dia in enumerate(self.dias):

            ttk.Label(self.frame1,text=dia, padding=(20,10,20,20)).grid(row=1,column=i+1)

            self.fecha=self.inicio_semana+timedelta(days=i)

            self.etiquetas=ttk.Label(self.frame1,text=self.fecha.strftime("%d/%m"))
            self.etiquetas.grid(row=2,column=i+1)

            self.lista_etiquetas.append(self.etiquetas)

        self.eventos_diarios=ttk.Treeview(self.frame1, columns=('Fecha','Hora','Titulo'),show='headings', selectmode='browse')
        self.eventos_diarios.heading('Fecha',text='Fecha')
        self.eventos_diarios.heading('Hora',text='Hora')
        self.eventos_diarios.heading('Titulo',text='Titulo')
        self.eventos_diarios.column('Fecha')
        self.eventos_diarios.column('Hora')
        self.eventos_diarios.column('Titulo')
        self.eventos_diarios.grid(row=3, column=1,columnspan=7,pady=10)

        self.eventos_diarios.bind('<<TreeviewSelect>>',self.seleccion)

        
        ttk.Button(self.frame1, text='>>', command=self.posterior).grid(row=2,column=8)

        ttk.Button(self.frame1, text='Vista Mensual', command=self.mensual).grid(row=5, column=4)


        '''El frame2 es el contenedor de la vista mensual, estan superpuestos 
        con el frame1 y se habilitan de a 1 por vez'''

        self.frame2=ttk.Frame(self,width=1200,height=1200,padding=10,relief='solid')
        self.frame2.grid(row=0,column=0,sticky='nw')

        self.meses=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        hoy=datetime.now()
        self.mes=hoy.strftime("%m")
        self.anio=hoy.strftime("%Y")
        
        self.etiqueta_mes=ttk.Label(self.frame2,text='Mes: '+hoy.strftime("%m-%Y"), anchor='center',padding=10)
        self.etiqueta_mes.grid(columnspan=9)
        
        ttk.Button(self.frame2,text='<<', command=self.ant_mes).grid(row=2)

        mes=self.meses[int(hoy.strftime("%m"))-1]
        self.eti_mes=ttk.Label(self.frame2,text=mes, padding=(20,10,20,20))
        self.eti_mes.grid(row=1,column=1, columnspan=7)

        self.eventos_mensuales=ttk.Treeview(self.frame2, columns=('Fecha','Hora','Titulo'),show='headings', selectmode='browse')
        self.eventos_mensuales.heading('Fecha',text='Fecha')
        self.eventos_mensuales.heading('Hora',text='Hora')
        self.eventos_mensuales.heading('Titulo',text='Titulo')
        self.eventos_mensuales.column('Fecha')
        self.eventos_mensuales.column('Hora')
        self.eventos_mensuales.column('Titulo')
        self.eventos_mensuales.grid(row=3, column=1,columnspan=7,pady=10)

        self.eventos_mensuales.bind('<<TreeviewSelect>>',self.seleccion)

        
        ttk.Button(self.frame2, text='>>', command=self.post_mes).grid(row=2,column=8)

        ttk.Button(self.frame2, text='Vista Semanal', command=self.semanal).grid(row=5, column=4)

        #Aqui activo inicialmente el frame1, que muestra de forma semanal
        self.semanal()


        '''En el frame 3 se muestra la información completa de cada evento
        desde aqui tambien se permite crear nuevos eventos, modificarlos o borrarlos'''

        self.frame3=ttk.Frame(self,width=300,height=404,padding=10,relief='solid')
        self.frame3.grid(row=0,column=1,sticky='ne')
        ttk.Label(self.frame3,text='EVENTO',font=('',14)).grid(row=0,columnspan=5, pady=5)
        
        ttk.Label(self.frame3,text='Titulo').grid(row=1,column=1,padx=10,pady=10)
        self.m_tit=ttk.Label(self.frame3,text='')
        self.m_tit.grid(row=1,column=2, columnspan=2,padx=10, pady=10)

        ttk.Label(self.frame3,text='Fecha').grid(row=2,column=1,padx=10,pady=10)
        self.m_fec=ttk.Label(self.frame3,text='')
        self.m_fec.grid(row=2,column=2, columnspan=2,padx=10, pady=10)

        ttk.Label(self.frame3,text='Hora').grid(row=3,column=1,padx=10,pady=10)
        self.m_hor=ttk.Label(self.frame3,text='')
        self.m_hor.grid(row=3,column=2, columnspan=2,padx=10, pady=10)

        ttk.Label(self.frame3,text='Duración').grid(row=4,column=1,padx=10,pady=10)
        self.m_dur=ttk.Label(self.frame3,text='')
        self.m_dur.grid(row=4,column=2, columnspan=2,padx=10, pady=10)

        ttk.Label(self.frame3,text='Importancia').grid(row=5,column=1,padx=10,pady=10)
        self.m_imp=ttk.Label(self.frame3,text='')
        self.m_imp.grid(row=5,column=2, columnspan=2,padx=10, pady=10)

        ttk.Label(self.frame3,text='Descripción').grid(row=6,column=1,padx=10,pady=10)
        self.m_tex=tk.Text(self.frame3, width=24, height=5,background='#F5F5F5', border=0)
        self.m_tex.grid(row=6, column=2, columnspan=3, pady=10)
    
      
        ttk.Button(self.frame3, text='Nuevo Evento',command=self.altas).grid(row=9,column=1,padx=5, pady=13)

        self.btn_modificar=ttk.Button(self.frame3, text='Modificar Evento',command=self.modificaciones, state='disabled')
        self.btn_modificar.grid(row=9,column=2,padx=5, pady=13)

        self.btn_borrar=ttk.Button(self.frame3, text='Borrar Evento',command=self.bajas, state='disabled')
        self.btn_borrar.grid(row=9,column=3,padx=5, pady=13)


    def recordatorio(self):
        
        '''Este metodo gestiona los recordatorios de eventos'''

        lista=self.arch_evento.traer_datos()
        for i in range(len(lista)):
            fecha=datetime.strptime(lista[i]['fecha rec'],'%d-%m-%Y').date()
            hora=datetime.strptime(lista[i]['hora rec'], '%H:%M').time()
            fecha_hora=datetime.combine(fecha,hora)
            hora_presente=datetime.now()
            delay=(fecha_hora-hora_presente).total_seconds()*1000
            if delay>0:
                self.after(int(delay), lambda : self.recordar(lista[i]['titulo']))
        
    def recordar(self,str):

        '''Este metodo solamente muestra el mensaje del recordatorio
        es llamado desde el metodo recordatorio()'''

        messagebox.showinfo(message='Tiene un evento: '+str, title='Recordatorio')


    def seleccion(self,event):

        '''Este metodo es llamado desde el evento seleccion de la lista de eventos
        carga en el frame3 los datos de cada evento que se selecciona'''

        seleccion=event.widget.selection()
        for item in seleccion:
            valores=event.widget.item(item)['values']
        lista=self.arch_evento.traer_datos()
        for evento in lista:
            if evento['fecha']==valores[0] and evento['hora']==valores[1] and evento['titulo']==valores[2]:
                datos=evento
                break
        self.m_tit.configure(text=datos['titulo'])
        self.m_fec.configure(text=datos['fecha'])
        self.m_hor.configure(text=datos['hora'])
        self.m_dur.configure(text=datos['duracion'])
        self.m_imp.configure(text=datos['importancia'])
        self.m_tex.delete('1.0','end')
        self.m_tex.insert('1.0',datos['descripcion'])
        self.btn_modificar.state(['!disabled'])
        self.btn_borrar.state(['!disabled'])


    def carga_treeview(self,f_ini,f_fin):

        '''Este metodo carga lo que seria el listbox semanal de eventos'''

        lista=self.arch_evento.traer_datos()
        datos=[]
        if lista!=[]:
            for evento in lista:
                if f_ini<=datetime.strptime(evento['fecha'],'%d-%m-%Y').date()<=f_fin:
                    datos.append(evento)
        datos=sorted(datos, key=lambda x: datetime.strptime(x['fecha'] + ' ' + x['hora'], '%d-%m-%Y %H:%M'))
        if len(self.eventos_diarios.get_children()) > 0:
            self.eventos_diarios.delete(*self.eventos_diarios.get_children())
        for i in range(len(datos)):
            if datos[i]['importancia']=='Importante':
                tags=('importante',)
            else:
                tags=()
            self.eventos_diarios.tag_configure("importante", background="red")
            self.eventos_diarios.insert('',tk.END, values=(datos[i]['fecha'],datos[i]['hora'],datos[i]['titulo']),tags=tags)


    def carga_treeview_mensual(self,mes,anio):

        '''Este metodo carga lo que seria el listbox mensual de eventos'''

        lista=self.arch_evento.traer_datos()
        datos=[]
        if lista!=[]:
            for evento in lista:
                if mes+'-'+anio==evento['fecha'][3:]:
                    datos.append(evento)
        datos=sorted(datos, key=lambda x: datetime.strptime(x['fecha'] + ' ' + x['hora'], '%d-%m-%Y %H:%M'))
        if len(self.eventos_mensuales.get_children()) > 0:
            self.eventos_mensuales.delete(*self.eventos_mensuales.get_children())
        for i in range(len(datos)):
            if datos[i]['importancia']=='Importante':
                tags=('importante',)
            else:
                tags=()
            self.eventos_mensuales.tag_configure("importante", background="red")
            self.eventos_mensuales.insert('',tk.END, values=(datos[i]['fecha'],datos[i]['hora'],datos[i]['titulo']), tags=tags)



    def anterior(self):

        '''Este metodo se encarga del movimiento de las semanas hacia la izquierda
        muestra las semanas anteriores'''

        self.inicio_semana=self.inicio_semana-timedelta(days=7)
        for i in range(7):
            self.fecha=self.inicio_semana+timedelta(days=i)
            self.lista_etiquetas[i].configure(text=self.fecha.strftime("%d/%m"))
        self.etiqueta.configure(text='Semana: '+self.fecha.strftime("%W-%Y"))
        self.carga_treeview(self.inicio_semana.date(),(self.inicio_semana+timedelta(days=6)).date())

    def posterior(self):

        '''Este metodo se encarga del movimiento de las semanas hacia la derecha
        muestra las semanas posteriores'''

        self.inicio_semana=self.inicio_semana+timedelta(days=7)
        for i in range(7):
            self.fecha=self.inicio_semana+timedelta(days=i)
            self.lista_etiquetas[i].configure(text=self.fecha.strftime("%d/%m"))
        self.etiqueta.configure(text='Semana: '+self.fecha.strftime("%W-%Y"))
        self.carga_treeview(self.inicio_semana.date(),(self.inicio_semana+timedelta(days=6)).date())

    def ant_mes(self):

        '''Este metodo se encarga del movimiento de los meses hacia la izquierda
        muestra los meses anteriores'''

        if int(self.mes)==1:
            self.mes=str(12).zfill(2)
            self.anio=str(int(self.anio)-1).zfill(2)
        else:
            self.mes=str(int(self.mes)-1).zfill(2)
        self.etiqueta_mes.configure(text='Mes: '+self.mes+'-'+self.anio)
        self.eti_mes.configure(text=self.meses[int(self.mes)-1])
        self.carga_treeview_mensual(self.mes,self.anio)
        

    def post_mes(self):

        '''Este metodo se encarga del movimiento de los meses hacia la derecha
        muestra los meses anteriores'''

        if int(self.mes)==12:
            self.mes=str(1).zfill(2)
            self.anio=str(int(self.anio)+1).zfill(2)
        else:
            self.mes=str(int(self.mes)+1).zfill(2)
        self.etiqueta_mes.configure(text='Mes: '+self.mes+'-'+self.anio)
        self.eti_mes.configure(text=self.meses[int(self.mes)-1])
        self.carga_treeview_mensual(self.mes,self.anio)

    def mensual(self):

        '''Este metodo se encarga de mantener el frame de la vista mensual activo
        mientras desactiva el semanal'''

        self.frame2.grid()
        self.frame1.grid_remove()
        self.carga_treeview_mensual(self.mes,self.anio)

    def semanal(self):

        '''Este metodo se encarga de mantener el frame de la vista semanal activo
        mientras desactiva el mensual'''

        self.frame1.grid()
        self.frame2.grid_remove()
        self.carga_treeview(self.inicio_semana.date(),(self.inicio_semana+timedelta(days=6)).date())

    def altas(self):

        '''Este metodo llama a la ventana secundaria y habilita el formulario para
        crear un nuevo evento'''

        toplevel=tk.Toplevel(self.parent)
        toplevel.resizable(tk.FALSE,tk.FALSE)
        Secundaria(toplevel,'Nuevo Evento',self.arch_evento).grid()

    def modificaciones(self):

        '''Este metodo llama a la ventana secundaria y habilita el formulario
        cargado con los datos del evento seleccionado para modificar'''

        lista=self.arch_evento.traer_datos()
        for evento in lista:
            print(self.m_fec['text'])
            if evento['fecha']==self.m_fec['text'] and evento['hora']==self.m_hor['text'] and evento['titulo']==self.m_tit['text']:
                datosV=evento
                break
        toplevel=tk.Toplevel(self.parent)
        toplevel.resizable(tk.FALSE,tk.FALSE)
        Secundaria(toplevel,'Modificar Evento',self.arch_evento,datosV).grid()

    def bajas(self):

        '''Este metodo se encarga de eliminar un evento seleccionado'''

        lista=self.arch_evento.traer_datos()
        for evento in lista:
            print(self.m_fec['text'])
            if evento['fecha']==self.m_fec['text'] and evento['hora']==self.m_hor['text'] and evento['titulo']==self.m_tit['text']:
                datos=evento
                break
        self.arch_evento.eliminar_evento(datos)


class Secundaria(ttk.Frame):

    '''Clase de la ventana secundaria de la app'''

    def __init__(self,parent,titulo,evento,dicV={}):

        '''Constructor'''

        super().__init__(parent)
        self.parent=parent
        self.evento=evento
        self.dicV=dicV
        parent.title(titulo)
        self.titulo=titulo
        parent.geometry("380x440")
        
        self.title=tk.StringVar()
        self.importancia=tk.StringVar()

        ttk.Label(self,text='EVENTO',font=('',12),padding=10).grid(row=0,columnspan=6)
        
        ttk.Label(self,text='Titulo del Evento: ',padding=10).grid(row=1,column=1)
        self.entry_title=ttk.Entry(self, textvariable=self.title, width=36)
        self.entry_title.grid(row=1, column=2, columnspan=3)
        self.entry_title.focus()

        ttk.Label(self,text='Fecha: ', padding=10).grid(row=2,column=1)
        self.fecha=DateEntry(self, date_patern='dd/MM/yyyy')
        self.fecha.grid(row=2,column=2)

        ttk.Label(self,text='Hora: ',padding=10).grid(row=2,column=3)
        horas = [str(h).zfill(2) for h in range(24)]
        minutos = [str(m*15).zfill(2) for m in range(4)]
        opciones = [h + ":" + m for h in horas for m in minutos]
        hora_actual = datetime.now().strftime('%H:%M')
        self.hora_combobox = ttk.Combobox(self, values=opciones,width=5)
        self.hora_combobox.grid(row=2, column=4)
        self.hora_combobox.set(hora_actual)

        ttk.Label(self,text='Duración: ',padding=10).grid(row=4,column=1)
        horas = [str(h).zfill(2) for h in range(5)]
        minutos = [str(m*30).zfill(2) for m in range(2)]
        opciones = [h + ":" + m for h in horas for m in minutos]
        hora_actual = datetime.now().strftime('%H:%M')
        self.duracion = ttk.Combobox(self, values=opciones)
        self.duracion.grid(row=4, column=2, columnspan=3)
        self.duracion.set('01:00')

        ttk.Label(self,text='Importancia: ',padding=10).grid(row=5,column=1)
        ttk.Radiobutton(self, text="Importante", variable=self.importancia, value="Importante").grid(row=5,column=2, padx=10)
        ttk.Radiobutton(self, text="Normal", variable=self.importancia, value="Normal").grid(row=5,column=3,pady=10)

        ttk.Label(self,text='Descripción: ',padding=10).grid(row=6,column=1)
        self.descripcion=tk.Text(self, width=28, height=5)
        self.descripcion.grid(row=6, column=2, columnspan=3, pady=10)

        ttk.Label(self,text='RECORDATORIO',font=('',12),padding=10).grid(row=8,columnspan=6)

        ttk.Label(self,text='Fecha: ', padding=10).grid(row=9,column=1)
        self.fecha_r=DateEntry(self, date_patern='dd/MM/yyyy')
        self.fecha_r.grid(row=9,column=2)

        ttk.Label(self,text='Hora: ',padding=10).grid(row=9,column=3)
        horas = [str(h).zfill(2) for h in range(24)]
        minutos = [str(m*15).zfill(2) for m in range(4)]
        opciones = [h + ":" + m for h in horas for m in minutos]
        hora_actual = datetime.now().strftime('%H:%M')
        self.hora_rec = ttk.Combobox(self, values=opciones,width=5)
        self.hora_rec.grid(row=9, column=4)
        self.hora_rec.set(hora_actual)


        if self.dicV!={}:
            self.title.set(dicV['titulo'])
            self.fecha.set_date(dicV['fecha'])
            self.hora_combobox.set(dicV['hora'])
            self.duracion.set(dicV['duracion'])
            self.importancia.set(dicV['importancia'])
            self.descripcion.insert('1.0',dicV['descripcion'])
            self.fecha_r.set_date(dicV['fecha rec'])
            self.hora_rec.set(dicV['hora rec'])

        ttk.Button(self, text='Aceptar',command=self.aceptar).grid(row=10,column=1, columnspan=2 ,padx=5, pady=13)

        ttk.Button(self, text='Cancelar',command=parent.destroy).grid(row=10,column=3, columnspan=2,padx=5, pady=13)

    def aceptar(self):

        '''Este metodo es llamado por el boton aceptar tanto para altas como para
        modificaciones de eventos'''

        dic={}
        if self.title.get()==''and self.importancia.get()=='':
            messagebox.showwarning(message='Debe completar todos los campos', title='Completar campos vacios')
            self.entry_title.focus()
        else:
            if self.evento.coincide_fecha_hora(datetime.strftime(self.fecha.get_date(),'%d-%m-%Y'),self.hora_combobox.get()):
                messagebox.showwarning(message='Ya tiene otro evento con la misma fecha y hora',title='Evento Solapado')
                self.entry_title.focus()
            else:
                dic['titulo']=self.title.get()
                fecha_sel=self.fecha.get_date()
                fecha_form=datetime.strftime(fecha_sel,'%d-%m-%Y')
                dic['fecha']=fecha_form
                dic['hora']=self.hora_combobox.get()
                dic['duracion']=self.duracion.get()
                dic['importancia']=self.importancia.get()
                dic['descripcion']=self.descripcion.get('1.0','end')
                fecha_rec=self.fecha_r.get_date()
                fecha_r_form=datetime.strftime(fecha_rec,'%d-%m-%Y')
                dic['fecha rec']=fecha_r_form
                dic['hora rec']=self.hora_rec.get()
            if self.titulo=='Nuevo Evento' and dic!={}:
                self.evento.crear_eventos(dic)         
            else:
                if self.titulo=='Modificar Evento' and dic!={}:
                    self.evento.modificar_evento(self.dicV,dic)
            self.parent.destroy()




root=tk.Tk()
root.resizable(tk.FALSE,tk.FALSE)
App(root).grid()
root.mainloop()