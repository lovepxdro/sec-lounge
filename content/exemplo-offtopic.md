Title: Coisas que aprendi configurando meu setup de estudos
Date: 2026-06-01
Category: offtopic
Slug: setup-estudos-2026
status: published

# Coisas que aprendi configurando meu setup de estudos

Esse post não é sobre segurança. É sobre como eu monto o ambiente onde a segurança acontece.

Depois de muita tentativa e erro, cheguei num setup que funciona pra mim: Arch Linux com i3wm, Obsidian pra notas, e um terminal que fica aberto na metade da tela o tempo todo.

Não é nada revolucionário, mas algumas decisões foram contraintuitivas o suficiente pra valer um registro.

---

## Por que o i3wm convenceu depois de parecer impossível

A curva de aprendizado do i3 é real. As primeiras horas são de pura frustração: janelas que não somem, atalhos que não fazem sentido, nada de decoração de janela pra te guiar.

Mas depois que clica — e clica de verdade — fica impossível voltar. O conceito de *workspaces* com foco total em teclado elimina aquela micro-fadiga de ficar alternando janelas com o mouse.

Meu `~/.config/i3/config` virou um dos arquivos que mais mantenho cuidado no sistema.

---

## Obsidian como segundo cérebro (sem o hype)

Uso Obsidian de forma bem pragmática: sem plugins excessivos, sem Zettelkasten elaborado. Só pastas, links internos, e frontmatter YAML com `status: published` pra indicar o que vai pro blog.

O `sync_blog.py` cuida do resto.

O que não esperava: o grafo de notas virou uma ferramenta de revisão. Ver como os conceitos se conectam (ou não) diz muito sobre o que ainda precisa de mais estudo.

---

## Terminal como ambiente principal

Kitty como emulador, Zsh com plugins mínimos (autosuggestions, syntax-highlighting, nada mais). Nada de oh-my-zsh — pesado demais pra o que preciso.

A decisão mais útil foi mapear um atalho pra abrir um scratchpad de terminal flutuante no i3. Para uma nota rápida, um teste de comando, uma consulta ao `man` sem perder o contexto do que estava fazendo.

---

*Esse tipo de post vai aparecer aqui quando tiver algo fora do radar técnico que valha registro. Offtopic, mas parte do processo.*
