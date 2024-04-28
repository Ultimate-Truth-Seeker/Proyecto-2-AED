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

    }
}
