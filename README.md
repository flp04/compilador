## COMPILADOR DE PORTUGOL PARA JAVA
Projeto desenvolvido na unidade curricular Teoria da Computação e Compiladores do curso de Ciências da Computação. O programa, desenvolvido em Python, recebe um código fonte em Portugol como entrada e gera um código objeto em Java como saída.

## Execução
Para executar as fases do compilador execute o arquivo "main.py" na pasta raiz. Ele irá executar os scripts das fases de frontend e backend do compilador, contidos nas pastas do programa.

Após finalizar o processo de tradução, o programa irá criar os arquivos "tokens.txt", "semantyc_analyzer.txt", "tabela_simbolos.txt, decorrentes das análises do frontend, e como saída o "codigo_objeto.java" contendo um script correspondente ao "codigo_fonte.txt".

## Gramática da linguagem Portugol  
  **Tipos de variável:**  
    texto, inteiro, decimal

  **Palavras-chave:**  
    programa, fimprog, leia, escreva, se, senao, enquanto

  **Sintaxe da declaração de variável:**  
    &lt;tipo_variavel&gt; &lt;identificador&gt;;  

    *Exemplo:*
      int idade;  
  
  **Operador de atribuição**  
    :=

  **Sintaxe da atribuição de variável:**  
    &lt;identificador&gt; := &lt;expressao&gt;  

    *Exemplo:* 
      idade := 37;  
  
  **Operadores Aritméticos**  
    +, -, *, /  
    
    o + também pode ser usado como operador de concatenação
  
  **Operadores de Relação**  
    ==, !=, >=, <=, >, <

  **Sintaxe da estrutura condicional**  
    se (&lt;expressao&gt;) {
      comando a executar...
    } senao {
      comando a executar...
    }

    *Exemplo:*
      se (idade >= 18) {
        escreva("Maior de idade.")
      } senao {
        escreva("Menor de idade.")
      }

  **Sintaxe da estrutura de repetição**
    enquanto (&lt;expressao&gt;) {
      comando a executar...
    }

    *Exemplo:*
      inteiro contador;
      contador := 0;
      enquanto (contador <= 10) {
        escreva(contador);
        contador := contador + 1;
      }

  **Operadores de comentário**  
    //, \*...\*

      *Exemplo:*
        // comentário utilizando somente uma linha

        * comentário que pode
          utilizar múltiplas linhas *