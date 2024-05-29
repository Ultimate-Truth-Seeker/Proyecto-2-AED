import tkinter as tk
from tkinter import messagebox

get_similar_songs = """
MATCH (s:song {name: $song})-[r:similar]-(t:song)
MATCH (t)-[u:from]-(a:artist)
MATCH (t)-[v:from]-(b:album)
RETURN t AS song, a AS artist, b AS album, r 
ORDER BY r.weight DESC
LIMIT 5
"""

get_toptags = """
MATCH (n:tag)
RETURN n AS tags
ORDER BY COUNT{(s:song)-[r:is]-(n)} DESC
LIMIT 5;
"""
get_songs_bytag = """
MATCH (n:tag {name: $tag})-[r:is]-(s:song)
MATCH (s)-[u:from]-(a:artist)
MATCH (s)-[v:from]-(b:album)
RETURN s AS song, a AS artist, b AS album
ORDER BY s.playcount DESC
LIMIT 5
"""

get_song = """
MATCH (s:song {name: $song})
MATCH (s)-[r:from]-(a:artist)
MATCH (s)-[t:from]-(b:album)
RETURN s AS song, a AS artist, b AS album
"""

sign_up = """
CREATE (u:user {name: $name, password: $password, id: randomuuid()})
RETURN TRUE;
"""

check_user = """
MATCH (u:user {name: $name})
RETURN COUNT{(u)} AS present
"""


login = """
MATCH (u:user {name: $name, password: $password})
RETURN u AS user
"""

add_favorite = """
CREATE (s:song {id: $Id})<-[r:favorite]-(u:user {id: $uid})
RETURN TRUE
"""

remove_favorite = """
DELETE (s:song {id: $Id})<-[r:favorite]-(u:user {id: $uid})
RETURN TRUE
"""

get_user_favorites = """
MATCH (u:user {id:$uid})-[r:favorite]-(s:song)
RETURN s AS song
"""

#Esta función ejecuta una consulta en Neo4j y devuelve los resultados
def makeQuery(tx, query, name=None, password = None, uid=None, Id= None, song=None, tag=None):
    result = tx.run(query, name=name, password = password, uid=uid, Id= Id, song=song, tag=tag)
    return list(result)


import os
from neo4j import GraphDatabase


# son las credenciales para conectarse a la base de datos de Neo4j
URI = "neo4j+ssc://07e5e662.databases.neo4j.io"
AUTH = ("neo4j", "Gyay1_asYeu7DCXRMkBeRLDg90a5oc2K1yhWR8F17iw")

#  se encarga de ejecutar las consultas en la base de datos Neo4j
def run(query, name=None, password = None, uid=None, Id= None, song=None, tag=None):
    #Conexión a la base de datos 
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        #Verifica si la conexión se ha establecido correctamente 
        driver.verify_connectivity()
        #Inicia sesión con la base de datos 
        with driver.session(database="neo4j") as session:
            return session.execute_write(makeQuery, query, name, password, uid, Id, song, tag)


