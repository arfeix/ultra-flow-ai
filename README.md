# 🚀 ULTRA FLOW AI

**Autonomous Multi-Market Trading System**

Supports: Crypto | Forex | Stocks | Commodities

---

## ✨ Features

- 🤖 **AI-Powered Scoring Engine** - Advanced flow analysis with weighted metrics
- 📊 **Multi-Market Support** - Trade across crypto, forex, stocks, and commodities
- 🛡️ **Risk Management** - Built-in position sizing and daily loss limits
- 🔗 **TradingView Integration** - Webhook-ready for automated signals
- 📈 **Real-time Execution** - CCXT-powered order execution
- 🔴 **Risk Guard** - Prevents over-trading based on daily loss thresholds
- 📦 **Containerized** - Docker & Docker Compose ready
- ⚡ **Scalable** - Production-grade architecture

---

## 🏗️ Architecture

```
ultra-flow-ai/
├── backend/              # Python/FastAPI (Port 9000)
│   ├── ai/              # Scoring engine
│   ├── trade/           # Execution & risk management
│   └── core/            # Configuration
├── gateway/             # Node.js/Express (Port 3000)
│   └── TradingView Webhook receiver
├── tradingview/         # PineScript indicator
└── docker-compose.yml   # Full stack orchestration
```

---

## 📋 Prerequisites

- Docker & Docker Compose (or)
- Python 3.11+ & Node.js 20+
- Exchange API keys (Bybit, Binance, etc.)
- TradingView account (for webhook signals)

---

## 🚀 Quick Start

### 1️⃣ Clone Repository
```bash
git clone https://github.com/arfeix/ultra-flow-ai.git
cd ultra-flow-ai
```

### 2️⃣ Configure Environment
```bash
cp .env.example .env
# Edit .env and add your API keys
nano .env
```

### 3️⃣ Start Services
```bash
docker compose up --build
```

### 4️⃣ Verify Services
```bash
# Backend API
curl http://localhost:9000/docs

# Gateway Health
curl http://localhost:3000/health

# Redis
redis-cli -h localhost ping
```

---

## 🔧 Configuration

### Backend (.env)
```env
EXCHANGE=bybit
API_KEY=your_exchange_api_key
API_SECRET=your_exchange_api_secret

RISK_PERCENT=0.01          # 1% per trade
MAX_DAILY_LOSS=0.03        # 3% daily max loss
MIN_AI_SCORE=70            # Minimum score to execute
```

### Database & Redis
```env
DB_HOST=localhost
REDIS_HOST=redis
```

---

## 📡 API Endpoints

### Backend (FastAPI)
- `POST /api/v1/signal` - Process trading signals
- `GET /api/v1/health` - Health check
- `GET /docs` - Swagger documentation

### Gateway (Express)
- `POST /tv` - TradingView webhook endpoint
- `GET /health` - Gateway health check

---

## 🎯 TradingView Integration

### 1. Create Webhook Alert
In TradingView Strategy/Indicator:
```
Webhook URL: http://YOUR_IP:3000/tv
Message Format:
{
  "symbol": "BTCUSDT",
  "side": "buy",
  "features": {
    "structure": 85,
    "liquidity": 90,
    "reaction": 78,
    "volume": 88,
    "session": 72
  },
  "balance": 10000,
  "stop_pct": 0.02
}
```

### 2. Signal Flow
```
TradingView Alert 
  ↓
Gateway (/tv) 
  ↓
Backend (/signal) 
  ↓
AI Scoring 
  ↓
Risk Check 
  ↓
Order Execution
```

---

## 🧠 AI Scoring Engine

The system evaluates signals using weighted metrics:

| Metric | Weight | Purpose |
|--------|--------|---------|
| Structure | 25% | Pattern recognition |
| Liquidity | 25% | Market depth |
| Reaction | 20% | Price momentum |
| Volume | 20% | Trading activity |
| Session | 10% | Market conditions |

**Minimum Score Required:** 70 (configurable)

---

## 💰 Risk Management

### Position Sizing
```python
position_size = (balance × risk_pct × confidence) / stop_pct
```

### Daily Loss Limit
- Maximum daily loss: 3% (configurable)
- Prevents over-trading after losses

### Risk Guard
- Real-time loss tracking
- Automatic trade rejection if limit reached

---

## 📊 File Structure

```
backend/
├── main.py                 # FastAPI app
├── requirements.txt        # Dependencies
├── Dockerfile              # Container config
├── core/
│   └── config.py          # Environment settings
├── ai/
│   └── engine.py          # Scoring engine
└── trade/
    ├── executor.py        # Order execution
    ├── risk.py            # Position sizing
    └── guard.py           # Risk protection

gateway/
├── server.js              # Express server
├── package.json           # Node dependencies
└── Dockerfile             # Container config

tradingview/
└── ultra_flow_ai.pine     # PineScript indicator
```

---

## 🐳 Docker Commands

### Start Services
```bash
docker compose up --build
```

### Stop Services
```bash
docker compose down
```

### View Logs
```bash
docker compose logs -f backend
docker compose logs -f gateway
docker compose logs -f redis
```

### Restart Specific Service
```bash
docker compose restart backend
```

---

## 🔌 Manual Setup (Without Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Gateway
```bash
cd gateway
npm install
node server.js
```

### Redis
```bash
# Using Docker
docker run -d -p 6379:6379 redis:7-alpine

# Or install locally and run
redis-server
```

---

## 📈 Advanced Configuration

### Custom Scoring Weights
Edit `backend/core/config.py`:
```python
WEIGHTS = {
    "structure": 0.30,
    "liquidity": 0.20,
    "reaction": 0.25,
    "volume": 0.15,
    "session": 0.10
}
```

### Multiple Exchange Support
```python
# .env
EXCHANGE=binance  # or: bybit, kraken, coinbase, etc.
```

---

## 🚨 Troubleshooting

### Backend won't start
```bash
# Check logs
docker compose logs backend

# Verify Python environment
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Gateway connection failed
```bash
# Check if backend is running
curl http://localhost:9000/health

# Verify network
docker compose ps
```

### Redis connection error
```bash
# Restart Redis
docker compose restart redis

# Check Redis status
redis-cli ping
```

---

## 📚 Documentation

- [FastAPI Docs](http://localhost:9000/docs) - Interactive API docs
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [CCXT Exchange Library](https://docs.ccxt.com/)
- [TradingView Webhooks](https://www.tradingview.com/pine_script_docs/)

---

## ⚠️ Risk Disclaimer

**TRADING INVOLVES RISK. THIS SYSTEM IS PROVIDED AS-IS.**

- Use only with capital you can afford to lose
- Always test with paper trading first
- Monitor trades carefully
- Adjust risk parameters according to your risk tolerance
- Past performance ≠ future results

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

---

## 📄 License

MIT License - see LICENSE file

---

## 📞 Support

Issues & feature requests: [GitHub Issues](https://github.com/arfeix/ultra-flow-ai/issues)

---

**Built with ❤️ for traders who demand automation** 🚀