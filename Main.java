import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.io.File;

public class Main {

    static String csvFile = "datosdeprueba.csv";
    static double umbral = 0.2;
    static Map<String, Object> weights = new HashMap<>();
    
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

    private static void conexion(Grafo<Cancion> grafo, double umbral) {
        
        List<Cancion> canciones = new ArrayList<>();
        canciones.addAll(grafo.getAdjList().keySet());

        //Calcula la similitud de las canciones
        double[][] similitud = new double[canciones.size()][canciones.size()];
        for (int i = 0; i < canciones.size(); i++) {
            Cancion cancion1 = canciones.get(i);
            for (int j = i; j < canciones.size(); j++) {
                Cancion cancion2 = canciones.get(j);
                similitud[i][j] = cancion1.calcularDistanciaEuclidiana(cancion2);
                //Esto es para que no sea direccionado, y se puedan correlacionar
                similitud[j][i] = similitud[i][j]; 
            }
        }
        
        //Conecta las canciones basándose en la similitud del umbral
        for (int i = 0; i < similitud.length; i++) {
            for (int j = i + 1; j < similitud[i].length; j++) {
                if (similitud[i][j] >= umbral) {
                    grafo.addEdge(canciones.get(i), canciones.get(j));
                }
            }
        }
    }

    private static Grafo<Cancion> loadSongs() {
        List<Cancion> canciones = new ArrayList<>();
        try (Scanner sc = new Scanner(new File(csvFile))) {
            boolean FirstRow = true;

            while (sc.hasNextLine()) {
                Scanner sl = new Scanner(sc.nextLine());
                sl.useDelimiter(",");
                if (FirstRow) {
                    FirstRow = false;
                    continue;
                }
                Map<String, Object> values = new HashMap<>(); 
                String name = "";
                for (String field : weights.keySet()) {
                    if (field.equals("Name")) {
                        values.put(field, 0);
                        name = sl.next();
                    } else {
                        values.put(field, sl.next()); 
                    }
                }
                canciones.add(new Cancion(name, Cancion.makeVector(values, weights)));
            }

            return new Grafo<>(canciones);
            
        } catch (Exception e) {
            System.err.println("* Error de lectura");
            return null;
        }
    }
}