import re, time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient

BASE = "https://www.pokecardex.com"
LISTE = f"{BASE}/series"
N_SERIES = 5
WAIT = 20
SCROLL_PAUSE = .6
ALT_RE = re.compile(r"(.+?)\s+\d+/\d+\s*<br/>(.+)", re.I)

def make_driver() -> webdriver.Chrome:
    o = Options()
    o.add_argument("--headless=new")
    o.add_argument("--no-sandbox")
    o.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=o)

def accept_cookies(d: webdriver.Chrome) -> None:
    try:
        WebDriverWait(d, 4).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#didomi-notice-agree-button"))
        ).click()
    except Exception:
        pass

def list_series_urls(d: webdriver.Chrome) -> List[str]:
    d.get(LISTE)
    accept_cookies(d)
    links = d.find_elements(By.CSS_SELECTOR, "a.d-block.no-decoration-link.text-reset")[:N_SERIES]
    return [l.get_attribute("href") for l in links]

def scroll(d: webdriver.Chrome) -> None:
    h = d.execute_script("return document.body.scrollHeight")
    while True:
        d.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(SCROLL_PAUSE)
        new_h = d.execute_script("return document.body.scrollHeight")
        if new_h == h:
            break
        h = new_h

def grab_card(img, serie: str) -> Dict:
    alt = img.get_attribute("alt") or ""
    m = ALT_RE.match(alt)
    nom, illu = m.groups() if m else (alt.replace("<br/>", " "), "")
    return {"serie": serie, "nom": nom.strip(), "illustrateur": illu.strip()}

def scrape_serie(d: webdriver.Chrome, url: str) -> List[Dict]:
    code = url.rstrip("/").split("/")[-1]
    print(f"↳ {code}")
    d.get(url)
    accept_cookies(d)
    WebDriverWait(d, WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.serie-details-carte img"))
    )
    scroll(d)
    imgs = d.find_elements(By.CSS_SELECTOR, "div.serie-details-carte img")
    cards = []
    for img in imgs:
        card = grab_card(img, code)
        cards.append(card)
        print(f"   · {card['nom']}")
    print(f"   → {len(cards)} cartes")
    return cards

def main():
    d = make_driver()
    try:
        print("▶ Récupération des séries…")
        series = list_series_urls(d)
        print(f"{len(series)} séries trouvées.")
        all_cards: List[Dict] = []
        for url in series:
            all_cards += scrape_serie(d, url)
    finally:
        d.quit()
    client = MongoClient("mongodb://localhost:27017/")
    db = client["pokemon"]
    collection = db["cards"]
    collection.delete_many({})
    collection.insert_many(all_cards)
    print(f"✅ {len(all_cards)} cartes insérées dans MongoDB !")

if __name__ == "__main__":
    main()