Title: Fechando uma proposta provisória para o TCC
Date: 2026-09-13
Category: experimentos
Slug: proposta-tcc
status: published

# Fechando uma proposta proviósria para o TCC

Continuando essa saga, eu terminei o último post com duas linhas de pesquisas promissoras:

1. Interação entre detector e estrátegia de threshold;
2. Calibração de threhsold para controle de falsos positivos.

A ideia agora é aprofundar cada uma delas separadamente e descobrir qual eu prefiro para seguir com o TCC. Como de costume, fiz todas as buscas no Consensus, porém, como a ideia é fechar uma proposta, as próximas buscas serão feitas usando strings de busca (e também porque acabaram os meus créditos no Consensus).

## Primeiro caminho: detector x threshold

A primeira busca tentou entender melhor uma pergunta que já havia aparecido:

> A estratégia de threshold depende do detector utilizado?

A literatura indica que sim. Detectores diferentes produzem anomaly scores diferentes, por isso, um threshold que funciona bem para um detector não necessariamente funciona bem para outro.

Isso reforça um ponto já levantado no primeiro post: investigar como diferentes modelos de detecção influenciam a escolha do threshold. E isso nós leva a uma pergunta interessante:

> Como diferentes estratégias de threshold interagem com diferentes detectores e distrbuições de anomaly scores?

Porém, talvez o problema mais fundamental nem seja a identidade do detector, mas as características da distibuição dos scores produzidos por ele. Em vez de perguntar qual threshold funciona melhor para Isolation Forest, a pergunta pode ser:

> Quais propriedades da distribuição dos anomaly scores influenciam o desempenho de diferentes estratégias de threshold ?

É uma linha interessante, mas ela tem o risco de simplesmente virar um benchmark com combinações de detectores e threhsolds. O que não é um problema propriamente dito, mas preciso avaliar se seria do meu interesse fazer um benchmark gigantesco como TCC.

## Segundo caminho: controle de falsos positivos

Essa linha parte para um problema mais operacional: Como calibrar thresholds para controlar falsos positivos?

Nesse contexto, apareceram algumas famílias de soluções:

- EVT/POT;
- quantis e order statistics;
- métodos baseados em contaminação;
- métodos conformais.

Uma das principais vantagens de métodos conformais é justamente oferecer garantias estatísticas sobre o comportamento das decisões. Em conformal anomaly detection, isso significa que, sob determinadas hipóteses, o método pode controlar a taxa de falsos positivos em torno de um nível nominal definido, como 5%.

Em outras palavras, o threshold deixa de ser apenas um corte heurístico e passa a estar associado a uma expectativa formal de erro. Essas garantias, porém, dependem de condições específicas sobre os dados usados na calibração.

## O problema das garantias conformais

Beleza, garantias conformais são legais e tudo mais, mas em quais situações elas deixam de funcionar bem?

A literatura aponta alguns fatores importantes:

- violação de exchangeability;
- distribution shift;
- dependência temporal;
- conjuntos de calibração pequenos;
- desbalanceamento extremo;
- contaminação do conjunto de calibração.

O problema da contaminação me pareceu interessante. Em conformal anomaly detection, o conjunto de calibração funciona como uma referência para definir aquilo que é considerado comportamento normal. Mas e se essa referência não estiver perfeitamente limpa?

Em um cenário de segurança, pode ser difícil garantir que um conjunto supostamente normal realmente não contenha nenhum evento anômalo. Isso gera uma pergunta bem mais específica:

> Como a presença de anomalias no conjunto de calibração afeta o comportamento do método conformal?

## O que a literatura já sabe?

Um resultado importante é que, em cenários de contaminação não adversarial, o efeito esperado não é necessariamente um aumento de falsos positivos. Na verdade, a tendência pode ser o contrário.

A presença de anomalias no conjunto de calibração pode fazer o threshold ficar mais conservador, preservando o controle de erro do tipo I, mas reduzindo o poder de detecção.

Em outras palavras:

**menos falsos positivos, mas potencialmente mais falsos negativos.**

O problema (**talvez**) parece estar mais no equilíbrio entre **controle de falsos positivos e capacidade de detecção**.

## E isso já foi feito em segurança?

