## COMPILADOR DE PORTUGOL PARA JAVA
Projeto de compilador desenvolvido na unidade curricular Teoria da Computação e Compiladores do curso de Ciências da Computação. O programa, desenvolvido em Python, recebe um código fonte em Portugol como entrada e gera um código objeto em Java como saída.

## Execução
Para executar as fases do compilador execute o arquivo "main.py" na pasta raiz. Ele irá executar os scripts das fases de frontend e backend do compilador, contidas nas pastas do programa.

Após finalizar o processo de tradução, o programa irá gerar como saída "codigo_objeto.java" na pasta raiz do programa, contendo um script de saída correspondente ao "codigo_fonte", também na pasta raiz.

## Gramática da linguagem Portugol
  **Tipos de variável**  
    - inteiro: número inteiro  
    - decimal: número decimal  

  **Declaração de variável**  
    *Sintaxe*: <tipo_variavel> <identificador>;  
    *Exemplo:* int idade;  
  
  **Atribuição de variável**  
    *Sintaxe:* <identificador> := <expressao>  

    *Exemplo:*
      idade = 37;  
  
  **Estrutura condicional**  
    *Sintaxe:* 
      se (<expressao> <operador_relacao> <expressao>) {
        // comando a executar
      } senao {
        // comando a executar
      }

    *Exemplo:*
      se (idade >= 18) {
        escreva("Maior de idade.")
      } senao {
        escreva("Menor de idade.")
      }
    
  **Operadores de Relação**