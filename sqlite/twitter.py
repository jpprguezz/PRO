from __future__ import annotations

import re
import sqlite3

DB_PATH = "twitter.db"

TWEET_EMOJI = "🐦"
RETWEET_EMOJI = "🔁"
MAX_TWEET_LENGTH = 280


def create_db(db_path: str = DB_PATH) -> None:
    """Crea la base de datos y las siguientes tablas:
    - user (id, username, password, bio)
    - tweet (id, content, user_id, retweet_from)
        └ user_id es clave ajena de user(id)
        └ retweet_from es clave ajena de tweet(id)"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    sql = """CREATE TABLE user (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        bio TEXT
    )"""
    cur.execute(sql)

    sql = """CREATE TABLE tweet (
        id INTEGER PRIMARY KEY,
        content TEXT,
        FOREIGN KEY(user_id) REFERENCES user(id),
        FOREIGN KEY(retweet_from) REFERENCES tweet(id)
    )"""
    cur.execute(sql)

    con.commit()
    con.close()


class User:
    def __init__(self, username: str, password: str, bio: str = "", user_id: int = 0):
        """Constructor de la clase User.
        - Crea los atributos con y cur para la conexión a la base de datos (con factoría Row).
        - Crea los atributos username, password, bio, id y logged.
        """
        self.con = sqlite3.connect(DB_PATH)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.username = username
        self.password = password
        self.bio = bio
        self.user_id = user_id
        self.logged = False

    def save(self) -> None:
        """Guarda en la base de datos un objeto de tipo User.
        Además actualiza el atributo "id" del objeto a partir de lo que devuelve la inserción."""
        sql = "INSERT INTO user (username, password, bio) VALUES (?,?,?)"
        data = (self.username, self.password, self.bio)
        self.cur.execute(sql, data)
        self.id = self.cur.lastrowid
        self.con.commit()
        # 2. Actualizar el id del objeto (self.id) a partir de la id devuelta por la inserción (cur.lastrowid)
        self.id = self.cur.lastrowid

    def login(self, password: str) -> None:
        """Realiza el login del usuario.
        Comprueba si existe este usuario con el password pasado por parámetro en la BBDD
        y actualiza los atributos correspondientes."""
        sql = "SELECT * from users WHERE username = ? AND password = ?"
        data = (self.username, password)
        if self.cur.execute(sql, data).fetchone() is not None:
            self.logged = True
        else:
            self.logged = False

    def tweet(self, content: str) -> Tweet:
        """Crea un tweet con el contenido indicado y lo almacena en la base de datos.
        - Utiliza el método save propio de la clase Tweet.
        - Hay que retornar el tweet creado.
        - Si el usuario no está logeado hay que lanzar una excepción de tipo TwitterError
        con el mensaje: User <usuario> is not logged in!
        - Si el tweet supera el límite de caracteres hay que lanzar una excepción de tipo
        TwitterError con el mensaje: Tweet hasta more than 280 chars!"""
        if not self.logged:
            raise TwitterError(f"User {self.username} is not logged in!")
        if len(content) > 280:
            raise TwitterError("Tweet hasta more than 280 chars!")
        new_tweet = Tweet(content)
        # le paso el mismo objeto creado como parámetro, por eso el self
        new_tweet.save(self)
        return new_tweet

    def retweet(self, tweet_id: int) -> Tweet:
        """Crea un retweet con el contenido indicado y lo almacena en la base de datos.
        - Utiliza el método save propio de la clase Tweet.
        - Hay que retornar el tweet creado.
        - Si el usuario no está logeado hay que lanzar una excepción de tipo TwitterError
        con el mensaje: User <usuario> is not logged in!
        - Si tweet_id no existe en la base de datos hay que lanzar una excepción de tipo
        TwitterError con el mensaje: Tweet with id <id> does not exist!"""
        if not self.logged:
            raise TwitterError(f"User {self.username} is not logged in!")
        sql = "SELECT id FROM tweet WHERE id = ?"
        if self.cur.execute(sql, (tweet_id,)).fetchone() is None:
            raise TwitterError(f"Tweet with id {tweet_id} does not exist!")
        sql = "SELECT * FROM tweet WHERE id = ?"
        retweet_content = self.cur.execute(sql, (tweet_id,)).fetchone()["content"]
        new_retweet = Tweet(retweet_content, retweet_from=tweet_id)
        new_retweet.save(self)
        return new_retweet

    @property
    def tweets(self):
        """Función generadora que devuelve todos los tweets propios del usuario.
        - Lo que se devuelven son objetos de tipo Tweet (usar el método from_db_row)."""
        sql = "SELECT * FROM tweet WHERE id = ?"
        for row in self.cur.execute(sql, (self.user_id,)).fetchall:
            yield Tweet.from_db_row(row)

    def __repr__(self):
        """Representa un usuario con el formato:
        <usuario>: <bio>"""
        return f"{self.username}: {self.bio}"

    @classmethod
    def from_db_row(cls, row: sqlite3.Row):
        """Crea un objeto de tipo User a partir de una fila de consulta SQL"""
        id, username, password, bio = row
        return User(username, password, bio, id)


class Tweet:
    def __init__(self, content: str = "", retweet_from: int = 0, tweet_id: int = 0):
        """Constructor de la clase Tweet.
        - Crea los atributos con y cur para la conexión a la base de datos (con factoría Row)
        - Crea los atributos _content, retweet_from e id.
        - retweet_from indica el id del tweet que se retuitea.
          Un id válido debe ser mayor o igual que 1.
        - Si es un retweet el contenido debe ser la cadena vacía.
        """
        self.con = sqlite3.connect(DB_PATH)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.retweet_from = retweet_from
        self.tweet_id = tweet_id
        self._content = "" if self.retweet_from > 0 else content

    @property
    def is_retweet(self) -> bool:
        """Indica si el tweet es un retweet."""
        return self.retweet_from != 0

    @property
    def content(self) -> str:
        """Devuelve el contenido del tweet.
        - Si es un retweet el contenido habrá que buscarlo en el tweet retuiteado."""
        if self.is_retweet:
            sql = "SELECT content where id = ?"
            sql = "SELECT * FROM tweet WHERE id = ?"
            self.cur.execute(sql, (self.retweet_from,))  # Ejecutar la consulta
            row = self.cur.fetchone()  # Obtener el resultado de la consulta
            # Extraer el contenido del resultado
            result = row["content"]
        else:
            result = self._content
        return result

    def save(self, user: User) -> None:
        """Guarda el tweet en la base de datos.
        - El parámetro user es el usuario que escribe el tweet.
        Además actualiza el atributo "id" del objeto a partir de lo que devuelve la inserción."""
        sql = "INSERT INTO tweet(content, user_id, retweet_from) VALUES (?, ?, ?)"
        parameters = (self._content, user.user_id, self.retweet_from)
        self.cur.execute(sql, parameters)
        self.con.commit()
        self.id = self.cur.lastrowid

    def __repr__(self):
        """Representa un tweet con el formato:
        <emoji> <content> (id=<id>)"""
        emoji_symbol = RETWEET_EMOJI if self.is_retweet else TWEET_EMOJI
        return f"{emoji_symbol} {self._content} (id={self.tweet_id})"

    @classmethod
    def from_db_row(cls, row: sqlite3.Row) -> Tweet:
        """Crea un objeto de tipo Tweet a partir de una fila de consulta SQL"""
        return cls(row["content"], row["retweet_from"], row["tweet_id"])

    # otra manera
    # row_dict = dict(row)
    # return cls(**row_dict)


class Twitter:
    def __init__(self):
        """Constructor de la clase Twitter.
        - Crea los atributos con y cur para la conexión a la base de datos (con factoría Row)
        """
        self.con = sqlite3.connect(DB_PATH)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    def add_user(self, username: str, password: str, bio: str = "") -> User:
        """Crea un objeto de tipo User y lo guarda en la base de datos.
        - Haz uso de los métodos ya creados.
        - Hay que retornar el objeto creado.
        - La contraseña debe seguir el siguiente formato:
          * Empezar con una arroba o un signo igual.
          * Continuar con 2, 3 o 4 dígitos.
          * Continuar con 2, 3 o 4 letras de la A-Z (incluyendo minúsculas).
          * Terminar con una exclamación o un asterisco.
        Si no sigue este formato hay que elevar una excepción de tipo TwitterError
        con el mensaje: Password does not follow security rules!"""
        password_requirements = r"[@=]\d{2,4}[a-zA-Z]{2,4}[!*]"
        if not re.fullmatch(password_requirements, password):
            raise TwitterError("Password does not follow security rules!")
        new_user = User(username, password, bio)
        new_user.save()
        return new_user

    def get_user(self, user_id: int) -> User:
        """Devuelve el usuario con el user_id indicado.
        Si el usuario no existe hay elevar una excepción de tipo TwitterError con el mensaje:
        User with id <id> does not exist!"""
        sql = "SELECT * FROM user WHERE id = ?"
        if row := self.cur.execute(sql, (user_id,)).fetchone():
            return User.from_db_row(row)
        else:
            raise TwitterError(f"User with id {user_id} does not exist!")


class TwitterError(Exception):
    def __init__(self, message=""):
        err_info = message
        # Llamada al constructor de la clase base
        super().__init__(err_info)