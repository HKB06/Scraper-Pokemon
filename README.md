# Scraper Pokémon - Back

Ce script Python (`scraper.py`) permet de scraper les cartes Pokémon depuis Pokécardex et de les stocker dans MongoDB.

## Lancer le scraper

```bash
pip install -r requirements.txt
python scraper.py
```

## Fonctionnement

- Utilise Selenium pour naviguer sur le site Pokécardex
- Récupère les séries et les cartes (nom, illustrateur, série)
- Stocke les résultats dans MongoDB (ou dans un fichier JSON si besoin)