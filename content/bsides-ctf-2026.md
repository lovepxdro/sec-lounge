Title: BSides Recife 2026 — tomei uma surra, mas foi legal
Date: 2026-06-10
Category: offtopic
Slug: bsides-recife-2026 
status: published

# BSides Recife 2026 — tomei uma surra, mas foi legal

Semana passada participei do CTF da BSides Recife. Foi meu primeiro CTF presencial e, spoiler, não ganhei. Fiquei em 6º lugar entre uns 14 ou 15 times. Mas saí de lá com mais vontade de estudar do que entrei, então vou considerar isso uma vitória particular.

---

## O formato

Eram 5 desafios no total — 2 fáceis, 2 médios e 1 difícil. Competindo em equipe, tive contato direto com 3 deles. O resto ficou com o time enquanto eu estava enfiado nos que vou detalhar aqui.

~~honestamente os médios já eram difíceis e o 'difícil' era impossível para mim.~~

---

## Quase first blood no SQL Injection

O primeiro desafio era uma API de busca de funcionários. A resposta inicial já entregava tudo que precisava saber:

```json
{ "message": "Employee search api", "usage": "/search?q=name" }
```

Fui direto ao ponto. Testei `q='+OR+'1'='1` — retornou todos os funcionários. SQL Injection confirmado.

O próximo passo foi mapear a estrutura da query. Com `ORDER BY N--` fui incrementando até o erro aparecer: 4 colunas. Confirmei com `UNION SELECT NULL,NULL,NULL,NULL--`, que funcionou e revelou os campos `id`, `name`, `email` e `department`.

Aí ficou interessante. Rodei `UNION SELECT name,NULL,NULL,NULL FROM sqlite_master WHERE type='table'--` — banco era SQLite, tabela era `employees`. Depois puxei o schema completo com `UNION SELECT sql,NULL,NULL,NULL FROM sqlite_master--` e apareceu uma coluna `password` no `CREATE TABLE` que não aparecia em nenhuma busca normal.

O último payload foi direto:

```sql
' UNION SELECT password,NULL,NULL,NULL FROM employees--
```

O problema foi velocidade. Fiz tudo certo, mas outro time enviou pouco tempo antes. First blood escapou por pouco.

Mas foi o momento que mais me animou no dia, confirmou que o básico está funcionando.

---

## A brecha que não deu tempo

O desafio que mais me orgulho foi um dos difíceis, uma API com autenticação.

Fiquei um bom tempo tentando entender o fluxo de requisições, mapeando endpoints, testando comportamentos inesperados nas respostas. Em determinado momento achei uma inconsistência no tratamento de um parâmetro — uma brecha que indicava que o caminho certo era por ali.

Não deu tempo de finalizar. O CTF encerrou com a exploração incompleta.

Mas sair de um desafio difícil tendo _avançado_, mesmo sem a flag, foi satisfatório de um jeito diferente. É a diferença entre não saber por onde começar e saber exatamente onde está o buraco mas não ter tido tempo de entrar.

---

## O desafio que ninguém resolvia

O último desafio era lendário no mau sentido: era a terceira edição seguida que ele aparecia em CTFs e ninguém tinha resolvido ainda. Nessa edição também ficou sem solução... exceto pelo time que ficou em primeiro.

Depois do CTF eles explicaram a resolução. Era elegante e não estava no meu repertório atual. Fiquei com a sensação clássica de "faz sentido agora que eu sei a resposta" — o que significa que o gap não era de lógica, era de referência. Não conhecia a técnica.

Vale registrar: o time vencedor trabalha na Tempest e na CISSA. São profissionais que fazem isso no dia a dia. O abismo existe e é real.

---

## O que fica

Duas lições concretas saíram desse dia.

A primeira é que preciso ampliar o repertório de técnicas e desafios resolvidos. Não faltou raciocínio no último desafio — faltou já ter visto algo parecido antes. CTF tem muito de reconhecimento de padrão, e padrão só vem com volume.

A segunda é sobre perspectiva. Ver de perto o nível de quem trabalha na área foi útil de um jeito que vídeo e post não entregam. O abismo ficou visível, mas também ficou _mensurável_. Isso é melhor do que imaginar que ele é infinito.

6º lugar. Próximo CTF, diferente.