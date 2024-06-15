## COMPILADOR DE PORTUGOL PARA JAVA
Projeto desenvolvido na unidade curricular Teoria da Computação e Compiladores do curso de Ciências da Computação. O programa, desenvolvido em Python, recebe um código fonte em Portugol como entrada e gera um código objeto em Java como saída.

## Execução
*Requisitos*: ambiente Python instalado

Para executar o processo de tradução execute o arquivo "main.py" na pasta raiz.

Ele irá executar os scripts das fases de frontend e backend do compilador, gerando os arquivos **tokens.txt**, **ast.txt**, **tabela_simbolos.txt**, **codigo_intermediario.txt** e por fim o **codigo_final.java**, contendo um script correspondente ao **codigo_fonte.txt**, presente na pasta raiz do projeto.

## Gramática da linguagem Portugol  
  **Identificadores:**  
    Devem iniciar com uma letra minúscula ou underline (_) e não podem possuir caracteres especiais.

  **Tipos de variável:**  
    texto, inteiro, decimal

  **Palavras-chave:**  
    programa, fimprog, leia, escreva, se, senao, enquanto, para

  **Sintaxe da declaração de variável:**  
    &lt;tipo_variavel&gt; &lt;identificador&gt;;  

    *Exemplo:*
      int idade;  

  *Observação:* você deve declarar a variável antes de atribuir o valor.
  
  **Operador de atribuição:**  
    :=

  **Sintaxe da atribuição de variável:**  
    &lt;identificador&gt; := &lt;expressao&gt;  

    *Exemplo:* 
      idade := 37;  
  
  **Operadores Aritméticos:**  
    +, -, *, /  
    
    o + também pode ser usado como operador de concatenação
  
  **Operadores de Relação:**  
    ==, !=, >=, <=, >, <

  **Sintaxe da estrutura condicional:**  
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

  **Sintaxe da estrutura de repetição enquanto:**  
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

  **Sintaxe da estrutura de repetição para:**  
    para (&lt;declaracao&gt;; &lt;expressao&gt;; &lt;expressao&gt;) {
      comando a executar...
    }

    *Exemplo:*
      inteiro i;
      para (i := 10; i >= 0; i - 1) {
        escreva(i);
      }

  **Operadores de comentário:**  
    //, \*...\*

      *Exemplo:*
        // comentário utilizando somente uma linha

        * comentário que pode
          utilizar múltiplas linhas *