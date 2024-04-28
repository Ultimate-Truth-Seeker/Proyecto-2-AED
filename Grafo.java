import java.util.*;

class Grafo<T> {
    private int numVertices;
    private LinkedList<T> adjListArray[];

    // constructor
    Grafo(int numVertices) {
        this.numVertices = numVertices;

        // define el tamaño del array como número de vértices
        adjListArray = new LinkedList[numVertices];

        // Crea una nueva lista para cada vértice de tal manera que se puedan almacenar nodos adyacentes
        for(int i = 0; i < numVertices ; i++){
            adjListArray[i] = new LinkedList<>();
        }
    }

    // Agrega una arista a un grafo no dirigido
    void addEdge(T src, T dest) {
        // Agrega una arista de src a dest.
        adjListArray[src].add(dest);

        // Dado que el grafo es no dirigido, agrega una arista de dest a src también
        adjListArray[dest].add(src);
    }

    // Una función de utilidad para imprimir la representación de la lista de adyacencia del grafo
    void printGraph() {
        for(int v = 0; v < numVertices; v++) {
            System.out.println("Lista de adyacencia del vértice "+ v);
            System.out.print("head");
            for(T pCrawl: adjListArray[v]){
                System.out.print(" -> "+pCrawl);
            }
            System.out.println("\n");
        }
    }
}