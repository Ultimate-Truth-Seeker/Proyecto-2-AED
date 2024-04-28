import java.util.*;

class Grafo<T> {
    private int numVertices;
    private Map<T, LinkedList<T>> adjList;

    // constructor
    Grafo(List<T> Vertices) {
        this.numVertices = Vertices.size();

        adjList = new HashMap<>();

        // Crea una nueva lista para cada vértice de tal manera que se puedan almacenar nodos adyacentes
        for(int i = 0; i < numVertices ; i++){
            adjList.put(Vertices.get(i), new LinkedList<>());
        }
    }

    // Agrega una arista a un grafo no dirigido
    void addEdge(T src, T dest) {
        if (!adjList.containsKey(src)) {
            adjList.put(src, new LinkedList<>());
        }
        if (!adjList.containsKey(dest)) {
            adjList.put(dest, new LinkedList<>());
        }

        // Agrega una arista de src a dest.
        adjList.get(src).add(dest);

        // Dado que el grafo es no dirigido, agrega una arista de dest a src también
        adjList.get(dest).add(src);
    }

    // Una función de utilidad para imprimir la representación de la lista de adyacencia del grafo
    void printGraph() {;
        for(T v : adjList.keySet()) {
            System.out.println("Lista de adyacencia del vértice "+ v);
            System.out.print("head");
            for(T pCrawl: adjList.get(v)){
                System.out.print(" -> "+pCrawl);
            }
            System.out.println("\n");
        }
    }
}