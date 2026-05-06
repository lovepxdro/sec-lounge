import os
import re

OBSIDIAN_VAULT = "/home/pedro/lovepxdro"
CONTENT_DIR = "content"


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Filtro simples pelo frontmatter
    if "status: published" not in content:
        return

    # Converte links [[Nome da Nota]] para [Nome da Nota]({filename}Nome-da-Nota.md)
    def link_replacer(match):
        nota = match.group(1)
        nome_arquivo = nota.lower().replace(" ", "-") + ".md"
        return f"[{nota}]({{filename}}{nome_arquivo})"

    content_converted = re.sub(r"\[\[(.*?)\]\]", link_replacer, content)

    filename = os.path.basename(filepath)
    # Formata o nome do arquivo de destino para lowercase e hífens
    dest_filename = filename.lower().replace(" ", "-")
    dest_path = os.path.join(CONTENT_DIR, dest_filename)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content_converted)

    print(f"Sincronizado: {dest_filename}")


def sync():
    if not os.path.exists(OBSIDIAN_VAULT):
        print("Erro: Caminho do vault não encontrado.")
        return

    for root, _, files in os.walk(OBSIDIAN_VAULT):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file))


if __name__ == "__main__":
    sync()
