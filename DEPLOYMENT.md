# EVE Online Trading Tool - Deployment Anleitung

## Überblick

Das EVE Online Trading Tool ist eine vollständige Webanwendung bestehend aus:
- **Backend**: FastAPI-basierte REST API mit SQLAlchemy ORM
- **Frontend**: React-Anwendung mit TailwindCSS und shadcn/ui
- **Datenbank**: SQLite (lokal) oder PostgreSQL (Produktion)
- **Automatisierung**: Täglicher Datenimport via GitHub Actions

## Lokale Entwicklung

### Voraussetzungen
- Python 3.11+
- Node.js 20+
- pnpm

### Backend Setup
```bash
cd eve-trading-tool
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
pnpm install
pnpm run dev --host
```

## Deployment auf Hugging Face Spaces

### 1. Repository vorbereiten
```bash
git init
git add .
git commit -m "Initial commit: EVE Online Trading Tool"
```

### 2. Hugging Face Space erstellen
1. Gehe zu https://huggingface.co/spaces
2. Klicke "Create new Space"
3. Wähle "Docker" als SDK
4. Repository-URL eingeben

### 3. Konfiguration
Die `README.md` enthält bereits die notwendige Hugging Face Spaces Konfiguration:
```yaml
title: EVE Online Trading Tool
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 8000
```

### 4. Automatische Builds
Das `Dockerfile` ist bereits konfiguriert und wird automatisch von Hugging Face Spaces verwendet.

## Deployment auf anderen Plattformen

### Railway
```bash
railway login
railway init
railway up
```

### Render
1. Repository mit Render verbinden
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `python app.py`

### Heroku
```bash
heroku create eve-trading-tool
git push heroku main
```

## Umgebungsvariablen

### Erforderliche Variablen
- `DATABASE_URL`: Datenbank-Verbindungsstring
- `API_HOST`: Host-Adresse (Standard: 0.0.0.0)
- `API_PORT`: Port (Standard: 8000)

### Optionale Variablen
- `ESI_BASE_URL`: EVE Online ESI API URL
- `USER_AGENT`: User-Agent für API-Requests

## Datenbank Setup

### SQLite (Entwicklung)
```bash
export DATABASE_URL="sqlite:///./market.db"
python -c "from models import Base; from database import engine; Base.metadata.create_all(bind=engine)"
```

### PostgreSQL (Produktion)
```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
python -c "from models import Base; from database import engine; Base.metadata.create_all(bind=engine)"
```

## Automatisierung

### GitHub Actions
Die `.github/workflows/update-market-data.yml` Datei konfiguriert:
- Tägliche Ausführung um 00:00 UTC
- Automatischer Datenimport
- Commit und Push der aktualisierten Daten

### Manueller Datenimport
```bash
python fetch_market.py
```

## Monitoring und Logs

### API Health Check
```bash
curl http://localhost:8000/
curl http://localhost:8000/market-health
```

### Logs anzeigen
```bash
# Docker Logs
docker logs <container_id>

# Lokale Logs
tail -f app.log
```

## Troubleshooting

### Häufige Probleme

1. **Port bereits belegt**
   ```bash
   export API_PORT=8001
   python app.py
   ```

2. **Datenbank-Verbindung fehlgeschlagen**
   - Überprüfe DATABASE_URL
   - Stelle sicher, dass die Datenbank existiert

3. **ESI API Rate Limiting**
   - Implementiere Retry-Logic
   - Reduziere Request-Frequenz

4. **Frontend Build Fehler**
   ```bash
   cd frontend
   rm -rf node_modules
   pnpm install
   pnpm run build
   ```

## Performance-Optimierung

### Backend
- Verwende Connection Pooling
- Implementiere Caching (Redis)
- Optimiere Datenbankabfragen

### Frontend
- Code Splitting
- Lazy Loading
- Image Optimization

### Datenbank
- Indizes auf häufig abgefragte Spalten
- Partitionierung großer Tabellen
- Regelmäßige Wartung

## Sicherheit

### API Sicherheit
- Rate Limiting implementieren
- CORS korrekt konfigurieren
- Input Validation

### Datenbank Sicherheit
- Sichere Verbindungsstrings
- Regelmäßige Backups
- Zugriffskontrolle

## Backup und Recovery

### Datenbank Backup
```bash
# SQLite
cp market.db market_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Recovery
```bash
# SQLite
cp market_backup_20240101.db market.db

# PostgreSQL
psql $DATABASE_URL < backup_20240101.sql
```

## Support und Wartung

### Regelmäßige Aufgaben
- Datenbank-Optimierung (wöchentlich)
- Log-Rotation (täglich)
- Dependency Updates (monatlich)
- Sicherheits-Updates (bei Bedarf)

### Monitoring
- API Response Times
- Datenbank Performance
- Disk Space Usage
- Error Rates

## Lizenz

MIT License - siehe LICENSE Datei für Details.

