Title: Levantando problemas para o TCC
Date: 2026-08-25
Category: offtopic
Slug: problema-inicial-tcc
status: published

# Levantando problemas para o TCC

Cheguei na tão temida fase em que preciso me preocupar com o TCC. Acho que o maior problema para alguém interessado em várias coisas é justamente escolher apenas uma. Algumas ideias já foram descartadas pelo caminho, mas acredito que cheguei a um tema promissor:

> detecção de anomalias e explicabilidade no contexto de cibersegurança

Além de estar relacionado aos meus interesses, o tema também conversa com a pesquisa da IC que já venho fazendo. Antes de tudo, preciso descobrir se existe um problema de pesquisa que realmente faça sentido. Já adianto, todas as buscas foram feitas usando o Consensus.

## Antes da pesquisa

Como disse, algumas ideias foram descartadas. Uma delas era investigar a possibilidade de uma graduação específica em cibersegurança. A ideia ainda me interessa, mas como existem muitos problemas conceituais, prefiro elaborar ela aqui no blog, longe da pressão de uma pesquisa acadêmica.

Outra envolvia um sistema de ensino adaptativo ao perfil do estudante. A proposta seria pensar em uma graduação de computação que permitisse uma especialização maior em determinadas áreas. O problema é que eu ainda não tinha uma resposta convincente para questões básicas como "por que isso seria melhor?" e "como isso funcionaria na prática?".

Também surgiu a possibilidade de trabalhar com redes 6G, principalmente em problemas de segurança. Essa ideia veio de uma conversa com o professor que inicialmente seria meu orientador, mas uma mudança de orientação acabou me dando a oportunidade de reconsiderar outras possibilidades.

Foi nesse momento que voltei para IA aplicada à segurança.

## Primeira busca

Com um tema amplo em mãos, fiz a primeira busca para descobrir quais problemas aparecem com frequência na literatura quando juntamos detecção de anomalias, IA, segurança e SOC.

A pesquisa acabou apontando principalmente para algumas áreas:

- avaliação de métricas;
- seleção de thresholds;
- explicabilidade;
- alert fatigue;
- validação operacional;
- colaboração entre humanos e IA.

A questão do **thresholds** chamou minha atenção. Mesmo quando um detector consegue produzir um bom anomaly score, ainda é necessário decidir a partir de qual valor aquilo vira um alerta. Existem trabalhos propondo thresholds adaptativos e baseados em custo, mas a validação operacional ainda parece limitada.

Outra interessante seria **como saber se a IA realmente é útil para um SOC**. Aparentemente, ainda não há um framework consolidado de como medir isso, mas esse trabalho naturalmente levaria a uma pesquisa com pessoas, o que eu prefiro evitar.

Nesse ponto, as possibilidades aparentes são:

1. Como avaliar sistemas de detecção de anomalias além das métricas tradicionais?
2. Como escolher thresholds de forma mais adequada?
3. Como avaliar a explicabilidade desses sistemas?

Uma combinação interessante pode ser **threshold + XAI**.

## Segunda rodada

A segunda rodada focou em descobrir quais dessas possibilidades realmente seriam viáveis para um TCC. O resultado reduziu bastante o espaço, as principais direções eram:

- thresholds adaptativos ou cost-aware;
- métricas de avaliação para ambientes SOC;
- benchmark quantitativo de XAI;
- combinação entre threshold e XAI.

A opção de threshold + avaliação operacional parecia inicialmente a mais simples. A ideia seria pear um detector existente, gerar anomaly scores, aplicar diferentes estratégias de threshold e comparar métricas como MCC, F1, recall, falsos positivos, volume de alertar e custo de FP/FN.

O problema é que um dos trabalhos citados já faz uma comparação de métodos. Então preciso descobrir o que ainda não foi feito.

## Analisando os papers (alguns... dois pra ser sincero)

Os papers analisados foram:

- Komadina et al. — Threshold Selection
- Arreche et al. — E-XAI

O trabalho de Komadina faz justamente a comparação de métodos de seleção de threshold para network anomaly detection.

