# GIOTTUS Documentation

## English

Welcome to the GIOTTUS documentation for bt_api.

### Quick Start

```bash
pip install bt_api_giottus
```

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "GIOTTUS___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("GIOTTUS___SPOT", "BTCUSDT")
print(ticker)
```

## 中文

欢迎使用 bt_api 的 GIOTTUS 文档。

### 快速开始

```bash
pip install bt_api_giottus
```

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "GIOTTUS___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("GIOTTUS___SPOT", "BTCUSDT")
print(ticker)
```

## API Reference

See source code in `src/bt_api_giottus/` for detailed API documentation.
