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
