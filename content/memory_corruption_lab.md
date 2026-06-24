Title: Lab de memory corruption da minha disciplina de segurança
Date: 2026-06-22
Category: writeups
Slug: memory-corruption-lab 
status: published

# Lab de memory corruption da minha disciplina de segurança

Antes de tudo, um breve resumo: essa atividade consiste em explorar um binário e burlar o seu sistema de verificação. O binário é um executável ELF de 32 bits (x86), compilado sem proteções modernas de stack.

A análise foi feita em um ambiente nativo Linux (Debian) e dentro da ferramenta GDB, com o ASLR desativado conforme exigido pelo enunciado da atividade.

**obs: o binario teve o seu nome alterado para esse writeup**
![Pasted image 20260619150041.png]({static}/images/Pasted%20image%2020260619150041.png)
## Passo 0: Contexto

Antes de qualquer coisa, vamos ver o comportamento padrão do binário.
![Pasted image 20260622230611.png]({static}/images/Pasted%20image%2020260622230611.png)
O programa nunca autoriza o acesso pelo caminho normal, não importa o que seja digitado. Ou seja, a única forma de ter acesso é explorando uma vulnerabilidade no código.

## Passo 1: Análise estática

Primeiramente eu listei todas as funções utilizando o comando `info functions`.
![Pasted image 20260621131335.png]({static}/images/Pasted%20image%2020260621131335.png)
As funções  que eu queria desassemblar eram: `main`, `login` e `grant_access`. Os "desassemble" de `main` e `grant_access` não revelaram nada que poderia ser explorado. Porém, a função `login` revelou um problema. Também notei alguns elementos de **libc**, o que pode abrir margem para a técnica **ret2libc**.
![Pasted image 20260621131821.png]({static}/images/Pasted%20image%2020260621131821.png)
A instrução `0x080485c4 <+31>: lea -0x48(%ebp),%eax` calcula o endereço do buffer local (de 72 bytes). Em seguida, a instrução `0x080485c7 <+34>: mov %eax,(%esp)` coloca esse endereço como argumento na pilha, para então a instrução `0x080485ca <+37>: call 0x80483b0 <gets@plt>` chamar `gets()` passando esse buffer.

O problema desse fluxo é: `gets()` não recebe nenhum parâmetro de tamanho máximo, diferente de funções seguras como `fgets()`, e portanto não há nenhuma verificação do limite do buffer durante a leitura da entrada do usuário, o que caracteriza uma vulnerabilidade de buffer overflow (especificamente um stack based buffer overflow).

## Passo 2: Preparando e executando o exploit

A lógica do ataque é: qualquer entrada maior que 72 bytes sobrescreve sequencialmente o EBP salvo e, em seguida, o endereço de retorno armazenado na pilha. Em outras palavras, **ret2func**.

Para determinar exatamente quantos bytes são necessários até alcançar o endereço de retorno, soma-se o tamanho do buffer ao tamanho do EBP salvo:

| Componente          | Tamanho         | Origem                 |
| ------------------- | --------------- | ---------------------- |
| Buffer local        | 72 bytes (0x48) | `lea -0x48(%ebp),%eax` |
| EBP Salvo           | 4 bytes         | `push %ebp` no prólogo |
| Total até o retorno | 76 bytes        | 72 + 4                 |

Para além do valor calculado estaticamente, utilizei, um cyclic pattern de 100 bytes via pwntools. O EIP no momento do crash exibiu o valor ``0x61746161``, e o ``cyclic_find``retornou 74. Porém, já adiantando o resultado, o exploit com 74 bytes resultou em segfault sem imprimir a flag.

![Pasted image 20260622231944.png]({static}/images/Pasted%20image%2020260622231944.png)

Honestamente, não tenho certeza do motivo dessa divergência de valores. Mas (spoiler!) o exploit funcionou corretamente com 76 bytes. Então, para todos os efeitos, o nosso offset é de 76 bytes.

O endereço alvo é: **grant_access** em ``0x080484fd``. Como x86 usa little-endian, esse endereço vira `\xfd\x84\x04\x08` no payload. O exploit final fica:

`python3 -c "import sys; sys.stdout.buffer.write(b'A'*76 + b'\xfd\x84\x04\x08')" | /caminho/do/binario`

Ou seja: 76 bytes de preenchimento para chegar até o endereço de retorno, seguidos dos 4 bytes que sobrescrevem esse endereço com `grant_access`.

![Pasted image 20260622232051.png]({static}/images/Pasted%20image%2020260622232051.png)

Como também foi pedido no enunciado, o exploit foi pensado e executado diretamente no terminal, fora do GDB.

A mensagem de "Acesso Negado" ocorre porque o fluxo normal da função `login()` sempre termina em falha, entretanto, ao final da função desviamos o fluxo de execução para `grant_access()`, assim imprimindo a flag. Já a "Falha de segmentação", acredito que seja porque a pilha permanece corrompida após`grant_access()` retornar, mas como isso ocorre após a impressão da flag, não muda nada no resultado.

Flag obtida: FLAG{09f5dafb209fee74}