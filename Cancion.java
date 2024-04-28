import java.util.Arrays;

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
}
