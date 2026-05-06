# sec-lounge

Blog estático voltado para anotações, writeups e pesquisas em cibersegurança. Desenvolvido com uma estética minimalista e deploy automatizado.

## Stack Tecnológica

- SSG: Pelican (Python)
- Gestão de Conhecimento: Obsidian
- Hospedagem & CI/CD: GitHub Pages + Actions
- Design: Tema próprio (Dark Minimalist)

## Estrutura e Sincronização

O fluxo de publicações é integrado ao Obsidian. Apenas notas finalizadas são enviadas ao blog.

1. Escreva a nota no formato Markdown no Obsidian.
2. Adicione `status: published` no frontmatter YAML da nota.
3. Execute o script local de sincronização (`python sync_blog.py`). Ele filtrará os arquivos, converterá os links internos e fará a cópia para o diretório do projeto.
4. Realize o commit e push para a branch `main`.
5. O GitHub Actions assume a pipeline, gerando os arquivos estáticos e publicando no Pages.

## Foco de Conteúdo

- Writeups de CTFs e resolução de laboratórios (ex: pentest e análises de logs).
- Registros de experimentos de pesquisa (ex: arquiteturas de defesa e machine learning).
- Referências e conceitos de Blue Team e SOC.
