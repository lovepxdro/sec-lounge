AUTHOR = "Pedro"
SITENAME = "sec-lounge"
SITEURL = ""

PATH = "content"
TIMEZONE = "America/Recife"
DEFAULT_LANG = "pt-br"
LOAD_CONTENT_CACHE = False

# URLs amigáveis
ARTICLE_URL = "{category}/{slug}/"
ARTICLE_SAVE_AS = "{category}/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"

# Exibição e Paginação
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True
DEFAULT_PAGINATION = 10
THEME = "themes/sec-lounge"
