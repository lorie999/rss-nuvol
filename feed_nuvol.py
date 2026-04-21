import cloudscraper
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

URL = "https://www.nuvol.com/llibres"

print("Descarregant la pagina...")
scraper = cloudscraper.create_scraper()
resposta = scraper.get(URL)

if resposta.status_code != 200:
    print(f"Error: codi {resposta.status_code}")
    exit()

print("Pagina descarregada correctament")
sopa = BeautifulSoup(resposta.text, "html.parser")

fg = FeedGenerator()
fg.title("Nuvol - Llibres")
fg.link(href=URL)
fg.description("Articles de llibres a Nuvol")

articles = sopa.find_all("article")

if not articles:
    print("No s'han trobat articles.")
else:
    print(f"Trobats {len(articles)} articles")

for article in articles:
    titol_tag = article.find("h2") or article.find("h3")
    subtitol_tag = article.find("p", class_="subtitle")
    link_tag = article.find("a", href=True)

    if titol_tag and link_tag:
        titol = titol_tag.get_text(strip=True)
        link = link_tag["href"]
        subtitol = subtitol_tag.get_text(strip=True) if subtitol_tag else ""

        if link.startswith("/"):
            link = "https://www.nuvol.com" + link

        fe = fg.add_entry()
        fe.title(titol)
        fe.link(href=link)
        fe.description(subtitol if subtitol else titol)
        print(f"  -> {titol[:60]}...")

fg.rss_file("nuvol.rss")
print("Feed guardat com a nuvol.rss")