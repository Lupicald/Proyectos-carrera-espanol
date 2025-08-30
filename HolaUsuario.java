import java.util.Scanner;

public class HolaUsuario {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Escribe tu nombre: ");
        String nombre = sc.nextLine();

        System.out.print("¿Cuántos años tienes? ");
        int edad = sc.nextInt();
        sc.nextLine();

        System.out.print("Cuál es tu lenguaje favorito de programación?");
        String lenguaje = sc.nextLine();

        System.out.println("Hola " + nombre + ", tienes " + edad + " años.");
        System.out.println("El próximo año tendrás " + (edad + 1) + " 🎉");
        System.out.println("Tu lenguaje favorito es " + lenguaje);

        sc.close();
    }
}
