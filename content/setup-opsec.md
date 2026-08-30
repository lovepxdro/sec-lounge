Title: Meu setup dos sonhos... sendo um pouco paranóico
Date: 2026-08-27
Category: offtopic
Slug: setup-opsec
status: published

# Meu setup dos sonhos... sendo um pouco paranóico

Recentemente eu migrei para um thinkpad e quando eu liguei ele pela primeira vez, eu tive uma "overdose de ideias". Eu já usava linux em um notebook antigo (debian deu uma vida extra a ele), mas, por ele ser mais limitado, nunca havia pensando a fundo em um bom setup para ele. Agora que é interessante, elaborei um setup e achei interessante compartilhar.

## Antes da caça, vamos nos armar

Primeiro de tudo, é importante entender algumas coisas.

O setup que penso é um equilíbrio entre segurança/opsec e usabilidade, a ideia não é ter o setup mais **paranóico** possível (isso, inclusive, é muito mais comportamental do que técnico). Também não pretendo entrar em discussões sobre modificações a nível de hardware visando anonimato.

Além disso, irei manter uma filosofia minimalista no sistema, ou seja, vou manter ele o mais enxuto possível. Inclusive, mantendo arquivos pessoais em um dispositivo externo criptografado.

A arquitetura pensada é baseada em **compartimentação e níveis de confiança**. Nem toda atividade precisa do mesmo nível de isolamento, por isso, também foram pensadas em regras comportamentais para não misturarmos as coisas.

O objetivo, portanto, não é tornar qualquer atividade perfeitamente segura ou anônima. É limitar o quanto uma atividade pode afetar o restante do sistema caso algo dê errado.

Com isso em mente, vamos para a arquitetura:

```
Host NixOS
│
├── Browser 1 — alta confiança
├── Browser 2 — pessoal/casual
├── Browser 3 — descoberta
├── Obsidian
├── Password Manager
└── Virtualização
       │
       ├── VM 1 — Windows
       ├── VM 2 — Debian Development
       ├── VM 3 — Kali
       ├── VM 4 — Disposable
       └── VM 5 — Malware Analysis
```

# O host e o mais alto nível de confiança

A escolha de usar uma distro linux era óbvia, mas por que o NixOS?

Caso você não conheça, o Nix é um gerenciador de pacotes e sistema de configuração, enquanto o NixOS é uma distribuição construída em torno dele. A principal vantagem para este setup é a possibilidade de manter um **estado-base declarativo, reproduzível e relativamente fácil de reconstruir**.

A ideia é partir de uma instalação mínima e, depois de aplicar todas as configurações necessárias, chegar a um estado que conhecemos e consideramos confiável. A partir daí, podemos manter snapshots e backups desse estado, o que torna possível reinstalar o sistema com certa facilidade caso seja necessário.

Poderia até ser interessante fazer isso periodicamente, mas formatar uma máquina por si só não traz segurança. Se o estado que estamos restaurando estiver comprometido, simplesmente reinstalaremos o problema.

> **o computador não é algo que você precisa preservar indefinidamente; você preserva o estado confiável e consegue reconstruir a máquina.**

Com a OS explicada, vamos para o próximo ponto. O host opera no maior nível de confiança, a lógica é simples: se o host for comprometido, não há garantia de algo estar 100% seguro. Logo, para evitar isso, quanto menos uma atividade precisa confiar no host, menos ela deve interagir diretamente com ele.

## Navegadores, baseado em níveis de confiança

Antes de tudo, acho interessante falar o seguinte: Para além de separar contextos e identidades diferentes a nível de navegador, é ideal que o mesmo seja feito a nível de contas. Então, usar emails diferentes para propósitos diferentes é completamente bem-vindo.

Os navegadores foram separados em três, cada um com uma função dedicada e um nível de confiança:

1. Firefox, nível alto, uso crítico
2. Zen, nível médio, uso casual
3. Brave, nível baixo, uso exploratório

> O nível de confiança não é tanto sobre os sites que vou acessar, mas sobre o impacto que um comprometimento daquele contexto traria

A ideia é aplicar uma espécie de **privilégio mínimo à navegação**: cada contexto recebe apenas o nível de acesso e confiança necessário para a atividade. E, mais importante, contextos não se misturam.

### Firefox

O primeiro navegador seria dedicado a coisas críticas, como banco, serviços essencias e email principal. Aqui, muito mais do que extensões e configurações, o essencial é ter um uso mínimo, quanto menos coisas forem feitas nele, menor será a chance de essas identidades entrarem em contato com atividades desnecessárias.

Naturalmente gosto de salvar na barra de favs os sites que costumo usar, esse hábito cai como uma luva aqui. Uma vez que tenho salvo os sites que realmente precisam estar nesse navegador, a navegação é zero, e o acesso é direto.

