# Security_Lounge

Blog estático voltado para writeups, pesquisas e discussões em cibersegurança. Desenvolvido com estética minimalista e deploy automatizado.

## Stack

- **SSG:** Pelican (Python)
- **Templates:** Jinja2
- **Gestão de escrita:** Obsidian (.md)
- **Hospedagem & CI/CD:** GitHub Pages + Actions
- **Design:** Tema próprio (dark-minimalist)

## Sincronização

O fluxo de publicações é integrado ao Obsidian. Apenas notas finalizadas são enviadas ao blog.

1. Escreva a nota no formato Markdown no Obsidian.
2. Adicione `status: published` no frontmatter YAML da nota.
3. Execute o script local de sincronização (`python sync_blog.py`). Ele filtrará os arquivos, converterá os links internos e fará a cópia para o diretório do projeto.
4. Realize o commit e push para a branch `main`.
5. O GitHub Actions assume a pipeline, gerando os arquivos estáticos e publicando no Pages.

### YAML

---
Title: Título do post
Date: 2026-08-28
Category: experimentos
Slug: titulo-do-post
status: published
---

### Status disponíveis

- **published:** Nota concluída, pronta para ser publicada.
- **wip:** Nota em desenvolvimento, o script não publica, mas registra em wip.txt.

> Futura melhoria: Abandonar o **status** no YAML e criar uma organização física (VAULT_PATH) que represente cada um.

## Categorias

- **writeups** — Resolução de desafios relacionados a segurança.
- **experimentos** — Registro de pesquisas e desenvolvimento de projetos.
- **offtopic** — Discussões fora do radar técnico.

## Terminal no Rodapé

O rodapé do blog conta com um mini terminal interativo. Comandos disponíveis:

| Comando | Descrição |
|---|---|
| `ls --notes` | Lista notas em andamento |
| `open --repo` | Abre o repositório no GitHub |
| `radio --play` | Inicia rádio lofi |
| `radio --stop` | Para a rádio |
| `radio --status` | Status da rádio |
| `whoami` | Sobre o autor |
| `clear` | Limpa o terminal |

## Futuras melhorias

1. Sistema de tags para organização lógica.
3. Criar um .env.example.
4. Revisar código, estrutura e fluxo de publicação.
5. Adicionar logs de edições nos posts.
6. Melhorar visualização/leitura dos posts.
