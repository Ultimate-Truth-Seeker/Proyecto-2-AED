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

