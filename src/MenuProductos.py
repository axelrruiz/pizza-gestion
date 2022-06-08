class MenuProductos:
    
    def __init__(self, baseDeDatos, cursor):                                            # Constructor
        self.bD = baseDeDatos                                                           # Recibe BD para usar commit()
        self.miCursor = cursor                                                          # Recibe un cursor de BD

    def borrar(self, codigo):
        self.miCursor.execute("UPDATE menu SET visible = 0 WHERE menu_id = " + str(codigo)) # Comando SQL
        self.bD.connection.commit()                                                     # Confirma cambios en BD

    def insertar(self, descripcion, precioDeVenta):

        val = (descripcion, precioDeVenta)

        self.miCursor.execute(
            "INSERT INTO menu (descripcion, precio_venta, visible) VALUES (%s,%s,1)", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def imprimir(self):
        self.miCursor.execute("SELECT * FROM menu")                                     # Consulta SQL
        menus = self.miCursor.fetchall()                                                # Devuelve una tupla con las filas de la consulta
        
        for i in menus:
            print("Codigo: {}\tDescripcion: {}\tPrecio de Venta: {}\tVisible: {}".format
            (i[0], i[1], i[2], i[3]))
    
    def setDescripcion(self, codigo, descripcion):
        val = (str(descripcion), str(codigo))
        self.miCursor.execute("UPDATE menu SET descripcion = %s WHERE menu_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setPrecioVenta(self, codigo, precioVenta):
        val = (str(precioVenta), str(codigo))
        self.miCursor.execute("UPDATE menu SET precio_venta = %s WHERE menu_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setVisible(self, codigo, visible):
        val = (str(visible), str(codigo))
        self.miCursor.execute("UPDATE menu SET visible = %s WHERE menu_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD

