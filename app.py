#queris aplicación

#25 canciones parecidas
get_similar_songs = """
MATCH (s:song {name: $song})-[r:similar]-(t:song)
MATCH (t)-[u:from]-(a:artist)
MATCH (t)-[v:from]-(b:album)
RETURN t AS song, a AS artist, b AS album, r.weight AS weight 
ORDER BY r.weight DESC
LIMIT 5
"""

get_toptags = """
MATCH (n:tag)
RETURN n AS tags
ORDER BY COUNT{(s:song)-[r:is]-(n)} DESC
LIMIT 25;
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
        driver.verify_connectivity()
        with driver.session(database="neo4j") as session:
            return session.execute_write(makeQuery, query, name, password, uid, Id, song, tag)


import tkinter as tk

from tkinter import messagebox
from tkinter import ttk

#Esta clase se encargará de mostrar en pantalla todas las opciones
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Recomendación Musical")
        self.username = None
        self.password = None
        self.song = None
        self.tag = None
        self.uid  = None
        self.prevFrame = []

        self.frames = {}
        tpl = (LoginWindow, StartPage, Register)

        root.geometry("800x600")
        root.configure(background="white")
        style = ttk.Style()
        style.configure('TButton', 
                foreground='green', 
                background='white', 
                font=('Arial', 15, 'bold'), 
                bordercolor='green', 
                focusthickness=3, 
                focuscolor='green', 
                relief='flat', 
                highlightthickness=10, 
                highlightcolor='green', 
                highlightbackground='green', 
                bd=20)

        style.configure('TEntry', 
                foreground='green', 
                background='white', 
                font=('Arial', 15, 'bold'), 
                bordercolor='white', 
                focusthickness=3, 
                focuscolor='white', 
                relief='flat', 
                highlightthickness=10, 
                #highlightcolor='', 
                #highlightbackground='green', 
                bd=20)

        style.configure('TLabel', 
                foreground='green', 
                background='black', 
                font=('Arial', 15))

        
        
        
        for F in tpl:
            frame = F(root, self)
            frame.configure(bg="white", height=600, width =800)
            frame.pack_propagate(0)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

      
        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def update_frame(self, page):
        frame = page(self.root, self)
        frame.configure(bg="white", height=600, width = 800)
        frame.pack_propagate(0)
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
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        label = ttk.Label(self, text="Bienvenido")
        label.pack()
        button = ttk.Button(self, text="Iniciar sesión", command=lambda: controller.show_frame(LoginWindow))
        button.pack()
        button = ttk.Button(self, text="Registrarse", command=lambda: controller.show_frame(Register))
        button.pack()

#Agregar funcionalidades a distintos botones, o añadir mensajes en pantalla
class Home(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        welcome = ttk.Label(self, text="Bienvenido, " + controller.username)
        welcome.grid()
        label = ttk.Label(self, text="Búsqueda de canciones")
        label.grid()
        query = ttk.Entry(self)
        query.grid()
        button = ttk.Button(self, text="buscar", command=lambda: self.search(query.get()))
        button.grid()
        self.tags = run(get_toptags)
        #print(tags[0]["tags"])
        logout = ttk.Button(self, text="Cerrar Sesión", command=self.log_out)
        logout.grid()
        taglabel = ttk.Label(self, text="Categorías musicales")
        taglabel.grid()

        count = 0;
        for i in range(5):
            for j in range(5):
                tg = self.tags[count]; 
                ttk.Button(self, text=tg["tags"]["name"], width=10, command=lambda tg = tg: self.chooseTag(tg)).grid(column= i, row= j+10)
                count += 1;                
                
            
    def log_out(self):        
        self.controller.username = None
        self.controller.password = None
        self.controller.uid = None
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
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        button = ttk.Button(self, text="atras", command=lambda: controller.show_frame(Home))
        button.pack()
        song = controller.song
        if (song != None):
            srchresult = tk.Button(self, text=song["song"]["name"] + " | "+ song["artist"]["name"], command=lambda:controller.songPage(Search))
            srchresult.pack()

class Song(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        self.song = controller.song
        button = ttk.Button(self, text="atras", command=lambda: controller.back())
        button.pack()
        button = ttk.Button(self, text="Inicio", command=lambda: self.returnHome())
        button.pack()
        name = ttk.Label(self, text=controller.song["song"]["name"])
        artist = ttk.Label(self, text=controller.song["artist"]["name"])
        name.pack()
        artist.pack()
        ttk.Label(self, text="Album: " + controller.song["album"]["name"]).pack()
        if int(controller.song["song"]["duration"]) > 0:
            ttk.Label(self, text="Duración: " + controller.song["song"]["duration"]).pack()
        ttk.Label(self, text="Reproducciones: " + controller.song["song"]["playcount"]).pack()
        ttk.Label(self, text="Oyentes: " + controller.song["song"]["listeners"]).pack()
        
        
        label = ttk.Label(self, text="\ncanciones similares:")
        label.pack()
        similars = run(get_similar_songs, song=controller.song["song"]["name"])
        
        for i in range(len(similars)):
            s = similars[i]
            #print(s["song"]["name"])
            ttk.Button(self, text=s["song"]["name"]+ " | "+ s["artist"]["name"], command=lambda s=s: controller.select(s, self)).pack()

    def returnHome(self):
        self.controller.prevFrame.clear()
        self.controller.song = None
        self.controller.show_frame(Home)


class Tag(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        self.tag = controller.tag
        button = ttk.Button(self, text="Inicio", command=lambda: self.returnHome())
        button.pack()
        label = ttk.Label(self, text=self.tag["tags"]["name"] + "\nListado de Canciones")
        label.pack()
        
        songs = run(get_songs_bytag, tag=self.tag["tags"]["name"])
        for i in range(len(songs)):
            s = songs[i]
            print(s["song"]["name"])
            ttk.Button(self, text=s["song"]["name"] + " | "+ s["artist"]["name"], command=lambda s=s: controller.select(s, Tag)).pack()

    def returnHome(self):
        self.controller.prevFrame.clear()
        self.controller.song = None
        self.controller.show_frame(Home)


        
        
        
class LoginWindow(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
 #       self.root = root
#        self.root.title("Inicio de sesión")

        self.username_label = ttk.Label(self, text="Usuario")
        self.username_label.pack()

        self.username_entry = ttk.Entry(self)
        self.username_entry.pack()

        self.password_label = ttk.Label(self, text="Contraseña")
        self.password_label.pack()

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = ttk.Button(self, text="Iniciar sesión", command=self.login)
        self.login_button.pack()
        self.back_button = ttk.Button(self, text="Regresar", command=lambda: controller.show_frame(StartPage))
        self.back_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Aquí debes verificar las credenciales del usuario. Este es solo un ejemplo.

        u = run(login, name=username, password=password)
        
        if len(u) > 0:
            messagebox.showinfo("Inicio de sesión exitoso", "¡Bienvenido, " + username + "!")
            #print(u[0]["user"]["name"])
            self.controller.username = u[0]["user"]["name"]
            self.controller.password = u[0]["user"]["password"]
            self.controller.uid = u[0]["user"]["id"]
            self.controller.update_frame(Home)
            self.controller.show_frame(Home)
            
        else:
            messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos")

class Register(tk.Frame):
    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.controller = controller
        self.username_label = ttk.Label(self, text="Ingrese nombre de usuario:")
        self.username_label.pack()

        self.username_entry = ttk.Entry(self)
        self.username_entry.pack()

        self.password_label = ttk.Label(self, text="Ingrese contraseña:")
        self.password_label.pack()

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()

        self.password2_label = ttk.Label(self, text="Confirme contraseña:")
        self.password2_label.pack()

        self.password2_entry = ttk.Entry(self, show="*")
        self.password2_entry.pack()

        self.login_button = ttk.Button(self, text="Crear Usuario", command=self.verify)
        self.login_button.pack()

        self.back_button = ttk.Button(self, text="Regresar", command=lambda: controller.show_frame(StartPage))
        self.back_button.pack()

    def verify(self):
        user = self.username_entry.get()
        password = self.password_entry.get()
        password2 = self.password2_entry.get()
        if (password != password2):
            messagebox.showerror("Error de registro","¡Las contraseñas no coinciden!")
            return
        if (user == ""):
            messagebox.showerror("Error de registro","¡Nombre de usuario vacío!")
            return
        pr = run(check_user, name=user)
        print(pr)
        if len(pr) == 0:
            run(sign_up, name=user, password=password)
            messagebox.showinfo("Registro exitoso", "¡Creación exitosa de usario!")
            self.controller.show_frame(StartPage)
        else:
            messagebox.showerror("Error de registro", "El nombre de usuario ya está en uso")
            
        


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()




    
