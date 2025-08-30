import java.util.Scanner;

public class mio {
    public static void main(String[] args){
    Scanner sc = new Scanner(System.in);

    System.out.print("¿Cuál es el nombre de tu película favorita? ");
    String pelicula = sc.nextLine();

    System.out.print("¿Cuántas veces la has visto? ");
    int veces = sc.nextInt();

    System.out.println("Tu película favorita es " + pelicula + "y la has visto " + veces + " veces");
    System.out.println("El próximo año la verás " + (veces +1) + " veces más");
    }

}
