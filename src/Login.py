from Conexion import *
from tkinter import *

class Login:
    
    def __init__(self, cur, ico):

        self.cursor = cur
        self.icono = ico
        
        '''#   ********************                Ventana Login                                 ********************'''
        self.anchoVentana = 420
        self.altoVentana = 210

        self.ventanaLogin = Tk() 
        self.xventana = int(self.ventanaLogin.winfo_screenwidth()/2 - self.anchoVentana/2)
        self.yventana = int(self.ventanaLogin.winfo_screenheight()/2 - self.altoVentana/1.7)
        self.ventanaLogin.geometry(str(self.anchoVentana) + "x" + str(self.altoVentana)
        + "+" + str(self.xventana) + "+" + str(self.yventana))                   
        self.ventanaLogin.resizable(0,0)                                     
        self.ventanaLogin.title("Login")                                      
        self.ventanaLogin.iconbitmap(self.icono)                            

        self.usuarioId = IntVar(value=0)
        self.accesoOk = IntVar(value=0)

        self.marco=LabelFrame(self.ventanaLogin)
        self.marco.place(x=10, y=10, width=400, height=190)
            
        
        self.eticUsuario = Label(self.marco, text="Usuario: ")
        self.eticUsuario.place(x=80,y=10)

        self.eticCont = Label(self.marco, text="Contraseña: ")
        self.eticCont.place(x=80,y=50)

        self.contador = Label(self.marco)
        self.contador.place(x=60,y=100)

        self.textoUsuario = StringVar()
        self.usuario = Entry(self.marco, width=25, textvariable=self.textoUsuario)
        self.usuario.place(x=165,y=10)
        self.usuario.focus_set()
            
        self.textoCont = StringVar()
        self.cont = Entry(self.marco, width=25, textvariable=self.textoCont, show="*")
        self.cont.place(x=165,y=50)

        self.intentos = IntVar(value=3)

        self.botonAceptar = Button(self.marco, text="Aceptar", width=10, height=1, command=lambda:[self.verificarUsuario(self.cursor,
                            self.ventanaLogin, self.usuario.get(), self.cont.get(), self.intentos, self.accesoOk, self.contador,
                            self.usuarioId),
                            self.usuario.delete(0, "end"), self.cont.delete(0, "end")])
        self.botonAceptar.place(x=80,y=150)

        self.botonCancelar = Button(self.marco, text="Cancelar", width=10, height=1, command=lambda:self.ventanaLogin.destroy())
        self.botonCancelar.place(x=240,y=150)


        def teclaEnterUs(event):
            self.cont.focus_set()


        def teclaEnterCont(event):
            self.verificarUsuario(self.cursor, self.ventanaLogin, self.usuario.get(), self.cont.get(),
                                    self.intentos, self.accesoOk, self.contador, self.usuarioId)
            self.usuario.delete(0, "end")
            self.cont.delete(0, "end")
            self.usuario.focus_set()

        self.usuario.bind("<Return>", teclaEnterUs)
        self.cont.bind("<Return>", teclaEnterCont)


        self.ventanaLogin.mainloop()                      #loop de la ventana esperando accion del usuario

    
    def verificarUsuario(self, cursor, ventana, usuario, contrasenia, intentos, acceso, texto, usId):
        cursor.execute("SELECT * FROM usuarios WHERE usuario= '"+usuario+"' AND contrasenia='"+contrasenia+"'")
        self.consulta = cursor.fetchall()

        intentos.set(intentos.get() - 1)        
        texto.configure(text="Usuario o contraseña incorrecto. Quedan " +str(intentos.get())+ " intentos")
        
        if intentos.get() <= 0:
            exit()

        if self.consulta != []:
            acceso.set(1)
            usId.set(int(self.consulta[0][0]))
            ventana.destroy()
    
    def estaOk(self):
        return self.accesoOk.get()

    def getUsuario(self):
        return self.usuarioId.get()

    def __del__(self):
        pass        