#Esta clase se encargará de mostrar en pantalla todas las opciones
class App:
    def _init_(self, root):
        self.root = root
        self.root.title("Recomendación Musical")
        self.username = None
        self.password = None
        self.song = None
        self.tag = None
        self.prevFrame = []

        self.frames = {}
        tpl = (LoginWindow, StartPage, Register)
        for F in tpl:
            frame = F(root, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def update_frame(self, page):
        frame = page(self.root, self)
        self.frames[page] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def songPage(self, frame):
        self.prevFrame.append(frame)
        self.update_frame(Song)
        self.show_frame(Song)

    def select(self, s, page):
        self.song = s
        self.songPage(page)

    def back(self):
        if isinstance(self.prevFrame[len(self.prevFrame) - 1], Song):
            self.song = self.prevFrame[len(self.prevFrame) - 1].song
            self.update_frame(Song)
            self.show_frame(Song)
        else:
            self.show_frame(self.prevFrame[len(self.prevFrame) - 1])
        self.prevFrame.pop()

#Esta clase es la encargada de mostrar la página de inicio al entrar a la aplicación
class StartPage(tk.Frame):
    def _init_(self, root, controller):
        tk.Frame._init_(self, root)
        self.controller = controller
        label = tk.Label(self, text="Bienvenido")
        label.pack()
        button = tk.Button(self, text="Iniciar sesión", command=lambda: controller.show_frame(LoginWindow))
        button.pack()
        button = tk.Button(self, text="Registrarse", command=lambda: controller.show_frame(Register))
        button.pack()

#Agregar funcionalidades a distintos botones, o añadir mensajes en pantalla
class Home(tk.Frame):
    def _init_(self, root, controller):
        tk.Frame._init_(self, root)
        self.controller = controller
        welcome = tk.Label(self, text="Bienvenido, " + controller.username)
        welcome.pack()
        label = tk.Label(self, text="Búsqueda de canciones")
        label.pack()
        query = tk.Entry(self)
        query.pack()
        button = tk.Button(self, text="buscar", command=lambda: self.search(query.get()))
        button.pack()
        tags = run(get_toptags)
        logout = tk.Button(self, text="Cerrar Sesión", command=self.log_out)
        logout.pack()
        taglabel = tk.Label(self, text="Categorías musicales")
        taglabel.pack()
        for tg in tags:
            tk.Button(self, text=tg["tags"]["name"], command=lambda: self.chooseTag(tg)).pack()
            
    def log_out(self):        
        self.controller.username = None
        self.controller.password = None
        self.controller.update_frame(LoginWindow)
        self.controller.show_frame(StartPage)

    def search(self, song):
        srch = run(get_song, song=song)
        if (len(srch) >0):
            self.controller.song = srch[0]
        self.controller.update_frame(Search)
        self.controller.show_frame(Search)

    def chooseTag(self, tag):
        self.controller.tag = tag
        self.controller.update_frame(Tag)
        self.controller.show_frame(Tag)

class Search(tk.Frame):
    def _init_(self, root, controller):
        tk.Frame._init_(self, root)
        self.controller = controller
        button = tk.Button(self, text="atras", command=lambda: controller.show_frame(Home))
        button.pack()
        song = controller.song
        if (song != None):
            srchresult = tk.Button(self, text=song["song"]["name"] + " | "+ song["artist"]["name"], command=lambda:controller.songPage(Search))
            srchresult.pack()

class Song(tk.Frame):
    def _init_(self, root, controller):
        tk.Frame._init_(self, root)
        self.controller = controller
        self.song = controller.song
        button = tk.Button(self, text="atras", command=lambda: controller.back())
        button.pack()
        button = tk.Button(self, text="Inicio", command=lambda: self.returnHome())
        button.pack()
        name = tk.Label(self, text=controller.song["song"]["name"])
        artist = tk.Label(self, text=controller.song["artist"]["name"])
        name.pack()
        artist.pack()
        label = tk.Label(self, text="\ncanciones similares:")
        label.pack()
        similars = run(get_similar_songs, song=controller.song["song"]["name"])
        
        for s in similars:
            print(s["song"]["name"])
            tk.Button(self, text=s["song"]["name"], command=lambda: controller.select(s, self)).pack()

    def returnHome(self):
        self.controller.prevFrame.clear()
        self.controller.show_frame(Home)

class Tag(tk.Frame):
    def _init_(self, root, controller):
        tk.Frame._init_(self, root)
        self.controller = controller
        self.tag = controller.tag
        button = tk.Button(self, text="Inicio", command=lambda: controller.show_frame(Home))
        button.pack()
        label = tk.Label(self, text=self.tag["tags"]["name"] + "\nListado de Canciones")
        label.pack()
        
        songs = run(get_songs_bytag, tag=self.tag["tags"]["name"])
        for s in songs:
            print(s["song"]["name"])
            tk.Button(self, text=s["song"]["name"], command=lambda: controller.select(s, Tag)).pack()
