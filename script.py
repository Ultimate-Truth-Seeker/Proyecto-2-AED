import requests
import json

def obtener_datos_cancion(api_key, artista, cancion):
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&artist={artista}&track={cancion}&format=json"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

def obtener_datos_global(api_key, country, limit):
    url = f"http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={country}&api_key={api_key}&limit={limit}&format=json"
    response = requests.get(url)
    data = json.loads(response.text)
    return data

api_key = "d6e82d0ac7993c7a355900d8fc275fad"  # Reemplaza esto con tu API key de Last.fm

total = 150

tracks = obtener_datos_global(api_key, "guatemala", total)["tracks"]["track"]



import dotenv
import os
from neo4j import GraphDatabase

load_status = dotenv.load_dotenv("Neo4j-07e5e662-Created-2024-05-20.txt")
if load_status is False:
    raise RuntimeError('Environment variables not loaded.')

URI = "neo4j+ssc://07e5e662.databases.neo4j.io"
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    

    with driver.session(database="neo4j") as session:
            count = 0
            for song in tracks:
                count +=1;
                name = song["name"]
                duration = song["duration"]
                listeners = song["listeners"]
                artist = song["artist"]["name"]
                datos = obtener_datos_cancion(api_key, artist, name)["track"]
                album = ""; albumartist = "";
                try:
                    album = datos["album"]["title"]
                    albumartist = datos["album"]["artist"]
                except:
                    "no album"
                playcount = datos["playcount"]
                tagsraw = datos["toptags"]["tag"]
                tags = []
                for tag in tagsraw:
                    tags.append(tag["name"])
                
            print("done")
                