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


def add_song_tx(tx, count, name, duration, listeners, artist, playcount, album, albumartist, tags):
    
    
    # Create new Person node with given name, if not exists already
    result = tx.run("""
        MERGE (p:song {name: $name, duration: $duration, listeners: $listeners, playcount: $playcount, id: $count})
        RETURN p.id AS id
        """, name=name, duration = duration, listeners=listeners, playcount= playcount, count=count
    )
    ID = result.single()["id"]
    #print(ID)

    # Obtain most recent organization ID and the number of people linked to it
    result = tx.run("""
        MATCH (o:artist {name: $artist})
        RETURN o.name AS name, COUNT{(p:song)-[r:from]->(o)} AS songs
        
    """, artist = artist)
    org = result.single()

    if org is not None and org["songs"] == 0:
        raise Exception("Most recent artist is empty.")
        # Transaction will roll back -> not even Person is created!

    # If org does not have too many employees, add this Person to that
    if org is not None:
        result = tx.run("""
            MATCH (o:artist {name: $artist})
            MATCH (p:song {name: $name, id: $ID})
            MERGE (p)-[r:from{cost: 1}]->(o)
            RETURN $org_name AS name
            """, artist=artist, name=name, org_name= org["name"], ID=ID
        )

    # Otherwise, create a new Organization and link Person to it
    else:
        result = tx.run("""
            MATCH (p:song {name: $name, id: $ID})
            CREATE (o:artist {name: $artist})
            MERGE (p)-[r:from{cost: 1}]->(o)
            RETURN o.name AS artistnamename
            """, name=name, artist = artist, ID=ID
        )

    if album != "":
        #find album
        result = tx.run("""
            MATCH (o:album {name: $album, artist: $albumartist})
            RETURN o.name AS name, COUNT{(p:song)-[r:from]->(o)} AS songs, COUNT{(o)-[r:from]->(q:artist)} AS artists
            
        """, album=album, albumartist=albumartist 
                        )
        org = result.single()

        if org is not None and (org["songs"] == 0 or org["artists"] == 0):
            raise Exception("Most recent album is empty.")
            # Transaction will roll back -> not even Person is created!

        # If org does not have too many employees, add this Person to that
        if org is not None:
            result = tx.run("""
                MATCH (o:artist {name: $albumartist})
                MATCH (p:song {name: $name, id: $ID})
                MATCH (q:album {name: $album, artist: $albumartist})
                MERGE (p)-[r:from{cost: 1}]->(q)
                MERGE (q)-[s:from{cost: 1}]->(o)
                RETURN $org_name AS name
                """, albumartist=albumartist, name=name, org_name= org["name"], ID=ID, album=album
            )

        # Otherwise, create a new Organization and link Person to it
        else:
            result = tx.run("""
                MATCH (p:song {name: $name, id: $ID})
                MATCH (q:artist {name: $albumartist})
                CREATE (o:album {name: $album, artist: $albumartist})
                MERGE (p)-[r:from {cost: 1}]->(o)
                MERGE (o)-[s:from {cost: 1}]->(q)
                RETURN o.name AS artistname
                """, name=name, album=album, ID=ID, albumartist=albumartist
            )

    for tag in tags:
        #find album
        result = tx.run("""
            MATCH (o:tag {name: $tag})
            RETURN o.name AS name, COUNT{(p:song)-[r:is ]-(o)} AS songs
            
        """, tag=tag, 
                        )
        org = result.single()

        if org is not None and (org["songs"] == 0):
            raise Exception("Most recent tag is empty.")
            # Transaction will roll back -> not even Person is created!

        # If org does not have too many employees, add this Person to that
        if org is not None:
            result = tx.run("""
                MATCH (p:song {name: $name, id: $ID})
                MATCH (o:tag {name: $tag})
                MERGE (p)-[r:is {cost: 1}]-(o)
                RETURN $org_name AS name
                """, tag=tag, name=name, org_name= org["name"], ID=ID
            )

        # Otherwise, create a new Organization and link Person to it
        else:
            result = tx.run("""
                MATCH (p:song {name: $name, id: $ID})
                CREATE (o:tag {name: $tag})
                MERGE (p)-[r:is{cost: 1}]-(o)
                RETURN o.name AS name
                """, name=name, tag=tag, ID=ID
            )

    
    return "done"

def find_similarity(tx, count, total):

    for i in range(count, total + 1):
        if (i != count):
            result = tx.run("""
            MATCH (s:song {id: $count})
            MATCH (t:song {id: $i})
            CALL apoc.algo.dijkstra(s, t, "is|from" , "cost")
            YIELD weight
            RETURN weight AS w, COUNT{(s)-[r:similar]-(t)} AS similar, s.duration AS d1, t.duration AS d2, s.listeners AS l1, t.listeners AS l2, s.playcount AS p1, t.playcount AS p2
            """, i=i, count=count
            )
            dat = result.single()
            w = dat["w"]
            d1 = int(dat["d1"]); d2 = int(dat["d2"]); dw = 0
            if (d1 + d2)> 0:
                dw = (2*(d1-d2)/(d1+d2))**2 * 0.05
            l1 = int(dat["l1"]); l2 = int(dat["l2"]); lw = 0
            if (l1 + l2)> 0:
                lw = (2*(l1-l2)/(l1+l2))**2 * 0.5
            p1 = int(dat["p1"]); p2 = int(dat["p2"]); pw = 0
            if (p1 + p2) >0:
                pw = (2*(p1-p2)/(p1+p2))**2 * 0.5

            vect =  (dw + lw + pw )**0.5
            weight = 1/w * (1-vect)
            #print(weight)

            if dat is not None and dat["similar"] > 0:
                result = tx.run("""
                MATCH (s:song {id: $count})
                MATCH (t:song {id: $i})
                MATCH (s)-[r:similar]-(t)
                SET r.weight = $weight
                RETURN r.weight AS w
                """, i=i, count=count, weight=weight
                )
            else:
                result = tx.run("""
                MATCH (s:song {id: $count})
                MATCH (t:song {id: $i})
                MERGE (s)-[r:similar{weight: $weight}]-(t)
                RETURN s.id AS Id
                """, i=i, count=count, weight=weight
                )
    
    
    return "done"

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
                org_id = session.execute_write(add_song_tx, count, name, duration, listeners, artist, playcount, album, albumartist, tags)

            for j in range(1, total):
                x = session.execute_write(find_similarity, j, total)

            print("done")
                