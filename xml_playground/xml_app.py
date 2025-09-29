from bs4 import BeautifulSoup

with open("feed.xml", encoding="utf-8") as f:
    xml_doc = f.read()

soup = BeautifulSoup(xml_doc, "lxml-xml")

for entry in soup.find_all("entry"):
    title = entry.find("title").text.strip()
    link = entry.find("link").get("href")
    summary_tag = entry.find("summary")
    summary = summary_tag.text.strip() if summary_tag else "Немає опису"

    print(f"Заголовок: {title}")
    print(f"Посилання: {link}")
    print(f"Текст: {summary}")
    print("-" * 50)
