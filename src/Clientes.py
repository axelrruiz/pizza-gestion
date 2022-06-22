class Clientes:
    
    def __init__(self, baseDeDatos, cursor):                                            # Constructor
        self.bD = baseDeDatos                                                           # Recibe BD para usar commit()
        self.miCursor = cursor                                                                # Recibe un cursor de BD

    def borrar(self, id):
        self.miCursor.execute("UPDATE clientes SET visible = 0 WHERE clientes_id = " + str(id))             # Comando SQL
        self.bD.connection.commit()                                                     # Confirma cambios en BD

    def insertar(self, telefono, nombre, calle, altura, piso, departamento, barrio):

        self.miCursor.execute(
            "INSERT INTO clientes (telefono, nombre, calle, altura, piso, departamento, barrio, visible) VALUES ('"+
                        telefono+"','"+nombre+"','"+calle+"','"+altura+"','"+piso+"','"+departamento+"','"+barrio+",1')")
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def imprimir(self):
        self.miCursor.execute("SELECT * FROM clientes")                                 # Consulta SQL
        personas = self.miCursor.fetchall()                                             # Devuelve una tupla con las filas de la consulta
        
        for i in personas:
            print("ID: {}\tTelefono: {}\tNombre: {}\tCalle: {}\tAltura: {}\tPiso: {}\tDepartamento: {}\tBarrio: {}".format(
                i[0], i[1], i[2],i[3], i[4], i[5], i[6], i[7]))
    
    def setTelefono(self, id, telefono):
        val = (str(telefono), str(id))
        self.miCursor.execute("UPDATE clientes SET telefono = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setNombre(self, id, nombre):
        val = (str(nombre), str(id))
        self.miCursor.execute("UPDATE clientes SET nombre = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setCalle(self, id, calle):
        val = (str(calle), str(id))
        self.miCursor.execute("UPDATE clientes SET calle = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setAltura(self, id, altura):
        val = (str(altura), str(id))
        self.miCursor.execute("UPDATE clientes SET altura = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setPiso(self, id, piso):
        val = (str(piso), str(id))
        self.miCursor.execute("UPDATE clientes SET piso = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setDepartamento(self, id, departamento):
        val = (str(departamento), str(id))
        self.miCursor.execute("UPDATE clientes SET departamento = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setBarrio(self, id, barrio):
        val = (str(barrio), str(id))
        self.miCursor.execute("UPDATE clientes SET barrio = %s WHERE clientes_id =%s", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD


