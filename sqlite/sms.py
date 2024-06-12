import re
import sqlite3

DB_PATH = 'sms.db'

"""
Diagrama de clases:

            +-----------+                       +-----------+
            |           |                       |           |
      +-----+ DbHandler +------+                | SMSError  |
      |     |           |      |                |           |
      |     +-----------+      |                +-----------+
      |                        |                             
      |                        |                             
      |                        |                             
      v                        v                             
+------------+         +--------------+                      
|            |         |              |                      
|    SMS     |         |     SIM      |                      
|            |         |              |                      
+------------+         +--------------+                      
"""


class DbHandler:
    """Clase que representa un manejador a la base de datos."""

    def __init__(self, db_path: str = DB_PATH):
        """Crea la conexión a la base de datos (factoría Row) y el cursor correspondiente.
        También crea atributos homónimos a parámetros"""
        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    def create_db(self) -> None:
        """Crea la base de datos y sus tablas"""
        sql = """CREATE TABLE activity (
        id INTEGER PRIMARY KEY,
        sender TEXT,
        recipient TEXT,
        message TEXT
        );
        CREATE TABLE access(
        phone_number TEXT PRIMARY KEY,
        pin TEXT,
        puk TEXT)"""
        self.cur.executescript(sql)
        self.con.commit()


class SMS(DbHandler):
    """Clase que representa un SMS."""

    def __init__(self, sender: str, recipient: str, message: str):
        """Construye un objeto SMS con los mismos atributos que parámetros.
        Esta clase hereda de DbHandler...

        NO HAY QUE ALMACENAR NADA EN LA BASE DE DATOS"""
        super().__init__()
        self.sender = sender
        self.recipient = recipient
        self.message = message

    def send(self) -> None:
        """Simula el envío de este SMS (self) guardando todos sus campos en la tabla activity"""
        sql = 'INSERT INTO activity (sender, recipient, message) VALUES (?,?,?)'
        data = (self.sender, self.recipient, self.message)
        self.cur.execute(sql, data)
        self.con.commit()

    def __str__(self):
        """Representa un objeto de tipo SMS de la siguiente forma:
        From: <remitente>
        To: <destinatario>
        ---
        <mensaje>
        """
        return f'From: {self.sender}\nTo: {self.recipient}\n---\n{self.message}'


class SIM(DbHandler):
    """Clase que representa una tarjeta SIM."""

    def __init__(self, phone_number: str):
        """Construye una SIM guardando como atributo el número de teléfono.
        También es necesario crear un atributo unlocked (booleano) que indique si
        la tarjeta está bloqueada o no (si se ha accedido o no).

        Esta clase hereda de DbHandler...

        NO HAY QUE ALMACENAR NADA EN LA BASE DE DATOS"""
        super().__init__()
        self.phone_number = phone_number
        self.unlocked = False

    def unlock(self, pin: str, *, puk: str = '') -> None:
        """Intenta desbloquear la SIM, ACTUALIZANDO el atributo "unlocked" del objeto
        según el resultado de la operación.

        Si el PIN aportado no es correcto, se podrá desbloquear la SIM comprobando
        si el PUK aportado es el correcto.
        """
        sql = 'SELECT * FROM access WHERE phone_number = ?'
        if row := self.cur.execute(sql, (self.phone_number,)).fetchone():
            if row['pin'] == pin:
                self.unlocked = True
            elif row['puk'] == puk:
                self.unlocked = True
            else:
                self.unlocked = False
        else:
            self.unlocked = False

    @staticmethod
    def unlock_required(method):
        """Decorador que lanza una excepción SMSError si la SIM está bloqueada.
        El mensaje de la excepción debe ser:
        SMS "<phone_number>" is locked!

        Ojo! La excepción recibe en su constructor tanto el mensaje de error
        como el objeto actual de tipo SMS."""

        def wrapper(self, *args, **kwargs):
            if not self.unlocked:
                raise SMSError(f'SMS "{self.phone_number}" is locked!', self)
            return method(self, *args, **kwargs)

        return wrapper

    @unlock_required
    def send_sms(self, *, recipient: str, message: str) -> None:
        """Realiza el "envío" de un SMS a través de un objeto de tipo SMS.

        Si "recipient" no tiene un formato válido de número de teléfono se debe
        lanzar una excepción de tipo SIMError con el mensaje:
        Recipient "<recipient>" has invalid format!

        Un número de teléfono válido es aquel que empieza por 6 o 7 y contiene
        un total de 9 dígitos. Ojo porque también puede aparecer un prefijo
        con 2 dígitos:
        ✔ +34 678543559
        ✔ 678543559
        ✔ +51 732869123
        ✔ 732869123

        Ojo! La excepción recibe en el constructor tanto el PIN
        como el objeto actual de tipo SIM.
        """
        regex = r'(\+\d{2}\s)?[6-7]\d{8}'
        if not re.fullmatch(regex, recipient):
            raise SMSError(f'Recipient "{recipient}" has invalid phone format!', self)
        new_sms = SMS(self.phone_number, recipient, message)
        new_sms.send()

    @unlock_required
    def get_sms(self, sent: bool = True):
        """FUNCIÓN GENERADORA que devuelve objetos de tipo SMS:
        - Si el parámetro "sent" es True se devuelven los enviados
          por el número de teléfono del objeto.
        - Si el parámetro "sent" es False se devuelven los recibidos
          por el número de teléfono del objeto."""
        if sent:
            sql = 'SELECT * FROM activity where sender = ?'
            self.cur.execute(sql, (self.phone_number,))
        else:
            sql = 'SELECT * FROM activity WHERE recipient = ?'
            self.cur.execute(sql, (self.phone_number,))

        for row in self.cur.fetchall():
            yield SMS(row['sender'], row['recipient'], row['message'])


class SMSError(Exception):
    def __init__(self, message: str, db_handler: DbHandler):
        """Hay que cerrar la conexión a la base de datos"""
        err_info = message
        super().__init__(err_info)
        db_handler.con.close()