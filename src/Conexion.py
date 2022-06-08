import mysql.connector

class BaseDeDatos:
        
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
        host=host,
        user= user,
        password= password,
        database= database
        )

    def getCursor(self):                                                        # Se obtiene el cursor
        return self.connection.cursor()



