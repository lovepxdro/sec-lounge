Title: Da Ideia para a Rede: Implementando a Arquitetura Dual-GAM
Date: 2026-07-21
Category: experimentos
Slug: arquitetura-dual-gam
status: published

# Da Ideia para a Rede: Implementando a Arquitetura Dual-GAM

No [post anterior](https://lovepxdro.github.io/sec-lounge/experimentos/experimento-inicial-ic/), mostrei o experimento inicial da minha IC: dois modelos de IA em competição, onde uma GAN Atacante aprende a gerar tráfego DDoS capaz de evadir detecção, e uma GAN Defensora aprende continuamente a identificar esses ataques. O experimento rodou em notebook, com dados estáticos, e validou o conceito central.

Esse post é sobre o próximo passo: tirar isso do notebook e construir a arquitetura real — com rede Docker, tráfego de pacotes de verdade, e os dois modelos se comunicando em tempo real.

---

## Recapitulando rapidamente

A questão central da IC não é "detectar DDoS melhor" — isso já existe e funciona bem. A questão é: **como criar uma defesa que se adapte a ataques que ela nunca viu antes?**

No experimento inicial, o resultado mais importante foi mostrar que um defensor com 99.91% de acurácia em dados estáticos é vulnerável quando o atacante evolui: na primeira rodada do ciclo adversarial, 75% dos ataques perturbados passaram sem ser detectados. Após 20 rodadas de co-evolução, o defensor chegou a ~98.3% — pagando um trade-off honesto entre acurácia e robustez.

O próximo problema era óbvio: no experimento inicial, o "ataque" era um vetor de números em memória. Na vida real, um ataque DDoS são pacotes de rede chegando num servidor. Precisávamos fechar esse gap.

---

## A arquitetura

O diagrama que guiou a implementação tem três camadas:

![Pasted image 20260721161242.png]({static}/images/Pasted%20image%2020260721161242.png)

**Camada de rede (Docker):** hosts legítimos (h1-h4) e uma fonte de ataque (h-attack) conectados a um switch (s1) que encaminha tráfego para um servidor alvo (h-target).

**Plano de controle SDN:** um controlador que monitora o tráfego, extrai features e aplica regras de bloqueio. Essa camada ainda está em desenvolvimento — por enquanto o switch é simulado pela bridge do Docker.

**Camada ML — Dual GAN:** os dois modelos do experimento inicial, agora integrados ao pipeline de rede.

Essa separação em camadas não é só organização — ela reflete como sistemas de defesa reais funcionam. Em redes SDN, o plano de dados (onde o tráfego passa) é separado do plano de controle (onde as decisões são tomadas). Colocar a inteligência adversarial no plano de controle significa que ela pode observar o tráfego de toda a rede e responder em tempo real, sem depender de um único ponto de inspeção. É uma arquitetura que escala e que tem paralelo direto com sistemas de detecção de intrusão em produção.

O fluxo completo funciona assim:

```
GAN Atacante  →  perturba amostras reais de DDoS
      ↓
GAN Defensora →  avalia probabilidade de detecção
      ↓
Translator    →  converte vetor de features → parâmetros de pacote
      ↓
Scapy         →  envia pacotes TCP/UDP reais na rede Docker
      ↓
Controller    →  registra taxa de evasão → próximo ciclo
```

Durante a implementação percebemos que existia um componente que o experimento inicial nunca precisou resolver: a tradução entre o espaço matemático aprendido pela GAN e o mundo real dos pacotes de rede. O **Translator** nasceu para resolver exatamente esse problema.

---

## O Translator: o problema mais interessante

O CIC-IDS2017, dataset que usamos, descreve *fluxos* de rede — estatísticas agregadas como taxa de pacotes por segundo, tamanho médio de pacote, contagem de flags TCP. Não descreve pacotes individuais.

A GAN Atacante aprende a perturbar vetores nesse espaço de 77 features. Mas o Scapy precisa de parâmetros concretos: quantos pacotes por segundo enviar, qual o tamanho do payload, quais flags TCP usar.

O Translator resolve isso desnormalizando o vetor (revertendo o StandardScaler do pré-processamento) e mapeando as features relevantes para parâmetros de ataque:

- `flow_packets_per_sec` → taxa de envio (pps)
- `fwd_packet_length_mean` + `avg_pkt_size` → tamanho do pacote
- `syn_flag_count`, `ack_flag_count`, etc. → flags TCP e tipo de ataque
- `flow_duration` → duração do ataque
- `init_fwd_win_bytes` → TCP window size

O mapeamento não é 1-para-1 perfeito — as estatísticas de fluxo não determinam unicamente os parâmetros de cada pacote. Mas é suficientemente fiel para que o tráfego gerado tenha as características gerais do que a GAN aprendeu.

---

## Decisões de desenvolvimento

### Por que Scapy com perturbação, não geração pura?

No experimento inicial testamos três abordagens para o atacante. As duas primeiras falharam:

**Geração pura (ruído → vetor):** o gerador aprendeu a produzir vetores fora de qualquer distribuição real — 100% de evasão técnica, mas 0% de realismo. O defensor classificava como benigno justamente porque não se parecia com nada que ele conhecia.

**Geração com loss de realismo:** melhorou a distribuição estatística, mas o problema de fundo persistiu.

**Perturbação adversarial:** pega amostras reais de DDoS e aprende perturbações pequenas que enganam o defensor. Essa foi a única que funcionou — e é o que implementamos aqui. O Scapy executa exatamente o que a perturbação indica: tráfego que ainda se parece com DDoS, mas sutilmente modificado para escapar da detecção.

### O problema do checkpoint final

Depois de treinar os modelos e rodar o primeiro ataque real, encontramos um problema inesperado: **0% de evasão em todos os ciclos**.

O motivo foi sutil. O treino salva o estado de ambos os modelos ao final de cada rodada. Quando o Controller carregava `atacante_final.pth` e `defensor_adaptativo_final.pth`, estava usando o par da rodada 20 — onde o defensor *já tinha respondido* ao atacante daquela rodada. Naturalmente, a evasão era zero.

A solução foi fazer o Controller escolher automaticamente o melhor par de checkpoints: o atacante da rodada com maior taxa de evasão na segunda metade do treino, combinado com o defensor da rodada *anterior* (que ainda não tinha visto aquele atacante específico).

```
melhor_rodada = rodada com maior evasão nas rodadas 10-20
atacante  ← checkpoint da melhor_rodada
defensor  ← checkpoint da melhor_rodada - 1
```

Essa lógica captura exatamente o momento em que o atacante está à frente — antes do defensor reagir.

---

## Resultados

**Aviso: infelizmente vou dever screenshots do terminal no momento das execuções por dois motivos:**

1. **O logging atual não favorece documentação -** O terminal exibe cada ataque conforme ele acontece, mas não apresenta um resumo consolidado ao final da execução. Isso é ótimo para depuração, mas ruim para documentação. Na prática, era mais simples salvar toda a saída do terminal do que produzir diversos screenshots. Segue um exemplo:

![Captura de tela de 2026-07-21 16-59-26.png]({static}/images/Captura%20de%20tela%20de%202026-07-21%2016-59-26.png)
(print referente a segunda execução, o que leva diretamente ao segundo problema)

2. **Divergência -** Durante cada ciclo, o Controller seleciona aleatoriamente amostras reais de DDoS e o Atacante gera novas perturbações sobre elas. Como consequência, cada execução produz conjuntos de ataques ligeiramente diferentes. Por isso, não faria sentido simplesmente executar novamente o experimento apenas para produzir screenshots. A interpretação permanece a mesma, mas os valores variam entre execuções.

Por causa desses motivos, usei no texto um resumo das tabelas que utilizei para análise.

**Prometo que na próxima implementação isso não acontece!!**

### Treino

| Rodada | Taxa de Evasão | Acc Defensor |
| -----: | :------------: | :----------: |
|      1 |      ~74%      |    98.2%     |
|      5 |      ~21%      |    98.3%     |
|     10 |      ~0%       |    98.3%     |
|     19 |      ~24%      |    99.3%     |
|     20 |      ~1%       |    99.2%     |

O comportamento replicou o experimento inicial, e algumas coisas merecem atenção.

A queda de 74% para ~0% nas primeiras rodadas não significa que o defensor "resolveu o problema" — significa que ele aprendeu a reconhecer *aquele atacante específico* daquele momento. Nas rodadas seguintes o atacante recomeça do zero, encontra novas perturbações que funcionam, e o ciclo se repete. É por isso que rodadas como a 19 mostram picos de 24% de evasão mesmo depois de o defensor ter suprimido o atacante várias vezes antes.

Esse padrão de oscilação é esperado em sistemas adversariais e tem um nome na literatura: o problema do equilíbrio trivial entre atacante e defensor. Nenhum dos dois converge para uma solução estável de longo prazo — eles continuam se adaptando um ao outro. Para fins de pesquisa, isso é o resultado desejado: mostra que o ciclo de co-evolução está funcionando de verdade.

O defensor adaptativo ficou em ~98.3% de acurácia ao longo do ciclo, contra os 99.91% do baseline estático. Esse trade-off já havia aparecido no experimento inicial e vale repetir: robustez adversarial tem custo. Um defensor que nunca viu ataques perturbados vai ter acurácia maior em dados limpos — mas vai ser mais vulnerável quando o atacante evoluir.

### Ataque real (10 ciclos, Scapy na bridge Docker)

| Ciclo | Vetores gerados | Evadiram | Taxa |
|-------|----------------|----------|------|
| 1     | 100            | 14       | 14%  |
| 2     | 100            | 28       | 28%  |
| 5     | 100            | 23       | 23%  |
| 10    | 100            | 33       | 33%  |

A taxa de evasão no pipeline real (14-33%) é menor do que nos ciclos de treino (até 74% na rodada 1), o que faz sentido: o Controller usa o par atacante/defensor da rodada 19, quando o defensor já tinha sido exposto a várias rodadas de perturbações. Não é o defensor mais fraco — é um defensor com experiência, e mesmo assim ~25% dos vetores gerados conseguem evadir.

Os parâmetros de ataque gerados pelo Translator foram coerentes com o perfil DDoS do CIC-IDS2017: ~24k pps, pacotes de 80-278 bytes, flags TCP variando entre SA, SAP, AP e A. A variação nas flags é particularmente interessante — o atacante não converge para um único padrão, continua explorando combinações diferentes a cada ciclo.

Uma nota sobre o volume de pacotes: a taxa real de envio do Scapy (~10-15 pacotes por 0.5s) é bem menor do que o `pps` pedido pelos AttackParams (~24k). Isso é uma limitação de raw sockets em container Docker — o kernel limita a taxa de envio. Para os fins desse experimento, o que importa é que os pacotes chegam ao h-target com as características certas.

---

## Métricas do servidor alvo

Durante o ataque, é possível monitorar o impacto em tempo real via endpoint `/metrics` do h-target:

```bash
watch -n1 'curl -s http://localhost:8080/metrics | python3 -m json.tool'
```

---

## Algumas limitações da implementação atual

Vale ser explícito sobre o que essa implementação ainda não faz, para não vender mais do que entrega.

**O feedback ainda é offline.** O retreino do Defensor usa amostras do dataset CIC-IDS2017, não tráfego capturado da rede em tempo real. Isso significa que o ciclo co-evolutivo acontece no espaço de features do dataset, não no espaço de pacotes reais. A ponte entre os dois existe (via Translator + Scapy), mas ainda não fecha o loop: o que o Defensor aprende não é alimentado de volta pelo que o Sender envia.

**O SDN ainda não fecha o ciclo.** A camada de controle SDN (Traffic Monitor → Extractor → Rule Enforcer) está no diagrama mas ainda não foi implementada. Por enquanto o switch s1 é a bridge padrão do Docker, sem inspeção de tráfego nem aplicação de regras. Fechar esse ciclo é o próximo passo concreto da IC.

**Volume de tráfego limitado em container.** Como mencionado nos resultados, raw sockets em Docker têm limitações de taxa de envio. O ambiente atual é suficiente para validar o pipeline, mas não para simular ataques volumétricos de escala real.

**Hosts legítimos simplificados.** Os h1-h4 são containers que fazem `curl` em loop — tráfego benigno mas pouco realista. Num ambiente mais completo, o tráfego legítimo deveria ter mais variedade para testar se o Defensor consegue distinguir DDoS de tráfego legítimo em condições mais difíceis.

---

## Melhorias possíveis

Algumas direções que valem ser pensadas (organizadas por área):

**Engenharia**

- **Arquivo de configuração centralizado** (`config.yaml`) para hiperparâmetros, endereços de rede, número de rodadas, epsilon de perturbação. Hoje esses valores estão espalhados pelo código.
- **Componente AttackEngine.** O Controller atualmente concentra responsabilidades demais (carregamento de modelos, geração, avaliação, tradução e execução dos ataques). Um `AttackEngine` permitiria separar a lógica de execução da lógica de orquestração.
- **Interfaces abstratas** para os componentes principais, desacoplando as implementações concretas do Controller.
- **Testes automatizados** — especialmente para o Translator, que tem lógica de mapeamento que pode silenciosamente produzir parâmetros inválidos sem testes.
- **Persistência do histórico de ataques.** O Controller já registra métricas de cada ciclo em memória, mas o arquivo `historico_ataques.json` só é salvo quando `executar_loop()` é utilizado. Em execuções que chamam apenas `executar_ciclo()`, o histórico é perdido ao final do processo.
- **Resumo consolidado ao final de cada ciclo.** Atualmente o logging registra cada ataque individualmente, mas não apresenta um resumo geral da execução. Gerar automaticamente uma tabela consolidada ao final de cada ciclo facilitaria tanto a análise quanto a documentação dos experimentos.

**Pesquisa**

- **Feedback online**: retreinar o Defensor com features extraídas do tráfego real capturado na rede, não com dados do dataset.
- **Métricas de realismo** mais sofisticadas para avaliar se as amostras perturbadas são plausíveis como tráfego de rede real.
- **Outros tipos de ataque** além de DDoS — o framework está estruturado para suportar isso, mas ainda não foi testado.

**Infraestrutura**

- Implementar o plano de controle SDN completo (Ryu + Open vSwitch).
- Tráfego legítimo mais realista nos hosts h1-h4.

---

## Revisão do projeto

Olhando para o plano de trabalho original da IC, ele descreve a pesquisa como dois modelos de IA em competição — GAN A vs GAN B. Essa descrição ainda é válida, mas ficou pequena para o que o projeto se tornou.

As GANs continuam sendo o núcleo da inteligência adaptativa, mas são um componente dentro de algo maior. O que construímos até agora é mais precisamente descrito como:

> **Um ambiente experimental para pesquisa em defesa adaptativa baseada em aprendizado adversarial.**

A diferença importa. Um ambiente experimental tem topologia de rede, geração de tráfego real, pipeline de pré-processamento, sistema de checkpoints, métricas de avaliação, e uma separação clara entre camada de dados e camada de controle. As GANs deixaram de ser o projeto — agora são o que torna o ambiente *inteligente*.

Essa mudança de perspectiva abre alguns caminhos que não eram óbvios no plano original. O ambiente pode ser usado para testar outros mecanismos de defesa além de GANs — qualquer componente que implemente a interface do Defensor pode ser plugado. O ciclo adversarial pode ser estudado em condições variadas de rede, não só com o dataset CIC-IDS2017. E a arquitetura em camadas (rede → SDN → ML) tem correspondência direta com sistemas reais, o que torna os resultados mais transferíveis.

O foco da IC continua sendo a questão original: como criar uma defesa que se adapte a ataques que ela nunca viu antes. A diferença é que agora temos uma plataforma para investigar isso de formas que um notebook nunca permitiria.

---
## Código

O repositório com o código completo, instruções de uso e resultados está em: [LINK_REPOSITÓRIO](https://github.com/lovepxdro/dual-gam)

**obs: todo esse post foi feito em cima da primeira versão da arquitetura (primeiro commit)**

A estrutura do projeto, decisões de arquitetura e como rodar estão documentadas no README.