Outra regra interessante é: nenhuma sessão permanece aberta depois do uso. Essa regra pode ser aplicada em todos os navegadores, mas em especial nesse, já que lida diretamente com coisas críticas.

### Zen

Aqui a regra é não ter identidade crítica. Redes sociais, sites que utilizo com frequência, navegação cotidiana e serviços pessoais ficam aqui. É provavelmente o navegador que eu mais utilizaria no dia a dia.

> Uma curiosidade: Praticamente todos os serviços eu prefiro usar a versão web do que a desktop, é por isso que tem poucas coisas realmente instaladas.

Além da identidade específica, é interessante ter algumas opções mais voltadas a privacidade ou melhor uso da internet, como extensões, o segundo email que falei (proton por exemplo) e até motores como duckduckgo.

A escolha do Zen inclusive é puramente por gosto pessoal.

### Brave

Podem haver discussões sobre o uso e a escolha desse navegador, mas vou me explicar. A regra não é simplesmente "uso para sites ruins", e sim não ter identidade.

Vamos a um exemplo: Suponha que eu queira assistir _Serial Experiments Lain_ e encontre o anime no Internet Archive. É um serviço no qual tenho confiança suficiente para assistir ao conteúdo, mas não existe nenhuma razão para associar essa atividade às minhas identidades pessoais ou críticas.

Ao mesmo tempo, acho inconveniente demais transformar uma atividade casual dessas em uma operação envolvendo uma VM.

Nesse exemplo não há logins, não há identidade importante, apenas a atividade. Novamente, a divisão é sobre o privilégio concedido a cada atividade.

E por que o Brave? Pela conveniência. Ele já traz bloqueio de anúncios e rastreadores integrado através do Shields, além de outros motores de busca, sem exigir que eu monte esse setup. E por que então o Brave não é o 2 navegador? Novamente, gosto pessoal, e eu posso montar um setup semelhante com extensões.

Acredito que com isso eu tenha antecipado e respondido as perguntas: Por que esse navegador existe, por que não usar uma VM para isso e por que o Brave não é o segundo navegador.

Mas, sobre a VM, já que entrou no assunto...

## VMs e o nível mais baixo de confiança

A ideia das VMs é dedicar uma parte do sistema à um tipo de atividade sem poluir (ou expor) o Host. Não tem muito o que comentar sobre elas, com excessão de uma.

### VM Windows

Essa VM é dedicada a qualquer coisa que eu não consiga fazer no Linux, é raro, mas pode acontecer.

### VM Dev

A ideia é ter um debian (também com setup minimal) dedicado a desenvolvimento de software. Inclusive, visando manter o debian limpo, cada projeto e suas dependências dentro de seus contâiners.

### VM Kali

Não tem mistério, uso para atividades de pentest e afins. Antes eu pensava em uma VM Parrot tanto para pentest, quanto para dev. Mas, mesmo que o parrot dê essa flexibilidade, acho mais interessante ter essa distinção.

### VM Malware Analysis

Não tem discussão, análise de malware deve ser feito em uma VM dedicada a isso. Não comentei sobre regras de segurança para VMs, mas particulamente aqui isso deve ser levado a sério.

### VM Descartável

Chegamos na VM interessante. Vamos voltar ao exemplo do anime Lain.

Vamos supor que ao invés de achar no Internet Archive, eu só tenha encontrado em um site aleatório e somente para download. O que fazer?

Simples, vamos usar uma VM dedicada para isso.

A VM descartável é usada quando existe uma necessidade de consumir ou baixar conteúdo de baixa confiança, mas queremos evitar que essa atividade interaja com o host.

A diferença entre o Brave e essa VM é a função para qual cada um foi pensado: o Brave foi pensado para não ter identidade, a VM foi pensada para isolar a atividade do host (não ter identidade é uma consequência). Aqui atuamos no nível mais baixo de confiança.

Para manter o modelo simples, eu adotaria uma regra rígida: **a VM descartável não é reutilizada entre atividades independentes**. Terminou a atividade? a VM morre.

Qual OS seria usada aqui? Honestamente, considerando que ela é descartável, acho que não faz diferença.

## O que faltou?

Como o post focou muito na arquitetura montada, não falei muito sobre tecnologias voltadas a privacidade e segurança, uso de rede, alternativas open source, etc. Também não comentei sobre mecanismos de segurança para as contas, como autenticação, políticas de senha, etc.

Faltou explicitar regras de segurança para o uso das VMs, debater a ideia de simplesmente ter dois dispositivos, e o principal, **qual a ameaça estou evitando?**