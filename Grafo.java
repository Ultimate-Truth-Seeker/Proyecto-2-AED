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
}