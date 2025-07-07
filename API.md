# EVE Online Trading Tool - API Dokumentation

## Überblick

Die EVE Online Trading Tool API bietet umfassende Endpunkte für den Zugriff auf Marktdaten, Arbitrage-Analysen und Preistrends aus dem EVE Online Universum.

**Base URL**: `http://localhost:8000` (lokal) oder `https://your-deployment-url.com`

**API Version**: 1.0.0

## Authentifizierung

Aktuell ist keine Authentifizierung erforderlich. Alle Endpunkte sind öffentlich zugänglich.

## Rate Limiting

- **Limit**: 100 Requests pro Minute pro IP
- **Headers**: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Endpunkte

### 1. Root Endpunkt

**GET** `/`

Gibt den API-Status zurück.

**Response**:
```json
{
  "message": "EVE Online Trading Tool API",
  "status": "running"
}
```

### 2. Items

**GET** `/items`

Gibt eine Liste aller verfügbaren Items zurück.

**Parameter**:
- `skip` (int, optional): Anzahl zu überspringender Items (Standard: 0)
- `limit` (int, optional): Maximale Anzahl Items (Standard: 100, Max: 1000)
- `search` (string, optional): Suchbegriff für Item-Namen

**Beispiel**: `/items?search=tritanium&limit=10`

**Response**:
```json
{
  "items": [
    {
      "type_id": 34,
      "name": "Tritanium",
      "group_id": 18,
      "market_group_id": 1033,
      "volume": 0.01,
      "description": "The most common ore type in the known universe...",
      "published": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1250,
  "skip": 0,
  "limit": 100
}
```

### 3. Regionen

**GET** `/regions`

Gibt alle verfügbaren Handelsregionen zurück.

