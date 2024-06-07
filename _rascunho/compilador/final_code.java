import java.util.Scanner;
public class Main { public static void main(String[] args) {
Scanner scanner = new Scanner(System.in);
double notaA1;
double notaA2;
double notaA3;
double media;
System.out.println("PROGRAMA PARA CALCULO DA MÉDIA SEMESTRAL DO ALUNO");
System.out.println("Digite a nota da A1");
notaA1 = scanner.nextDouble();
System.out.println("Digite a nota da A2");
notaA2 = scanner.nextDouble();
System.out.println("Digite a nota da A3");
notaA3 = scanner.nextDouble();
media = notaA1 + notaA2 + notaA3;
media = media / 3.0;
System.out.println(media);
}}