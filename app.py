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