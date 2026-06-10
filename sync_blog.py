import os
import re
import shutil
from dotenv import load_dotenv

load_dotenv()

OBSIDIAN_VAULT = os.getenv("VAULT_PATH") or ""
CONTENT_DIR = "content"
IMAGES_DIR = os.path.join(CONTENT_DIR, "images")
WIP_FILE = "wip.txt"

if not OBSIDIAN_VAULT:
    raise ValueError("VAULT_PATH não definido. Crie um arquivo .env com VAULT_PATH=/caminho/do/vault")


def build_file_index():
    index = {}
    for root, _, files in os.walk(OBSIDIAN_VAULT):
        for file in files:
            index[file] = os.path.join(root, file)
    return index


def get_meta(content, key):
    match = re.search(rf"^{key}:\s*(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else None


def read_wip():
    if not os.path.exists(WIP_FILE):
        return []
    with open(WIP_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def write_wip(titles):
    with open(WIP_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(titles) + ("\n" if titles else ""))


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

        img_url = img_nome.replace(" ", "%20")

        content = content.replace(
            f"![[{img_path}]]", f"![{img_nome}]({{static}}/images/{img_url})"
        )
        content = content.replace(f"]({img_path})", f"]({{static}}/images/{img_url})")

    return content


def process_file(filepath, file_index, wip_titles):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    status = get_meta(content, "status")
    title = get_meta(content, "Title") or os.path.basename(filepath)

    if status == "wip":
        if title not in wip_titles:
            wip_titles.append(title)
            print(f"WIP: {title}")
        return

    if status == "published":
        # remove do wip caso tenha sido promovida
        if title in wip_titles:
            wip_titles.remove(title)
            print(f"Removido do WIP: {title}")

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
        print(f"Erro: vault não encontrado em '{OBSIDIAN_VAULT}'. Verifique o .env.")
        return

    file_index = build_file_index()
    wip_titles = read_wip()

    for root, _, files in os.walk(OBSIDIAN_VAULT):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file), file_index, wip_titles)

    write_wip(wip_titles)


if __name__ == "__main__":
    sync()
