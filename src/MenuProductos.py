class MenuProductos:
    
    def __init__(self, baseDeDatos, cursor):                                            # Constructor
        self.bD = baseDeDatos                                                           # Recibe BD para usar commit()
        self.miCursor = cursor                                                          # Recibe un cursor de BD

    def borrar(self, id):
        self.miCursor.execute("UPDATE menu SET activo = 0 WHERE menu_id = " + str(id)) # Comando SQL
        self.bD.connection.commit()                                                     # Confirma cambios en BD

    def insertar(self, descripcion, precioDeVenta, categoria, usuario):

        val = (descripcion, precioDeVenta, categoria, usuario, usuario)

        self.miCursor.execute(
            "INSERT INTO menu (descripcion, precio_venta, activo, id_categorias_menu, id_usuario_crea,"+
            " id_usuario_modifica) VALUES (%s,%s,1,%s,%s,%s)", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def imprimir(self):
        self.miCursor.execute("SELECT * FROM menu")                                     # Consulta SQL
        menus = self.miCursor.fetchall()                                                # Devuelve una tupla con las filas de la consulta
        
        for i in menus:
            print("Codigo: {}\tDescripcion: {}\tPrecio de Venta: {}\tActivo: {}".format
            (i[0], i[4], i[5], i[6]))
    
    def setDescripcion(self, id, descripcion, usuario):
        val = (str(descripcion), str(usuario), str(id))
        self.miCursor.execute("UPDATE menu SET descripcion = %s, id_usuario_modifica = %s WHERE menu_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setPrecioVenta(self, id, precioVenta, usuario):
        val = (str(precioVenta), str(usuario), str(id))
        self.miCursor.execute("UPDATE menu SET precio_venta = %s, id_usuario_modifica = %s WHERE menu_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setCategoria(self, id, categoria, usuario):
        val = (str(categoria), str(usuario), str(id))
        self.miCursor.execute("UPDATE menu SET id_categorias_menu = %s, id_usuario_modifica = %s WHERE menu_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    