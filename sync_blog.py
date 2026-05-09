import os
import re
import shutil

OBSIDIAN_VAULT = "/home/pedro/lovepxdro"
CONTENT_DIR = "content"
IMAGES_DIR = os.path.join(CONTENT_DIR, "images")


def build_file_index():
    index = {}
    for root, _, files in os.walk(OBSIDIAN_VAULT):
        for file in files:
            index[file] = os.path.join(root, file)
    return index


def process_images(content, file_index):
    imagens_wiki = re.findall(r"!\[\[(.*?)\]\]", content)
    imagens_md = re.findall(r"!\[.*?\]\((.*?)\)", content)

    for img_path in imagens_wiki + imagens_md:
        img_nome = os.path.basename(img_path)
        origem = file_index.get(img_nome)

        if origem and os.path.exists(origem):
            os.makedirs(IMAGES_DIR, exist_ok=True)
            destino = os.path.join(IMAGES_DIR, img_nome)
            shutil.copy2(origem, destino)

        # Trata espaços na URL do Markdown para não quebrar o parser
        img_url = img_nome.replace(" ", "%20")

        content = content.replace(
            f"![[{img_path}]]", f"![{img_nome}](/images/{img_url})"
        )
        content = content.replace(f"]({img_path})", f"](/images/{img_url})")

    return content


def process_file(filepath, file_index):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "status: published" not in content:
        return

    content = process_images(content, file_index)

    def link_replacer(match):
        nota = match.group(1)
        nome_arquivo = nota.lower().replace(" ", "-") + ".md"
        return f"[{nota}]({{filename}}{nome_arquivo})"

    content = re.sub(r"(?<!\!)\[\[(.*?)\]\]", link_replacer, content)

    filename = os.path.basename(filepath)
    dest_filename = filename.lower().replace(" ", "-")

    os.makedirs(CONTENT_DIR, exist_ok=True)
    dest_path = os.path.join(CONTENT_DIR, dest_filename)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Sincronizado: {dest_filename}")


def sync():
    if not os.path.exists(OBSIDIAN_VAULT):
        print("Erro: Caminho do vault não encontrado.")
        return

    file_index = build_file_index()

    for root, _, files in os.walk(OBSIDIAN_VAULT):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file), file_index)


if __name__ == "__main__":
    sync()