**Response**:
```json
{
  "regions": [
    {
      "region_id": 10000002,
      "name": "The Forge (Jita)",
      "description": "The Forge region containing Jita trade hub",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### 4. Marktdaten

**GET** `/market-data/{type_id}`

Gibt Marktdaten für ein spezifisches Item zurück.

**Parameter**:
- `type_id` (int, required): EVE Online Type ID des Items
- `region_id` (int, optional): Spezifische Region ID
- `days` (int, optional): Anzahl Tage zurück (Standard: 7, Max: 365)

**Beispiel**: `/market-data/34?region_id=10000002&days=30`

**Response**:
```json
{
  "market_data": [
    {
      "id": 1,
      "type_id": 34,
      "region_id": 10000002,
      "buy_max": 5.50,
      "buy_min": 5.20,
      "buy_avg": 5.35,
      "buy_volume": 1000000,
      "buy_orders": 150,
      "sell_max": 5.70,
      "sell_min": 5.45,
      "sell_avg": 5.58,
      "sell_volume": 800000,
      "sell_orders": 120,
      "timestamp": "2024-01-01T12:00:00Z",
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### 5. Arbitrage-Möglichkeiten

**GET** `/arbitrage`

Findet profitable Handelsrouten zwischen verschiedenen Regionen.

**Parameter**:
- `min_profit` (float, optional): Mindestgewinn in ISK (Standard: 1000000)
- `limit` (int, optional): Maximale Anzahl Ergebnisse (Standard: 50, Max: 200)

**Beispiel**: `/arbitrage?min_profit=500000&limit=20`

**Response**:
```json
{
  "arbitrage_opportunities": [
    {
      "item": {
        "type_id": 34,
        "name": "Tritanium"
      },
      "buy_region": {
        "region_id": 10000002,
        "name": "The Forge (Jita)"
      },
      "sell_region": {
        "region_id": 10000043,
        "name": "Domain (Amarr)"
      },
      "buy_price": 5.50,
      "sell_price": 4.80,
      "profit": 0.70,
      "profit_margin": 14.58,
      "buy_volume": 1000000,
      "sell_volume": 800000
    }
  ]
}
```

### 6. Preistrends

**GET** `/price-trends/{type_id}`

Gibt historische Preistrends für ein Item in einer Region zurück.

**Parameter**:
- `type_id` (int, required): EVE Online Type ID
- `region_id` (int, required): Region ID
- `days` (int, optional): Anzahl Tage zurück (Standard: 30, Max: 365)

**Beispiel**: `/price-trends/34?region_id=10000002&days=90`

**Response**:
```json
{
  "historical_data": [
    {
      "id": 1,
      "type_id": 34,
      "region_id": 10000002,
      "date": "2024-01-01T00:00:00Z",
      "average": 5.35,
      "highest": 5.70,
      "lowest": 5.20,
      "order_count": 150,
      "volume": 1000000,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "market_data": [
    {
      "id": 1,
      "type_id": 34,
      "region_id": 10000002,
      "buy_avg": 5.35,
      "sell_avg": 5.58,
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### 7. Markt-Gesundheit

**GET** `/market-health`

Gibt allgemeine Marktstatistiken zurück.

**Response**:
```json
{
  "last_update": "2024-01-01T12:00:00Z",
  "active_items": 1250,
  "active_regions": 5,
  "total_buy_volume": 15000000,
  "total_sell_volume": 12000000,
  "total_orders": 45000
}
```

### 8. Marktdaten Update

**POST** `/update-market-data`

Triggert manuell ein Update der Marktdaten.

**Response**:
```json
{
  "message": "Market data update completed successfully"
}
```

**Error Response**:
```json
{
  "detail": "Market data update failed: Connection timeout"
}
```

## Fehlerbehandlung

### HTTP Status Codes

- `200 OK`: Erfolgreiche Anfrage
- `400 Bad Request`: Ungültige Parameter
- `404 Not Found`: Ressource nicht gefunden
- `422 Unprocessable Entity`: Validierungsfehler
- `429 Too Many Requests`: Rate Limit überschritten
- `500 Internal Server Error`: Serverfehler

### Fehler-Format

```json
{
  "detail": "Fehlerbeschreibung",
  "type": "validation_error",
  "errors": [
    {
      "loc": ["query", "limit"],
      "msg": "ensure this value is less than or equal to 1000",
      "type": "value_error.number.not_le"
    }
  ]
}
```

## Datenmodelle

### Item
```json
{
  "type_id": 34,
  "name": "Tritanium",
  "group_id": 18,
  "market_group_id": 1033,
  "volume": 0.01,
  "description": "Description text",
  "published": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### MarketData
```json
{
  "id": 1,
  "type_id": 34,
  "region_id": 10000002,
  "buy_max": 5.50,
  "buy_min": 5.20,
  "buy_avg": 5.35,
  "buy_volume": 1000000,
  "buy_orders": 150,
  "sell_max": 5.70,
  "sell_min": 5.45,
  "sell_avg": 5.58,
  "sell_volume": 800000,
  "sell_orders": 120,
  "timestamp": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T12:00:00Z"
}
```

## Code-Beispiele

### Python
```python
import requests

# Basis-URL
base_url = "http://localhost:8000"

# Items abrufen
response = requests.get(f"{base_url}/items?search=tritanium")
items = response.json()

# Marktdaten abrufen
response = requests.get(f"{base_url}/market-data/34?region_id=10000002")
market_data = response.json()

# Arbitrage-Möglichkeiten
response = requests.get(f"{base_url}/arbitrage?min_profit=1000000")
arbitrage = response.json()
```

### JavaScript
```javascript
const baseUrl = 'http://localhost:8000';

// Items abrufen
const getItems = async (search = '') => {
  const response = await fetch(`${baseUrl}/items?search=${search}`);
  return await response.json();
};

// Marktdaten abrufen
const getMarketData = async (typeId, regionId) => {
  const response = await fetch(`${baseUrl}/market-data/${typeId}?region_id=${regionId}`);
  return await response.json();
};

// Arbitrage-Möglichkeiten
const getArbitrage = async (minProfit = 1000000) => {
  const response = await fetch(`${baseUrl}/arbitrage?min_profit=${minProfit}`);
  return await response.json();
};
```

### cURL
```bash
# Items abrufen
curl "http://localhost:8000/items?search=tritanium&limit=10"

# Marktdaten abrufen
curl "http://localhost:8000/market-data/34?region_id=10000002&days=30"

# Arbitrage-Möglichkeiten
curl "http://localhost:8000/arbitrage?min_profit=500000&limit=20"

# Markt-Gesundheit
curl "http://localhost:8000/market-health"
```

## Swagger/OpenAPI

Die vollständige API-Dokumentation ist über Swagger UI verfügbar:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Versionierung

Die API verwendet semantische Versionierung (SemVer):
- **Major**: Breaking Changes
- **Minor**: Neue Features (rückwärtskompatibel)
- **Patch**: Bug Fixes

Aktuelle Version: `1.0.0`

## Support

Bei Fragen oder Problemen:
- GitHub Issues: [Repository URL]
- Email: support@eve-trading-tool.com
- Discord: [Discord Server Link]

