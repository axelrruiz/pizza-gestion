class CategoriasMenuProductos:
    
    def __init__(self, baseDeDatos, cursor):                                            # Constructor
        self.bD = baseDeDatos                                                           # Recibe BD para usar commit()
        self.miCursor = cursor                                                          # Recibe un cursor de BD

    def borrar(self, id):
        self.miCursor.execute("UPDATE categorias_menu SET activo = 0 WHERE categorias_menu_id = " + str(id))             # Comando SQL
        self.bD.connection.commit()                                                     # Confirma cambios en BD

    def insertar(self, categoria, usuario):

        self.miCursor.execute(
            "INSERT INTO categorias_menu (id_usuario_crea, id_usuario_modifica, descripcion, activo) VALUES ('"+
                str(usuario)+"','"+str(usuario)+"','"+categoria+"','1')")
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def imprimir(self):
        self.miCursor.execute("SELECT * FROM categorias_menu")                                 # Consulta SQL
        categorias = self.miCursor.fetchall()                                             # Devuelve una tupla con las filas de la consulta
        
        for i in categorias:
            print("ID: {}\tUsuario Creador: {}\tUsuario Modificador: {}\tDescripcion: {}\tActivo: {}".format(i[0], i[1], i[2],i[3], i[4]))
    
    def setDescripcion(self, id, categoria, usuario):
        val = (str(categoria), str(usuario), str(id))
        self.miCursor.execute("UPDATE categorias_menu SET descripcion = %s, id_usuario_modifica = %s WHERE categorias_menu_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    