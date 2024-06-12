import re
import sqlite3

DB_PATH = 'mail.db'

"""
Diagrama de clases:

            +-----------+                       +-----------+
            |           |                       |           |
      +-----+ DBHandler +------+                | MailError |
      |     |           |      |                |           |
      |     +-----------+      |                +-----------+
      |                        |                             
      |                        |                             
      |                        |                             
      v                        v                             
+------------+         +--------------+                      
|            |         |              |                      
|    Mail    |         |  MailServer  |                      
|            |         |              |                      
+------------+         +--------------+                      
"""


class DbHandler:
    db_path: str

    def __init__(self, db_path: str = DB_PATH):
        """Crea la conexión a la base de datos (factoría Row) y el cursor correspondiente.
        También crea atributos homónimos a parámetros"""
        self.db_path = db_path
        self.con = sqlite3.connect(self.db_path)
        self.cur = self.con.cursor()

    def create_db(self) -> None:
        """Crea la base de datos y sus tablas"""

        sql1 = '''CREATE TABLE activity (
    id INTEGER PRIMARY KEY,
    sender TEXT,
    recipient TEXT,
    subject TEXT,
    body TEXT
)'''
        sql2 = '''CREATE TABLE login (
    username TEXT PRIMARY KEY,
    password TEXT,
    domain TEXT
)'''
        self.cur.execute(sql1)
        self.cur.execute(sql2)
        self.con.commit()


class Mail(DbHandler):
    """Clase que representa un correo electrónico."""
    def __init__(self, sender: str, recipient: str, subject: str, body: str):
        """Construye un objeto Mail con los mismos atributos que parámetros.
        Esta clase hereda de DbHandler...

        NO HAY QUE ALMACENAR NADA EN LA BASE DE DATOS"""
        super().__init__()
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body = body

    def send(self) -> None:
        """Simula el envío de este correo (self) guardando todos sus campos en la tabla activity"""
        sql = 'INSERT INTO activity (sender, recipient, subject, body) VALUES (?, ?, ?, ?)'
        self.cur.execute(sql, (self.sender, self.recipient, self.subject, self.body))
        self.con.commit()

    def __str__(self):
        """Representa un objeto de tipo Mail de la siguiente forma:
        From: <remitente>
        To: <destinatario>
        ---
        <asunto pasado a mayúsculas>
        <cuerpo del correo>
        """
        # Debemos poner el f string de esta manera, ya que si pulsamos enter, el texto empieza en una linea más abajo y la linea anterior la detecta como un "/n"

        return f"""From: {self.sender}
To: {self.recipient}
---
{self.subject.upper()}
{self.body}"""

class MailServer(DbHandler):
    """Clase que representa un SERVIDOR DE CORREO."""

    def __init__(self, username: str):
        """Construye un MailServer creando el atributo de nombre de usuario.
        También es necesario crear un atributo logged (booleano) que indique si se ha logeado.
        Esta clase hereda de DbHandler..."""
        super().__init__()
        self.username = username
        self.logged = False # Por defecto el user no tiene sesion iniciada

    def login(self, password: str) -> None:
        """Intenta hacer el login del usuario comprobando con la contraseña que se pasa.
        También hay que ACTUALIZAR los atributos del objeto: "domain" y "logged".
        → La comprobación hay que hacerla consultando la base de datos.
        Notas:
          + Si el usuario se logea correctamente, su dominio será el que está almacenado en la
            base de datos.
          + Si el usuario no se logea correctamente, su dominio será la cadena vacía.
        """
        sql = f"SELECT * FROM login where username = '{self.username}'"  # Primero nos encargamos de conseguir el usuario a traves de us nombre, para luego conseguir la contraseña
        self.cur.execute(sql)
        user = self.cur.fetchone()

        self.domain = ''  # Ponemos un string vacío por defecto

        if user is None:  # Comprobar que el usuario no sea nulo. En caso de que lo sea, retorna None.
            return None
        
        if password == user[1]:  # Comprobarmos desde la tupla (username, password, domain) si la contraseña coincida con la pasada en argumentos de esta función
            self.logged = True
            self.domain = user[2]

    @staticmethod
    def login_required(method):  # Esta es la funcion a ejcutar, que va por debajo de la funcion, basicamente
        """Decorador que lanza una excepción MailError si el usuario no está logeado.
        El mensaje de la excepción debe ser:
        User "<username>" not logged in!

        Ojo! La excepción recibe en su constructor tanto el mensaje de error
        como el objeto actual de tipo MailServer."""
        def wrapper(self, *args, **kwargs):  # estos parametros son pasados por la funcion (method) siempre que se hace un wrapper
            if self.logged is True:
                return method(self, *args, **kwargs)  # siempre retornar la ejecucion del metodo
            else:
                raise MailError(f"User \"{self.username}\" not logged in!", self)
        return wrapper # retornar siempre wrapper (sin parentesis)

        

    @property
    def sender(self) -> str:
        """Formato: <nombre-de-usuario>@<dominio>

        No hay que aplicar decorador pero debes saber que esta propiedad
        sólo va a funcionar si se ha hecho login previamente, ya que en otro caso
        no disponemos del dominio."""
        return f'{self.username}@{self.domain}'

    @login_required
    def send_mail(self, *, recipient: str, subject: str, body: str) -> None:
        """Realiza el "envío" de un correo a través de un objeto de tipo Mail.
        Si recipient no tiene un formato válido de email se debe lanzar una excepción
        de tipo MailError con el mensaje:
        Recipient "<recipient>" has invalid mail format!

        Ojo! La excepción recibe en el constructor tanto el mensaje
        como el objeto actual de tipo MailServer."""
        regex = r'\w+(-\w+)*@\w+(\.\w+)+'
        if re.fullmatch(regex, recipient) is None:
            raise MailError(f'Recipient {recipient} has invalid mail format!', self)  # cuando cree un objeto, ya sea error o lo que sea, tengo que pasarle _TODO lo que me pida la clase/constructor
        mail = Mail(self.sender, recipient, subject, body)  # Instanciamos el nuevo Mail
        mail.send()  # Enviamos el nuevo correo

    @login_required
    def get_emails(self, sent: bool = True):
        """FUNCIÓN GENERADORA que devuelve objetos de tipo Mail.
        - Si el parámetro "sent" es True se devuelven los enviados por el usuario.
        - Si el parámetro "sent" es False se devuelven los recibidos por el usuario."""
        

class MailError(Exception):
    def __init__(self, message: str, mail_handler: Mail | MailServer):
        """Hay que cerrar la conexión a la base de datos"""
        super().__init__(message) # Cuando heredes de errores IMPORTANTE utilizar super para el message
        self.mail_handler = mail_handler
        self.mail_handler.con.close()