import java.util.Scanner;
public class Main { public static void main(String[] args) {
Scanner scanner = new Scanner(System.in);
double notaA1;
double notaA2;
double notaA3;
double soma_notas;
double media;
String aluno;
System.out.println("PROGRAMA PARA CALCULAR A MÉDIA DO SEMESTRE");
System.out.println("Digite o nome do aluno: ");
aluno = scanner.nextLine();
System.out.println("Digite a nota da A1");
notaA1 = scanner.nextDouble();
System.out.println("Digite a nota da A2");
notaA2 = scanner.nextDouble();
System.out.println("Digite a nota da A3");
notaA3 = scanner.nextDouble();
soma_notas = notaA1 + notaA2 + notaA3;
media = soma_notas / 3.0;
if (media >= 7.0) {
System.out.println("Média: " + media);
System.out.println(aluno + " aprovado.");
} else {
System.out.println("Média: " + media);
System.out.println(aluno + " reprovado.");
}
}}