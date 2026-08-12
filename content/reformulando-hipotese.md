Title: Explicitando a hipótese científica da IC  
Date: 2026-08-07  
Category: experimentos  
Slug: hipotese-cientifica-ic  
status: published

# Explicitando a hipótese científica da IC

Originalmente, esse post abordaria tanto a discussão sobre qual caminho a IC vai tomar quanto as atualizações feitas na primeira versão da arquitetura. Porém, a primeira parte ficou maior do que eu esperava. Por isso, decidi separar as coisas.

O próximo post será sobre a evolução da arquitetura. Neste, quero responder uma pergunta anterior a qualquer implementação:

> **O que exatamente estamos tentando investigar com essa arquitetura?**

---

## Revisando a revisão

No [post anterior](https://lovepxdro.github.io/sec-lounge/experimentos/arquitetura-dual-gam/), dediquei uma parte para revisar a proposta da IC como um todo. Como resultado, passei a pensar no projeto como:

> **Um ambiente experimental para pesquisa em defesa adaptativa baseada em aprendizado adversarial.**

Ainda acredito que essa descrição seja correta. Mas acredito que uma coisa ainda ficou em aberto:

> Um ambiente experimental para investigar exatamente o quê?

---

## O problema não é detectar DDoS

Depois de executar diversas vezes o ciclo de treinamento, um número chama atenção.

Antes mesmo do ciclo adversarial, o defensor já alcança aproximadamente **99,9% de acurácia** sobre o conjunto de teste convencional.

Inicialmente, isso parece estranho. Se o detector já consegue classificar DDoS quase perfeitamente antes mesmo de interagir com o atacante, qual seria a utilidade de continuar treinando os dois modelos?

Mas essa interpretação olha para a métrica errada. A tarefa da IC nunca foi construir um detector melhor de DDoS.

DDoS foi escolhido justamente como primeiro caso experimental por ser um ataque relativamente simples de identificar nesse cenário. Isso permite validar a arquitetura sem começar pelo problema de classificação mais complexo possível.

A acurácia de ~99,9%, portanto, funciona quase como uma sanity check:

```text
O defensor consegue detectar DDoS convencional?
                ↓
              sim
```

A pergunta seguinte é mais interessante:

> Um defensor que detecta quase perfeitamente DDoS convencional pode ser enganado por uma variante construída especificamente para explorar seu comportamento?

E a resposta observada até agora também é sim.

Durante o ciclo adversarial, um detector com alta acurácia convencional chegou a sofrer taxas elevadas de evasão quando exposto às perturbações produzidas pelo atacante.

Isso muda a interpretação do problema.

**Alta acurácia não significa necessariamente robustez adversarial.**

---

## O que o ciclo atual realmente demonstra?

O atacante atual não inventa um novo tipo de ataque.

Ele recebe amostras reais de DDoS e aprende pequenas perturbações capazes de fazer o defensor classificá-las incorretamente.

O fluxo é aproximadamente:

```text
DDoS conhecido
      ↓
Atacante
      ↓
Variante adversarial
      ↓
Defensor
      ↓
Evasão ou detecção
      ↓
Defensor aprende com as novas amostras
      ↓
Novo ciclo
```

Isso já permite observar uma dinâmica interessante.

O atacante encontra uma forma de evasão. O defensor aprende a reconhecê-la. Posteriormente, o atacante encontra outras perturbações capazes de voltar a elevar a evasão.

Mas é importante ser preciso sobre o que isso significa.

Hoje conseguimos investigar bem uma pergunta como:

> **Um detector pode se adaptar iterativamente a variantes adversariais construídas para evadi-lo?**

Isso não é exatamente a mesma coisa que perguntar:

> **O sistema consegue detectar ataques nunca vistos anteriormente?**


---

## O que significa um ataque "desconhecido"?

A expressão "ataque desconhecido" é ampla demais. Existem pelo menos três situações diferentes.

A primeira é uma **variante desconhecida de um ataque conhecido**. O defensor conhece DDoS, mas nunca viu aquela determinada combinação de características construída pelo atacante.

A segunda seria uma **nova técnica dentro de uma família conhecida**. Por exemplo, o sistema conhece determinados padrões de injeção, mas recebe uma técnica diferente que ainda pertence à mesma família.

E a terceira seria uma **classe completamente desconhecida**. O sistema nunca foi treinado com nenhum exemplo daquele tipo de ataque.

Esses três problemas não são equivalentes. A arquitetura atual trabalha principalmente com o primeiro.

O atacante conhece uma distribuição ofensiva existente e procura regiões dessa distribuição (ou próximas dela) capazes de explorar vulnerabilidades do defensor.

Portanto, neste momento, seria exagerado afirmar que a arquitetura está produzindo ataques completamente novos.

Uma formulação mais precisa seria falar em:

> **Variantes adversariais não observadas pelo defensor.**

E isso já é suficiente para formular perguntas científicas interessantes.

---

## Então, o que queremos testar?

A pesquisa passa a se organizar em torno de algumas hipóteses progressivas.

### H1 — Vulnerabilidade adversarial

> **Um detector com alta acurácia sobre ataques convencionais continua vulnerável a variantes adversariais desses ataques.**

Essa é a primeira constatação importante.

A acurácia convencional funciona como baseline. O objetivo não é superá-la, mas mostrar que ela não descreve toda a robustez do sistema.

Um defensor pode ter 99% de acurácia e ainda apresentar uma superfície significativa para evasão adversarial.

---

### H2 — Adaptação

> **A exposição contínua às variantes produzidas pelo atacante reduz a capacidade dessas variantes de evadir o defensor.**

Aqui está o núcleo do ciclo adversarial.

O atacante encontra uma variante eficaz.

O defensor é retreinado com ela.

Depois medimos se aquela estratégia continua funcionando.

Se a evasão cai, existe evidência de adaptação.

Mas isso ainda deixa uma pergunta mais importante.

O defensor aprendeu algo geral ou apenas memorizou aquela perturbação específica?

---

### H3 — Generalização

> **Um defensor submetido ao treinamento adversarial contínuo apresenta maior robustez contra variantes adversariais ainda não observadas do que um defensor convencional.**

Essa provavelmente é a hipótese mais importante.

O experimento ideal deixa de comparar apenas a acurácia do mesmo defensor antes e depois do ciclo.

Passamos a comparar dois sistemas:

```text
                 Mesmo treinamento inicial
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
         Defensor A             Defensor B
          baseline               adaptativo
                                    │
                              ciclo adversarial
              │                     │
              └──────────┬──────────┘
                         ↓
                    teste final
```

Os dois seriam avaliados contra:

- ataques convencionais;
    
- variantes adversariais utilizadas durante a adaptação;
    
- variantes adversariais que nenhum dos dois recebeu durante o treinamento.
    

É essa última comparação que interessa especialmente.

Se o defensor adaptativo detectar melhor variantes que ele nunca recebeu diretamente durante o treinamento, então não estamos observando apenas memorização.

Estamos começando a observar **generalização adversarial**.

---

## E onde entra a rede?

Existe ainda uma quarta pergunta, que depende diretamente da evolução da infraestrutura.

Atualmente o ciclo adversarial ocorre majoritariamente no espaço de features.

A GAN produz uma perturbação sobre um vetor do CIC-IDS2017, o defensor avalia esse vetor e, posteriormente, o Translator transforma suas características em parâmetros utilizados pelo Scapy para gerar tráfego real.

Isso cria uma ponte entre aprendizado e rede, mas o ciclo ainda não está completamente fechado.

O experimento futuro precisa conseguir realizar:

```text
Vetor adversarial
       ↓
Translator
       ↓
Pacotes reais
       ↓
Rede
       ↓
Captura do tráfego
       ↓
Extração de features
       ↓
Defensor
```

Isso leva a uma quarta hipótese.

### H4 — Transferência para o ambiente de rede

> **A robustez e a evasão observadas no espaço de features permanecem quando as variantes adversariais são materializadas, transmitidas e novamente observadas como tráfego de rede.**

Essa pergunta é especialmente importante porque existe uma transformação entre os dois espaços.

Um vetor estatisticamente adversarial não necessariamente continua adversarial depois de ser convertido em uma sequência concreta de pacotes.

Descobrir que essa propriedade se mantém seria um resultado. Descobrir que ela se perde também seria.

---

## O papel da arquitetura

Com essas hipóteses, fica mais fácil definir qual é o propósito da arquitetura.

Ela não existe apenas para colocar duas IAs competindo. Também não existe para construir o melhor detector possível de DDoS.

Seu objetivo é fornecer um ambiente controlado no qual seja possível estudar a interação entre **ataque adversarial, adaptação e generalização defensiva**.

A arquitetura deve permitir que diferentes componentes sejam substituídos e comparados:

```text
atacante
    ↓
estratégia de geração adversarial

defensor
    ↓
modelo ou mecanismo de detecção

rede
    ↓
condições experimentais

controle
    ↓
observação, decisão e resposta
```

DDoS é apenas o primeiro caso experimental.

No futuro, outros tipos de ataque, outros métodos de geração adversarial e outros modelos defensivos podem ocupar os mesmos pontos da arquitetura.

Isso também significa que o resultado final da IC não precisa ser:

> "Construímos um detector de DDoS melhor."

Uma conclusão muito mais interessante seria algo como:

> "Construímos um ambiente experimental capaz de avaliar em que condições treinamento adversarial contínuo produz detectores mais robustos e capazes de generalizar para variantes ofensivas ainda não observadas."

A arquitetura passa a ser tanto o artefato desenvolvido quanto o instrumento usado para investigar essas hipóteses.

---

## Onde estamos agora?

A implementação atual já permite observar algumas partes desse problema.

Temos um defensor convencional com alta acurácia.

Temos um atacante capaz de encontrar perturbações que reduzem significativamente essa eficácia.

Temos um ciclo em que o defensor é exposto a essas perturbações e responde a elas.

Também conseguimos materializar características dos vetores adversariais como tráfego dentro de uma rede experimental.

O que ainda falta é transformar esses comportamentos em um protocolo experimental mais rigoroso.

Principalmente:

- comparar explicitamente um defensor baseline com um defensor adaptativo;
    
- separar variantes utilizadas durante a adaptação de variantes reservadas para avaliação;
    
- medir generalização, e não apenas acurácia convencional;
    
- fechar o ciclo entre tráfego real, extração de features e decisão do defensor;
    
- repetir os experimentos sob diferentes condições e configurações.
    

Esse passa a ser o rumo da pesquisa. A pergunta deixou de ser simplesmente:

> **Como detectar ataques desconhecidos?**

E passou a ser algo mais específico:

> **Em que medida a exposição contínua a variantes adversariais pode tornar um sistema de detecção mais robusto e capaz de generalizar para variantes ofensivas que ainda não observou?**

Agora temos uma pergunta que a arquitetura pode efetivamente tentar responder.