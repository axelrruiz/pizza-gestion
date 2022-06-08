class Pedidos:
    
    def __init__(self, baseDeDatos, cursor):                                            # Constructor
        self.bD = baseDeDatos                                                           # Recibe BD para usar commit()
        self.miCursor = cursor                                                          # Recibe un cursor de BD

    def insertar(self, idCliente, pago, productoCantidad):                              # ProductoCantidad es una tupla dentro de una lista
        total = 0
        idPedido = 0

        # **************                  Suma el Total                                         **************
        for i in productoCantidad:
            self.miCursor.execute("SELECT precio_venta FROM menu WHERE menu_id = " + str(i[0]))  # Consulta de precio del producto
            consulta = self.miCursor.fetchall()
            total += float(consulta[0][0]) * i[1]                                       # Suma el precio multiplicado por la cantidad al tot
        
        # **************                  Guarda en Tabla pedidos                               **************
        val = (idCliente, total, pago)

        self.miCursor.execute("INSERT INTO pedidos (id_cliente, total, estado, pago) VALUES (%s,%s,'Preparacion',%s)", val)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
       
        # **************                  Guarda en Tabla detalle_pedidos                       **************
        self.miCursor.execute("SELECT * FROM pedidos order by pedidos_id desc limit 1")  # Consulta de el ultimo registro
        consulta = self.miCursor.fetchall()                                             # Resultado de la consulta
        idPedido = consulta[0][0]                                                       # Id del ultimo pedido

        for i in productoCantidad:                                                      # Recorre la lista agregando los productos
            val = (idPedido, i[0], i[1])
            
            self.miCursor.execute("INSERT INTO detalle_pedidos (id_pedido, id_menu, cantidad) VALUES (%s,%s,%s)", val)
            self.bD.connection.commit()
    
    def imprimir(self):
        self.miCursor.execute("SELECT * FROM pedidos")                                  # Consulta SQL
        pedidos = self.miCursor.fetchall()                                              # Devuelve una tupla con las filas de la consulta
        
        for i in pedidos:
            print("ID: {}\tCliente: {}\tTotal: {}\tEstado: {}\tPago: {}\tFecha: {}".format
            (i[0], i[1], i[2], i[3], i[4], i[5]))
    
    def setEstado(self, IdPedido, estado):
        self.miCursor.execute("UPDATE pedidos SET Estado = '"+estado+"' WHERE pedidos_id = "+IdPedido)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    
    def setPago(self, IdPedido, pago):
        self.miCursor.execute("UPDATE pedidos SET pago = '"+pago+"' WHERE pedidos_id = "+IdPedido)
        self.bD.connection.commit()                                                     # Confirma cambios en BD
    

