title: EVE Online Trading Tool
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 8000

# EVE Online Trading Tool

Ein umfassendes Handelstool für EVE Online, das täglich Marktdaten aus den wichtigsten Handelsregionen sammelt und erweiterte Analysefunktionen bietet.

## Features

- **Automatischer Datenimport**: Täglich um 00:00 UTC
- **Marktdaten-API**: RESTful API für alle gesammelten Daten  
- **Regionen**: Jita, Amarr, Dodixie, Rens, Hek
- **Frontend**: React-basierte Benutzeroberfläche
- **Analysefunktionen**: Preistrendanalyse, Arbitrage-Möglichkeiten, Markt-Gesundheit

## Verwendung

Das Tool läuft automatisch und sammelt täglich Marktdaten aus EVE Online. Über die Weboberfläche können Sie:

1. **Dashboard**: Überblick über Marktstatistiken
2. **Items**: Durchsuchen aller verfügbaren Items
3. **Arbitrage**: Profitable Handelsrouten finden
4. **Analyse**: Detaillierte Preis- und Volumenanalysen

## API Endpoints

- `GET /` - API Status
- `GET /items` - Alle Items
- `GET /market-data/{type_id}` - Marktdaten für Item
- `GET /arbitrage` - Arbitrage-Möglichkeiten
- `GET /market-health` - Markt-Gesundheitsstatistiken

