# Kalshi API Documentation

This is a local copy of the Kalshi API documentation. For the most up-to-date docs, visit: https://docs.kalshi.com/

## Key Documentation Links

### Getting Started
- [Making Your First Request](https://docs.kalshi.com/getting_started/making_your_first_request) - Make your first API call and start trading on Kalshi.
- [API Keys](https://docs.kalshi.com/getting_started/api_keys) - Learn how to generate and manage your API credentials.
- [Demo Environment](https://docs.kalshi.com/getting_started/demo_env) - Test your integration in the safe demo environment.
- [Rate Limits](https://docs.kalshi.com/getting_started/rate_limits) - Understand API rate limits and best practices.
- [Kalshi Glossary](https://docs.kalshi.com/getting_started/terms) - Learn key terms and concepts used in the Kalshi exchange.

### API Reference
- [Complete API Documentation](https://docs.kalshi.com/api-reference) - Explore all endpoints and parameters.
- [WebSocket API](https://docs.kalshi.com/getting_started/quick_start_websockets) - Learn about real-time data streaming via WebSockets.
- [Market Data Quick Start](https://docs.kalshi.com/getting-market-data) - Guide for accessing market data.

### Specifications
- [OpenAPI Specification](https://docs.kalshi.com/openapi.yaml) - Download the OpenAPI spec for API integration.
- [AsyncAPI Specification](https://docs.kalshi.com/asyncapi.yaml) - Download the AsyncAPI spec for WebSocket integration.

### Additional Resources
- [Changelog](https://docs.kalshi.com/changelog) - Stay updated with the latest API changes.
- [Trading Console](https://kalshi.com/) - Access the Kalshi trading platform.
- [Kalshi Academy](https://help.kalshi.com/) - Explore educational resources and tutorials.
- [Developer Agreement](https://kalshi.com/developer-agreement) - Legal agreement for API usage.

## Common API Endpoints Used in KalshiBot

### Market Data
```
GET /markets - List all available markets
GET /markets/{ticker} - Get details for a specific market
GET /markets/{ticker}/order_book - Get order book for a market
```

### Positions & Portfolio
```
GET /portfolio - Get account information
GET /positions - Get all current positions
GET /portfolio/balance - Get account balance
```

### Trading
```
POST /orders - Create a new order
GET /orders - List all orders
DELETE /orders/{order_id} - Cancel an order
```

### Market Events
```
GET /events - List all available events
GET /events/{ticker} - Get event details
```

## Notes for KalshiBot Development

- All API endpoints are on: `https://api.elections.kalshi.com/trade-api/v2`
- Authentication uses API key/secret pair from `.env`
- Demo environment: `https://demo-api.kalshi.com/trade-api/v2`
- Rate limits: Check documentation for current limits
- WebSocket URL: `wss://stream.kalshi.com/v1` (for market data streaming)

## Python SDK

KalshiBot uses `kalshi_python_sync` - the official Python SDK for Kalshi API.

Useful classes:
- `KalshiClient` - Main client for API interaction
- `Configuration` - Configuration object for auth
- `MarketPosition` - Market position objects
- `EventPosition` - Event position objects

See the Python SDK documentation for more details on available methods and models.
