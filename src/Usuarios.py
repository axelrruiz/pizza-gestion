class Usuarios:
    
    def __init__(self, baseDeDatos, cursor):                                            # Constructor
        self.bD = baseDeDatos                                                           # Recibe BD para usar commit()
        self.miCursor = cursor                                                          # Recibe un cursor de BD

    def borrar(self, id):
        self.miCursor.execute("UPDATE usuarios SET activo = 0 WHERE usuarios_id = " + str(id))             # Comando SQL
        self.bD.connection.commit()                                                     # Confirma cambios en BD

    def insertar(self, usuario, contrasenia, nombre, telefono, mail, calle, altura, piso, departamento, barrio):

        self.miCursor.execute(
            "INSERT INTO usuarios (usuario, contrasenia, nombre, telefono, mail, calle, altura, piso, departamento,"+
                        "barrio, activo) VALUES ('"+usuario+"','"+contrasenia+"','"+nombre+"','"+telefono+"','"+mail+"','"+
                        calle+"','"+altura+"','"+piso+"','"+departamento+"','"+barrio+"','1')")
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def imprimir(self):
        self.miCursor.execute("SELECT * FROM usuarios")                                 # Consulta SQL
        usuarios = self.miCursor.fetchall()                                             # Devuelve una tupla con las filas de la consulta
        
        for i in usuarios:
            print("ID: {}\tUsuario: {}\tContrasenia: {}\tNombre: {}\tTelefono: {}\tMail: {}".format(i[0], i[1], i[2],i[3], i[4], i[5])+
            "\nCalle: {}\tAltura: {}\tPiso: {}\tDepartamento: {}\tBarrio: {}".format(i[6], i[7], i[8], i[9], i[10]))
    
    def setUsuario(self, id, usuario):
        val = (str(usuario), str(id))
        self.miCursor.execute("UPDATE usuarios SET usuario = %s WHERE usuarios_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setContrasenia(self, id, contrasenia):
        val = (str(contrasenia), str(id))
        self.miCursor.execute("UPDATE usuarios SET contrasenia = %s WHERE usuarios_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setNombre(self, id, nombre):
        val = (str(nombre), str(id))
        self.miCursor.execute("UPDATE usuarios SET nombre = %s WHERE usuarios_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setTelefono(self, id, telefono):
        val = (str(telefono), str(id))
        self.miCursor.execute("UPDATE usuarios SET telefono = %s WHERE usuarios_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setMail(self, id, mail):
        val = (str(mail), str(id))
        self.miCursor.execute("UPDATE usuarios SET mail = %s WHERE usuarios_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setCalle(self, id, calle):
        val = (str(calle), str(id))
        self.miCursor.execute("UPDATE usuarios SET calle = %s WHERE usuarios_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setAltura(self, id, altura):
        val = (str(altura), str(id))
        self.miCursor.execute("UPDATE usuarios SET altura = %s WHERE usuarios_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setPiso(self, id, piso):
        val = (str(piso), str(id))
        self.miCursor.execute("UPDATE usuarios SET piso = %s WHERE usuarios_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setDepartamento(self, id, departamento):
        val = (str(departamento), str(id))
        self.miCursor.execute("UPDATE usuarios SET departamento = %s WHERE usuarios_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setBarrio(self, id, barrio):
        val = (str(barrio), str(id))
        self.miCursor.execute("UPDATE usuarios SET barrio = %s WHERE usuarios_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
