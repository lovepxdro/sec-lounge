Title: Refinando o problema do TCC
Date: 2026-09-09
Category: experimentos
Slug: refinando-problema-tcc
status: published

# Refinando o problema do TCC

No [último post sobre o TCC](https://lovepxdro.github.io/sec-lounge/offtopic/problema-inicial-tcc/), eu levantei algumas pesquisas e terminei com uma pergunta promissora.

> Como a seleção de threshold afeta a qualidade e o custo das explicações geradas por sistemas de detecção de anomalias em cibersegurança?

Acredito que cheguei em um ponto interessante, uma interseção entre dois assuntos, mas isso não significa que eu tenho um problema de pesquisa bem definido. Aqui, pretendo me dedicar em refinar essa pergunta e chegar em possíveis problemas bem definidos.

## Qual o nosso ponto de partida atual (feedback)?

Antes de começar novas pesquisas, é importante entender onde estamos.

Até então, estava conduzindo pesquisas muito direcionadas para segurança. Isso me levou aos dois trabalhos analisados e a combinação de ambos levou a hipótese descrita. O problema é que, do jeito que eu estava conduzindo a pesquisa, comecei a explorar possíveis soluções antes de delimitar com precisão o problema.

Um dos problemas desse processo foi o viés para segurança. Não falo sobre abandonar esse contexto, mas sim em ampliar a busca: se existe uma técnica que ainda não foi muito aplicada em segurança, vale descobrir **onde ela já foi utilizada, qual problema ela resolveu e quais resultados produziu**.

Outro problema é o escopo. Detecção de anomalias abre várias ramificações: ensemble, rejeição, thresholds adaptativos, múltiplos thresholds, diferentes detectores, diferentes distribuições de scores e assim por diante.

Não pretendo trabalhar com ensemble ou rejeição, mas conhecer essas ramificações é importante justamente para poder dizer explicitamente **o que entra e o que não entra no trabalho**. O que leva diretamente a entender qual o problema específico que estamos trabalhando.

E por fim, talvez seja mais interessante aprofundar primeiro a pesquisa sobre **threshold** antes de voltar para Shapley/XAI. Antes de perguntar como o threshold influencia a explicabilidade, eu preciso entender melhor:

> qual problema de threshold eu realmente quero estudar?

## Voltando para o Consensus

Com esse feedback em mente, podemos voltar as pesquisas e concentrar elas em coisas específicas, deliberadamente saindo do contexto de segurança. Novamente, todas as buscas foram feitas no Consensus.

> Parte do feedback também foi a recomendação de outras ferramentas. Pretendo usar elas em conjunto com o Consensus, mas para as pesquisas descritas aqui, usei apenas o consesus.

A primeira busca tentou mapear o problema de threshold em anomaly detection de forma mais ampla, incluindo manufatura, manutenção preditiva, saúde, fraude, sensores, energia e séries temporais. A pergunta principal era:

> Quais são os principais problemas associados à seleção de threshold e quais famílias de solução já foram propostas?

Essa busca mostrou que a seleção de threshold não é um problema único, mas envolve diferentes desafios, como contaminação desconhecida, drift, custos assimétricos entre falsos positivos e falsos negativos, volume de alertas e problemas de calibração e avaliação.

Ela também revelou várias famílias de solução já usadas em diferentes domínios, como métodos estatísticos/EVT, cost-sensitive, adaptativos, conformais e baseados em contaminação.

A partir desse mapa, ficou mais fácil identificar três questões que valiam uma investigação separada: a relação entre **detector e threshold**, o **controle de falsos positivos por calibração** e os **problemas metodológicos na avaliação de thresholds**.

## Detector x Threshold

A primeira pergunta específica foi: **A estratégia de threshold depende do detector utilizado?**

A resposta encontrada foi basicamente **sim**. Detectores diferentes produzem anomaly scores com distribuições, escalas e comportamentos diferentes. Isso significa que uma estratégia que funciona bem para um detector pode funcionar pior para outro.

A parte interessante é que existem muitos trabalhos comparando detectores e muitos trabalhos comparando thresholds, mas menos trabalhos estudando explicitamente a **interação entre detector e threshold** sob um mesmo protocolo experimental.

Isso abre uma possível linha de pesquisa:

> **Como diferentes estratégias de threshold interagem com diferentes detectores e distribuições de anomaly score?**

É uma linha interessante, mas há o risco de virar simplesmente um benchmark grande demais.

## Controle de falsos positivos

A segunda busca específica foi sobre: **Como calibrar thresholds para controlar falsos positivos?**

Aqui apareceram principalmente três famílias mais maduras:

- EVT;
- quantis/order statistics;
- métodos conformais.

Essas abordagens já aparecem em áreas como monitoramento industrial, saúde, sistemas de controle e streaming, enquanto a avaliação direta delas em anomaly detection de segurança parece bem menor.

A parte que mais chamou atenção foi a calibração conformal. Em vez de simplesmente procurar o threshold que maximiza F1, métodos conformais podem formular a decisão em termos de controle explícito de uma taxa de erro, desde que determinadas hipóteses sejam respeitadas.

Isso leva a uma possível pergunta:

> Métodos de calibração com controle explícito de falsos positivos produzem decisões mais previsíveis do que thresholds heurísticos em detecção de anomalias de segurança?

É uma linha bem promissora, com um problema operacional claro, e com um caminho natural para avaliar se as técnicas funcionam bem no contexto de segurança.

## Problemas de avaliação

A última busca foi sobre uma pergunta metodológica: **Como avaliar thresholds corretamente?**

Esse resultado foi importante porque mostrou vários problemas recorrentes em trabalhos de anomaly detection.

Um dos principais é escolher o threshold utilizando rótulos do próprio conjunto de teste. Isso introduz informação que não estaria disponível em um cenário real e pode inflar artificialmente métricas como F1.

Outro problema é comparar detectores utilizando thresholds diferentes sem separar claramente as duas coisas. A recomendação encontrada na literatura é tratar detector e threshold como duas camadas distintas:

**detector → qualidade do anomaly score**

e

**threshold → qualidade da decisão operacional**

Também aparecem recomendações como utilizar validação separada, preservar a estrutura temporal quando necessário, reportar métricas adequadas ao desbalanceamento e analisar a sensibilidade ao threshold.

## Onde estou agora?

Acredito que a principal mudança foi a direção de foco. Se antes eu estava pensando diretamente em **threshold + XAI**, agora eu penso em algo mais fundamental:

> qual problema associado ao threshold quero estudar?

As duas principais linhas que encontrei foram:

- **interação entre detector e estratégia de threshold**;
- **calibração de threshold para controle de falsos positivos**.

Uma formulação provisória pode ser:

> Métodos de calibração com controle explícito de erro produzem trade-offs mais previsíveis entre falsos positivos e falsos negativos do que thresholds heurísticos em detecção de anomalias de segurança?

Ainda não é uma pergunta definitiva, mas já é um norte promissor. Também não descartei explicabilidade. A diferença é que agora XAI deixa de ser o ponto de partida.

Primeiro preciso entender o comportamento do threshold e definir exatamente o problema que estou tentando resolver. Mas, por ora, o próximo passo é discutir novamente com a minha orientadora antes de fazer novas rodadas de buscas.

## Referências

1. **Chat usado no Consensus:** https://consensus.app/search/anomaly-detection-threshold-selection/ZpUhmA3YSxuMeQKyOZ-HXw/?utm_source=share&utm_medium=clipboard