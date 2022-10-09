class Clientes:
    
    def __init__(self, baseDeDatos, cursor):                                            # Constructor
        self.bD = baseDeDatos                                                           # Recibe BD para usar commit()
        self.miCursor = cursor                                                                # Recibe un cursor de BD

    def borrar(self, id):
        self.miCursor.execute("UPDATE clientes SET activo = 0 WHERE clientes_id = " + str(id))             # Comando SQL
        self.bD.connection.commit()                                                     # Confirma cambios en BD

    def insertar(self, telefono, nombre, calle, altura, piso, departamento, barrio, usuario):

        self.miCursor.execute(
            "INSERT INTO clientes (telefono, nombre, calle, altura, piso, departamento, barrio, activo,"+
             "id_usuario_crea, id_usuario_modifica) VALUES ('"+telefono+"','"+nombre+"','"+calle+"','"+altura+"','"+
             piso+"','"+departamento+"','"+barrio+"','1','"+usuario+"','"+usuario+"')")
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def imprimir(self):
        self.miCursor.execute("SELECT * FROM clientes")                                 # Consulta SQL
        personas = self.miCursor.fetchall()                                             # Devuelve una tupla con las filas de la consulta
        
        for i in personas:
            print("ID: {}\tTelefono: {}\tNombre: {}\tCalle: {}\tAltura: {}\tPiso: {}\tDepartamento: {}\tBarrio: {}".format(
                i[0], i[3], i[4],i[5], i[6], i[7], i[8], i[9]))
    
    def setTelefono(self, id, telefono, usuario):
        val = (str(telefono), str(usuario), str(id))
        self.miCursor.execute("UPDATE clientes SET telefono = %s, id_usuario_modifica = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD

    def setNombre(self, id, nombre, usuario):
        val = (str(nombre), str(usuario), str(id))
        self.miCursor.execute("UPDATE clientes SET nombre = %s, id_usuario_modifica = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setCalle(self, id, calle, usuario):
        val = (str(calle), str(usuario), str(id))
        self.miCursor.execute("UPDATE clientes SET calle = %s, id_usuario_modifica = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setAltura(self, id, altura, usuario):
        val = (str(altura), str(usuario), str(id))
        self.miCursor.execute("UPDATE clientes SET altura = %s, id_usuario_modifica = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setPiso(self, id, piso, usuario):
        val = (str(piso), str(usuario), str(id))
        self.miCursor.execute("UPDATE clientes SET piso = %s, id_usuario_modifica = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setDepartamento(self, id, departamento, usuario):
        val = (str(departamento), str(usuario), str(id))
        self.miCursor.execute("UPDATE clientes SET departamento = %s, id_usuario_modifica = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setBarrio(self, id, barrio, usuario):
        val = (str(barrio), str(usuario), str(id))
        self.miCursor.execute("UPDATE clientes SET barrio = %s, id_usuario_modifica = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD


