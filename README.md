# security_lounge

Blog estático voltado para anotações, writeups e pesquisas em cibersegurança. Desenvolvido com estética minimalista e deploy automatizado.

## Stack Tecnológica

- **SSG:** Pelican (Python)
- **Gestão de Conhecimento:** Obsidian
- **Hospedagem & CI/CD:** GitHub Pages + Actions
- **Design:** Tema próprio (Dark Minimalist)

## Estrutura e Sincronização

O fluxo de publicações é integrado ao Obsidian. Apenas notas finalizadas são enviadas ao blog.

1. Escreva a nota no formato Markdown no Obsidian.
2. Adicione `status: published` no frontmatter YAML da nota.
3. Execute o script local de sincronização (`python sync_blog.py`). Ele filtrará os arquivos, converterá os links internos e fará a cópia para o diretório do projeto.
4. Realize o commit e push para a branch `main`.
5. O GitHub Actions assume a pipeline, gerando os arquivos estáticos e publicando no Pages.

## Categorias

- **writeups** — CTFs e resolução de laboratórios (pentest, análise de logs, etc.)
- **experimentos** — Registros de pesquisa (arquiteturas de defesa, machine learning, etc.)
- **offtopic** — Discussões fora do radar técnico: setup, processo, referências e afins.

## Terminal no Rodapé

O rodapé do blog conta com um mini terminal interativo. Comandos disponíveis:

| Comando | Descrição |
|---|---|
| `ls --notes` | Lista notas em andamento |
| `cat wip.log` | Detalhe das notas WIP |
| `open --repo` | Abre o repositório no GitHub |
| `radio --play` | Inicia rádio lofi |
| `radio --stop` | Para a rádio |
| `radio --status` | Status da rádio |
| `whoami` | Sobre o autor |
| `clear` | Limpa o terminal |

## Blue Team / SOC

Referências e conceitos de Blue Team, SOC e segurança defensiva aparecem distribuídos entre writeups e experimentos.
