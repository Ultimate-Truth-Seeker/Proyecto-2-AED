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