A próxima busca tentou responder exatamente essa pergunta. Conformal prediction já aparece em trabalhos de cibersegurança. Existem aplicações em:

- 5G;
- CAN bus;
- IoT;
- IDS;
- cyber-physical systems;
- análise de logs.

Então o gap não é "ainda não aplicaram em segurança", mas os trabalhos encontrados normalmente:

- assumem conjuntos de calibração limpos;
- estudam drift;
- trabalham com selective prediction;
- avaliam FDR;
- usam conformal como camada de confiabilidade.

O que não apareceu foi um experimento controlado em que o conjunto de calibração é progressivamente contaminado com anomalias e o impacto sobre o controle de falsos positivos é medido em datasets de IDS.

Isso parece separar três linhas que já existem:

**conformal + contaminação**:  já foi estudado teoricamente e fora de segurança;

**contaminação + anomaly detection em segurança**: também já foi estudado, principalmente durante o treinamento dos detectores;

**conformal + segurança**: já existe.

Mas a combinação:

> **conformal + contaminação do calibration set + IDS**

aparentemente ainda não foi bem explorada.

## Última verificação

Para vitar construir o TCC inteiro sobre um gap que já tivesse sido resolvido, fiz uma última busca focada exatamente nesse experimento.

> Adeus créditos no Consesus.

A pergunta era básicamente:

> Alguém já contaminou sistematicamente um conjunto de calibração conformal em datasets públicos de IDS e mediu a diferença entre FPR nominal e FPR observado?

Até o conjunto de trabalhos encontrados, a resposta foi não.

Também não encontrei uma comparação direta, sob esse mesmo cenário de contaminação, entre conformal calibration e outros métodos de threshold como EVT/POT, quantis ou métodos baseados em contaminação. Então, podemos chegar em uma conclusão mais específica:

> Ainda há pouca evidência empírica sobre como a contaminação do conjunto de calibração afeta o controle de falsos positivos de métodos conformais em detecção de anomalias aplicada à cibersegurança.

# Uma proposta provisória

Com isso, finalmente consigo formular algo mais próximo de um problema de pesquisa.

## Problema

Métodos conformais oferecem garantias estatísticas de controle de falsos positivos sob determinadas hipóteses sobre os dados de calibração.

Em cibersegurança, porém, conjuntos perfeitamente limpos contendo somente comportamento normal podem ser difíceis de obter.

Ainda não está claro como a presença de anomalias nesses dados de calibração afeta, na prática, o controle de falsos positivos e a capacidade de detecção em sistemas de IDS.

## Pergunta de pesquisa

> Como a contaminação controlada do conjunto de calibração afeta o controle de falsos positivos e o desempenho de detecção de métodos conformais aplicados à detecção de anomalias em cibersegurança?

## Hipótese

> O aumento da contaminação no conjunto de calibração torna o método conformal mais conservador, preservando ou aproximando o controle nominal de falsos positivos, mas reduzindo progressivamente o poder de detecção e o recall.

Essa hipótese ainda precisa ser discutida e refinada, mas já é bem mais específica do que as perguntas com que comecei a pesquisa.

## Escopo

Para evitar que o trabalho volte a crescer demais, a ideia seria manter um escopo pequeno. Algo próximo de:

- um detector fixo, possivelmente Isolation Forest;
- um método conformal principal;
- dois métodos de threshold como baseline;
- um ou dois datasets públicos de IDS;
- diferentes níveis controlados de contaminação;
- conjuntos separados de treino, calibração e teste;
- nenhuma escolha de threshold utilizando rótulos do conjunto de teste.

As principais métricas poderiam ser:

- FPR nominal;
- FPR observado;
- diferença entre FPR nominal e observado;
- recall;
- precision;
- FNR;
- MCC;
- volume de alertas.

Por enquanto, coisas como ensemble, rejeição, drift, online conformal, múltiplos detectores e XAI ficariam fora do escopo.

# Referências

**Chat com o Consensus:** [https://consensus.app/search/anomaly-detector-threshold-interaction/-jIm3xomTR-j3zIzpqcblQ/](https://consensus.app/search/anomaly-detector-threshold-interaction/-jIm3xomTR-j3zIzpqcblQ/)