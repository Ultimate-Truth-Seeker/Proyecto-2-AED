import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String args[]) {
        // crea el grafo dado en la figura anterior
        Grafo<String> graph = new Grafo<String>(List.of());
        graph.addEdge("Usuario1", "Canción1");
        graph.addEdge("Usuario1", "Canción2");
        graph.addEdge("Usuario2", "Canción1");
        graph.addEdge("Usuario2", "Canción3");
        graph.addEdge("Canción1", "Usuario1");
        graph.addEdge("Canción1", "Usuario2");
        graph.addEdge("Canción2", "Usuario1");
        graph.addEdge("Canción3", "Usuario2");

        // imprime la representación de la lista de adyacencia del grafo anterior
        graph.printGraph();

    }

    private static void conexion(Grafo<String> grafo, double umbral) {
        
        List<Cancion> canciones = new ArrayList<>();


    }
}