Os autores levantaram cinco metódos supervisionados e vinte não supervisionados, organizam essas abordagens e fazem experimentos com logs reais de firewall contendo anomalias injetadas. Para gerar os _anomaly scores_, utilizam ECOD. Além disso, a avaliação não fica apenas em F1: eles utilizam MCC e também medem o tempo necessário para gerar o threshold.

O resultado é que não existe um único "melhor threshold". O desempenho varia conforme o cenário e o método utilizado. Entre os métodos não supervisionados, por exemplo, POT e ECDF obtiveram alguns dos melhores resultados médios.

Isso elimina a possibilidade do TCC ser apenas uma nova comparação de métodos de threshold. Por outro lado, o trabalho levanta algumas possibilidades para pesquisas futuras, entre elas investigar como diferentes modelos de detecção influenciam a escolha do threshold.

Isso leva a uma nova pergunta que preciso ter em mente:

> A escolha do threshold deveria depender do detector de anomalias utilizado?

O segundo paper (E-XAI, de Arreche et al) propõe um framework para avaliar métodos de XAI aplicados a network intrusion detection. Eles comparam SHAP e LIME em três datasets e sete modelos de IA utilizando seis métricas:

- descriptive accuracy;
- sparsity;
- stability;
- efficiency;
- robustness;
- completeness.

> **Nota:** Os autores conseguem fazer a avaliação sem depender de usuários humanos, o que é ótimo para o meu TCC.

Aqui também existe o mesmo problema do dataset anterior, fazer a mesma comparação em outro dataset (ou modelo) não parece uma boa contribuição. Então comecei a pensar nas duas coisas como partes de um mesmo sistema.

## Threshold e XAI

Os dois trabalhos analisados estudam partes diferentes do mesmo pipeline. Um trabalho com **anomaly score → threshold → alerta** e o outro com **modelo → alerta → explicação**. Mas e se o threshold também influenciar a explicação?

Por exemplo, um threshold baixo pode gerar muitos alertas, enquanto um threshold alto pode selecionar apenas os casos mais extremos. Isso significa que não estamos apenas alterando a quantidade de alertas: estamos alterando também **quais amostras serão explicadas**.

Isso abre uma possibilidade:

> Como diferentes estratégias de seleção de threshold afetam a qualidade das explicações geradas para alertas de um sistema de detecção de anomalias?

Mas ainda preciso descobrir se alguém já fez isso.

## Terceira rodada

Essa rodada procurou especificamente pela interseção entre **threshold + XAI**. A pergunta era simples:

> Alguém já fez o experimento de variar o threshold de um detector de anomalias e medir como isso altera as métricas das explicações?

Até o conjunto de trabalhos encontrados, a resposta foi... **não**.

Os trabalhos de threshold avaiam coisas como detecção, custo, calibração e volume de alertar. Os trabalhos de XAI avaliam estabilidade, sparsity, fidelidade, robustez, completude e latência. O que não aparece é uma conexão entre os dois.

Isso não significa que a novidade esteja comprovada, uma busca no Consensus não é exatamente uma revisão sistemática. Mas parece existir um gap suficientemente interessante para continuar investigando.

## A hipótese atual

Por hora, a ideia que estou investigando é:

> Como a seleção de threshold afeta a qualidade e o custo das explicações geradas por sistemas de detecção de anomalias em cibersegurança?

Se dois thresholds produzem explicações diferentes, isso aconteceu porque o threshold realmente alterou as propriedades das explicações ou simplesmente porque cada threshold selecionou uma população diferente de amostras?

Isso pode ser investigado experimentalmente, sem precisar de analistas SOC.

Por enquanto ainda não há um título ou problema definitivo. Mas tenho uma possível pergunta de pesquisa e um gap que vale a pena investigar. O próximo passo é transformar essa hipotése em um problema de pesquisa e descobrir como seria possível testá-la.

## Referências

Infelizmente vou dever tudo, os links dos papers, os prompts exatos e a resposta bruta do Consensus. Fica para a próxima xD.