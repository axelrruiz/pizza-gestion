class Reportes:
    
    def __init__(self, baseDeDatos, cursor):                                            # Constructor
        self.bD = baseDeDatos                                                           # Recibe BD para usar commit()
        self.miCursor = cursor                                                          # Recibe un cursor de BD

    def mensual(self, anio, mes):
        fecha = (anio, mes)

        self.miCursor.execute("SELECT pedidos.pedidos_id,crea.usuario AS crea,modifica.usuario AS modifica,pedidos.total,pedidos.estado,"+
                                "pedidos.fecha FROM pedidos INNER JOIN usuarios AS crea on pedidos.id_usuario_crea=crea.usuarios_id "+
                                "INNER JOIN usuarios AS modifica ON pedidos.id_usuario_modifica=modifica.usuarios_id "+
                                "WHERE YEAR( fecha ) = '%s' AND MONTH( fecha ) = '%s' ORDER BY pedidos.pedidos_id ASC", fecha)
        
        return self.miCursor.fetchall()                                                 # Devuelve una lista con una tupla por cada elemento
                
    
    def parcial(self, desdeAnio, desdeMes, desdeDia, hastaAnio, hastaMes, hastaDia):
        
        self.miCursor.execute("SELECT pedidos.pedidos_id,crea.usuario AS crea,modifica.usuario AS modifica,pedidos.total,pedidos.estado,"+
                                "pedidos.fecha FROM pedidos INNER JOIN usuarios AS crea on pedidos.id_usuario_crea=crea.usuarios_id "+
                                "INNER JOIN usuarios AS modifica ON pedidos.id_usuario_modifica=modifica.usuarios_id "+
                                "WHERE pedidos.fecha BETWEEN '" + str(desdeAnio) +"-" + str(desdeMes) +"-"+ str(desdeDia) +
                                " 00:00:00' AND '" + str(hastaAnio) +"-" + str(hastaMes) + "-"+ str(hastaDia) +
                                " 23:59:59' ORDER BY pedidos.pedidos_id ASC")
        
        return self.miCursor.fetchall()                                                 # Devuelve una lista con una tupla por cada elemento
         
    def imprimirMensual(self, anio, mes):
        fecha = (anio, mes)

        self.miCursor.execute("SELECT * FROM pedidos WHERE YEAR( fecha ) = '%s' AND MONTH( fecha ) = '%s'", fecha)
        consulta = self.miCursor.fetchall()

        for i in consulta:
            print("Pedido N° ", i[0], "\tCliente N° ", i[1], "\tTotal: $", i[2], "\tEstado ", i[3], "\tPago: ", i[4],  "\tFecha: ", i[5])
        

    def imprimirParcial(self, desdeAnio, desdeMes, desdeDia, hastaAnio, hastaMes, hastaDia):

        self.miCursor.execute("SELECT * FROM pedidos WHERE fecha BETWEEN '" + str(desdeAnio) +"-" + str(desdeMes) +
        "-"+ str(desdeDia) +" 00:00:00' AND '" + str(hastaAnio) +"-" + str(hastaMes) + "-"+ str(hastaDia) +" 23:59:59'")
        consulta = self.miCursor.fetchall()

        for i in consulta:
            print("Pedido N° ", i[0], "\tCliente N° ", i[1], "\tTotal: $", i[2], "\tEstado ", i[3], "\tPago: ", i[4],  "\tFecha: ", i[5])
        
