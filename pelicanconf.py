import re
from math import ceil

AUTHOR = "Pedro"
SITENAME = "Security_Lounge"
SITEURL = ""

MESES_PT = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN",
            "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]


def data_abreviada(value):
    """Formata uma data como '12 AGO 2026', independente do locale do sistema."""
    return f"{value.day:02d} {MESES_PT[value.month - 1]} {value.year}"


def tempo_leitura(html_content):
    """Estima o tempo de leitura (em minutos) a partir do HTML do artigo."""
    texto = re.sub(r"<[^>]+>", " ", html_content or "")
    palavras = len(texto.split())
    return max(1, ceil(palavras / 200))


JINJA_FILTERS = {
    "data_abreviada": data_abreviada,
    "tempo_leitura": tempo_leitura,
}

PATH = "content"
TIMEZONE = "America/Recife"
DEFAULT_LANG = "pt-br"
LOAD_CONTENT_CACHE = False

STATIC_PATHS = ["images", "wip.txt"]
EXTRA_PATH_METADATA = {"images/favicon.svg": {"path": "favicon.svg"}}

# URLs amigáveis
ARTICLE_URL = "{category}/{slug}/"
ARTICLE_SAVE_AS = "{category}/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"
ARCHIVES_SAVE_AS = "arquivo/index.html"

# Exibição e Paginação
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True
DEFAULT_PAGINATION = 10

THEME = "themes/sec-lounge"
