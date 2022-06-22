from Conexion import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *                                                     #hay que instalarlo  pip install tkcalendar
from datetime import date
from datetime import datetime
from Pedidos import *
from Reportes import *
from Clientes import *
from MenuProductos import *
#from Login import *


class PizzaYa():
    def __init__(self):

        self.bd = BaseDeDatos("localhost", "root", "", "pizzaya")
        self.cursorBD = self.bd.getCursor()
        self.icono = r"..\img\logo.ico"
        self.reporte = Reportes(self.bd, self.cursorBD)
        self.cliente = Clientes(self.bd, self.cursorBD)
        self.men = MenuProductos(self.bd, self.cursorBD)
        self.pedidos= Pedidos(self.bd, self.cursorBD)



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
        self.ventana.title("PizzaYa")                                                        # Titulo de la ventana
        self.ventana.iconbitmap(self.icono)                                                       # Icono de la ventana
        self.barraMenu=Menu(self.ventana)                                                         # crea la barra de menu
        self.ventana.config(menu=self.barraMenu)                                                  # vincula la barra de menu con la ventana


        #   ********************                Barra de Menu                                        ********************

        self.opcionesMenu = Menu(self.barraMenu, tearoff=0)                            
        self.barraMenu.add_cascade(label="Opciones", menu=self.opcionesMenu)

        self.opcionesMenu.add_separator()                                         #linea separador
        self.opcionesMenu.add_command(label="Salir", command=lambda:self.salir())

        self.ventanaEmergenteCLientes = Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Clientes", command=lambda:self.clientes(self.cursorBD, self.ventana, self.cliente))

        self.ventanaEmergenteMenu = Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Menu", command=lambda:self.menu(self.cursorBD, self.ventana, self.men))

        ventanaEmergenteReporte = Menu(self.barraMenu, tearoff=0)
        self.barraMenu.add_cascade(label="Reporte", menu= ventanaEmergenteReporte)
        ventanaEmergenteReporte.add_command(label="Reporte Mensual", command=lambda:self.reporteMensual(self.reporte, self.ventana))
        ventanaEmergenteReporte.add_command(label="Reporte Parcial", command=lambda:self.reporteParcial(self.reporte, self.ventana))


        #   ********************                Ventana Principal Pedidos                          ********************


        self.pedidoId = StringVar()
        self.estado = IntVar()
        self.pago = IntVar()
        
        def click(event):
            id= self.listaPedidos.selection()[0]
            self.vaciarTabla(self.listaDetallePedido)
            if int(id)>0:
                self.pedidoId.set(value=(self.listaPedidos.item(id, "values")[8]))
                self.completarTablaDetallePedidos(self.cursorBD, self.listaDetallePedido, self.pedidoId.get())
                self.telefono.config(text="Telefono:  "+self.listaPedidos.item(id, "values")[1])
                self.nombre.config(text="Nombre:  "+self.listaPedidos.item(id, "values")[2])
                self.calle.config(text="Direccion:  "+self.listaPedidos.item(id, "values")[3])
                self.altura.config(text=self.listaPedidos.item(id, "values")[4])
                self.piso.config(text="Piso: "+self.listaPedidos.item(id, "values")[5])
                self.departamento.config(text="Depto: "+self.listaPedidos.item(id, "values")[6])
                self.barrio.config(text=self.listaPedidos.item(id, "values")[7])
                self.total.config(text=("$",self.listaPedidos.item(id, "values")[10]))
                self.hora.config(text=(self.listaPedidos.item(id, "values")[13])[11:16])
                if (self.listaPedidos.item(id, "values")[12]) == "Si":
                    self.pago.set(1)
                elif (self.listaPedidos.item(id, "values")[12]) == "No":
                    self.pago.set(0)
                if (self.listaPedidos.item(id, "values")[11]) == "Preparacion":
                    self.estado.set(1)
                elif (self.listaPedidos.item(id, "values")[11]) == "En Camino":
                    self.estado.set(2)
                elif (self.listaPedidos.item(id, "values")[11]) == "Entregado":
                    self.estado.set(3)
                elif (self.listaPedidos.item(id, "values")[11]) == "Cancelado":
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
                                    command=lambda:self.cambiarEstadoPedido(self.pedidos, self.ventana, self.estado.get(), self.pedidoId.get()))
        self.preparacion.place(x=620, y=50)

        self.enCamino=Radiobutton(self.marcoSuperior, text="En Camino", variable=self.estado, value=2,
                                    command=lambda:self.cambiarEstadoPedido(self.pedidos, self.ventana, self.estado.get(), self.pedidoId.get()))
        self.enCamino.place(x=620, y=75)

        self.entregado=Radiobutton(self.marcoSuperior, text="Entregado", variable=self.estado, value=3,
                                    command=lambda:self.cambiarEstadoPedido(self.pedidos, self.ventana, self.estado.get(), self.pedidoId.get()))
        self.entregado.place(x=620, y=100)

        self.cancelado=Radiobutton(self.marcoSuperior, text="Cancelado", variable=self.estado, value=4,
                                    command=lambda:self.cambiarEstadoPedido(self.pedidos, self.ventana, self.estado.get(), self.pedidoId.get()))
        self.cancelado.place(x=620, y=125)

        self.estaPago=Checkbutton(self.marcoSuperior, text="Esta Pago", variable=self.pago, onvalue=1, offvalue=0,
                                    command=lambda:self.cambiarEstadoPago(self.pedidos, self.pago.get(), self.pedidoId.get()))
        self.estaPago.place(x=620, y=165)


        self.botonNuevoPedido = Button(self.marcoSuperior, text="Nuevo Pedido", width=15, height=1, command=lambda:[self.nuevoPedido(self.cursorBD,
                                    self.ventana, self.cliente, self.pedidos)])
        self.botonNuevoPedido.place(x=620, y=200)


        #                    Lista Detalle de Pedidos                                   

        self.listaDetallePedido=ttk.Treeview(self.marcoSuperior, columns= ("detalle_pedidos_id","id_pedido","id_menu","cantidad","menu_id", "descripcion",
                                    "precio_venta", "visible"),
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

        self.listaPedidos=ttk.Treeview(self.marcoPedidos, columns= ("clientes_id","telefono","nombre","calle","altura","piso","departamento",
                                    "barrio","pedidos_id","id_clientes","total","estado","pago","fecha"),
                                    displaycolumns=("calle","altura","piso","departamento","barrio",
                                    "estado","pago","total","nombre","telefono"))
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

        self.scrollTexto=Scrollbar(self.marcoPedidos, command=self.listaPedidos.yview)        #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollTexto.place(width=15, height=self.altoVentana -200, x=self.anchoVentana -35)  #el scroll toma la dimencion del cuadro de texto
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


        self.marcoSuperior=Frame(self.ventanaReporteMensual)
        self.marcoSuperior.place(y=10, width=640, height=50)
        self.marcoReporte=Frame(self.ventanaReporteMensual)
        self.marcoReporte.place(y=70, width=640, height=400)
            

        self.botonSalir = Button(self.marcoSuperior, text="Salir", width=10, height=1,
                                command=lambda:self.ventanaReporteMensual.destroy())
        self.botonSalir.place(x=500, y=15)

        self.listaPedidos=ttk.Treeview(self.marcoReporte, columns= ("pedidos_id","id_clientes","total","estado","pago","fecha"),
                                    displaycolumns= ("id_clientes","total","estado","pago","fecha"))
        self.listaPedidos.column("#0",width=0, stretch=NO)
        self.listaPedidos.column("id_clientes",width=50, anchor=CENTER)
        self.listaPedidos.column("total",width=150, anchor=CENTER) 
        self.listaPedidos.column("estado",width=100, anchor=CENTER)
        self.listaPedidos.column("pago",width=50, anchor=CENTER) 
        self.listaPedidos.column("fecha",width=150, anchor=CENTER)
        self.listaPedidos.pack()
        self.listaPedidos.place(width=600, height=400, x=10)
        
        self.listaPedidos.heading("#0",text="")
        self.listaPedidos.heading("id_clientes",text="Cliente")
        self.listaPedidos.heading("total",text="Total")
        self.listaPedidos.heading("estado",text="Estado")
        self.listaPedidos.heading("pago",text="Pago")
        self.listaPedidos.heading("fecha",text="Fecha")

        consulta = reporte.mensual(date.today().year, date.today().month)
        for i in consulta:
            id = i[0]
            self.listaPedidos.insert("", END, id, values= i)
        
        self.scrollTexto=Scrollbar(self.marcoReporte, command=self.listaPedidos.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollTexto.place(width=15, height=400, x=615)                    #el scroll toma la dimencion del cuadro de texto
        self.listaPedidos.config(yscrollcommand=self.scrollTexto.set)
            

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


        self.marcoSuperior=Frame(self.ventanaReporteParcial)
        self.marcoSuperior.place(y=10, width=640, height=50)
        self.marcoReporte=Frame(self.ventanaReporteParcial)
        self.marcoReporte.place(y=70, width=640, height=400)
            

        self.textoDesde = Label(self.marcoSuperior, text="Desde: ")
        self.textoDesde.grid(row=0, column=0, padx=(10,0))

        self.textoHasta = Label(self.marcoSuperior, text="Hasta: ")
        self.textoHasta.grid(row=0, column=2, padx=(10,0))

        self.fechaDesde = DateEntry(self.marcoSuperior, date_pattern='dd/mm/yyyy')
        self.fechaDesde.grid(row=0, column=1)

        self.fechaHasta = DateEntry(self.marcoSuperior, date_pattern='dd/mm/yyyy')
        self.fechaHasta.grid(row=0, column=3)
        
        self.botonBuscar = Button(self.marcoSuperior, text="Buscar", width=10, height=1, command=lambda:[self.vaciarTabla(self.listaPedidos),
                self.completarTablareportes(reporte, self.listaPedidos,self.fechaDesde.get()[6:10], self.fechaDesde.get()[3:5], self.fechaDesde.get()[0:2],
                                            self.fechaHasta.get()[6:10], self.fechaHasta.get()[3:5], self.fechaHasta.get()[0:2])])
        self.botonBuscar.grid(row=0, column=4, padx=(130,0), pady=10)

        self.botonSalir = Button(self.marcoSuperior, text="Salir", width=10, height=1,
                                command=lambda:[self.ventanaReporteParcial.destroy()])
        self.botonSalir.grid(row=0, column=5, padx=(10), pady=10)

        self.listaPedidos=ttk.Treeview(self.marcoReporte, columns= ("pedidos_id","id_clientes","total","estado","pago","fecha"),
                                    displaycolumns=("id_clientes","total","estado","pago","fecha"))
        self.listaPedidos.column("#0",width=0, stretch=NO)
        self.listaPedidos.column("id_clientes",width=50, anchor=CENTER)
        self.listaPedidos.column("total",width=150, anchor=CENTER)
        self.listaPedidos.column("estado",width=100, anchor=CENTER)
        self.listaPedidos.column("pago",width=50, anchor=CENTER)
        self.listaPedidos.column("fecha",width=150, anchor=CENTER)
        self.listaPedidos.pack()                                 
        self.listaPedidos.place(width=600, height=400, x=10)
        
        self.listaPedidos.heading("#0",text="")
        self.listaPedidos.heading("id_clientes",text="Cliente")
        self.listaPedidos.heading("total",text="Total")
        self.listaPedidos.heading("estado",text="Estado")
        self.listaPedidos.heading("pago",text="Pago")
        self.listaPedidos.heading("fecha",text="Fecha")

        scrollTexto=Scrollbar(self.marcoReporte, command=self.listaPedidos.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        scrollTexto.place(width=15, height=400, x=615)                    #el scroll toma la dimencion del cuadro de texto
        self.listaPedidos.config(yscrollcommand=scrollTexto.set)



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


        self.marcoSuperior=LabelFrame(self.ventanabuscarCliente)
        self.marcoSuperior.place(x=10, y=10, width=620, height=140)
        self.marcoClientes=Frame(self.ventanabuscarCliente)
        self.marcoClientes.place(y=170, width=640, height=300)
            
        
        self.eticNombre = Label(self.marcoSuperior, text="Nombre: ")
        self.eticNombre.place(x=0,y=0)

        self.eticTelefono = Label(self.marcoSuperior, text="Telefono: ")
        self.eticTelefono.place(x=250,y=0)


        self.eticCalle = Label(self.marcoSuperior, text="Calle: ")
        self.eticCalle.place(x=0,y=50)

        self.eticAltura = Label(self.marcoSuperior, text="Altura: ")
        self.eticAltura.place(x=180,y=50)

        self.eticPiso = Label(self.marcoSuperior, text="Piso: ")
        self.eticPiso.place(x=290,y=50)

        self.eticDepartamento = Label(self.marcoSuperior, text="Departamento: ")
        self.eticDepartamento.place(x=380,y=50)

        self.eticBarrio = Label(self.marcoSuperior, text="Barrio: ")
        self.eticBarrio.place(x=0,y=100)
        
        self.nombre = Label(self.marcoSuperior, width=20)
        self.nombre.place(x=55,y=0)
            
        self.textoTelefono = StringVar()
        self.telefono = Entry(self.marcoSuperior, width=15, textvariable=self.textoTelefono)
        self.telefono.place(x=310,y=0)
        
            
        self.calle = Label(self.marcoSuperior, width=15)
        self.calle.place(x=40,y=50)
        
        self.altura = Label(self.marcoSuperior, width=6)
        self.altura.place(x=225,y=50)
                
        self.piso = Label(self.marcoSuperior, width=5)
        self.piso.place(x=325,y=50)
                
        self.departamento = Label(self.marcoSuperior, width=5)
        self.departamento.place(x=470,y=50)

        self.barrio = Label(self.marcoSuperior, width=15)
        self.barrio.place(x=45,y=100)

        
        self.clienteId=StringVar()
        
        
        self.botonBuscar = Button(self.marcoSuperior, text="Buscar", width=10, height=1, command=lambda:[ self.vaciarTabla(self.listaClientes),
                            self.busquedaCliente(cursor, self.ventanabuscarCliente, self.listaClientes,self.telefono.get())])
        self.botonBuscar.place(x=300,y=100)
        
        self.botonSeleccionar = Button(self.marcoSuperior, text="Seleccionar", width=10, height=1, command=lambda:[   #borra y completa los datos
                            telPedido.delete(0, "end"),nomPedido.delete(0, "end"),
                            telPedido.insert(0,self.telefono.get()),nomPedido.insert(0,self.nombre.cget("text")),
                            calPedido.delete(0, "end"),altPedido.delete(0, "end"),
                            calPedido.insert(0,self.calle.cget("text")),altPedido.insert(0,self.altura.cget("text")),
                            pisPedido.delete(0, "end"),depPedido.delete(0, "end"),
                            pisPedido.insert(0,self.piso.cget("text")),depPedido.insert(0,self.departamento.cget("text")),
                            barPedido.delete(0, "end"),barPedido.insert(0,self.barrio.cget("text")),
                            self.ventanabuscarCliente.destroy()]) 
                            
        self.botonSeleccionar.place(x=400,y=100)

        self.botonSalir = Button(self.marcoSuperior, text="Cancelar", width=10, height=1, command=lambda:self.ventanabuscarCliente.destroy())
        self.botonSalir.place(x=500,y=100)

        def click(event):
            id= self.listaClientes.selection()[0]
            if int(id)>0:
                self.clienteId.set(value=(self.listaClientes.item(id, "values")[0]))
                self.telefono.delete(0, "end")
                tel=self.listaClientes.item(id, "values")[1]
                self.telefono.insert(0, tel)
                self.nombre.config(text=self.listaClientes.item(id, "values")[2])
                self.calle.config(text=self.listaClientes.item(id, "values")[3])
                self.altura.config(text=self.listaClientes.item(id, "values")[4])
                self.piso.config(text=self.listaClientes.item(id, "values")[5])
                self.departamento.config(text=self.listaClientes.item(id, "values")[6])
                self.barrio.config(text=self.listaClientes.item(id, "values")[7])

        self.listaClientes=ttk.Treeview(self.marcoClientes, columns=
                        ("clientes_id","telefono","nombre","calle","altura","piso","departamento","barrio"),
                        displaycolumns=("telefono","nombre","calle","altura","piso","departamento","barrio"))
        self.listaClientes.column("#0",width=0, stretch=NO) 
        self.listaClientes.column("telefono",width=100, anchor=CENTER) 
        self.listaClientes.column("nombre",width=150, anchor=CENTER) 
        self.listaClientes.column("calle",width=150, anchor=CENTER) 
        self.listaClientes.column("altura",width=50, anchor=CENTER) 
        self.listaClientes.column("piso",width=50, anchor=CENTER) 
        self.listaClientes.column("departamento",width=50, anchor=CENTER)
        self.listaClientes.column("barrio",width=150, anchor=CENTER) 
        self.listaClientes.pack()                                 
        self.listaClientes.place(width=600, height=270, x=10)
        self.listaClientes.bind("<<TreeviewSelect>>", click)
        
        self.listaClientes.heading("#0",text="")
        self.listaClientes.heading("telefono",text="Telefono")
        self.listaClientes.heading("nombre",text="Nombre")
        self.listaClientes.heading("calle",text="Calle")
        self.listaClientes.heading("altura",text="Altura")
        self.listaClientes.heading("piso",text="Piso")
        self.listaClientes.heading("departamento",text="Departamento")
        self.listaClientes.heading("barrio",text="Barrio")

        self.scrollVertical=Scrollbar(self.marcoClientes, command=self.listaClientes.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVertical.place(width=15, height=270, x=615)                      #el scroll toma la dimencion del cuadro de texto
        self.listaClientes.config(yscrollcommand=self.scrollVertical.set)
        
        self.scrollHotizontal=Scrollbar(self.marcoClientes, command=self.listaClientes.xview, orient=HORIZONTAL)
        self.scrollHotizontal.place(width=600, height=15, x=10, y=280)
        self.listaClientes.config(xscrollcommand=self.scrollHotizontal.set)

        self.completarTabla(cursor,self.listaClientes, "clientes")


    '''#   ********************                Ventana Nuevo Pedido                              ********************'''

    def nuevoPedido(self, cursor, vent, cliente, pedidos):
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


        self.marcoSuperior=LabelFrame(self.ventanaNuevoPedido)
        self.marcoSuperior.place(x=10, y=10, width=620, height=140)
        self.marcoMenu=LabelFrame(self.ventanaNuevoPedido)
        self.marcoMenu.place(x=10, y=170, width=300, height=300)
        self.marcoPedido=LabelFrame(self.ventanaNuevoPedido)
        self.marcoPedido.place(x=330, y=170, width=300, height=300)

        self.menuId=IntVar()
        self.productoId=IntVar()
        self.listaProductos=dict()                                             # Listado de Productos seleccionados
        

        self.eticNombre = Label(self.marcoSuperior, text="Nombre: ")
        self.eticNombre.place(x=0,y=0)

        self.eticTelefono = Label(self.marcoSuperior, text="Telefono: ")
        self.eticTelefono.place(x=250,y=0)


        self.eticCalle = Label(self.marcoSuperior, text="Calle: ")
        self.eticCalle.place(x=0,y=50)

        self.eticAltura = Label(self.marcoSuperior, text="Altura: ")
        self.eticAltura.place(x=180,y=50)

        self.eticPiso = Label(self.marcoSuperior, text="Piso: ")
        self.eticPiso.place(x=290,y=50)

        self.eticDepartamento = Label(self.marcoSuperior, text="Departamento: ")
        self.eticDepartamento.place(x=380,y=50)

        self.eticBarrio = Label(self.marcoSuperior, text="Barrio: ")
        self.eticBarrio.place(x=0,y=100)
        
        textoNombre = StringVar()
        nombre = Entry(self.marcoSuperior, width=20, textvariable=textoNombre)
        nombre.place(x=55,y=0)
            
        textoTelefono = StringVar()
        telefono = Entry(self.marcoSuperior, width=15, textvariable=textoTelefono)
        telefono.place(x=310,y=0)
        
            
        textoCalle = StringVar()
        calle = Entry(self.marcoSuperior, width=15, textvariable=textoCalle)
        calle.place(x=40,y=50)
        
        textoAltura = StringVar()
        altura = Entry(self.marcoSuperior, width=6, textvariable=textoAltura)
        altura.place(x=225,y=50)
                
        textoPiso = StringVar()
        piso = Entry(self.marcoSuperior, width=5, textvariable=textoPiso)
        piso.place(x=325,y=50)
                
        textoDepartamento = StringVar()
        departamento = Entry(self.marcoSuperior, width=5, textvariable=textoDepartamento)
        departamento.place(x=470,y=50)

        textoBarrio = StringVar()
        barrio = Entry(self.marcoSuperior, width=15, textvariable=textoBarrio)
        barrio.place(x=45,y=100)

        self.eticMenu = Label(self.marcoMenu, text="Menu", font="Arial 10 underline")
        self.eticMenu.place(x=0,y=0)

        self.eticPedido = Label(self.marcoPedido, text="Pedido", font="Arial 10 underline")
        self.eticPedido.place(x=0,y=0)

        self.eticTotal = Label(self.marcoPedido, text="Total")
        self.eticTotal.place(x=10,y=250)

        self.textoTotal = Label(self.marcoPedido, text="$ 0")
        self.textoTotal.place(x=230,y=250)


        self.botonBuscar = Button(self.marcoSuperior, text="Buscar Cliente", width=15, height=1, command=lambda:[self.buscarCliente(cursor,
                            self.ventanaNuevoPedido, telefono, nombre, calle, altura, piso, departamento, barrio)])
        self.botonBuscar.place(x=200,y=100)
        
        self.botonBuscar = Button(self.marcoSuperior, text="Guardar Pedido", width=15, height=1, command=lambda:[self.agregarPedido(cursor,
                            self.ventanaNuevoPedido, cliente, pedidos, telefono.get(), nombre.get(), calle.get(), altura.get(),
                            piso.get(), departamento.get(), barrio.get(),self.listaProductos.items()),
                            self.vaciarTabla(self.listaPedidos),self.completarTablaPedidos(cursor, self.listaPedidos), self.ventanaNuevoPedido.destroy()])
        self.botonBuscar.place(x=350,y=100)

        self.botonSalir = Button(self.marcoSuperior, text="Cancelar", width=10, height=1, command=lambda:self.ventanaNuevoPedido.destroy())
        self.botonSalir.place(x=500,y=100)

        self.botonAgregar = Button(self.marcoMenu, text="Agregar", width=10, height=1, command=lambda:[
            self.agregarProductoMenu(self.listaProductos,self.menuId.get()),self.vaciarTabla(self.listaPedido),
                self.completarTablaProductosMenu(cursor,self.listaPedido, "menu", self.listaProductos.items(), self.textoTotal)])
        self.botonAgregar.place(x=190,y=10)

        self.botonBorrar = Button(self.marcoPedido, text="Borrar", width=10, height=1, command=lambda:[
            self.eliminarProductoMenu(self.listaProductos,self.productoId.get()),self.vaciarTabla(self.listaPedido),
                self.completarTablaProductosMenu(cursor,self.listaPedido, "menu", self.listaProductos.items(), self.textoTotal)])
        self.botonBorrar.place(x=190,y=10)

        def clickMenu(event):
            id= self.listaMenu.selection()[0]
            if int(id)>0:
                self.menuId.set(value=(self.listaMenu.item(id, "values")[0]))
                            
        def clickPedido(event):
            id= self.listaPedido.selection()[0]
            if int(id)>0:
                self.productoId.set(value=(self.listaMenu.item(id, "values")[0]))
                
        self.listaMenu=ttk.Treeview(self.marcoMenu, columns=("menu_id","descripcion","precio_venta"),
                                    displaycolumns=("descripcion","precio_venta"))
        self.listaMenu.column("#0",width=0, stretch=NO) 
        self.listaMenu.column("descripcion",width=150)
        self.listaMenu.column("precio_venta",width=50, anchor=CENTER)
        self.listaMenu.pack()                                 
        self.listaMenu.place(width=260, height=220, x=10, y=50)
        self.listaMenu.bind("<<TreeviewSelect>>", clickMenu)
        
        self.listaMenu.heading("#0",text="")
        self.listaMenu.heading("descripcion",text="Descripcion")
        self.listaMenu.heading("precio_venta",text="Precio")

        self.scrollVertical=Scrollbar(self.marcoMenu, command=self.listaMenu.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVertical.place(width=15, height=220, x=275, y=50)                      #el scroll toma la dimencion del cuadro de texto
        self.listaMenu.config(yscrollcommand=self.scrollVertical.set)
        
        self.listaPedido=ttk.Treeview(self.marcoPedido, columns=("unidades","menu_id","descripcion","precio_venta"),
                                    displaycolumns=("unidades","descripcion","precio_venta"))
        self.listaPedido.column("#0",width=0, stretch=NO) 
        self.listaPedido.column("unidades",width=20, anchor=CENTER)
        self.listaPedido.column("descripcion",width=150)
        self.listaPedido.column("precio_venta",width=50, anchor=CENTER)
        self.listaPedido.pack()                                 
        self.listaPedido.place(width=260, height=200, x=10, y=50)
        self.listaPedido.bind("<<TreeviewSelect>>", clickPedido)
        
        self.listaPedido.heading("#0",text="")
        self.listaPedido.heading("unidades",text="")
        self.listaPedido.heading("descripcion",text="Descripcion")
        self.listaPedido.heading("precio_venta",text="Precio")

        self.scrollVerticalPed=Scrollbar(self.marcoPedido, command=self.listaPedido.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVerticalPed.place(width=15, height=200, x=275, y=50)                      #el scroll toma la dimencion del cuadro de texto
        self.listaPedido.config(yscrollcommand=self.scrollVerticalPed.set)
        

        self.completarTablaMenu(cursor,self.listaMenu)


    '''#   ********************                Ventana Clientes                                  ********************'''

    def clientes(self, cursor, vent, cliente):
        self.anchoVentana = 640
        self.altoVentana = 480

        self.ventanaClientes = Tk()
        self.xventana = int(vent.winfo_screenwidth()/2 - self.anchoVentana/2)
        self.yventana = int(vent.winfo_screenheight()/2 - self.altoVentana/1.7)
        self.ventanaClientes.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)
        + "+" + str(self.xventana) + "+" + str(self.yventana))                       
        self.ventanaClientes.resizable(0,0)                                     
        self.ventanaClientes.title("clientes")                                  
        self.ventanaClientes.iconbitmap(self.icono)                            


        self.marcoSuperior=LabelFrame(self.ventanaClientes)
        self.marcoSuperior.place(x=10, y=10, width=620, height=140)
        self.marcoClientes=Frame(self.ventanaClientes)
        self.marcoClientes.place(y=170, width=640, height=300)
            
        
        self.eticNombre = Label(self.marcoSuperior, text="Nombre: ")
        self.eticNombre.place(x=0,y=0)

        self.eticTelefono = Label(self.marcoSuperior, text="Telefono: ")
        self.eticTelefono.place(x=250,y=0)


        self.eticCalle = Label(self.marcoSuperior, text="Calle: ")
        self.eticCalle.place(x=0,y=50)

        self.eticAltura = Label(self.marcoSuperior, text="Altura: ")
        self.eticAltura.place(x=180,y=50)

        self.eticPiso = Label(self.marcoSuperior, text="Piso: ")
        self.eticPiso.place(x=290,y=50)

        self.eticDepartamento = Label(self.marcoSuperior, text="Departamento: ")
        self.eticDepartamento.place(x=380,y=50)

        self.eticBarrio = Label(self.marcoSuperior, text="Barrio: ")
        self.eticBarrio.place(x=0,y=100)
        
        self.textoNombre = StringVar()
        self.nombre = Entry(self.marcoSuperior, width=20, textvariable=self.textoNombre)
        self.nombre.place(x=55,y=0)
            
        self.textoTelefono = StringVar()
        self.telefono = Entry(self.marcoSuperior, width=15, textvariable=self.textoTelefono)
        self.telefono.place(x=310,y=0)
        
            
        self.textoCalle = StringVar()
        self.calle = Entry(self.marcoSuperior, width=15, textvariable=self.textoCalle)
        self.calle.place(x=40,y=50)
        
        self.textoAltura = StringVar()
        self.altura = Entry(self.marcoSuperior, width=6, textvariable=self.textoAltura)
        self.altura.place(x=225,y=50)
                
        self.textoPiso = StringVar()
        self.piso = Entry(self.marcoSuperior, width=5, textvariable=self.textoPiso)
        self.piso.place(x=325,y=50)
                
        self.textoDepartamento = StringVar()
        self.departamento = Entry(self.marcoSuperior, width=5, textvariable=self.textoDepartamento)
        self.departamento.place(x=470,y=50)

        self.textoBarrio = StringVar()
        self.barrio = Entry(self.marcoSuperior, width=15, textvariable=self.textoBarrio)
        self.barrio.place(x=45,y=100)

        
        self.clienteId=StringVar()
        
        self.botonBuscar = Button(self.marcoSuperior, text="Modificar", width=10, height=1, command=lambda:[self.modificarCliente(cursor,
                            self.ventanaClientes, cliente, self.clienteId.get(), self.telefono.get(), self.nombre.get(), self.calle.get(),
                            self.altura.get(), self.piso.get(), self.departamento.get(), self.barrio.get()),
                            self.vaciarTabla(self.listaClientes), self.completarTabla(cursor, self.listaClientes, "clientes")])
        self.botonBuscar.place(x=200,y=100)
        
        self.botonBuscar = Button(self.marcoSuperior, text="Eliminar", width=10, height=1, command=lambda:[self.borrarCliente(cliente,
                            self.ventanaClientes, self.clienteId.get()), self.vaciarTabla(self.listaClientes),
                            self.completarTabla(cursor, self.listaClientes, "clientes")])
        self.botonBuscar.place(x=300,y=100)
        
        self.botonBuscar = Button(self.marcoSuperior, text="Guardar", width=10, height=1, command=lambda:[self.guardarCliente(cursor,
                            self.ventanaClientes, cliente, self.telefono.get(), self.nombre.get(), self.calle.get(),
                            self.altura.get(), self.piso.get(),self.departamento.get(), self.barrio.get()),
                            self.vaciarTabla(self.listaClientes), self.completarTabla(cursor, self.listaClientes, "clientes")])
        self.botonBuscar.place(x=400,y=100)

        self.botonSalir = Button(self.marcoSuperior, text="Salir", width=10, height=1, command=lambda:self.ventanaClientes.destroy())
        self.botonSalir.place(x=500,y=100)

        def click(event):
            id= self.listaClientes.selection()[0]
            if int(id)>0:
                self.clienteId.set(value=(self.listaClientes.item(id, "values")[0]))
                self.telefono.delete(0, "end")
                self.tel=self.listaClientes.item(id, "values")[1]
                self.telefono.insert(0, self.tel)
                self.nombre.delete(0, "end")
                self.nom=self.listaClientes.item(id, "values")[2]
                self.nombre.insert(0, self.nom)
                self.calle.delete(0, "end")
                self.call=self.listaClientes.item(id, "values")[3]
                self.calle.insert(0, self.call)
                self.altura.delete(0, "end")
                self.alt=self.listaClientes.item(id, "values")[4]
                self.altura.insert(0, self.alt)
                self.piso.delete(0, "end")
                self.pis=self.listaClientes.item(id, "values")[5]
                self.piso.insert(0, self.pis)
                self.departamento.delete(0, "end")
                self.dep=self.listaClientes.item(id, "values")[6]
                self.departamento.insert(0, self.dep)
                self.barrio.delete(0, "end")
                self.bar=self.listaClientes.item(id, "values")[7]
                self.barrio.insert(0, self.bar)
                

        self.listaClientes=ttk.Treeview(self.marcoClientes, columns=
                        ("clientes_id","telefono","nombre","calle","altura","piso","departamento","barrio"),
                        displaycolumns=("nombre","telefono","calle","altura","piso","departamento","barrio"))
        self.listaClientes.column("#0",width=0, stretch=NO) 
        self.listaClientes.column("telefono",width=100, anchor=CENTER) 
        self.listaClientes.column("nombre",width=150) 
        self.listaClientes.column("calle",width=150, anchor=CENTER) 
        self.listaClientes.column("altura",width=50, anchor=CENTER) 
        self.listaClientes.column("piso",width=50, anchor=CENTER) 
        self.listaClientes.column("departamento",width=50, anchor=CENTER)
        self.listaClientes.column("barrio",width=150, anchor=CENTER) 
        self.listaClientes.pack()                                 
        self.listaClientes.place(width=600, height=270, x=10)
        self.listaClientes.bind("<<TreeviewSelect>>", click)
        
        self.listaClientes.heading("#0",text="")
        self.listaClientes.heading("telefono",text="Telefono")
        self.listaClientes.heading("nombre",text="Nombre")
        self.listaClientes.heading("calle",text="Calle")
        self.listaClientes.heading("altura",text="Altura")
        self.listaClientes.heading("piso",text="Piso")
        self.listaClientes.heading("departamento",text="Departamento")
        self.listaClientes.heading("barrio",text="Barrio")

        self.scrollVertical=Scrollbar(self.marcoClientes, command=self.listaClientes.yview)   #scroll para el cuadro de texto yview posiciona el escrol verticalmente
        self.scrollVertical.place(width=15, height=270, x=615)                      #el scroll toma la dimencion del cuadro de texto
        self.listaClientes.config(yscrollcommand=self.scrollVertical.set)
        
        scrollHotizontal=Scrollbar(self.marcoClientes, command=self.listaClientes.xview, orient=HORIZONTAL)
        scrollHotizontal.place(width=600, height=15, x=10, y=280)
        self.listaClientes.config(xscrollcommand=scrollHotizontal.set)

        self.completarTabla(cursor,self.listaClientes, "clientes")


    '''#   ********************                Ventana Menu                                  ********************'''

    def menu(self, cursor, vent, menu):
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


        self.marcoSuperior=LabelFrame(self.ventanaMenu)
        self.marcoSuperior.place(x=10, y=10, width=620, height=140)
        self.marcoMenu=Frame(self.ventanaMenu)
        self.marcoMenu.place(y=170, width=640, height=300)
            
        
        self.eticDescripcion = Label(self.marcoSuperior, text="Descripcion: ")
        self.eticDescripcion.place(x=10,y=0)

        self.eticPrecioVenta = Label(self.marcoSuperior, text="Precio de Venta: ")
        self.eticPrecioVenta.place(x=10,y=50)

        self.textoDescripcion = StringVar()
        self.descripcion = Entry(self.marcoSuperior, width=50, textvariable=self.textoDescripcion)
        self.descripcion.place(x=85,y=0)
            
        self.textoPrecioVenta = StringVar()
        self.precioVenta = Entry(self.marcoSuperior, width=10, textvariable=self.textoPrecioVenta)
        self.precioVenta.place(x=105,y=50)

        
        self.menuId=StringVar()

        self.botonBuscar = Button(self.marcoSuperior, text="Modificar", width=10, height=1, command=lambda:[self.modificarMenu(
                            self.ventanaMenu, menu, self.menuId.get(), self.descripcion.get(), self.precioVenta.get()),
                            self.vaciarTabla(self.listaMenu), self.completarTablaMenu(cursor, self.listaMenu)])
        self.botonBuscar.place(x=200,y=100)
        
        self.botonBuscar = Button(self.marcoSuperior, text="Eliminar", width=10, height=1, command=lambda:[self.borrarMenu(menu,
                            self.ventanaMenu, self.menuId.get()), self.vaciarTabla(self.listaMenu), self.completarTablaMenu(cursor, self.listaMenu)])
        self.botonBuscar.place(x=300,y=100)
        
        self.botonBuscar = Button(self.marcoSuperior, text="Guardar", width=10, height=1, command=lambda:[self.guardarMenu(cursor,
                            self.ventanaMenu, menu, self.descripcion.get(), self.precioVenta.get()),
                            self.vaciarTabla(self.listaMenu), self.completarTablaMenu(cursor, self.listaMenu)])
        self.botonBuscar.place(x=400,y=100)

        self.botonSalir = Button(self.marcoSuperior, text="Salir", width=10, height=1, command=lambda:self.ventanaMenu.destroy())
        self.botonSalir.place(x=500,y=100)


        def click(event):
            id= self.listaMenu.selection()[0]
            if int(id)>0:
                self.menuId.set(value=(self.listaMenu.item(id, "values")[0]))
                self.descripcion.delete(0, "end")
                self.des=self.listaMenu.item(id, "values")[1]
                self.descripcion.insert(0, self.des)
                self.precioVenta.delete(0, "end")
                self.pv=self.listaMenu.item(id, "values")[2]
                self.precioVenta.insert(0, self.pv)
                

        self.listaMenu=ttk.Treeview(self.marcoMenu, columns=("menu_id","descripcion","precio_venta"),
                                    displaycolumns=("descripcion","precio_venta"))
        self.listaMenu.column("#0",width=0, stretch=NO) 
        self.listaMenu.column("descripcion",width=300)
        self.listaMenu.column("precio_venta",width=50, anchor=CENTER)
        self.listaMenu.pack()                                 
        self.listaMenu.place(width=600, height=270, x=10)
        self.listaMenu.bind("<<TreeviewSelect>>", click)
        
        self.listaMenu.heading("#0",text="")
        self.listaMenu.heading("descripcion",text="Descripcion")
        self.listaMenu.heading("precio_venta",text="Precio de Venta")

        self.scrollVertical=Scrollbar(self.marcoMenu, command=self.listaMenu.yview)
        self.scrollVertical.place(width=15, height=270, x=615)     
        self.listaMenu.config(yscrollcommand=self.scrollVertical.set)
        
        scrollHotizontal=Scrollbar(self.marcoMenu, command=self.listaMenu.xview, orient=HORIZONTAL)   
        scrollHotizontal.place(width=600, height=15, x=10, y=280)     
        self.listaMenu.config(xscrollcommand=scrollHotizontal.set)

        self.completarTablaMenu(cursor,self.listaMenu)

            

    #   ***********************************************************************************************************
    #   ********************                Funciones                                          ********************
    #   ***********************************************************************************************************
            
    def vaciarTabla(self, tabla):
        filas= tabla.get_children()
        for i in filas:
            tabla.delete(i)

    def completarTablaPedidos(self, cursor, tabla):
                cursor.execute("SELECT * FROM clientes INNER JOIN pedidos ON clientes.clientes_id=pedidos.id_cliente"+
                                " WHERE fecha BETWEEN '" + datetime.today().strftime('%Y-%m-%d')
                                    +" 00:00:00' AND '" + datetime.today().strftime('%Y-%m-%d')+" 23:59:59' AND (estado ='Preparacion' OR estado ='En Camino')")
                self.consulta = cursor.fetchall()
                
                for i in self.consulta:
                    id = i[8]
                    tabla.insert("", END, id, values= i)

    def completarTablaDetallePedidos(self, cursor, tabla, pedidoID):
        cursor.execute("SELECT * FROM detalle_pedidos INNER JOIN menu ON detalle_pedidos.id_menu=menu.menu_id WHERE id_pedido = "+
                            str(pedidoID))
        self.consulta = cursor.fetchall()

        for i in self.consulta:
            id = i[0]
            tabla.insert("", END, id, values= i)

    def completarTablareportes(self, reporte, tabla, desdeAnio, desdeMes, desdeDia, hastaAnio, hastaMes, hastaDia):
                
        self.consulta = reporte.parcial(desdeAnio, desdeMes, desdeDia, hastaAnio, hastaMes, hastaDia)
        for i in self.consulta:
            id = i[0]
            tabla.insert("", END, id, values= i)
    
    def completarTablaMenu(self, cursor, tabla):
        
        cursor.execute("SELECT * FROM menu WHERE visible = 1")                                 # Consulta SQL
        self.consulta = cursor.fetchall() 
                
        for i in self.consulta:
            id = i[0]
            tabla.insert("", END, id, values= i)
      
    def completarTabla(self, cursor, tabla, nombreTabla):
        
        cursor.execute("SELECT * FROM "+ nombreTabla)                                 # Consulta SQL
        self.consulta = cursor.fetchall() 
                
        for i in self.consulta:
            id = i[0]
            tabla.insert("", END, id, values= i)
    
    def completarTablaProductosMenu(self, cursor, tabla, nombreTabla, listaPedido, textoTotal):
        self.total=0
        for i in listaPedido:
            cursor.execute("SELECT * FROM "+nombreTabla+" WHERE menu_id= "+str(i[0]))                                 # Consulta SQL
            self.consulta = cursor.fetchall()
            
            for j in self.consulta:
                id = j[0]
                tabla.insert("", END, id, values= (i[1],j[0],j[1],j[2]))
                self.total +=(j[2]*i[1])
        textoTotal.config(text=("$ "+str(self.total)))

    def agregarProductoMenu(self, listaProducto, producto):
        self.cantidad=0

        if listaProducto.get(producto) == None:
            listaProducto.setdefault(producto,1)
        else:
            self.cantidad += listaProducto.get(producto)+1
            listaProducto.pop(producto)
            listaProducto.setdefault(producto,self.cantidad)

    def eliminarProductoMenu(self, listaProducto, producto):
        self.cantidad=0

        if listaProducto.get(producto) == 1:
            listaProducto.pop(producto)
        else:
            self.cantidad += listaProducto.get(producto)-1
            listaProducto.pop(producto)
            listaProducto.setdefault(producto,self.cantidad)

    def agregarPedido(self, cursor, ventana, cliente, pedidos, telefono, nombre, calle, altura, piso, departamento, barrio, listaProductos):
        if nombre == "" or telefono == "" or calle == "" or altura == "":
            messagebox.showerror("Nuevo Pedido", "No se genero el pedido, informacion del cliente incompleta", parent=ventana)
            
        else:
            cursor.execute("SELECT * FROM clientes WHERE telefono= '"+telefono+"' AND nombre= '"+nombre+"' AND calle= '"+
            calle+"' AND altura= '"+altura+"'")
            self.consulta = cursor.fetchall()
        
            if self.consulta == []:
                cliente.insertar(telefono, nombre, calle, altura, piso, departamento, barrio)
                cursor.execute("SELECT MAX(clientes_id) FROM clientes")         # busca el ultimo id generado
                self.consulta = cursor.fetchall()
                pedidos.insertar(self.consulta[0][0], "No", listaProductos)
                messagebox.showinfo("Nuevo Pedido", "Se genero un nuevo pedido y se agendo un nuevo cliente",
                                    parent=ventana)
            else:
                pedidos.insertar(self.consulta[0][0], "No", listaProductos)
                messagebox.showinfo("Nuevo Pedido", "Se genero un nuevo pedido", parent=ventana)

    def busquedaCliente(self, cursor, ventana, tabla, telefono):
        cursor.execute("SELECT * FROM clientes WHERE telefono= "+telefono)
        self.consulta = cursor.fetchall()
        
        if self.consulta == []:                                                          # Si no existe
            messagebox.showinfo("Buscar Cliente", "No Hay Ningun Cliente Asociado con el Numero Telefonico", parent=ventana)
        else:
            for i in self.consulta:
                id = i[0]
                tabla.insert("", END, id, values= i)

    def guardarCliente(self, cursor, ventana, cliente, telefono, nombre, calle, altura, piso, departamento, barrio):
        cursor.execute("SELECT * FROM clientes WHERE nombre= '"+nombre+              # Busca Existente
            "' AND telefono= '"+telefono+"' AND calle= '"+calle+"'")
        self.consulta = cursor.fetchall()
        
        if self.consulta == []:                                                          # Si no existe lo guarda
            if telefono =="" or nombre =="":                                        # Tiene que tener telefono y nombre
                messagebox.showerror("Cliente", "No se Pueden Agregar Clientes sin Nombre ni Telefono", parent=ventana)
            else:
                cliente.insertar(telefono, nombre, calle, altura, piso, departamento, barrio)
                messagebox.showinfo("Cliente", "Se Agrego el Cliente Exitosamente", parent=ventana)
        else:
            messagebox.showinfo("Cliente", "El Cliente Ya Existe", parent=ventana)

    def borrarCliente(self, cliente, ventana, id):
        self.respuesta = messagebox.askyesno("Cliente", "¿Eliminar Cliente?", parent=ventana)
        if self.respuesta == True:
            print(id)
            cliente.borrar(id)

    def modificarCliente(self, cursor, ventana, cliente, id, telefono, nombre, calle, altura, piso, departamento, barrio):
        self.respuesta = messagebox.askyesno("Cliente", "¿Modificar Cliente?", parent=ventana)
        if self.respuesta == True:
            cliente.setTelefono(id, telefono)
            cliente.setNombre(id, nombre)
            cliente.setCalle(id, calle)
            cliente.setAltura(id, altura)
            cliente.setPiso(id, piso)
            cliente.setDepartamento(id, departamento)
            cliente.setBarrio(id, barrio)

    def guardarMenu(self, cursor, ventana, menu, descripcion, precioVenta):
        cursor.execute("SELECT * FROM menu WHERE descripcion= '"+descripcion+"'")
        self.consulta = cursor.fetchall()
        
        if self.consulta == []:                                                          # Si no existe lo guarda
            menu.insertar(descripcion, precioVenta)
            messagebox.showinfo("Menu", "Se Agrego el Producto Exitosamente", parent=ventana)
        else:
            messagebox.showinfo("Menu", "El Producto Ya Existe", parent=ventana)

    def borrarMenu(self, menu, ventana, id):
        self.respuesta = messagebox.askyesno("Menu", "¿Eliminar Producto?", parent=ventana)
        if self.respuesta == True:
            menu.borrar(id)
            
    def modificarMenu(self, ventana, menu, id, descripcion, precioVenta):
        self.respuesta = messagebox.askyesno("Menu", "¿Modificar Producto?", parent=ventana)
        if self.respuesta == True:
            menu.setDescripcion(id, descripcion)
            menu.setPrecioVenta(id, precioVenta)

    def cambiarEstadoPedido(self, pedidos, ventana, estado, id):
        if estado == 1:
            pedidos.setEstado(id, "Preparacion")
        if estado == 2:
            pedidos.setEstado(id, "En Camino")
        if estado == 3:
            self.respuesta = messagebox.askyesno("Pedido", "¿Modificar estado a Entregado?", parent=ventana)
            if self.respuesta == True:
                pedidos.setEstado(id, "Entregado")
        if estado == 4:
            self.respuesta = messagebox.askyesno("Pedido", "¿Modificar estado a Cancelado?", parent=ventana)
            if self.respuesta == True:
                pedidos.setEstado(id, "Cancelado")

        self.vaciarTabla(self.listaPedidos)
        self.completarTablaPedidos(self.cursorBD, self.listaPedidos)

    def cambiarEstadoPago(self, pedidos, pago, id):
        if pago == 0:
            pedidos.setPago(id, "No")
        if pago == 1:
            pedidos.setPago(id, "Si")
        
        self.vaciarTabla(self.listaPedidos)
        self.completarTablaPedidos(self.cursorBD, self.listaPedidos)
    
    def salir(self):                                                        #boton de salir con mensaje de confirmacion
        self.espuesta = messagebox.askquestion("Salir", "Desea Salir", parent=self.ventana)

        if self.respuesta == "yes":
            self.ventana.destroy()



def main():
    mi_app = PizzaYa()
    return(0)

if __name__ == '__main__':
    main()