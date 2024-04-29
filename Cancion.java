import java.util.Arrays;
import java.util.Map;

public class Cancion {
    private String nombre;
    private double[] caracteristicas;

    // Constructor
    public Cancion(String nombre, double[] caracteristicas) {
        this.nombre = nombre;
        this.caracteristicas = caracteristicas;
    }

    // Getters
    public String getNombre() {
        return nombre;
    }

    public double[] getCaracteristicas() {
        return caracteristicas;
    }

    // Método para calcular la distancia euclidiana
    public double calcularDistanciaEuclidiana(Cancion otraCancion) {
        double[] otrasCaracteristicas = otraCancion.getCaracteristicas();
        double suma = 0.0;
        for (int i = 0; i < this.caracteristicas.length; i++) {
            suma += Math.pow(this.caracteristicas[i] - otrasCaracteristicas[i], 2);
        }
        return Math.sqrt(suma);
    }

    // Método para crear un vector a partir de los mapas dados fields y weights
    public static double[] makeVector(Map<String, Object> fields, Map<String, Object> weights) {
        double[] vector = new double[fields.size()];

        int count = 0;
        for (String field : fields.keySet()) {
            if (fields.get(field) instanceof Number) {
                vector[count] = (double) fields.get(field) * (double) weights.get(field);
            } else if (fields.get(field).getClass() == String.class) {
                if (!((Map) weights.get(field)).containsKey(fields.get(field))) {
                    Double position = ((Map) weights.get(field)).size() + 1.0;
                    ((Map) weights.get(field)).put(fields.get(field), position);
                }
                vector[count] = (Double) ((Map) weights.get(field)).get(fields.get(field));
            }
            count ++;
        }
        return vector;
        
    }
}