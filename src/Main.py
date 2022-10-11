import os
from Conexion import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import *                                                     #hay que instalarlo  pip install tkcalendar
from datetime import date
from datetime import datetime
from Pedidos import *
from Reportes import *
from Clientes import *
from Usuarios import *
from MenuProductos import *
from CategoriasMenuProductos import *
from Login import *


class PizzaYa():
    def __init__(self, cue, cur, ico, rep, cli, cat, me, ped, usu):

        self.cuentaUsuario = cue
        self.cursorBD = cur
        self.icono = ico
        self.reporte = rep
        self.cliente = cli
        self.categoriaMen = cat
        self.men = me
        self.pedidos= ped
        self.usuario = usu

       
        #   ***********************************************************************************************************
        #   ********************                Ventanas                                           ********************
        #   ***********************************************************************************************************

       
        '''   ********************                Ventana Principal                                  ********************'''

        self.anchoVentana = 800
        self.altoVentana = 600

        self.ventana = Tk()                                                                  # Ventana Principal
        self.xventana = int(self.ventana.winfo_screenwidth()/2 - self.anchoVentana/2)                  # Variable para obtener la mitad de la pantalla
        self.yventana = int(self.ventana.winfo_screenheight()/2 - self.altoVentana/1.7)                # Variable para obtener la mitad de la pantalla
        self.ventana.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)                     # Tamaño de la ventana
        + "+" + str(self.xventana) + "+" + str(self.yventana))                                    # Posicion de la ventana en windows
        self.ventana.title("PizzaYa")                                                             # Titulo de la ventana
        self.ventana.iconbitmap(self.icono)                                                       # Icono de la ventana
        self.barraMenu=Menu(self.ventana)                                                         # crea la barra de menu
        self.ventana.config(menu=self.barraMenu)                                                  # vincula la barra de menu con la ventana
        self.ventana.protocol("WM_DELETE_WINDOW", lambda:self.salir())

        #   ********************                Barra de Menu                                        ********************

        self.opcionesMenu = Menu(self.barraMenu, tearoff=0)                            
        self.barraMenu.add_cascade(label="Opciones", menu=self.opcionesMenu)
        self.opcionesMenu.add_command(label="Actualizar Precios por Categorias", command=lambda:self.preciosPorCategoria(self.cursorBD, self.ventana, self.men, self.cuentaUsuario))
        self.opcionesMenu.add_command(label="Actualizar Precios por Productos", command=lambda:self.preciosPorProducto(self.cursorBD, self.ventana, self.men, self.cuentaUsuario))
        self.opcionesMenu.add_command(label="Administrar Usuarios", command=lambda:self.usuarios(self.cursorBD, self.ventana, self.usuario))
        self.opcionesMenu.add_separator()                                         #linea separador
        self.opcionesMenu.add_command(label="Cerrar Sesión", command=lambda:self.cerrarSesion())
        self.opcionesMenu.add_command(label="Salir", command=lambda:self.salir())

        self.ventanaEmergenteCLientes = Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Clientes", command=lambda:self.clientes(self.cursorBD, self.ventana, self.cliente, self.cuentaUsuario))

        self.ventanaEmergenteMenu = Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Menu", menu=self.ventanaEmergenteMenu)
        self.ventanaEmergenteMenu.add_command(label="Administrar Categorias", command=lambda:self.categoriasMenu(self.cursorBD, self.ventana, self.categoriaMen, self.cuentaUsuario))
        self.ventanaEmergenteMenu.add_command(label="Administrar Menu", command=lambda:self.menu(self.cursorBD, self.ventana, self.men, self.cuentaUsuario))

        self.ventanaEmergenteReporte = Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Reporte", menu=self.ventanaEmergenteReporte)
        self.ventanaEmergenteReporte.add_command(label="Reporte Mensual", command=lambda:self.reporteMensual(self.reporte, self.ventana))
        self.ventanaEmergenteReporte.add_command(label="Reporte Parcial", command=lambda:self.reporteParcial(self.reporte, self.ventana))


        #   ********************                Ventana Principal Pedidos                          ********************


        self.pedidoId = StringVar()
        self.estado = IntVar()
        self.pago = IntVar()
        
        def click(event):
            if len(self.listaPedidos.selection())>0:
                self.vaciarTabla(self.listaDetallePedido)
                id= self.listaPedidos.selection()[0]
                self.pedidoId.set(value=(self.listaPedidos.item(id, "values")[0]))
                self.completarTablaDetallePedidos(self.cursorBD, self.listaDetallePedido, self.pedidoId.get())
                self.telefono.config(text="Telefono:  "+self.listaPedidos.item(id, "values")[10])
                self.nombre.config(text="Nombre:  "+self.listaPedidos.item(id, "values")[9])
                self.calle.config(text="Direccion:  "+self.listaPedidos.item(id, "values")[1])
                self.altura.config(text=self.listaPedidos.item(id, "values")[2])
                self.piso.config(text="Piso: "+self.listaPedidos.item(id, "values")[3])
                self.departamento.config(text="Depto: "+self.listaPedidos.item(id, "values")[4])
                self.barrio.config(text=self.listaPedidos.item(id, "values")[5])
                self.total.config(text= "$" + self.listaPedidos.item(id, "values")[8])
                self.hora.config(text=(self.listaPedidos.item(id, "values")[11])[11:16])
                if (self.listaPedidos.item(id, "values")[7]) == "Si":
                    self.pago.set(1)
                elif (self.listaPedidos.item(id, "values")[7]) == "No":
                    self.pago.set(0)
                if (self.listaPedidos.item(id, "values")[6]) == "Preparacion":
                    self.estado.set(1)
                elif (self.listaPedidos.item(id, "values")[6]) == "En Camino":
                    self.estado.set(2)
                elif (self.listaPedidos.item(id, "values")[6]) == "Entregado":
                    self.estado.set(3)
                elif (self.listaPedidos.item(id, "values")[6]) == "Cancelado":
                    self.estado.set(4)

        self.marcoSuperior=LabelFrame(self.ventana)
        self.marcoSuperior.place(x=10, y=10, width=self.anchoVentana-30, height=240)
        self.marcoPedidos=Frame(self.ventana)
        self.marcoPedidos.place(y=260, width=self.anchoVentana, height=(self.altoVentana -285))


        self.nombre = Label(self.marcoSuperior)
        self.nombre.grid(row=0, column=0, padx=10, pady=10)

        self.telefono = Label(self.marcoSuperior)
        self.telefono.grid(row=0, column=1, padx=10, pady=10)


        self.calle = Label(self.marcoSuperior)
        self.calle.grid(row=0, column=2, padx=[10,0], pady=10)

        self.altura = Label(self.marcoSuperior)
        self.altura.grid(row=0, column=3, pady=10)

        self.piso = Label(self.marcoSuperior)
        self.piso.grid(row=0, column=4, pady=10)

        self.departamento = Label(self.marcoSuperior)
        self.departamento.grid(row=0, column=5, pady=10)

        self.barrio = Label(self.marcoSuperior)
        self.barrio.grid(row=0, column=6, padx=10, pady=10, columnspan=2)

        self.horaTexto = Label(self.marcoSuperior, text="Hora del pedido:")
        self.horaTexto.place(x=10,y=210)

        self.hora = Label(self.marcoSuperior)
        self.hora.place(x=120,y=210)

        self.totalTexto = Label(self.marcoSuperior, text="Total:")
        self.totalTexto.place(x=400,y=210)

        self.total = Label(self.marcoSuperior)
        self.total.place(x=480,y=210)


        self.preparacion=Radiobutton(self.marcoSuperior, text="Preparacion", variable=self.estado, value=1,
                                    command=lambda:self.cambiarEstadoPedido(self.pedidos, self.ventana, self.estado.get(), self.pedidoId.get(), self.cuentaUsuario))
        self.preparacion.place(x=620, y=50)

        self.enCamino=Radiobutton(self.marcoSuperior, text="En Camino", variable=self.estado, value=2,
                                    command=lambda:self.cambiarEstadoPedido(self.pedidos, self.ventana, self.estado.get(), self.pedidoId.get(), self.cuentaUsuario))
        self.enCamino.place(x=620, y=75)

        self.entregado=Radiobutton(self.marcoSuperior, text="Entregado", variable=self.estado, value=3,
                                    command=lambda:self.cambiarEstadoPedido(self.pedidos, self.ventana, self.estado.get(), self.pedidoId.get(), self.cuentaUsuario))
        self.entregado.place(x=620, y=100)
        
        self.cancelado=Radiobutton(self.marcoSuperior, text="Cancelado", variable=self.estado, value=4,
                                    command=lambda:self.cambiarEstadoPedido(self.pedidos, self.ventana, self.estado.get(), self.pedidoId.get(), self.cuentaUsuario))
        self.cancelado.place(x=620, y=125)

        self.estaPago=Checkbutton(self.marcoSuperior, text="Esta Pago", variable=self.pago, onvalue=1, offvalue=0,
                                    command=lambda:self.cambiarEstadoPago(self.pedidos, self.pago.get(), self.pedidoId.get(), self.cuentaUsuario))
        self.estaPago.place(x=620, y=165)


        self.botonNuevoPedido = Button(self.marcoSuperior, text="Nuevo Pedido", width=15, height=1, command=lambda:[self.nuevoPedido(self.cursorBD,
                                    self.ventana, self.cliente, self.pedidos, self.cuentaUsuario)])
        self.botonNuevoPedido.place(x=620, y=200)


        #                    Lista Detalle de Pedidos                                   

        self.listaDetallePedido=ttk.Treeview(self.marcoSuperior, columns= ("detalle_pedidos_id","cantidad","descripcion","precio_venta"),
                                                displaycolumns=("cantidad","descripcion","precio_venta"))
        self.listaDetallePedido.column("#0",width=0, stretch=NO)
        self.listaDetallePedido.column("cantidad",width=10, anchor=CENTER)
        self.listaDetallePedido.column("descripcion",width=250) 
        self.listaDetallePedido.column("precio_venta",width=50, anchor=CENTER)
        self.listaDetallePedido.place(width=(self.anchoVentana -250), height=(self.altoVentana -450), x=10, y=50)


        self.listaDetallePedido.heading("#0",text="")
        self.listaDetallePedido.heading("cantidad",text="Unidades")
        self.listaDetallePedido.heading("descripcion",text="Descripcion")
        self.listaDetallePedido.heading("precio_venta",text="Precio")

        self.scrollDetallePedido=Scrollbar(self.marcoSuperior, command=self.listaDetallePedido.yview)    #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollDetallePedido.place(width=15, height=self.altoVentana -450, x=560, y=50)  #el scroll toma la dimencion del cuadro de texto
        self.listaDetallePedido.config(yscrollcommand=self.scrollDetallePedido.set)



        #                    Lista Pedidos                                          

        self.listaPedidos=ttk.Treeview(self.marcoPedidos, columns= ("pedidos_id","calle","altura","piso","departamento","barrio",
                                    "estado","pago","total","nombre","telefono","fecha","crea","modifica"),
                                    displaycolumns=("calle","altura","piso","departamento","barrio",
                                    "estado","pago","total","nombre","telefono","crea","modifica"))
        self.listaPedidos.column("#0",width=0, stretch=NO)
        self.listaPedidos.column("telefono",width=100, anchor=CENTER)
        self.listaPedidos.column("nombre",width=150, anchor=CENTER)
        self.listaPedidos.column("calle",width=250)
        self.listaPedidos.column("altura",width=50, anchor=CENTER)
        self.listaPedidos.column("piso",width=50, anchor=CENTER) 
        self.listaPedidos.column("departamento",width=50, anchor=CENTER)
        self.listaPedidos.column("barrio",width=150, anchor=CENTER)
        self.listaPedidos.column("total",width=50, anchor=CENTER) 
        self.listaPedidos.column("estado",width=100, anchor=CENTER)
        self.listaPedidos.column("pago",width=50, anchor=CENTER) 
        self.listaPedidos.column("fecha",width=100, anchor=CENTER)
        self.listaPedidos.column("crea",width=100, anchor=CENTER)
        self.listaPedidos.column("modifica",width=100, anchor=CENTER)
        self.listaPedidos.pack()
        self.listaPedidos.place(width=(self.anchoVentana -50), height=(self.altoVentana -310), x=10)
        self.listaPedidos.bind("<<TreeviewSelect>>", click)


        self.listaPedidos.heading("#0",text="")
        self.listaPedidos.heading("telefono",text="Telefono")
        self.listaPedidos.heading("nombre",text="Nombre")
        self.listaPedidos.heading("calle",text="Calle")
        self.listaPedidos.heading("altura",text="Altura")
        self.listaPedidos.heading("piso",text="Piso")
        self.listaPedidos.heading("departamento",text="Depto")
        self.listaPedidos.heading("barrio",text="Barrio")
        self.listaPedidos.heading("total",text="Total")
        self.listaPedidos.heading("estado",text="Estado")
        self.listaPedidos.heading("pago",text="Pago")
        self.listaPedidos.heading("fecha",text="Hora")
        self.listaPedidos.heading("crea",text="Creado Por")
        self.listaPedidos.heading("modifica",text="Modificado Por")

        self.scrollTexto=Scrollbar(self.marcoPedidos, command=self.listaPedidos.yview)        #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollTexto.place(width=15, height=self.altoVentana -305, x=self.anchoVentana -35)  #el scroll toma la dimencion del cuadro de texto
        self.listaPedidos.config(yscrollcommand=self.scrollTexto.set)

        self.scrollHotizontal=Scrollbar(self.marcoPedidos, command=self.listaPedidos.xview, orient=HORIZONTAL)
        self.scrollHotizontal.place(width=self.anchoVentana -45, height=15, x=10, y=self.altoVentana- 305)
        self.listaPedidos.config(xscrollcommand=self.scrollHotizontal.set)

        self.completarTablaPedidos(self.cursorBD, self.listaPedidos)
        
        self.ventana.mainloop()                      #loop de la ventana esperando accion del usuario


    '''#   ********************                Ventanas Reportes                                  ********************'''


    def reporteMensual(self, reporte, vent):
        self.anchoVentana = 640
        self.altoVentana = 480

        self.ventanaReporteMensual = Tk()
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)                     #variable para obtener la mitad de la pantalla
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)                   #variable para obtener la mitad de la pantalla
        self.ventanaReporteMensual.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)       #tamanio de la ventana
        + "+" + str(self.xventana) + "+" + str(self.yventana))                                    #posicion de la ventana en windows
        self.ventanaReporteMensual.resizable(0,0)                                            #desactiva modificar tamanio desde el mouse
        self.ventanaReporteMensual.title("Reporte Mensual")                                  #titulo de la ventana
        self.ventanaReporteMensual.iconbitmap(self.icono)                                         #self.icono de la ventana


        self.marcoSuperiorMensual=Frame(self.ventanaReporteMensual)
        self.marcoSuperiorMensual.place(y=10, width=640, height=100)
        self.marcoReporteMensual=Frame(self.ventanaReporteMensual)
        self.marcoReporteMensual.place(y=120, width=640, height=350)
            
        self.textoEntregadosreporteMensual = Label(self.marcoSuperiorMensual, text="Pedidos Entregados: ")
        self.textoEntregadosreporteMensual.place(x=10, y=10)
        
        self.numeroEntregadosreporteMensual = Label(self.marcoSuperiorMensual)
        self.numeroEntregadosreporteMensual.place(x=120, y=10)

        self.textoCanceladoreporteMensual = Label(self.marcoSuperiorMensual, text="Pedidos Cancelados: ")
        self.textoCanceladoreporteMensual.place(x=250, y=10)
        
        self.numeroCanceladoreporteMensual = Label(self.marcoSuperiorMensual)
        self.numeroCanceladoreporteMensual.place(x=360, y=10)

        self.textoTotalreporteMensual = Label(self.marcoSuperiorMensual, text="Total Vendido: ")
        self.textoTotalreporteMensual.place(x=10, y=65)
        
        self.totalreporteMensual = Label(self.marcoSuperiorMensual, text="$ 0")
        self.totalreporteMensual.place(x=100, y=65)

        self.botonSalirreporteMensual = Button(self.marcoSuperiorMensual, text="Salir", width=10, height=1,
                                command=lambda:self.ventanaReporteMensual.destroy())
        self.botonSalirreporteMensual.place(x=500, y=65)

        self.listaReporteMensual=ttk.Treeview(self.marcoReporteMensual, columns= ("pedidos_id","crea","modifica","total","estado","fecha"),
                                    displaycolumns= ("pedidos_id","total","estado","fecha","crea","modifica"))
        self.listaReporteMensual.column("#0",width=0, stretch=NO)
        self.listaReporteMensual.column("pedidos_id",width=100, anchor=CENTER)
        self.listaReporteMensual.column("total",width=150, anchor=CENTER) 
        self.listaReporteMensual.column("estado",width=150, anchor=CENTER) 
        self.listaReporteMensual.column("fecha",width=150, anchor=CENTER)
        self.listaReporteMensual.column("crea",width=100, anchor=CENTER) 
        self.listaReporteMensual.column("modifica",width=100, anchor=CENTER)
        self.listaReporteMensual.pack()
        self.listaReporteMensual.place(width=600, height=330, x=10)
        
        self.listaReporteMensual.heading("#0",text="")
        self.listaReporteMensual.heading("pedidos_id",text="Pedido N°")
        self.listaReporteMensual.heading("total",text="Total")
        self.listaReporteMensual.heading("estado",text="Estado")
        self.listaReporteMensual.heading("fecha",text="Fecha")
        self.listaReporteMensual.heading("crea",text="Creado Por")
        self.listaReporteMensual.heading("modifica",text="Modificado Por")

        self.totreporteMensual=IntVar()
        self.totEntregadoreporteMensual=IntVar()
        self.totCanceladoreporteMensual=IntVar()

        self.consultareporteMensual = reporte.mensual(date.today().year, date.today().month)
        for i in self.consultareporteMensual:
            idlistaReporteMensual = i[0]
            self.listaReporteMensual.insert("", END, idlistaReporteMensual, values= i)
            if i[4] == "Entregado":
                self.totreporteMensual.set(self.totreporteMensual.get()+i[3])
                self.totEntregadoreporteMensual.set(self.totEntregadoreporteMensual.get()+1)
            elif i[4] == "Cancelado":
                self.totCanceladoreporteMensual.set(self.totCanceladoreporteMensual.get()+1)
                
        self.totalreporteMensual.config(text=("$ "+ str(self.totreporteMensual.get())))
        self.numeroEntregadosreporteMensual.config(text=(self.totEntregadoreporteMensual.get()))
        self.numeroCanceladoreporteMensual.config(text=(self.totCanceladoreporteMensual.get()))
         
        self.scrollTextoreporteMensual=Scrollbar(self.marcoReporteMensual, command=self.listaReporteMensual.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollTextoreporteMensual.place(width=15, height=330, x=615)                    #el scroll toma la dimencion del cuadro de texto
        self.listaReporteMensual.config(yscrollcommand=self.scrollTexto.set)
        
        self.scrollHotizontalreporteMensual=Scrollbar(self.marcoReporteMensual, command=self.listaReporteMensual.xview, orient=HORIZONTAL)
        self.scrollHotizontalreporteMensual.place(width=self.anchoVentana -45, height=15, x=10, y=self.altoVentana- 145)
        self.listaReporteMensual.config(xscrollcommand=self.scrollHotizontal.set)
    
    def reporteParcial(self, reporte, vent):
        self.anchoVentana = 640
        self.altoVentana = 480

        self.ventanaReporteParcial = Tk()
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)         #variable para obtener la mitad de la pantalla
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)       #variable para obtener la mitad de la pantalla
        self.ventanaReporteParcial.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)         #tamanio de la ventana
        + "+" + str(self.xventana) + "+" + str(self.yventana))                        #posicion de la ventana en windows
        self.ventanaReporteParcial.resizable(0,0)                                              #desactiva modificar tamanio desde el mouse
        self.ventanaReporteParcial.title("Reporte Parcial")                                    #titulo de la ventana
        self.ventanaReporteParcial.iconbitmap(self.icono)                                           #self.icono de la ventana


        self.marcoSuperiorParcial=Frame(self.ventanaReporteParcial)
        self.marcoSuperiorParcial.place(y=10, width=640, height=150)
        self.marcoReporteParcial=Frame(self.ventanaReporteParcial)
        self.marcoReporteParcial.place(y=170, width=640, height=300)
            

        self.textoDesdeReporteParcial = Label(self.marcoSuperiorParcial, text="Desde: ")
        self.textoDesdeReporteParcial.grid(row=0, column=0, padx=(10,0))

        self.textoHastaReporteParcial = Label(self.marcoSuperiorParcial, text="Hasta: ")
        self.textoHastaReporteParcial.grid(row=0, column=2, padx=(10,0))

        self.fechaDesdeReporteParcial = DateEntry(self.marcoSuperiorParcial, date_pattern='dd/mm/yyyy')
        self.fechaDesdeReporteParcial.grid(row=0, column=1)

        self.fechaHastaReporteParcial = DateEntry(self.marcoSuperiorParcial, date_pattern='dd/mm/yyyy')
        self.fechaHastaReporteParcial.grid(row=0, column=3)

        self.textoEntregadosReporteParcial = Label(self.marcoSuperiorParcial, text="Pedidos Entregados: ")
        self.textoEntregadosReporteParcial.place(x=10, y=60)
        
        self.numeroEntregadosReporteParcial = Label(self.marcoSuperiorParcial)
        self.numeroEntregadosReporteParcial.place(x=120, y=60)

        self.textoCanceladoReporteParcial = Label(self.marcoSuperiorParcial, text="Pedidos Cancelados: ")
        self.textoCanceladoReporteParcial.place(x=250, y=60)
        
        self.numeroCanceladoReporteParcial = Label(self.marcoSuperiorParcial)
        self.numeroCanceladoReporteParcial.place(x=360, y=60)

        self.textoTotalReporteParcial = Label(self.marcoSuperiorParcial, text="Total Vendido: ")
        self.textoTotalReporteParcial.place(x=10, y=115)
        
        self.totalReporteParcial = Label(self.marcoSuperiorParcial, text="$ 0")
        self.totalReporteParcial.place(x=100, y=115)
    
        
        self.botonBuscarReporteParcial = Button(self.marcoSuperiorParcial, text="Buscar", width=10, height=1, command=lambda:[self.vaciarTabla(self.listaReporteParcial),
                                    self.completarTablareportes(reporte, self.listaReporteParcial,self.fechaDesdeReporteParcial.get()[6:10], self.fechaDesdeReporteParcial.get()[3:5],
                                    self.fechaDesdeReporteParcial.get()[0:2], self.fechaHastaReporteParcial.get()[6:10], self.fechaHastaReporteParcial.get()[3:5], self.fechaHastaReporteParcial.get()[0:2],
                                    self.totalReporteParcial, self.numeroEntregadosReporteParcial, self.numeroCanceladoReporteParcial)])
        self.botonBuscarReporteParcial.place(x=400, y=115)

        self.botonSalirReporteParcial = Button(self.marcoSuperiorParcial, text="Salir", width=10, height=1,
                                command=lambda:[self.ventanaReporteParcial.destroy()])
        self.botonSalirReporteParcial.place(x=500, y=115)

        self.listaReporteParcial=ttk.Treeview(self.marcoReporteParcial, columns= ("pedidos_id","crea","modifica","total","estado","fecha"),
                                    displaycolumns=("pedidos_id","total","estado","fecha","crea","modifica"))
        self.listaReporteParcial.column("#0",width=0, stretch=NO)
        self.listaReporteParcial.column("pedidos_id",width=100, anchor=CENTER)
        self.listaReporteParcial.column("total",width=150, anchor=CENTER)
        self.listaReporteParcial.column("estado",width=150, anchor=CENTER)
        self.listaReporteParcial.column("fecha",width=150, anchor=CENTER)
        self.listaReporteParcial.column("crea",width=100, anchor=CENTER)
        self.listaReporteParcial.column("modifica",width=100, anchor=CENTER)
        self.listaReporteParcial.pack()                                 
        self.listaReporteParcial.place(width=600, height=280, x=10)
        
        self.listaReporteParcial.heading("#0",text="")
        self.listaReporteParcial.heading("pedidos_id",text="Pedido N°")
        self.listaReporteParcial.heading("total",text="Total")
        self.listaReporteParcial.heading("estado",text="Estado")
        self.listaReporteParcial.heading("fecha",text="Fecha")
        self.listaReporteParcial.heading("crea",text="Creado Por")
        self.listaReporteParcial.heading("modifica",text="Modificado Por")

        scrollTextoReporteParcial=Scrollbar(self.marcoReporteParcial, command=self.listaReporteParcial.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        scrollTextoReporteParcial.place(width=15, height=280, x=615)                    #el scroll toma la dimencion del cuadro de texto
        self.listaReporteParcial.config(yscrollcommand=scrollTextoReporteParcial.set)
        
        self.scrollHotizontalReporteParcial=Scrollbar(self.marcoReporteParcial, command=self.listaReporteParcial.xview, orient=HORIZONTAL)
        self.scrollHotizontalReporteParcial.place(width=self.anchoVentana -45, height=15, x=10, y=self.altoVentana- 195)
        self.listaReporteParcial.config(xscrollcommand=self.scrollHotizontalReporteParcial.set)


    '''#   ********************                Ventana Buscar Cliente                            ********************'''

    def buscarCliente(self, cursor, vent, telPedido, nomPedido, calPedido, altPedido,
                        pisPedido, depPedido, barPedido):
        self.anchoVentana = 640
        self.altoVentana = 380

        self.ventanabuscarCliente = Tk()
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)
        self.ventanabuscarCliente.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)
        + "+" + str(self.xventana) + "+" + str(self.yventana))                       
        self.ventanabuscarCliente.resizable(0,0)                                     
        self.ventanabuscarCliente.title("Buscar Cliente")                                  
        self.ventanabuscarCliente.iconbitmap(self.icono)                            


        self.marcoSuperiorbuscarCliente=LabelFrame(self.ventanabuscarCliente)
        self.marcoSuperiorbuscarCliente.place(x=10, y=10, width=620, height=140)
        self.marcoClientesbuscarCliente=Frame(self.ventanabuscarCliente)
        self.marcoClientesbuscarCliente.place(y=170, width=640, height=300)
            
        
        self.eticNombrebuscarCliente = Label(self.marcoSuperiorbuscarCliente, text="Nombre: ")
        self.eticNombrebuscarCliente.place(x=0,y=0)

        self.eticTelefonobuscarCliente = Label(self.marcoSuperiorbuscarCliente, text="Telefono: ")
        self.eticTelefonobuscarCliente.place(x=250,y=0)


        self.eticCallebuscarCliente = Label(self.marcoSuperiorbuscarCliente, text="Calle: ")
        self.eticCallebuscarCliente.place(x=0,y=50)

        self.eticAlturabuscarCliente = Label(self.marcoSuperiorbuscarCliente, text="Altura: ")
        self.eticAlturabuscarCliente.place(x=180,y=50)

        self.eticPisobuscarCliente = Label(self.marcoSuperiorbuscarCliente, text="Piso: ")
        self.eticPisobuscarCliente.place(x=290,y=50)

        self.eticDepartamentobuscarCliente = Label(self.marcoSuperiorbuscarCliente, text="Departamento: ")
        self.eticDepartamentobuscarCliente.place(x=380,y=50)

        self.eticBarriobuscarCliente = Label(self.marcoSuperiorbuscarCliente, text="Barrio: ")
        self.eticBarriobuscarCliente.place(x=0,y=100)
        
        self.nombrebuscarCliente = Label(self.marcoSuperiorbuscarCliente, width=20)
        self.nombrebuscarCliente.place(x=55,y=0)
            
        self.textoTelefonobuscarCliente = StringVar()
        self.telefonobuscarCliente = Entry(self.marcoSuperiorbuscarCliente, width=15, textvariable=self.textoTelefonobuscarCliente)
        self.telefonobuscarCliente.place(x=310,y=0)
        
            
        self.callebuscarCliente = Label(self.marcoSuperiorbuscarCliente, width=15)
        self.callebuscarCliente.place(x=40,y=50)
        
        self.alturabuscarCliente = Label(self.marcoSuperiorbuscarCliente, width=6)
        self.alturabuscarCliente.place(x=225,y=50)
                
        self.pisobuscarCliente = Label(self.marcoSuperiorbuscarCliente, width=5)
        self.pisobuscarCliente.place(x=325,y=50)
                
        self.departamentobuscarCliente = Label(self.marcoSuperiorbuscarCliente, width=5)
        self.departamentobuscarCliente.place(x=470,y=50)

        self.barriobuscarCliente = Label(self.marcoSuperiorbuscarCliente, width=15)
        self.barriobuscarCliente.place(x=45,y=100)

        
        self.clienteIdbuscarCliente=StringVar()
        
        
        self.botonBuscarbuscarCliente = Button(self.marcoSuperiorbuscarCliente, text="Buscar", width=10, height=1, command=lambda:[ self.vaciarTabla(self.listaClientesbuscarCliente),
                            self.busquedaCliente(cursor, self.ventanabuscarCliente, self.listaClientesbuscarCliente,self.telefonobuscarCliente.get())])
        self.botonBuscarbuscarCliente.place(x=300,y=100)
        
        self.botonSeleccionarbuscarCliente = Button(self.marcoSuperiorbuscarCliente, text="Seleccionar", width=10, height=1, command=lambda:[   #borra y completa los datos
                            telPedido.delete(0, "end"),nomPedido.delete(0, "end"),
                            telPedido.insert(0,self.telefonobuscarCliente.get()),nomPedido.insert(0,self.nombrebuscarCliente.cget("text")),
                            calPedido.delete(0, "end"),altPedido.delete(0, "end"),
                            calPedido.insert(0,self.callebuscarCliente.cget("text")),altPedido.insert(0,self.alturabuscarCliente.cget("text")),
                            pisPedido.delete(0, "end"),depPedido.delete(0, "end"),
                            pisPedido.insert(0,self.pisobuscarCliente.cget("text")),depPedido.insert(0,self.departamentobuscarCliente.cget("text")),
                            barPedido.delete(0, "end"),barPedido.insert(0,self.barriobuscarCliente.cget("text")),
                            self.ventanabuscarCliente.destroy()]) 
                            
        self.botonSeleccionarbuscarCliente.place(x=400,y=100)

        self.botonSalirbuscarCliente = Button(self.marcoSuperiorbuscarCliente, text="Cancelar", width=10, height=1, command=lambda:self.ventanabuscarCliente.destroy())
        self.botonSalirbuscarCliente.place(x=500,y=100)

        def clickbuscarCliente(event):
           if len(self.listaClientesbuscarCliente.selection())>0:
                idbuscarCliente= self.listaClientesbuscarCliente.selection()[0]
                self.clienteIdbuscarCliente.set(value=(self.listaClientesbuscarCliente.item(idbuscarCliente, "values")[0]))
                self.telefonobuscarCliente.delete(0, "end")
                tel=self.listaClientesbuscarCliente.item(idbuscarCliente, "values")[1]
                self.telefonobuscarCliente.insert(0, tel)
                self.nombrebuscarCliente.config(text=self.listaClientesbuscarCliente.item(idbuscarCliente, "values")[2])
                self.callebuscarCliente.config(text=self.listaClientesbuscarCliente.item(idbuscarCliente, "values")[3])
                self.alturabuscarCliente.config(text=self.listaClientesbuscarCliente.item(idbuscarCliente, "values")[4])
                self.pisobuscarCliente.config(text=self.listaClientesbuscarCliente.item(idbuscarCliente, "values")[5])
                self.departamentobuscarCliente.config(text=self.listaClientesbuscarCliente.item(idbuscarCliente, "values")[6])
                self.barriobuscarCliente.config(text=self.listaClientesbuscarCliente.item(idbuscarCliente, "values")[7])

        self.listaClientesbuscarCliente=ttk.Treeview(self.marcoClientesbuscarCliente, columns=
                        ("clientes_id","telefono","nombre","calle","altura","piso","departamento","barrio"),
                        displaycolumns=("telefono","nombre","calle","altura","piso","departamento","barrio"))
        self.listaClientesbuscarCliente.column("#0",width=0, stretch=NO) 
        self.listaClientesbuscarCliente.column("telefono",width=100, anchor=CENTER) 
        self.listaClientesbuscarCliente.column("nombre",width=150, anchor=CENTER) 
        self.listaClientesbuscarCliente.column("calle",width=150, anchor=CENTER) 
        self.listaClientesbuscarCliente.column("altura",width=50, anchor=CENTER) 
        self.listaClientesbuscarCliente.column("piso",width=50, anchor=CENTER) 
        self.listaClientesbuscarCliente.column("departamento",width=50, anchor=CENTER)
        self.listaClientesbuscarCliente.column("barrio",width=150, anchor=CENTER) 
        self.listaClientesbuscarCliente.pack()                                 
        self.listaClientesbuscarCliente.place(width=600, height=270, x=10)
        self.listaClientesbuscarCliente.bind("<<TreeviewSelect>>", clickbuscarCliente)
        
        self.listaClientesbuscarCliente.heading("#0",text="")
        self.listaClientesbuscarCliente.heading("telefono",text="Telefono")
        self.listaClientesbuscarCliente.heading("nombre",text="Nombre")
        self.listaClientesbuscarCliente.heading("calle",text="Calle")
        self.listaClientesbuscarCliente.heading("altura",text="Altura")
        self.listaClientesbuscarCliente.heading("piso",text="Piso")
        self.listaClientesbuscarCliente.heading("departamento",text="Departamento")
        self.listaClientesbuscarCliente.heading("barrio",text="Barrio")

        self.scrollVerticalbuscarCliente=Scrollbar(self.marcoClientesbuscarCliente, command=self.listaClientesbuscarCliente.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVerticalbuscarCliente.place(width=15, height=270, x=615)                      #el scroll toma la dimencion del cuadro de texto
        self.listaClientesbuscarCliente.config(yscrollcommand=self.scrollVerticalbuscarCliente.set)
        
        self.scrollHotizontalbuscarCliente=Scrollbar(self.marcoClientesbuscarCliente, command=self.listaClientesbuscarCliente.xview, orient=HORIZONTAL)
        self.scrollHotizontalbuscarCliente.place(width=600, height=15, x=10, y=280)
        self.listaClientesbuscarCliente.config(xscrollcommand=self.scrollHotizontalbuscarCliente.set)

        self.sqlBuscarClientes = "SELECT clientes_id,telefono,nombre,calle,altura,piso,departamento,barrio FROM clientes WHERE activo = 1"
        self.completarTabla(cursor,self.listaClientesbuscarCliente,self.sqlBuscarClientes)


    '''#   ********************                Ventana Nuevo Pedido                              ********************'''

    def nuevoPedido(self, cursor, vent, cliente, pedidos, usuario):
        self.anchoVentana = 640
        self.altoVentana = 480

        self.ventanaNuevoPedido = Tk()
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)
        self.ventanaNuevoPedido.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)
        + "+" + str(self.xventana) + "+" + str(self.yventana))                       
        self.ventanaNuevoPedido.resizable(0,0)                                     
        self.ventanaNuevoPedido.title("Nuevo Pedido")                                  
        self.ventanaNuevoPedido.iconbitmap(self.icono)                            


        self.marcoSuperiorNP=LabelFrame(self.ventanaNuevoPedido)
        self.marcoSuperiorNP.place(x=10, y=10, width=620, height=140)
        self.marcoMenuNP=LabelFrame(self.ventanaNuevoPedido)
        self.marcoMenuNP.place(x=10, y=170, width=300, height=300)
        self.marcoPedidoNP=LabelFrame(self.ventanaNuevoPedido)
        self.marcoPedidoNP.place(x=330, y=170, width=300, height=300)

        self.menuIdNP=IntVar()
        self.productoIdNP=IntVar()
        self.listaProductosNP=dict()                                            # Listado de Productos seleccionados
        self.sqlMenuNP = "SELECT menu_id,descripcion,precio_venta FROM menu WHERE activo = 1 ORDER BY descripcion ASC"

        self.eticNombreNP = Label(self.marcoSuperiorNP, text="Nombre: ")
        self.eticNombreNP.place(x=0,y=0)

        self.eticTelefonoNP = Label(self.marcoSuperiorNP, text="Telefono: ")
        self.eticTelefonoNP.place(x=250,y=0)

        self.eticCalleNP = Label(self.marcoSuperiorNP, text="Calle: ")
        self.eticCalleNP.place(x=0,y=50)

        self.eticAlturaNP = Label(self.marcoSuperiorNP, text="Altura: ")
        self.eticAlturaNP.place(x=180,y=50)

        self.eticPisoNP = Label(self.marcoSuperiorNP, text="Piso: ")
        self.eticPisoNP.place(x=290,y=50)

        self.eticDepartamentoNP = Label(self.marcoSuperiorNP, text="Departamento: ")
        self.eticDepartamentoNP.place(x=380,y=50)

        self.eticBarrioNP = Label(self.marcoSuperiorNP, text="Barrio: ")
        self.eticBarrioNP.place(x=0,y=100)
        
        self.textoNombreNP = StringVar()
        self.nombreNP = Entry(self.marcoSuperiorNP, width=20, textvariable=self.textoNombreNP)
        self.nombreNP.place(x=55,y=0)
            
        self.textoTelefonoNP = StringVar()
        self.telefonoNP = Entry(self.marcoSuperiorNP, width=15, textvariable=self.textoTelefonoNP)
        self.telefonoNP.place(x=310,y=0)
                    
        self.textoCalleNP = StringVar()
        self.calleNP = Entry(self.marcoSuperiorNP, width=15, textvariable=self.textoCalleNP)
        self.calleNP.place(x=40,y=50)
        
        self.textoAlturaNP = StringVar()
        self.alturaNP = Entry(self.marcoSuperiorNP, width=6, textvariable=self.textoAlturaNP)
        self.alturaNP.place(x=225,y=50)
                
        self.textoPisoNP = StringVar()
        self.pisoNP = Entry(self.marcoSuperiorNP, width=5, textvariable=self.textoPisoNP)
        self.pisoNP.place(x=325,y=50)
                
        self.textoDepartamentoNP = StringVar()
        self.departamentoNP = Entry(self.marcoSuperiorNP, width=5, textvariable=self.textoDepartamentoNP)
        self.departamentoNP.place(x=470,y=50)

        self.textoBarrioNP = StringVar()
        self.barrioNP = Entry(self.marcoSuperiorNP, width=15, textvariable=self.textoBarrioNP)
        self.barrioNP.place(x=45,y=100)

        self.eticMenuNP = Label(self.marcoMenuNP, text="Menu", font="Arial 10 underline")
        self.eticMenuNP.place(x=0,y=0)

        self.eticPedidoNP = Label(self.marcoPedidoNP, text="Pedido", font="Arial 10 underline")
        self.eticPedidoNP.place(x=0,y=0)

        self.eticTotalNP = Label(self.marcoPedidoNP, text="Total")
        self.eticTotalNP.place(x=10,y=250)

        self.textoTotalNP = Label(self.marcoPedidoNP, text="$ 0")
        self.textoTotalNP.place(x=230,y=250)


        self.botonBuscarNP = Button(self.marcoSuperiorNP, text="Buscar Cliente", width=15, height=1, command=lambda:[self.buscarCliente(cursor,
                            self.ventanaNuevoPedido, self.telefonoNP, self.nombreNP, self.calleNP, self.alturaNP, self.pisoNP, self.departamentoNP, self.barrioNP)])
        self.botonBuscarNP.place(x=200,y=100)
              
        self.botonBuscar = Button(self.marcoSuperiorNP, text="Guardar Pedido", width=15, height=1, command=lambda:[self.agregarPedido(cursor,
                            self.ventanaNuevoPedido, cliente, pedidos, self.telefonoNP.get(), self.nombreNP.get(), self.calleNP.get(), self.alturaNP.get(),
                            self.pisoNP.get(), self.departamentoNP.get(), self.barrioNP.get(), usuario, self.listaProductosNP.items()),
                            self.vaciarTabla(self.listaPedidos),self.completarTablaPedidos(cursor, self.listaPedidos), self.ventanaNuevoPedido.destroy()])
        self.botonBuscar.place(x=350,y=100)
       
        self.botonSalirNP = Button(self.marcoSuperiorNP, text="Cancelar", width=10, height=1, command=lambda:self.ventanaNuevoPedido.destroy())
        self.botonSalirNP.place(x=500,y=100)

        self.botonAgregarNP = Button(self.marcoMenuNP, text="Agregar", width=10, height=1, command=lambda:[
            self.agregarProductoMenu(self.listaProductosNP,self.menuIdNP.get(),self.ventanaNuevoPedido),self.vaciarTabla(self.listaPedidoNP),
                self.completarTablaProductosMenu(cursor,self.listaPedidoNP, self.listaProductosNP, self.textoTotalNP)])
        self.botonAgregarNP.place(x=190,y=10)

        self.botonBorrarNP = Button(self.marcoPedidoNP, text="Borrar", width=10, height=1, command=lambda:[
            self.eliminarProductoMenu(self.listaProductosNP,self.productoIdNP.get()),self.vaciarTabla(self.listaPedidoNP),
                self.completarTablaProductosMenu(cursor,self.listaPedidoNP, self.listaProductosNP, self.textoTotalNP)])
        self.botonBorrarNP.place(x=190,y=10)

        def clickMenuNP(event):
            if len(self.listaMenuNP.selection())>0:
                idclickMenuNP = self.listaMenuNP.selection()[0]
                self.menuIdNP.set(value=(self.listaMenuNP.item(idclickMenuNP, "values")[0]))
                            
        def clickPedidoNP(event):
            if len(self.listaPedidoNP.selection())>0:
                idclickPedidoNP= self.listaPedidoNP.selection()[0]
                self.productoIdNP.set(value=(self.listaMenuNP.item(idclickPedidoNP, "values")[0]))
          
        self.listaMenuNP=ttk.Treeview(self.marcoMenuNP, columns=("menu_id","descripcion","precio_venta"),
                                    displaycolumns=("descripcion","precio_venta"))
        self.listaMenuNP.column("#0",width=0, stretch=NO) 
        self.listaMenuNP.column("descripcion",width=150)
        self.listaMenuNP.column("precio_venta",width=50, anchor=CENTER)
        self.listaMenuNP.pack()                                 
        self.listaMenuNP.place(width=260, height=220, x=10, y=50)
        self.listaMenuNP.bind("<<TreeviewSelect>>", clickMenuNP)
        
        self.listaMenuNP.heading("#0",text="")
        self.listaMenuNP.heading("descripcion",text="Descripcion")
        self.listaMenuNP.heading("precio_venta",text="Precio")

        self.scrollVerticalNP=Scrollbar(self.marcoMenuNP, command=self.listaMenuNP.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVerticalNP.place(width=15, height=220, x=275, y=50)                      #el scroll toma la dimencion del cuadro de texto
        self.listaMenuNP.config(yscrollcommand=self.scrollVerticalNP.set)
        
        self.listaPedidoNP=ttk.Treeview(self.marcoPedidoNP, columns=("unidades","menu_id","descripcion","precio_venta"),
                                    displaycolumns=("unidades","descripcion","precio_venta"))
        self.listaPedidoNP.column("#0",width=0, stretch=NO) 
        self.listaPedidoNP.column("unidades",width=20, anchor=CENTER)
        self.listaPedidoNP.column("descripcion",width=150)
        self.listaPedidoNP.column("precio_venta",width=50, anchor=CENTER)
        self.listaPedidoNP.pack()                                 
        self.listaPedidoNP.place(width=260, height=200, x=10, y=50)
        self.listaPedidoNP.bind("<<TreeviewSelect>>", clickPedidoNP)
        
        self.listaPedidoNP.heading("#0",text="")
        self.listaPedidoNP.heading("unidades",text="")
        self.listaPedidoNP.heading("descripcion",text="Descripcion")
        self.listaPedidoNP.heading("precio_venta",text="Precio")

        self.scrollVerticalPedNP=Scrollbar(self.marcoPedidoNP, command=self.listaPedidoNP.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVerticalPedNP.place(width=15, height=200, x=275, y=50)                      #el scroll toma la dimencion del cuadro de texto
        self.listaPedidoNP.config(yscrollcommand=self.scrollVerticalPedNP.set)
        

        self.completarTabla(cursor,self.listaMenuNP,self.sqlMenuNP)


    '''#   ********************                Ventana Actualizacion Precios por Producto                     ********************'''
    
    def preciosPorProducto(self, cursor, vent, menu, usuario):
        self.anchoVentana = 640
        self.altoVentana = 480

        self.ventanaPreciosPorProducto = Tk()
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)
        self.ventanaPreciosPorProducto.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)
        + "+" + str(self.xventana) + "+" + str(self.yventana))                       
        self.ventanaPreciosPorProducto.resizable(0,0)                                     
        self.ventanaPreciosPorProducto.title("Actualizacion de Precios por Producto")                                  
        self.ventanaPreciosPorProducto.iconbitmap(self.icono)                            


        self.marcoSuperiorPreciosPorProducto=LabelFrame(self.ventanaPreciosPorProducto)
        self.marcoSuperiorPreciosPorProducto.place(x=10, y=10, width=620, height=140)
        self.marcoMenuActualPP=LabelFrame(self.ventanaPreciosPorProducto)
        self.marcoMenuActualPP.place(x=10, y=170, width=300, height=300)
        self.marcoMenuNuevoPP=LabelFrame(self.ventanaPreciosPorProducto)
        self.marcoMenuNuevoPP.place(x=330, y=170, width=300, height=300)

        self.menuIdPrecioPP=IntVar()
        self.productoIdPrecioPP=IntVar()
        self.listaPrecioProductos=list()                                             # Listado de Productos seleccionados
        self.opcionModificacionPP=IntVar()
        self.sqlMenuPP = "SELECT menu_id,descripcion,precio_venta FROM menu WHERE activo = 1 ORDER BY descripcion ASC"

        self.aumentoPorPP=Radiobutton(self.marcoSuperiorPreciosPorProducto, text="Aumentar: %", variable=self.opcionModificacionPP, value=1,
                                    command=lambda:[self.aumentoPorcentrajePP.config(state="normal"), self.opcionModificacionPP.set(1),
                                    self.rebajaPorcentajePP.delete(0, "end"),self.rebajaPorcentajePP.config(state="disable"),
                                    self.aumentoFijoPP.delete(0, "end"),self.aumentoFijoPP.config(state="disable"),
                                    self.rebajaFijoPP.delete(0, "end"),self.rebajaFijo.PPconfig(state="disable")])
        self.aumentoPorPP.place(x=10, y=10)
        
        self.rebajaPorPP=Radiobutton(self.marcoSuperiorPreciosPorProducto, text="Rebajar: %", variable=self.opcionModificacionPP, value=2,
                                    command=lambda:[self.aumentoPorcentrajePP.delete(0, "end"),self.aumentoPorcentrajePP.config(state="disable"),
                                    self.rebajaPorcentajePP.config(state="normal"), self.opcionModificacionPP.set(2),
                                    self.aumentoFijoPP.delete(0, "end"),self.aumentoFijoPP.config(state="disable"),
                                    self.rebajaFijoPP.delete(0, "end"),self.rebajaFijoPP.config(state="disable")])
        self.rebajaPorPP.place(x=300, y=10)
        
        self.aumentoFijPP=Radiobutton(self.marcoSuperiorPreciosPorProducto, text="Aumentar: $", variable=self.opcionModificacionPP, value=3,
                                    command=lambda:[self.aumentoPorcentrajePP.delete(0, "end"),self.aumentoPorcentrajePP.config(state="disable"),
                                    self.rebajaPorcentajePP.delete(0, "end"),self.rebajaPorcentajePP.config(state="disable"),
                                    self.aumentoFijoPP.config(state="normal"), self.opcionModificacionPP.set(3),
                                    self.rebajaFijoPP.delete(0, "end"),self.rebajaFijoPP.config(state="disable")])
        self.aumentoFijPP.place(x=10, y=60)
        
        self.rebajaFijPP=Radiobutton(self.marcoSuperiorPreciosPorProducto, text="Rebajar: $", variable=self.opcionModificacionPP, value=4,
                                    command=lambda:[self.aumentoPorcentrajePP.delete(0, "end"),self.aumentoPorcentrajePP.config(state="disable"),
                                    self.rebajaPorcentajePP.delete(0, "end"),self.rebajaPorcentajePP.config(state="disable"),
                                    self.aumentoFijoPP.delete(0, "end"),self.aumentoFijoPP.config(state="disable"), self.opcionModificacionPP.set(4),
                                    self.rebajaFijoPP.config(state="normal")])
        self.rebajaFijPP.place(x=300, y=60)
        
               
        self.textoAumentoPorcentrajePP = StringVar()
        self.aumentoPorcentrajePP = Entry(self.marcoSuperiorPreciosPorProducto, width=10, textvariable=self.textoAumentoPorcentrajePP, state="disable")
        self.aumentoPorcentrajePP.place(x=110,y=10)
            
        self.textoRebajaPorcentajePP = StringVar()
        self.rebajaPorcentajePP = Entry(self.marcoSuperiorPreciosPorProducto, width=10, textvariable=self.textoRebajaPorcentajePP, state="disable")
        self.rebajaPorcentajePP.place(x=385,y=10)
                    
        self.textoAumentoFijoPP = StringVar()
        self.aumentoFijoPP = Entry(self.marcoSuperiorPreciosPorProducto, width=10, textvariable=self.textoAumentoFijoPP, state="disable")
        self.aumentoFijoPP.place(x=110,y=60)
        
        self.textoRebajaFijoPP = StringVar()
        self.rebajaFijoPP = Entry(self.marcoSuperiorPreciosPorProducto, width=10, textvariable=self.textoRebajaFijoPP, state="disable")
        self.rebajaFijoPP.place(x=385,y=60)
        
        self.eticMenuActualPP = Label(self.marcoMenuActualPP, text="Menu Actual", font="Arial 10 underline")
        self.eticMenuActualPP.place(x=0,y=0)

        self.eticMenuNuevoPP = Label(self.marcoMenuNuevoPP, text="Productos con Precio Actualizado", font="Arial 10 underline")
        self.eticMenuNuevoPP.place(x=0,y=0)

        self.botonBuscarPP = Button(self.marcoSuperiorPreciosPorProducto, text="Actualizar Lista", width=15, height=1, command=lambda:[
                                    self.vaciarTabla(self.listaMenuNuevoPP),
                                    self.completarTablaProductosMenuActualizado(cursor,self.listaMenuNuevoPP, self.listaPrecioProductos,
                                    self.opcionModificacionPP.get(),self.aumentoPorcentrajePP.get(), self.rebajaPorcentajePP.get(),
                                    self.aumentoFijoPP.get(),self.rebajaFijoPP.get(),self.ventanaPreciosPorProducto)])
        self.botonBuscarPP.place(x=200,y=100)
        
        self.botonBuscarPP = Button(self.marcoSuperiorPreciosPorProducto, text="Cambiar Precios", width=15, height=1, command=lambda:[
                                    self.cambiarPrecioMenuActualizado(cursor,self.listaMenuNuevoPP, self.listaPrecioProductos,
                                    self.opcionModificacionPP.get(),self.aumentoPorcentrajePP.get(), self.rebajaPorcentajePP.get(),
                                    self.aumentoFijoPP.get(),self.rebajaFijoPP.get(),self.ventanaPreciosPorProducto,menu,usuario)])
        self.botonBuscarPP.place(x=350,y=100)

        self.botonSalirPP = Button(self.marcoSuperiorPreciosPorProducto, text="Cancelar", width=10, height=1, command=lambda:self.ventanaPreciosPorProducto.destroy())
        self.botonSalirPP.place(x=500,y=100)

        self.botonAgregarPP = Button(self.marcoMenuActualPP, text="Agregar", width=10, height=1, command=lambda:[
                self.agregarProductoMenuActualizado(self.listaPrecioProductos,self.menuIdPrecioPP.get(),self.ventanaPreciosPorProducto),
                self.vaciarTabla(self.listaMenuNuevoPP),
                self.completarTablaProductosMenuActualizado(cursor,self.listaMenuNuevoPP, self.listaPrecioProductos,self.opcionModificacionPP.get(),
                                                            self.aumentoPorcentrajePP.get(), self.rebajaPorcentajePP.get(),self.aumentoFijoPP.get(),
                                                            self.rebajaFijoPP.get(),self.ventanaPreciosPorProducto)])
        self.botonAgregarPP.place(x=190,y=10)

        self.botonBorrarPP = Button(self.marcoMenuNuevoPP, text="Borrar", width=10, height=1, command=lambda:[
                self.eliminarProductoMenuActualizado(self.listaPrecioProductos,self.productoIdPrecioPP.get()),
                self.vaciarTabla(self.listaMenuNuevoPP),
                self.completarTablaProductosMenuActualizado(cursor,self.listaMenuNuevoPP, self.listaPrecioProductos,self.opcionModificacionPP.get(),
                                                            self.aumentoPorcentrajePP.get(), self.rebajaPorcentajePP.get(),self.aumentoFijoPP.get(),
                                                            self.rebajaFijoPP.get(),self.ventanaPreciosPorProducto)])
        self.botonBorrarPP.place(x=190,y=10)

        def clickMenuActualPP(event):
            if len(self.listaMenuActualPP.selection())>0:
                idPP= self.listaMenuActualPP.selection()[0]
                self.menuIdPrecioPP.set(value=(self.listaMenuActualPP.item(idPP, "values")[0]))
                
        def clickMenuNuevoPP(event):
            if len(self.listaMenuNuevoPP.selection())>0:
                idPPN= self.listaMenuNuevoPP.selection()[0]
                self.productoIdPrecioPP.set(value=(self.listaMenuNuevoPP.item(idPPN, "values")[0]))
                
        self.listaMenuActualPP=ttk.Treeview(self.marcoMenuActualPP, columns=("menu_id","descripcion","precio_venta"),
                                    displaycolumns=("descripcion","precio_venta"))
        self.listaMenuActualPP.column("#0",width=0, stretch=NO) 
        self.listaMenuActualPP.column("descripcion",width=150)
        self.listaMenuActualPP.column("precio_venta",width=50, anchor=CENTER)
        self.listaMenuActualPP.pack()                                 
        self.listaMenuActualPP.place(width=260, height=220, x=10, y=50)
        self.listaMenuActualPP.bind("<<TreeviewSelect>>", clickMenuActualPP)
        
        self.listaMenuActualPP.heading("#0",text="")
        self.listaMenuActualPP.heading("descripcion",text="Descripcion")
        self.listaMenuActualPP.heading("precio_venta",text="Precio")

        self.scrollVertical=Scrollbar(self.marcoMenuActualPP, command=self.listaMenuActualPP.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVertical.place(width=15, height=220, x=275, y=50)                      #el scroll toma la dimencion del cuadro de texto
        self.listaMenuActualPP.config(yscrollcommand=self.scrollVertical.set)
        
        self.listaMenuNuevoPP=ttk.Treeview(self.marcoMenuNuevoPP, columns=("menu_id","descripcion","precio_venta"),
                                    displaycolumns=("descripcion","precio_venta"))
        self.listaMenuNuevoPP.column("#0",width=0, stretch=NO) 
        self.listaMenuNuevoPP.column("descripcion",width=150)
        self.listaMenuNuevoPP.column("precio_venta",width=50, anchor=CENTER)
        self.listaMenuNuevoPP.pack()                                 
        self.listaMenuNuevoPP.place(width=260, height=220, x=10, y=50)
        self.listaMenuNuevoPP.bind("<<TreeviewSelect>>", clickMenuNuevoPP)
        
        self.listaMenuNuevoPP.heading("#0",text="")
        self.listaMenuNuevoPP.heading("descripcion",text="Descripcion")
        self.listaMenuNuevoPP.heading("precio_venta",text="Precio")

        self.scrollVerticalPed=Scrollbar(self.marcoMenuNuevoPP, command=self.listaMenuNuevoPP.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVerticalPed.place(width=15, height=200, x=275, y=50)                      #el scroll toma la dimencion del cuadro de texto
        self.listaMenuNuevoPP.config(yscrollcommand=self.scrollVerticalPed.set)
        

        self.completarTabla(cursor,self.listaMenuActualPP,self.sqlMenuPP)



    '''#   ********************                Ventana Actualizacion Precios por Categoria                     ********************'''

    def preciosPorCategoria(self, cursor, vent, menu, usuario):
        self.anchoVentana = 640
        self.altoVentana = 480

        self.ventanaPreciosPorCategoria = Tk()
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)
        self.ventanaPreciosPorCategoria.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)
        + "+" + str(self.xventana) + "+" + str(self.yventana))                       
        self.ventanaPreciosPorCategoria.resizable(0,0)                                     
        self.ventanaPreciosPorCategoria.title("Actualizacion de Precios por Categorias")                                  
        self.ventanaPreciosPorCategoria.iconbitmap(self.icono)                            


        self.marcoSuperiorPreciosPorCategoria=LabelFrame(self.ventanaPreciosPorCategoria)
        self.marcoSuperiorPreciosPorCategoria.place(x=10, y=10, width=620, height=140)
        self.marcoMenuActual=LabelFrame(self.ventanaPreciosPorCategoria)
        self.marcoMenuActual.place(x=10, y=170, width=300, height=300)
        self.marcoMenuNuevo=LabelFrame(self.ventanaPreciosPorCategoria)
        self.marcoMenuNuevo.place(x=330, y=170, width=300, height=300)

        self.opcionModificacion=IntVar()
        self.sqlMenuPC = "SELECT menu_id,descripcion,precio_venta FROM menu WHERE activo = 1 ORDER BY descripcion ASC"

        self.aumentoPor=Radiobutton(self.marcoSuperiorPreciosPorCategoria, text="Aumentar: %", variable=self.opcionModificacion, value=1,
                                    command=lambda:[self.aumentoPorcentraje.config(state="normal"), self.opcionModificacion.set(1),
                                    self.rebajaPorcentaje.delete(0, "end"),self.rebajaPorcentaje.config(state="disable"),
                                    self.aumentoFijo.delete(0, "end"),self.aumentoFijo.config(state="disable"),
                                    self.rebajaFijo.delete(0, "end"),self.rebajaFijo.config(state="disable")])
        self.aumentoPor.place(x=10, y=10)
        
        self.rebajaPor=Radiobutton(self.marcoSuperiorPreciosPorCategoria, text="Rebajar: %", variable=self.opcionModificacion, value=2,
                                    command=lambda:[self.aumentoPorcentraje.delete(0, "end"),self.aumentoPorcentraje.config(state="disable"),
                                    self.rebajaPorcentaje.config(state="normal"), self.opcionModificacion.set(2),
                                    self.aumentoFijo.delete(0, "end"),self.aumentoFijo.config(state="disable"),
                                    self.rebajaFijo.delete(0, "end"),self.rebajaFijo.config(state="disable")])
        self.rebajaPor.place(x=200, y=10)
        
        self.aumentoFij=Radiobutton(self.marcoSuperiorPreciosPorCategoria, text="Aumentar: $", variable=self.opcionModificacion, value=3,
                                    command=lambda:[self.aumentoPorcentraje.delete(0, "end"),self.aumentoPorcentraje.config(state="disable"),
                                    self.rebajaPorcentaje.delete(0, "end"),self.rebajaPorcentaje.config(state="disable"),
                                    self.aumentoFijo.config(state="normal"), self.opcionModificacion.set(3),
                                    self.rebajaFijo.delete(0, "end"),self.rebajaFijo.config(state="disable")])
        self.aumentoFij.place(x=10, y=60)
        
        self.rebajaFij=Radiobutton(self.marcoSuperiorPreciosPorCategoria, text="Rebajar: $", variable=self.opcionModificacion, value=4,
                                    command=lambda:[self.aumentoPorcentraje.delete(0, "end"),self.aumentoPorcentraje.config(state="disable"),
                                    self.rebajaPorcentaje.delete(0, "end"),self.rebajaPorcentaje.config(state="disable"),
                                    self.aumentoFijo.delete(0, "end"),self.aumentoFijo.config(state="disable"), self.opcionModificacion.set(4),
                                    self.rebajaFijo.config(state="normal")])
        self.rebajaFij.place(x=200, y=60)
        
               
        self.textoAumentoPorcentraje = StringVar()
        self.aumentoPorcentraje = Entry(self.marcoSuperiorPreciosPorCategoria, width=10, textvariable=self.textoAumentoPorcentraje, state="disable")
        self.aumentoPorcentraje.place(x=110,y=10)
            
        self.textoRebajaPorcentaje = StringVar()
        self.rebajaPorcentaje = Entry(self.marcoSuperiorPreciosPorCategoria, width=10, textvariable=self.textoRebajaPorcentaje, state="disable")
        self.rebajaPorcentaje.place(x=285,y=10)
                    
        self.textoAumentoFijo = StringVar()
        self.aumentoFijo = Entry(self.marcoSuperiorPreciosPorCategoria, width=10, textvariable=self.textoAumentoFijo, state="disable")
        self.aumentoFijo.place(x=110,y=60)
        
        self.textoRebajaFijo = StringVar()
        self.rebajaFijo = Entry(self.marcoSuperiorPreciosPorCategoria, width=10, textvariable=self.textoRebajaFijo, state="disable")
        self.rebajaFijo.place(x=285,y=60)
        
        self.eticMenuActual = Label(self.marcoSuperiorPreciosPorCategoria, text="Actualizar Categoria")
        self.eticMenuActual.place(x=435,y=10)

        self.listaCategoriaProducto = self.completarListaCategoria(cursor)
        self.categoriaProducto = Combobox(self.marcoSuperiorPreciosPorCategoria, width=20, state="readonly", values=self.listaCategoriaProducto)
        self.categoriaProducto.place(x=420,y=35)

        self.eticMenuActual = Label(self.marcoMenuActual, text="Menu Actual", font="Arial 10 underline")
        self.eticMenuActual.place(x=0,y=0)

        self.eticMenuNuevo = Label(self.marcoMenuNuevo, text="Productos con Precio Actualizado", font="Arial 10 underline")
        self.eticMenuNuevo.place(x=0,y=0)

        self.botonBuscar = Button(self.marcoSuperiorPreciosPorCategoria, text="Actualizar Lista", width=15, height=1, command=lambda:[
                                    self.vaciarTabla(self.listaMenuNuevo),
                                    self.completarTablaProductosCatMenuActualizado(cursor,self.listaMenuNuevo,self.opcionModificacion.get(),
                                    self.categoriaProducto.get(), self.aumentoPorcentraje.get(),self.rebajaPorcentaje.get(),self.aumentoFijo.get(),
                                    self.rebajaFijo.get(),self.ventanaPreciosPorCategoria),
                                    self.vaciarTabla(self.listaMenuActual),
                                    self.completarTabla(cursor,self.listaMenuActual,("SELECT menu.menu_id,menu.descripcion,menu.precio_venta FROM menu "+
                                                        "INNER JOIN categorias_menu ON menu.id_categorias_menu=categorias_menu.categorias_menu_id "+
                                                        "WHERE menu.activo = 1 AND categorias_menu.activo = 1 AND categorias_menu.descripcion = '"+
                                                        self.categoriaProducto.get()+"' ORDER BY menu.descripcion ASC"))])
        self.botonBuscar.place(x=200,y=100)
        
        self.botonBuscar = Button(self.marcoSuperiorPreciosPorCategoria, text="Cambiar Precios", width=15, height=1, command=lambda:[
                                    self.cambiarPrecioCatMenuActualizado(cursor,self.listaMenuNuevo,self.opcionModificacion.get(),
                                    self.categoriaProducto.get(),self.aumentoPorcentraje.get(), self.rebajaPorcentaje.get(),
                                    self.aumentoFijo.get(),self.rebajaFijo.get(),self.ventanaPreciosPorCategoria,menu,usuario)])
        self.botonBuscar.place(x=350,y=100)

        self.botonSalir = Button(self.marcoSuperiorPreciosPorCategoria, text="Cancelar", width=10, height=1, command=lambda:self.ventanaPreciosPorCategoria.destroy())
        self.botonSalir.place(x=500,y=100)
         
        self.listaMenuActual=ttk.Treeview(self.marcoMenuActual, columns=("menu_id","descripcion","precio_venta"),
                                    displaycolumns=("descripcion","precio_venta"), cursor="plus")
        self.listaMenuActual.column("#0",width=0, stretch=NO) 
        self.listaMenuActual.column("descripcion",width=150)
        self.listaMenuActual.column("precio_venta",width=50, anchor=CENTER)
        self.listaMenuActual.pack()                                 
        self.listaMenuActual.place(width=260, height=220, x=10, y=50)
        self.listaMenuActual.bind("<<TreeviewSelect>>")
        
        self.listaMenuActual.heading("#0",text="")
        self.listaMenuActual.heading("descripcion",text="Descripcion")
        self.listaMenuActual.heading("precio_venta",text="Precio")

        self.scrollVertical=Scrollbar(self.marcoMenuActual, command=self.listaMenuActual.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVertical.place(width=15, height=220, x=275, y=50)                      #el scroll toma la dimencion del cuadro de texto
        self.listaMenuActual.config(yscrollcommand=self.scrollVertical.set)
        
        self.listaMenuNuevo=ttk.Treeview(self.marcoMenuNuevo, columns=("menu_id","descripcion","precio_venta"),
                                    displaycolumns=("descripcion","precio_venta"), cursor="x_cursor")
        self.listaMenuNuevo.column("#0",width=0, stretch=NO) 
        self.listaMenuNuevo.column("descripcion",width=150)
        self.listaMenuNuevo.column("precio_venta",width=50, anchor=CENTER)
        self.listaMenuNuevo.pack()                                 
        self.listaMenuNuevo.place(width=260, height=220, x=10, y=50)
        self.listaMenuNuevo.bind("<<TreeviewSelect>>")
        
        self.listaMenuNuevo.heading("#0",text="")
        self.listaMenuNuevo.heading("descripcion",text="Descripcion")
        self.listaMenuNuevo.heading("precio_venta",text="Precio")

        self.scrollVerticalPed=Scrollbar(self.marcoMenuNuevo, command=self.listaMenuNuevo.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVerticalPed.place(width=15, height=200, x=275, y=50)                      #el scroll toma la dimencion del cuadro de texto
        self.listaMenuNuevo.config(yscrollcommand=self.scrollVerticalPed.set)
        

        self.completarTabla(cursor,self.listaMenuActual,self.sqlMenuPC)

    
    '''#   ********************                Ventana Clientes                                  ********************'''

    def clientes(self, cursor, vent, cliente, usuario):
        self.anchoVentana = 640
        self.altoVentana = 480

        self.ventanaClientes = Tk()
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)
        self.ventanaClientes.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)
        + "+" + str(self.xventana) + "+" + str(self.yventana))                       
        self.ventanaClientes.resizable(0,0)                                     
        self.ventanaClientes.title("Clientes")                          
        self.ventanaClientes.iconbitmap(self.icono)                            


        self.marcoSuperiorClientes=LabelFrame(self.ventanaClientes)
        self.marcoSuperiorClientes.place(x=10, y=10, width=620, height=140)
        self.marcoClientes=Frame(self.ventanaClientes)
        self.marcoClientes.place(y=170, width=640, height=300)
            
        
        self.eticNombreClientes = Label(self.marcoSuperiorClientes, text="Nombre: ")
        self.eticNombreClientes.place(x=0,y=0)

        self.eticTelefonoClientes = Label(self.marcoSuperiorClientes, text="Telefono: ")
        self.eticTelefonoClientes.place(x=250,y=0)


        self.eticCalleClientes = Label(self.marcoSuperiorClientes, text="Calle: ")
        self.eticCalleClientes.place(x=0,y=50)

        self.eticAlturaClientes = Label(self.marcoSuperiorClientes, text="Altura: ")
        self.eticAlturaClientes.place(x=180,y=50)

        self.eticPisoClientes = Label(self.marcoSuperiorClientes, text="Piso: ")
        self.eticPisoClientes.place(x=290,y=50)

        self.eticDepartamentoClientes = Label(self.marcoSuperiorClientes, text="Departamento: ")
        self.eticDepartamentoClientes.place(x=380,y=50)

        self.eticBarrioClientes = Label(self.marcoSuperiorClientes, text="Barrio: ")
        self.eticBarrioClientes.place(x=0,y=100)
        
        self.textoNombreClientes = StringVar()
        self.nombreClientes = Entry(self.marcoSuperiorClientes, width=20, textvariable=self.textoNombreClientes)
        self.nombreClientes.place(x=55,y=0)
            
        self.textoTelefonoClientes = StringVar()
        self.telefonoClientes = Entry(self.marcoSuperiorClientes, width=15, textvariable=self.textoTelefonoClientes)
        self.telefonoClientes.place(x=310,y=0)
        
            
        self.textoCalleClientes = StringVar()
        self.calleClientes = Entry(self.marcoSuperiorClientes, width=15, textvariable=self.textoCalleClientes)
        self.calleClientes.place(x=40,y=50)
        
        self.textoAlturaClientes = StringVar()
        self.alturaClientes = Entry(self.marcoSuperiorClientes, width=6, textvariable=self.textoAlturaClientes)
        self.alturaClientes.place(x=225,y=50)
                
        self.textoPisoClientes = StringVar()
        self.pisoClientes = Entry(self.marcoSuperiorClientes, width=5, textvariable=self.textoPisoClientes)
        self.pisoClientes.place(x=325,y=50)
                
        self.textoDepartamentoClientes = StringVar()
        self.departamentoClientes = Entry(self.marcoSuperiorClientes, width=5, textvariable=self.textoDepartamentoClientes)
        self.departamentoClientes.place(x=470,y=50)

        self.textoBarrioClientes = StringVar()
        self.barrioClientes = Entry(self.marcoSuperiorClientes, width=15, textvariable=self.textoBarrioClientes)
        self.barrioClientes.place(x=45,y=100)

        
        self.clienteId=StringVar()
        self.sqlClientes = ("SELECT clientes.clientes_id,crea.usuario,modifica.usuario,clientes.telefono,clientes.nombre,clientes.calle,clientes.altura,"+
                            "clientes.piso,clientes.departamento,clientes.barrio FROM clientes INNER JOIN usuarios AS crea on "+
                            "clientes.id_usuario_crea=crea.usuarios_id INNER JOIN usuarios AS modifica ON clientes.id_usuario_modifica=modifica.usuarios_id"+
                            " WHERE clientes.activo = 1 ORDER BY clientes.nombre ASC")
        
        self.botonModificarClientes = Button(self.marcoSuperiorClientes, text="Modificar", width=10, height=1, command=lambda:[self.modificarCliente(
                            self.ventanaClientes, cliente, self.clienteId.get(), self.telefonoClientes.get(), self.nombreClientes.get(), self.calleClientes.get(),
                            self.alturaClientes.get(), self.pisoClientes.get(), self.departamentoClientes.get(), self.barrioClientes.get(), usuario) ,
                            self.vaciarTabla(self.listaClientes), self.completarTabla(cursor, self.listaClientes, self.sqlClientes)])
        self.botonModificarClientes.place(x=200,y=100)
        
        self.botonEliminarClientes = Button(self.marcoSuperiorClientes, text="Eliminar", width=10, height=1, command=lambda:[self.borrarCliente(cliente,
                            self.ventanaClientes, self.clienteId.get()), self.vaciarTabla(self.listaClientes),
                            self.completarTabla(cursor, self.listaClientes, self.sqlClientes)])
        self.botonEliminarClientes.place(x=300,y=100)
        
        self.botonGuardarClientes = Button(self.marcoSuperiorClientes, text="Guardar", width=10, height=1, command=lambda:[self.guardarCliente(cursor,
                            self.ventanaClientes, cliente, self.telefonoClientes.get(), self.nombreClientes.get(), self.calleClientes.get(),
                            self.alturaClientes.get(), self.pisoClientes.get(),self.departamentoClientes.get(), self.barrioClientes.get(), usuario),
                            self.vaciarTabla(self.listaClientes), self.completarTabla(cursor, self.listaClientes, self.sqlClientes)])
        self.botonGuardarClientes.place(x=400,y=100)

        self.botonSalirClientes = Button(self.marcoSuperiorClientes, text="Salir", width=10, height=1, command=lambda:self.ventanaClientes.destroy())
        self.botonSalirClientes.place(x=500,y=100)

        def clickClientes(event):
            if len(self.listaClientes.selection())>0:
                idClientes= self.listaClientes.selection()[0]
                self.clienteId.set(value=(self.listaClientes.item(idClientes, "values")[0]))
                self.telefonoClientes.delete(0, "end")
                self.telClientes=self.listaClientes.item(idClientes, "values")[3]
                self.telefonoClientes.insert(0, self.telClientes)
                self.nombreClientes.delete(0, "end")
                self.nomClientes=self.listaClientes.item(idClientes, "values")[4]
                self.nombreClientes.insert(0, self.nomClientes)
                self.calleClientes.delete(0, "end")
                self.callClientes=self.listaClientes.item(idClientes, "values")[5]
                self.calleClientes.insert(0, self.callClientes)
                self.alturaClientes.delete(0, "end")
                self.altClientes=self.listaClientes.item(idClientes, "values")[6]
                self.alturaClientes.insert(0, self.altClientes)
                self.pisoClientes.delete(0, "end")
                self.pisClientes=self.listaClientes.item(idClientes, "values")[7]
                self.pisoClientes.insert(0, self.pisClientes)
                self.departamentoClientes.delete(0, "end")
                self.depClientes=self.listaClientes.item(idClientes, "values")[8]
                self.departamentoClientes.insert(0, self.depClientes)
                self.barrioClientes.delete(0, "end")
                self.barClientes=self.listaClientes.item(idClientes, "values")[9]
                self.barrioClientes.insert(0, self.barClientes)
                

        self.listaClientes=ttk.Treeview(self.marcoClientes, columns=
                        ("clientes_id","crea","modifica","telefono","nombre","calle","altura",
                        "piso","departamento","barrio"),
                        displaycolumns=("nombre","telefono","calle","altura","piso","departamento","barrio",
                        "crea","modifica"))
        self.listaClientes.column("#0",width=0, stretch=NO) 
        self.listaClientes.column("telefono",width=100, anchor=CENTER) 
        self.listaClientes.column("nombre",width=150) 
        self.listaClientes.column("calle",width=150, anchor=CENTER) 
        self.listaClientes.column("altura",width=50, anchor=CENTER) 
        self.listaClientes.column("piso",width=50, anchor=CENTER) 
        self.listaClientes.column("departamento",width=50, anchor=CENTER)
        self.listaClientes.column("barrio",width=150, anchor=CENTER) 
        self.listaClientes.column("crea",width=100, anchor=CENTER) 
        self.listaClientes.column("modifica",width=100, anchor=CENTER) 
        self.listaClientes.pack()                                 
        self.listaClientes.place(width=600, height=270, x=10)
        self.listaClientes.bind("<<TreeviewSelect>>", clickClientes)
        
        self.listaClientes.heading("#0",text="")
        self.listaClientes.heading("telefono",text="Telefono")
        self.listaClientes.heading("nombre",text="Nombre")
        self.listaClientes.heading("calle",text="Calle")
        self.listaClientes.heading("altura",text="Altura")
        self.listaClientes.heading("piso",text="Piso")
        self.listaClientes.heading("departamento",text="Departamento")
        self.listaClientes.heading("barrio",text="Barrio")
        self.listaClientes.heading("crea",text="Creado Por")
        self.listaClientes.heading("modifica",text="Modificado Por")

        self.scrollVertical=Scrollbar(self.marcoClientes, command=self.listaClientes.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVertical.place(width=15, height=270, x=615)                      #el scroll toma la dimencion del cuadro de texto
        self.listaClientes.config(yscrollcommand=self.scrollVertical.set)
        
        scrollHotizontal=Scrollbar(self.marcoClientes, command=self.listaClientes.xview, orient=HORIZONTAL)
        scrollHotizontal.place(width=600, height=15, x=10, y=280)
        self.listaClientes.config(xscrollcommand=scrollHotizontal.set)

        self.completarTabla(cursor,self.listaClientes,self.sqlClientes)


    '''#   ********************                Ventana Usuarios                                  ********************'''

    def usuarios(self, cursor, vent, usuario):
        self.anchoVentana = 640
        self.altoVentana = 480

        self.ventanaUsuarios = Tk()
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)
        self.ventanaUsuarios.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)
        + "+" + str(self.xventana) + "+" + str(self.yventana))                       
        self.ventanaUsuarios.resizable(0,0)                                     
        self.ventanaUsuarios.title("Usuarios")                                  
        self.ventanaUsuarios.iconbitmap(self.icono)                            


        self.marcoSuperiorUsuarios=LabelFrame(self.ventanaUsuarios)
        self.marcoSuperiorUsuarios.place(x=10, y=10, width=620, height=190)
        self.marcoUsuarios=Frame(self.ventanaUsuarios)
        self.marcoUsuarios.place(y=220, width=640, height=250)
            
        
        self.eticUsuario = Label(self.marcoSuperiorUsuarios, text="Usuario: ")
        self.eticUsuario.place(x=0,y=1)

        self.eticContrasenia = Label(self.marcoSuperiorUsuarios, text="Contraseña: ")
        self.eticContrasenia.place(x=250,y=1)

        self.eticNombre = Label(self.marcoSuperiorUsuarios, text="Nombre: ")
        self.eticNombre.place(x=0,y=50)

        self.eticTelefono = Label(self.marcoSuperiorUsuarios, text="Telefono: ")
        self.eticTelefono.place(x=200,y=50)
        
        self.eticTelefono = Label(self.marcoSuperiorUsuarios, text="Mail: ")
        self.eticTelefono.place(x=435,y=50)

        self.eticCalle = Label(self.marcoSuperiorUsuarios, text="Calle: ")
        self.eticCalle.place(x=0,y=100)

        self.eticAltura = Label(self.marcoSuperiorUsuarios, text="Altura: ")
        self.eticAltura.place(x=180,y=100)

        self.eticPiso = Label(self.marcoSuperiorUsuarios, text="Piso: ")
        self.eticPiso.place(x=290,y=100)

        self.eticDepartamento = Label(self.marcoSuperiorUsuarios, text="Departamento: ")
        self.eticDepartamento.place(x=380,y=100)

        self.eticBarrio = Label(self.marcoSuperiorUsuarios, text="Barrio: ")
        self.eticBarrio.place(x=0,y=150)
        
        self.textoUsuario = StringVar()
        self.usuarioUsuario = Entry(self.marcoSuperiorUsuarios, width=20, textvariable=self.textoUsuario)
        self.usuarioUsuario.place(x=55,y=1)
            
        self.textoContrasenia = StringVar()
        self.contraseniaUsuario = Entry(self.marcoSuperiorUsuarios, width=15, textvariable=self.textoContrasenia, show="*")
        self.contraseniaUsuario.place(x=325,y=1)
        
        self.textoNombre = StringVar()
        self.nombreUsuario = Entry(self.marcoSuperiorUsuarios, width=20, textvariable=self.textoNombre)
        self.nombreUsuario.place(x=55,y=50)
            
        self.textoTelefono = StringVar()
        self.telefonoUsuario = Entry(self.marcoSuperiorUsuarios, width=15, textvariable=self.textoTelefono)
        self.telefonoUsuario.place(x=260,y=50)
                    
        self.textoMail = StringVar()
        self.mailUsuario = Entry(self.marcoSuperiorUsuarios, width=15, textvariable=self.textoMail)
        self.mailUsuario.place(x=470,y=50)
                    
        self.textoCalle = StringVar()
        self.calleUsuario = Entry(self.marcoSuperiorUsuarios, width=15, textvariable=self.textoCalle)
        self.calleUsuario.place(x=40,y=100)
        
        self.textoAltura = StringVar()
        self.alturaUsuario = Entry(self.marcoSuperiorUsuarios, width=6, textvariable=self.textoAltura)
        self.alturaUsuario.place(x=225,y=100)
                
        self.textoPiso = StringVar()
        self.pisoUsuario = Entry(self.marcoSuperiorUsuarios, width=5, textvariable=self.textoPiso)
        self.pisoUsuario.place(x=325,y=100)
                
        self.textoDepartamento = StringVar()
        self.departamentoUsuario = Entry(self.marcoSuperiorUsuarios, width=5, textvariable=self.textoDepartamento)
        self.departamentoUsuario.place(x=470,y=100)

        self.textoBarrio = StringVar()
        self.barrioUsuario = Entry(self.marcoSuperiorUsuarios, width=15, textvariable=self.textoBarrio)
        self.barrioUsuario.place(x=45,y=150)

        
        self.usuarioId=StringVar()
        self.sqlUsuarios = "SELECT * FROM usuarios WHERE activo = 1"
        
        self.botonModificar = Button(self.marcoSuperiorUsuarios, text="Modificar", width=10, height=1, command=lambda:[self.modificarUsuario(cursor,
                            self.ventanaUsuarios, usuario, self.usuarioId.get(), self.usuarioUsuario.get(), self.contraseniaUsuario.get(), self.nombreUsuario.get(),
                            self.telefonoUsuario.get(), self.mailUsuario.get(), self.calleUsuario.get(), self.alturaUsuario.get(), self.pisoUsuario.get(),
                            self.departamentoUsuario.get(), self.barrioUsuario.get()), self.vaciarTabla(self.listaUsuarios),
                            self.completarTabla(cursor, self.listaUsuarios, self.sqlUsuarios)])
        self.botonModificar.place(x=200,y=150)
        
        self.botonEliminar = Button(self.marcoSuperiorUsuarios, text="Eliminar", width=10, height=1, command=lambda:[self.borrarUsuario(usuario,
                            self.ventanaUsuarios, self.usuarioId.get()), self.vaciarTabla(self.listaUsuarios),
                            self.completarTabla(cursor, self.listaUsuarios, self.sqlUsuarios)])
        self.botonEliminar.place(x=300,y=150)
        
        self.botonGuardar = Button(self.marcoSuperiorUsuarios, text="Guardar", width=10, height=1, command=lambda:[self.guardarUsuario(cursor,
                            self.ventanaUsuarios, usuario, self.usuarioUsuario.get(), self.contraseniaUsuario.get(), self.nombreUsuario.get(),
                            self.telefonoUsuario.get(), self.mailUsuario.get(), self.calleUsuario.get(), self.alturaUsuario.get(), self.pisoUsuario.get(),
                            self.departamentoUsuario.get(), self.barrioUsuario.get()),self.vaciarTabla(self.listaUsuarios),
                            self.completarTabla(cursor, self.listaUsuarios, self.sqlUsuarios)])
        self.botonGuardar.place(x=400,y=150)

        self.botonSalir = Button(self.marcoSuperiorUsuarios, text="Salir", width=10, height=1, command=lambda:self.ventanaUsuarios.destroy())
        self.botonSalir.place(x=500,y=150)

        def clickUsuarios(event):
            if len(self.listaUsuarios.selection())>0:
                idUsuarios= self.listaUsuarios.selection()[0]
                self.usuarioId.set(value=(self.listaUsuarios.item(idUsuarios, "values")[0]))
                self.usuarioUsuario.delete(0, "end")
                self.usuUsuario=self.listaUsuarios.item(idUsuarios, "values")[1]
                self.usuarioUsuario.insert(0, self.usuUsuario)
                self.contraseniaUsuario.delete(0, "end")
                self.conUsuario=self.listaUsuarios.item(idUsuarios, "values")[2]
                self.contraseniaUsuario.insert(0, self.conUsuario)
                self.nombreUsuario.delete(0, "end")
                self.nomUsuario=self.listaUsuarios.item(idUsuarios, "values")[3]
                self.nombreUsuario.insert(0, self.nomUsuario)
                self.telefonoUsuario.delete(0, "end")
                self.telUsuario=self.listaUsuarios.item(idUsuarios, "values")[4]
                self.telefonoUsuario.insert(0, self.telUsuario)
                self.mailUsuario.delete(0, "end")
                self.maiUsuario=self.listaUsuarios.item(idUsuarios, "values")[5]
                self.mailUsuario.insert(0, self.maiUsuario)
                self.calleUsuario.delete(0, "end")
                self.callUsuario=self.listaUsuarios.item(idUsuarios, "values")[6]
                self.calleUsuario.insert(0, self.callUsuario)
                self.alturaUsuario.delete(0, "end")
                self.altUsuario=self.listaUsuarios.item(idUsuarios, "values")[7]
                self.alturaUsuario.insert(0, self.altUsuario)
                self.pisoUsuario.delete(0, "end")
                self.pisUsuario=self.listaUsuarios.item(idUsuarios, "values")[8]
                self.pisoUsuario.insert(0, self.pisUsuario)
                self.departamentoUsuario.delete(0, "end")
                self.depUsuario=self.listaUsuarios.item(idUsuarios, "values")[9]
                self.departamentoUsuario.insert(0, self.depUsuario)
                self.barrioUsuario.delete(0, "end")
                self.barUsuario=self.listaUsuarios.item(idUsuarios, "values")[10]
                self.barrioUsuario.insert(0, self.barUsuario)
                

        self.listaUsuarios=ttk.Treeview(self.marcoUsuarios, columns=
                        ("clientes_id","usuario","contrasenia","nombre","telefono","mail","calle","altura","piso",
                        "departamento","barrio"),displaycolumns=("usuario","nombre","telefono","mail","calle",
                        "altura","piso","departamento","barrio"))
        self.listaUsuarios.column("#0",width=0, stretch=NO) 
        self.listaUsuarios.column("usuario",width=100) 
        self.listaUsuarios.column("nombre",width=150, anchor=CENTER) 
        self.listaUsuarios.column("telefono",width=100, anchor=CENTER) 
        self.listaUsuarios.column("mail",width=100, anchor=CENTER) 
        self.listaUsuarios.column("calle",width=150, anchor=CENTER) 
        self.listaUsuarios.column("altura",width=50, anchor=CENTER) 
        self.listaUsuarios.column("piso",width=50, anchor=CENTER)
        self.listaUsuarios.column("departamento",width=50, anchor=CENTER)
        self.listaUsuarios.column("barrio",width=150, anchor=CENTER) 
        self.listaUsuarios.pack()                                 
        self.listaUsuarios.place(width=600, height=220, x=10)
        self.listaUsuarios.bind("<<TreeviewSelect>>", clickUsuarios)
        
        self.listaUsuarios.heading("#0",text="")
        self.listaUsuarios.heading("usuario",text="Usuario")
        self.listaUsuarios.heading("nombre",text="Nombre")
        self.listaUsuarios.heading("telefono",text="Telefono")
        self.listaUsuarios.heading("mail",text="Mail")
        self.listaUsuarios.heading("calle",text="Calle")
        self.listaUsuarios.heading("altura",text="Altura")
        self.listaUsuarios.heading("piso",text="Piso")
        self.listaUsuarios.heading("departamento",text="Departamento")
        self.listaUsuarios.heading("barrio",text="Barrio")

        self.scrollVertical=Scrollbar(self.marcoUsuarios, command=self.listaUsuarios.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVertical.place(width=15, height=220, x=615)                      #el scroll toma la dimencion del cuadro de texto
        self.listaUsuarios.config(yscrollcommand=self.scrollVertical.set)
        
        scrollHotizontal=Scrollbar(self.marcoUsuarios, command=self.listaUsuarios.xview, orient=HORIZONTAL)
        scrollHotizontal.place(width=600, height=15, x=10, y=230)
        self.listaUsuarios.config(xscrollcommand=scrollHotizontal.set)

        self.completarTabla(cursor,self.listaUsuarios,self.sqlUsuarios)


    '''#   ********************                Ventana Menu                                  ********************'''

    def menu(self, cursor, vent, menu, usuario):
        self.anchoVentana = 640
        self.altoVentana = 480

        self.ventanaMenu = Tk() 
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)
        self.ventanaMenu.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)
        + "+" + str(self.xventana) + "+" + str(self.yventana))                   
        self.ventanaMenu.resizable(0,0)                                     
        self.ventanaMenu.title("Menu")                                      
        self.ventanaMenu.iconbitmap(self.icono)                            


        self.marcoSuperiorMenu=LabelFrame(self.ventanaMenu)
        self.marcoSuperiorMenu.place(x=10, y=10, width=620, height=140)
        self.marcoMenu=Frame(self.ventanaMenu)
        self.marcoMenu.place(y=170, width=640, height=300)
            
        
        self.eticDescripcionMenu = Label(self.marcoSuperiorMenu, text="Descripcion: ")
        self.eticDescripcionMenu.place(x=10,y=10)

        self.eticPrecioVentaMenu = Label(self.marcoSuperiorMenu, text="Precio de Venta: ")
        self.eticPrecioVentaMenu.place(x=10,y=50)

        self.eticCategoriaMenu = Label(self.marcoSuperiorMenu, text="Categoria: ")
        self.eticCategoriaMenu.place(x=200,y=50)

        self.textoDescripcionMenu = StringVar()
        self.descripcionMenu = Entry(self.marcoSuperiorMenu, width=50, textvariable=self.textoDescripcionMenu)
        self.descripcionMenu.place(x=85,y=10)
            
        self.textoPrecioVentaMenu = StringVar()
        self.precioVentaMenu = Entry(self.marcoSuperiorMenu, width=10, textvariable=self.textoPrecioVentaMenu)
        self.precioVentaMenu.place(x=105,y=50)
            
        self.listaCategoriaMenu = self.completarListaCategoria(cursor)
        self.categoriaMenu = Combobox(self.marcoSuperiorMenu, width=10, state="readonly", values=self.listaCategoriaMenu)
        self.categoriaMenu.place(x=265,y=50)

        
        self.menuId=StringVar()
        self.sqlMenu= ("SELECT menu.menu_id,menu.descripcion,menu.precio_venta, crea.usuario AS crea, modifica.usuario AS modifica, "+
                        "categorias_menu.descripcion AS categoria,categorias_menu.categorias_menu_id FROM menu "+
                        "INNER JOIN categorias_menu ON menu.id_categorias_menu=categorias_menu.categorias_menu_id "+
                        "INNER JOIN usuarios AS crea ON menu.id_usuario_crea=crea.usuarios_id "+
                        "INNER JOIN usuarios AS modifica ON menu.id_usuario_modifica=modifica.usuarios_id WHERE menu.activo = 1 "+
                        "ORDER BY menu.descripcion ASC")

        self.botonBuscar = Button(self.marcoSuperiorMenu, text="Modificar", width=10, height=1, command=lambda:[self.modificarMenu(
                            self.ventanaMenu, menu, self.menuId.get(), self.descripcionMenu.get(), self.precioVentaMenu.get(),
                            (int(self.categoriaMenu.current())+1), usuario),
                            self.vaciarTabla(self.listaMenu), self.completarTabla(cursor, self.listaMenu, self.sqlMenu)])
        self.botonBuscar.place(x=200,y=100)
        
        self.botonBuscar = Button(self.marcoSuperiorMenu, text="Eliminar", width=10, height=1, command=lambda:[self.borrarMenu(menu,
                            self.ventanaMenu, self.menuId.get()), self.vaciarTabla(self.listaMenu), self.completarTabla(cursor,
                            self.listaMenu, self.sqlMenu)])
        self.botonBuscar.place(x=300,y=100)
        
        self.botonBuscar = Button(self.marcoSuperiorMenu, text="Guardar", width=10, height=1, command=lambda:[self.guardarMenu(cursor,
                            self.ventanaMenu, menu, self.descripcionMenu.get(), self.precioVentaMenu.get(), (int(self.categoriaMenu.current())+1),usuario),
                            self.vaciarTabla(self.listaMenu), self.completarTabla(cursor, self.listaMenu, self.sqlMenu)])
        self.botonBuscar.place(x=400,y=100)

        self.botonSalir = Button(self.marcoSuperiorMenu, text="Salir", width=10, height=1, command=lambda:self.ventanaMenu.destroy())
        self.botonSalir.place(x=500,y=100)


        def clickMenu(event):
            if len(self.listaMenu.selection())>0:
                idMenu= self.listaMenu.selection()[0]
                self.menuId.set(value=(self.listaMenu.item(idMenu, "values")[0]))
                self.descripcionMenu.delete(0, "end")
                self.desMenu=self.listaMenu.item(idMenu, "values")[1]
                self.descripcionMenu.insert(0, self.desMenu)
                self.precioVentaMenu.delete(0, "end")
                self.pvMenu=self.listaMenu.item(idMenu, "values")[2]
                self.precioVentaMenu.insert(0, self.pvMenu)
                self.categoriaMenu.current(int(self.listaMenu.item(idMenu, "values")[6])-1)
                                

        self.listaMenu=ttk.Treeview(self.marcoMenu, columns=("menu_id","descripcion","precio_venta","crea","modifica",
                                    "categoria","categorias_menu.categorias_menu_id"),
                                    displaycolumns=("descripcion","precio_venta","categoria","crea","modifica"))
        self.listaMenu.column("#0",width=0, stretch=NO) 
        self.listaMenu.column("descripcion",width=300)
        self.listaMenu.column("precio_venta",width=100, anchor=CENTER)
        self.listaMenu.column("categoria",width=100, anchor=CENTER)
        self.listaMenu.column("crea",width=100, anchor=CENTER)
        self.listaMenu.column("modifica",width=100, anchor=CENTER)
        self.listaMenu.pack()                                 
        self.listaMenu.place(width=600, height=270, x=10)
        self.listaMenu.bind("<<TreeviewSelect>>", clickMenu)
        
        self.listaMenu.heading("#0",text="")
        self.listaMenu.heading("descripcion",text="Descripcion")
        self.listaMenu.heading("precio_venta",text="Precio de Venta")
        self.listaMenu.heading("categoria",text="Categoria")
        self.listaMenu.heading("crea",text="Creado Por")
        self.listaMenu.heading("modifica",text="Modificado Por")

        self.scrollVertical=Scrollbar(self.marcoMenu, command=self.listaMenu.yview)
        self.scrollVertical.place(width=15, height=270, x=615)     
        self.listaMenu.config(yscrollcommand=self.scrollVertical.set)
        
        scrollHotizontal=Scrollbar(self.marcoMenu, command=self.listaMenu.xview, orient=HORIZONTAL)   
        scrollHotizontal.place(width=600, height=15, x=10, y=280)     
        self.listaMenu.config(xscrollcommand=scrollHotizontal.set)

        self.completarTabla(cursor,self.listaMenu,self.sqlMenu)

            
    '''#   ********************            Ventana Categorias Menu                            ********************'''

    def categoriasMenu(self, cursor, vent, categorias, usuario):
        self.anchoVentana = 640
        self.altoVentana = 480

        self.ventanaCategoriasMenu = Tk() 
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)
        self.ventanaCategoriasMenu.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)
        + "+" + str(self.xventana) + "+" + str(self.yventana))                   
        self.ventanaCategoriasMenu.resizable(0,0)                                     
        self.ventanaCategoriasMenu.title("Categorias")                                      
        self.ventanaCategoriasMenu.iconbitmap(self.icono)                            


        self.marcoSuperiorCategoriasMenu=LabelFrame(self.ventanaCategoriasMenu)
        self.marcoSuperiorCategoriasMenu.place(x=10, y=10, width=620, height=140)
        self.marcoCategoriasMenu=Frame(self.ventanaCategoriasMenu)
        self.marcoCategoriasMenu.place(y=170, width=640, height=300)
            
        
        self.eticDescripcion = Label(self.marcoSuperiorCategoriasMenu, text="Descripcion: ")
        self.eticDescripcion.place(x=100,y=50)

        self.textoDescripcion = StringVar()
        self.descripcion = Entry(self.marcoSuperiorCategoriasMenu, width=50, textvariable=self.textoDescripcion)
        self.descripcion.place(x=185,y=50)

        
        self.categoriasMenuId=StringVar()
        self.sqlCategoriasMenu= ("SELECT categorias_menu.categorias_menu_id,categorias_menu.descripcion, crea.usuario AS crea, "+
                        "modifica.usuario AS modifica FROM categorias_menu "+
                        "INNER JOIN usuarios AS crea ON categorias_menu.id_usuario_crea=crea.usuarios_id "+
                        "INNER JOIN usuarios AS modifica ON categorias_menu.id_usuario_modifica=modifica.usuarios_id "+
                        "WHERE categorias_menu.activo = 1 ORDER BY categorias_menu.descripcion ASC;")

        self.botonBuscarCategoriasMenu = Button(self.marcoSuperiorCategoriasMenu, text="Modificar", width=10, height=1, command=lambda:[self.modificarCategoriasMenu(
                            self.ventanaCategoriasMenu, categorias, self.categoriasMenuId.get(), self.descripcion.get(), usuario),
                            self.vaciarTabla(self.listaCategoriasMenu), self.completarTabla(cursor, self.listaCategoriasMenu, self.sqlCategoriasMenu)])
        self.botonBuscarCategoriasMenu.place(x=200,y=100)
        
        self.botonBuscarCategoriasMenu = Button(self.marcoSuperiorCategoriasMenu, text="Eliminar", width=10, height=1, command=lambda:[self.borrarCategoriasMenu(categorias,
                            self.ventanaCategoriasMenu, self.categoriasMenuId.get()), self.vaciarTabla(self.listaCategoriasMenu), self.completarTabla(cursor,
                            self.listaCategoriasMenu, self.sqlCategoriasMenu)])
        self.botonBuscarCategoriasMenu.place(x=300,y=100)
        
        self.botonBuscarCategoriasMenu = Button(self.marcoSuperiorCategoriasMenu, text="Guardar", width=10, height=1, command=lambda:[self.guardarCategoriasMenu(cursor,
                            self.ventanaCategoriasMenu, categorias, self.descripcion.get(), usuario),
                            self.vaciarTabla(self.listaCategoriasMenu), self.completarTabla(cursor, self.listaCategoriasMenu, self.sqlCategoriasMenu)])
        self.botonBuscarCategoriasMenu.place(x=400,y=100)

        self.botonSalirCategoriasMenu = Button(self.marcoSuperiorCategoriasMenu, text="Salir", width=10, height=1, command=lambda:self.ventanaCategoriasMenu.destroy())
        self.botonSalirCategoriasMenu.place(x=500,y=100)


        def clickCategoriasMenu(event):
            if len(self.listaCategoriasMenu.selection())>0:
                idCategoriasMenu= self.listaCategoriasMenu.selection()[0]
                self.categoriasMenuId.set(value=(self.listaCategoriasMenu.item(idCategoriasMenu, "values")[0]))
                self.descripcion.delete(0, "end")
                self.des=self.listaCategoriasMenu.item(idCategoriasMenu, "values")[1]
                self.descripcion.insert(0, self.des)
                

        self.listaCategoriasMenu=ttk.Treeview(self.marcoCategoriasMenu, columns=("categorias_menu_id","descripcion","crea","modifica"),
                                    displaycolumns=("descripcion","crea","modifica"))
        self.listaCategoriasMenu.column("#0",width=0, stretch=NO) 
        self.listaCategoriasMenu.column("descripcion",width=300)
        self.listaCategoriasMenu.column("crea",width=100, anchor=CENTER)
        self.listaCategoriasMenu.column("modifica",width=100, anchor=CENTER)
        self.listaCategoriasMenu.pack()                                 
        self.listaCategoriasMenu.place(width=600, height=270, x=10)
        self.listaCategoriasMenu.bind("<<TreeviewSelect>>", clickCategoriasMenu)
        
        self.listaCategoriasMenu.heading("#0",text="")
        self.listaCategoriasMenu.heading("descripcion",text="Descripcion")
        self.listaCategoriasMenu.heading("crea",text="Creado Por")
        self.listaCategoriasMenu.heading("modifica",text="Modificado Por")

        self.scrollVertical=Scrollbar(self.marcoCategoriasMenu, command=self.listaCategoriasMenu.yview)
        self.scrollVertical.place(width=15, height=270, x=615)     
        self.listaCategoriasMenu.config(yscrollcommand=self.scrollVertical.set)
        
        scrollHotizontal=Scrollbar(self.marcoCategoriasMenu, command=self.listaCategoriasMenu.xview, orient=HORIZONTAL)   
        scrollHotizontal.place(width=600, height=15, x=10, y=280)     
        self.listaCategoriasMenu.config(xscrollcommand=scrollHotizontal.set)

        self.completarTabla(cursor,self.listaCategoriasMenu,self.sqlCategoriasMenu)

            

    #   ***********************************************************************************************************
    #   ********************                Funciones                                          ********************
    #   ***********************************************************************************************************
            
    def vaciarTabla(self, tabla):
        filas= tabla.get_children()
        for i in filas:
            tabla.delete(i)

    def completarTablaPedidos(self, cursor, tabla):
                cursor.execute("SELECT pedidos.pedidos_id, clientes.calle, clientes.altura, clientes.piso, clientes.departamento, clientes.barrio,"+
                " pedidos.estado, pedidos.pago, pedidos.total, clientes.nombre, clientes.telefono, pedidos.fecha, crea.usuario AS crea, "+
                "modifica.usuario AS modifica FROM clientes INNER JOIN pedidos ON clientes.clientes_id=pedidos.id_cliente"+
                " INNER JOIN usuarios AS crea ON pedidos.id_usuario_crea=crea.usuarios_id INNER JOIN usuarios AS modifica"+
                " ON pedidos.id_usuario_modifica=modifica.usuarios_id WHERE fecha BETWEEN '" + datetime.today().strftime('%Y-%m-%d')
                +" 00:00:00' AND '" + datetime.today().strftime('%Y-%m-%d')+
                " 23:59:59' AND (estado ='Preparacion' OR estado ='En Camino') ORDER BY `pedidos`.`fecha` ASC")
                self.consultaCTP = cursor.fetchall()
                
                for i in self.consultaCTP:
                    tabla.insert("", END, i[0], values= i)

    def completarTablaDetallePedidos(self, cursor, tabla, pedidoID):
        cursor.execute("SELECT detalle_pedidos_id,cantidad,descripcion,precio_venta FROM detalle_pedidos "+
                        "INNER JOIN menu ON detalle_pedidos.id_menu=menu.menu_id WHERE id_pedido = "+ str(pedidoID))
        self.consultaCTDP = cursor.fetchall()

        for i in self.consultaCTDP:
            tabla.insert("", END, i[0], values= i)
         
    def completarTabla(self, cursor, tabla, consultaSql):
        cursor.execute(consultaSql)
        self.consultaCT = cursor.fetchall() 
                
        for i in self.consultaCT:
            tabla.insert("", END, i[0], values= i)

    def completarTablareportes(self, reporte, tabla, desdeAnio, desdeMes, desdeDia, hastaAnio, hastaMes, hastaDia, total, entregado, cancelado):
        self.consultaCTR = reporte.parcial(desdeAnio, desdeMes, desdeDia, hastaAnio, hastaMes, hastaDia)
        self.tot=IntVar()
        self.totEntregado=IntVar()
        self.totCancelado=IntVar()
       
        for i in self.consultaCTR:
            tabla.insert("", END, i[0], values= i)
            if i[4] == "Entregado":
                self.tot.set(self.tot.get()+i[3])
                self.totEntregado.set(self.totEntregado.get()+1)
            elif i[4] == "Cancelado":
                self.totCancelado.set(self.totCancelado.get()+1)
                
        total.config(text="$ "+str(self.tot.get()))
        entregado.config(text=self.totEntregado.get())
        cancelado.config(text=self.totCancelado.get())
        
    def completarTablaProductosMenu(self, cursor, tabla, listaPedido, textoTotal):
        self.totalCTPM=0
     
        cursor.execute("SELECT menu_id,descripcion,precio_venta FROM menu WHERE activo = 1 ORDER BY descripcion ASC")
        self.consultaCTPM = cursor.fetchall()
        
        for j in self.consultaCTPM:
            if listaPedido.get(j[0]):
                tabla.insert("", END, j[0], values= (listaPedido.get(j[0]),j[0],j[1],j[2]))
                self.totalCTPM +=(j[2]*listaPedido.get(j[0]))
       
        textoTotal.config(text=("$ "+str(self.totalCTPM)))
    
    def completarTablaProductosMenuActualizado(self, cursor, tabla, listaPedido, opcion, aumentoPorc,
                                                rebajaPorc, aumentoFij, rebajaFij, ventana):
        cursor.execute("SELECT menu_id,descripcion,precio_venta FROM menu WHERE activo = 1 ORDER BY descripcion ASC")
        self.consultaCTPMA = cursor.fetchall()
                        
        if opcion == 0:
            for j in self.consultaCTPMA:
                if listaPedido.count(j[0]):
                    tabla.insert("", END, j[0], values= (j[0],j[1],j[2]))         
        
        if opcion == 1:
            if aumentoPorc.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
                for j in self.consultaCTPMA:
                    if listaPedido.count(j[0]):
                        tabla.insert("", END, j[0], values= (j[0],j[1],(j[2] * float(aumentoPorc))/100+j[2]))
                       
        if opcion == 2:
            if rebajaPorc.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
                for j in self.consultaCTPMA:
                    if listaPedido.count(j[0]):
                        tabla.insert("", END, j[0], values= (j[0],j[1],j[2]-(j[2] * float(rebajaPorc))/100))
                   
        if opcion == 3:
            if aumentoFij.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
               for j in self.consultaCTPMA:
                    if listaPedido.count(j[0]):
                        tabla.insert("", END, j[0], values= (j[0],j[1],(float(aumentoFij)+j[2])))
                   
        if opcion == 4:
            if rebajaFij.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
               for j in self.consultaCTPMA:
                    if listaPedido.count(j[0]):
                        tabla.insert("", END, j[0], values= (j[0],j[1],(j[2] - float(rebajaFij))))
     
    def completarTablaProductosCatMenuActualizado(self, cursor, tabla, opcion, categoria, aumentoPorc,
                                                rebajaPorc, aumentoFij, rebajaFij, ventana):
        if categoria == "":
            return 0

        cursor.execute("SELECT menu.menu_id,menu.descripcion,menu.precio_venta FROM menu "+
                        "INNER JOIN categorias_menu ON menu.id_categorias_menu=categorias_menu.categorias_menu_id "+
                        "WHERE menu.activo = 1 AND categorias_menu.activo = 1 AND categorias_menu.descripcion = '"+categoria+"' "+
                        "ORDER BY menu.descripcion ASC")
        self.consultaCTPCMA = cursor.fetchall()

        if opcion == 0:
            for j in self.consultaCTPCMA:
                tabla.insert("", END, j[0], values= (j[0],j[1],j[2]))         
        
        if opcion == 1:
            if aumentoPorc.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
                for j in self.consultaCTPCMA:
                    tabla.insert("", END, j[0], values= (j[0],j[1],(j[2] * float(aumentoPorc))/100+j[2]))
                       
        if opcion == 2:
            if rebajaPorc.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
                for j in self.consultaCTPCMA:
                    tabla.insert("", END, j[0], values= (j[0],j[1],j[2]-(j[2] * float(rebajaPorc))/100))
                   
        if opcion == 3:
            if aumentoFij.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
               for j in self.consultaCTPCMA:
                    tabla.insert("", END, j[0], values= (j[0],j[1],(float(aumentoFij)+j[2])))
                   
        if opcion == 4:
            if rebajaFij.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
               for j in self.consultaCTPCMA:
                    tabla.insert("", END, j[0], values= (j[0],j[1],(j[2] - float(rebajaFij))))
                           
    def agregarProductoMenu(self, listaProducto, producto, ventana):
        self.cantidad=0

        if producto == 0:
            messagebox.showerror("Nuevo Pedido", "No selecciono ningun producto", parent=ventana)           # Si no se sellecciona producto no se genera
        else:
            if listaProducto.get(producto) == None:
                listaProducto.setdefault(producto,1)
            else:
                self.cantidad += listaProducto.get(producto)+1
                listaProducto.pop(producto)
                listaProducto.setdefault(producto,self.cantidad)

    def eliminarProductoMenu(self, listaProducto, producto):
        self.cantidad=0

        if len(listaProducto) == 0 or producto == 0:
            return 0

        if listaProducto.get(producto) == 1:
            listaProducto.pop(producto)
        else:
            self.cantidad += listaProducto.get(producto)-1
            listaProducto.pop(producto)
            listaProducto.setdefault(producto,self.cantidad)

    def agregarProductoMenuActualizado(self, listaProducto, producto, ventana):
       
        if producto == 0:
            messagebox.showerror("Precios del Menu", "No selecciono ningun producto", parent=ventana)           # Si no se sellecciona producto no se genera
        else:
            if listaProducto.count(producto) == 0:
               listaProducto.append(producto)
           
    def eliminarProductoMenuActualizado(self, listaProducto, producto):
        
        if listaProducto.count(producto) == 1:
            listaProducto.remove(producto)
    
    def cambiarPrecioMenuActualizado(self, cursor, tabla, listaPedido, opcion, aumentoPorc,
                                    rebajaPorc, aumentoFij, rebajaFij, ventana, menu, usuario):
        cursor.execute("SELECT menu_id,descripcion,precio_venta FROM menu WHERE activo = 1 ORDER BY descripcion ASC")
        self.consulta = cursor.fetchall()
         
        if opcion == 0:
            messagebox.showerror("Precios del Menu", "No Ingreso Ningun Valor", parent=ventana)           # Si no se sellecciona producto no se genera
                    
        if opcion == 1:
            if aumentoPorc.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
                for j in self.consulta:
                    if listaPedido.count(j[0]):
                        self.respuesta = messagebox.askyesno("Precios del Menu", "¿Modificar los Precios?", parent=ventana)
                        if self.respuesta == True:
                            menu.setPrecioVenta(j[0], (j[2] * float(aumentoPorc))/100+j[2], usuario)
                            ventana.destroy()
        if opcion == 2:
            if rebajaPorc.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
                for j in self.consulta:
                    if listaPedido.count(j[0]):
                        self.respuesta = messagebox.askyesno("Precios del Menu", "¿Modificar los Precios?", parent=ventana)
                        if self.respuesta == True:
                            menu.setPrecioVenta(j[0], j[2]-(j[2] * float(rebajaPorc))/100, usuario)
                            ventana.destroy()
                   
        if opcion == 3:
            if aumentoFij.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
               for j in self.consulta:
                    if listaPedido.count(j[0]):
                        self.respuesta = messagebox.askyesno("Precios del Menu", "¿Modificar los Precios?", parent=ventana)
                        if self.respuesta == True:
                            menu.setPrecioVenta(j[0], float(aumentoFij)+j[2], usuario)
                            ventana.destroy()
                        
        if opcion == 4:
            if rebajaFij.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
               for j in self.consulta:
                    if listaPedido.count(j[0]):
                        self.respuesta = messagebox.askyesno("Precios del Menu", "¿Modificar los Precios?", parent=ventana)
                        if self.respuesta == True:
                            menu.setPrecioVenta(j[0], j[2] - float(rebajaFij), usuario)
                            ventana.destroy()
      
    def cambiarPrecioCatMenuActualizado(self, cursor, tabla, opcion, categoria, aumentoPorc,
                                    rebajaPorc, aumentoFij, rebajaFij, ventana, menu, usuario):
        cursor.execute("SELECT menu.menu_id,menu.descripcion,menu.precio_venta FROM menu "+
                        "INNER JOIN categorias_menu ON menu.id_categorias_menu=categorias_menu.categorias_menu_id "+
                        "WHERE menu.activo = 1 AND categorias_menu.activo = 1 AND categorias_menu.descripcion = '"+categoria+"' "+
                        "ORDER BY menu.descripcion ASC")
        self.consulta = cursor.fetchall()
         
        if opcion == 0:
            messagebox.showerror("Precios del Menu", "No Ingreso Ningun Valor", parent=ventana)           # Si no se sellecciona producto no se genera
                    
        if opcion == 1:
            if aumentoPorc.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
                self.respuesta = messagebox.askyesno("Precios del Menu", "¿Modificar los Precios?", parent=ventana)
                if self.respuesta == True:
                    for j in self.consulta:
                        menu.setPrecioVenta(j[0], (j[2] * float(aumentoPorc))/100+j[2], usuario)
                        ventana.destroy()
        if opcion == 2:
            if rebajaPorc.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
                self.respuesta = messagebox.askyesno("Precios del Menu", "¿Modificar los Precios?", parent=ventana)
                if self.respuesta == True:
                    for j in self.consulta:
                        menu.setPrecioVenta(j[0], j[2]-(j[2] * float(rebajaPorc))/100, usuario)
                        ventana.destroy()
                   
        if opcion == 3:
            if aumentoFij.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
                self.respuesta = messagebox.askyesno("Precios del Menu", "¿Modificar los Precios?", parent=ventana)
                if self.respuesta == True:
                    for j in self.consulta:
                        menu.setPrecioVenta(j[0], float(aumentoFij)+j[2], usuario)
                        ventana.destroy()
                        
        if opcion == 4:
            if rebajaFij.isdigit() == False:
                messagebox.showerror("Precios del Menu", "Valor Invalido. Ingrese un numero", parent=ventana)           # Si no se sellecciona producto no se genera
            else:
                self.respuesta = messagebox.askyesno("Precios del Menu", "¿Modificar los Precios?", parent=ventana)
                if self.respuesta == True:
                    for j in self.consulta:
                        menu.setPrecioVenta(j[0], j[2] - float(rebajaFij), usuario)
                        ventana.destroy()
                        
    def agregarPedido(self, cursor, ventana, cliente, pedidos, telefono, nombre, calle, altura, piso, departamento, barrio, usuario, listaProductos):
        if nombre == "" or telefono == "" or calle == "" or altura == "":
            messagebox.showerror("Nuevo Pedido", "No se genero el pedido, informacion del cliente incompleta", parent=ventana)

        elif not listaProductos:
            messagebox.showerror("Nuevo Pedido", "No se genero el pedido, no agrego ningun producto", parent=ventana)

        else:
            
            cursor.execute("SELECT * FROM clientes WHERE telefono= '"+telefono+"' AND nombre= '"+nombre+"' AND calle= '"+
            calle+"' AND altura= '"+altura+"'")
            self.consulta = cursor.fetchall()
        
            if self.consulta == []:
                cliente.insertar(telefono, nombre, calle, altura, piso, departamento, barrio, str(usuario))
                cursor.execute("SELECT MAX(clientes_id) FROM clientes")         # busca el ultimo id generado
                self.consulta = cursor.fetchall()
                pedidos.insertar(self.consulta[0][0], "No", listaProductos, usuario)
                messagebox.showinfo("Nuevo Pedido", "Se genero un nuevo pedido y se agendo un nuevo cliente",
                                    parent=ventana)
            else:
                pedidos.insertar(self.consulta[0][0], "No", listaProductos, usuario)
                messagebox.showinfo("Nuevo Pedido", "Se genero un nuevo pedido", parent=ventana)
            
            self.imprimirTicket(cursor, telefono, nombre, calle, altura, piso, departamento, barrio, listaProductos)

    def imprimirTicket(self, cursor, telefono, nombre, calle, altura, piso, departamento, barrio, listaProductos):
        
        cursor.execute("SELECT pedidos_id, total, fecha FROM pedidos ORDER BY pedidos_id DESC LIMIT 1")
        self.consultaIT = cursor.fetchall()

        self.numeroTicket = str(self.consultaIT[0][0])
        self.ruta= "../Ticket/"+self.numeroTicket+".txt"

        self.archivo=open(self.ruta,"w") 
        self.archivo.write("**************************\n")
        self.archivo.write("*        PizzaYa         *\t\tTicket: "+self.numeroTicket+"\t\tFecha: "+str(self.consultaIT[0][2])+"\n")
        self.archivo.write("**************************\n\n")
        self.archivo.write("Nombre: "+nombre+"\t\t\tTelefono: "+telefono+"\n\n")
        self.archivo.write("Direccion: "+calle+" "+altura+"\tPiso: "+piso+" "+departamento+"\t\t\tBarrio: "+barrio+"\n")
        self.archivo.write("------------------------------------------------------------------------------------------\n")
        self.archivo.write("Cantidad\tDescripcion\t\t\t\t\t\t\tPrecio\n")
        self.archivo.write("------------------------------------------------------------------------------------------\n")
        
        for producto in listaProductos:
            cursor.execute("SELECT descripcion, precio_venta FROM menu WHERE menu_id= "+ str(producto[0]))
            self.consultaPro = cursor.fetchall()

            self.archivo.write(" "+str(producto[1])+"\t\t"+self.consultaPro[0][0]+"\t\t\t\t\t\t\t"+str(self.consultaPro[0][1])+"\n")

        self.archivo.write("------------------------------------------------------------------------------------------\n")
        self.archivo.write("\t\t\t\t\t\t\t\t\tTotal:  $"+str(self.consultaIT[0][1])+"\n")
        self.archivo.close()
        os.system("notepad.exe "+self.ruta)
        

    def busquedaCliente(self, cursor, ventana, tabla, telefono):
        cursor.execute("SELECT clientes_id,telefono,nombre,calle,altura,piso,departamento,barrio FROM clientes "+
                        "WHERE telefono= '"+telefono+"' AND activo=1")
        self.consulta = cursor.fetchall()

        if self.consulta == []:                                                          # Si no existe
            messagebox.showinfo("Buscar Cliente", "No Hay Ningun Cliente Asociado con el Numero Telefonico", parent=ventana)
        else:
            for i in self.consulta:
                tabla.insert("", END, i[0], values= i)

    def guardarCliente(self, cursor, ventana, cliente, telefono, nombre, calle, altura, piso, departamento, barrio, usuario):
        cursor.execute("SELECT * FROM clientes WHERE nombre= '"+nombre+              # Busca Existente
            "' AND telefono= '"+telefono+"' AND calle= '"+calle+"'")
        self.consulta = cursor.fetchall()
        
        if self.consulta == []:                                                          # Si no existe lo guarda
            if telefono =="" or nombre =="":                                        # Tiene que tener telefono y nombre
                messagebox.showerror("Cliente", "No se Pueden Agregar Clientes sin Nombre ni Telefono", parent=ventana)
            else:
                cliente.insertar(telefono, nombre, calle, altura, piso, departamento, barrio, str(usuario))
                messagebox.showinfo("Cliente", "Se Agrego el Cliente Exitosamente", parent=ventana)
        else:
            messagebox.showinfo("Cliente", "El Cliente Ya Existe", parent=ventana)

    def borrarCliente(self, cliente, ventana, id):
        self.respuesta = messagebox.askyesno("Cliente", "¿Eliminar Cliente?", parent=ventana)
        if self.respuesta == True:
            cliente.borrar(id)

    def modificarCliente(self, ventana, cliente, id, telefono, nombre, calle, altura, piso, departamento, barrio, usuario):
        self.respuesta = messagebox.askyesno("Cliente", "¿Modificar Cliente?", parent=ventana)
        if self.respuesta == True:
            cliente.setTelefono(id, telefono, usuario)
            cliente.setNombre(id, nombre, usuario)
            cliente.setCalle(id, calle, usuario)
            cliente.setAltura(id, altura, usuario)
            cliente.setPiso(id, piso, usuario)
            cliente.setDepartamento(id, departamento, usuario)
            cliente.setBarrio(id, barrio, usuario)

    def guardarUsuario(self, cursor, ventana, usuarios, usuario, contrasenia, nombre, telefono, mail,
                        calle, altura, piso, departamento, barrio):
        cursor.execute("SELECT * FROM usuarios WHERE usuario= '"+usuario+"'")              # Busca Existente
        self.consulta = cursor.fetchall()
        
        if self.consulta == []:                                                          # Si no existe lo guarda
            if usuario =="" or contrasenia =="":                                        # Tiene que tener telefono y nombre
                messagebox.showerror("Usuario", "Falta Completar Usuario o Contraseña", parent=ventana)
            else:
                usuarios.insertar(usuario, contrasenia, nombre, telefono, mail, calle, altura, piso, departamento, barrio)
                messagebox.showinfo("Usuario", "Se Agrego el Cliente Exitosamente", parent=ventana)
        else:
            messagebox.showinfo("Usuario", "El Usuario Ya Existe", parent=ventana)

    def borrarUsuario(self, usuario, ventana, id):
        self.respuesta = messagebox.askyesno("Usuario", "¿Eliminar Usuario?", parent=ventana)
        if self.respuesta == True:
            usuario.borrar(id)

    def modificarUsuario(self, cursor, ventana, usuario, id, usuar, contrasenia, nombre, telefono, mail, calle,
                        altura, piso, departamento, barrio):
        self.respuesta = messagebox.askyesno("Usuario", "¿Modificar Usuario?", parent=ventana)
        if self.respuesta == True:
            usuario.setUsuario(id, usuar)
            usuario.setContrasenia(id, contrasenia)
            usuario.setNombre(id, nombre)
            usuario.setTelefono(id, telefono)
            usuario.setMail(id, mail)
            usuario.setCalle(id, calle)
            usuario.setAltura(id, altura)
            usuario.setPiso(id, piso)
            usuario.setDepartamento(id, departamento)
            usuario.setBarrio(id, barrio)

    def guardarMenu(self, cursor, ventana, menu, descripcion, precioVenta, categoria, usuario):
        cursor.execute("SELECT * FROM menu WHERE descripcion= '"+descripcion+"'")
        self.consulta = cursor.fetchall()
        
        if self.consulta == []:                                                          # Si no existe lo guarda
            menu.insertar(descripcion, precioVenta, categoria, usuario)
            messagebox.showinfo("Menu", "Se Agrego el Producto Exitosamente", parent=ventana)
        else:
            messagebox.showinfo("Menu", "El Producto Ya Existe", parent=ventana)

    def borrarMenu(self, menu, ventana, id):
        self.respuesta = messagebox.askyesno("Menu", "¿Eliminar Producto?", parent=ventana)
        if self.respuesta == True:
            menu.borrar(id)
            
    def modificarMenu(self, ventana, menu, id, descripcion, precioVenta, categoria, usuario):
        self.respuesta = messagebox.askyesno("Menu", "¿Modificar Producto?", parent=ventana)
        if self.respuesta == True:
            menu.setDescripcion(id, descripcion, usuario)
            menu.setPrecioVenta(id, precioVenta, usuario)
            menu.setCategoria(id, categoria, usuario)
     
    def guardarCategoriasMenu(self, cursor, ventana, categorias, descripcion, usuario):
        cursor.execute("SELECT * FROM categorias_menu WHERE descripcion= '"+descripcion+"'")
        self.consulta = cursor.fetchall()
        
        if self.consulta == []:                                                          # Si no existe lo guarda
            categorias.insertar(descripcion, usuario)
            messagebox.showinfo("Categorias", "Se Agrego la Categorias Exitosamente", parent=ventana)
        else:
            messagebox.showinfo("Categorias", "La Categoria Ya Existe", parent=ventana)

    def borrarCategoriasMenu(self, categorias, ventana, id):
        self.respuesta = messagebox.askyesno("Categorias", "¿Eliminar Categoria?", parent=ventana)
        if self.respuesta == True:
            categorias.borrar(id)
            
    def modificarCategoriasMenu(self, ventana, categorias, id, descripcion, usuario):
        self.respuesta = messagebox.askyesno("Categorias", "¿Modificar Categoria?", parent=ventana)
        if self.respuesta == True:
            categorias.setDescripcion(id, descripcion, usuario)
     
    def completarListaCategoria(self, cursor):
        cursor.execute("SELECT * FROM categorias_menu WHERE activo = '1' "+
                        "ORDER BY descripcion ASC")
        self.consulta = cursor.fetchall()
        self.lista=[]

        for i in self.consulta:
            self.lista.append(i[3])
        return self.lista

    def cambiarEstadoPedido(self, pedidos, ventana, estado, id, usuario):
        if estado == 1:
            pedidos.setEstado(id, "Preparacion", usuario)
        if estado == 2:
            pedidos.setEstado(id, "En Camino", usuario)
        if estado == 3:
            self.respuesta = messagebox.askyesno("Pedido", "¿Modificar estado a Entregado?", parent=ventana)
            if self.respuesta == True:
                pedidos.setEstado(id, "Entregado", usuario)
        if estado == 4:
            self.respuesta = messagebox.askyesno("Pedido", "¿Modificar estado a Cancelado?", parent=ventana)
            if self.respuesta == True:
                pedidos.setEstado(id, "Cancelado", usuario)

        self.vaciarTabla(self.listaPedidos)
        self.completarTablaPedidos(self.cursorBD, self.listaPedidos)

    def cambiarEstadoPago(self, pedidos, pago, id, usuario):
        if pago == 0:
            pedidos.setPago(id, "No", usuario)
        if pago == 1:
            pedidos.setPago(id, "Si", usuario)
        
        self.vaciarTabla(self.listaPedidos)
        self.completarTablaPedidos(self.cursorBD, self.listaPedidos)

    def salir(self):                                                        #boton de salir con mensaje de confirmacion
        self.respuesta = messagebox.askquestion("Salir", "Desea Salir", parent=self.ventana)

        if self.respuesta == "yes":
            exit()
    
    def cerrarSesion(self):                                                        #boton de salir con mensaje de confirmacion
        self.respuesta = messagebox.askquestion("Cerrar Sesion", "Desea Cerrar Sesion", parent=self.ventana)

        if self.respuesta == "yes":
            self.ventana.destroy()
    
    def __del__(self):
        pass



def main():
    basDat = BaseDeDatos("localhost", "root", "", "pizzaya")
    cu = basDat.getCursor()
    ic = r"..\img\logo.ico"
    re = Reportes(basDat, cu)
    cl = Clientes(basDat, cu)
    ca = CategoriasMenuProductos(basDat, cu)
    me = MenuProductos(basDat, cu)
    pe = Pedidos(basDat, cu)
    us = Usuarios(basDat, cu)
    
    try:
        while True:
            log = Login(cu, ic)
                
            if log.estaOk() == 1:
                app = PizzaYa(log.getUsuario(), cu, ic, re, cl, ca, me, pe, us)

            else: 
                exit()
            del log
            del app

    except mysql.connector.errors.DatabaseError:
        messagebox.showerror("PizzaYa", "Sin Conexión con la Base de Datos.")

if __name__ == '__main__':
    main()
