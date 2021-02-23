# zenbot

## Mongo 

### Mac

```sh
brew services list
brew services start mongodb-community
```

### Linux

Install standalone version following [this manual](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition).

## Fill data

`./zenbot.sh backfill --days=1 binance.ETH-USDT`

## Paper mode

`./zenbot.sh trade binance.BNB-USDC --paper`

## Zenbot commands:

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --period=30m --strategy=random`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --period=5m --strategy=trend_ema --trend_ema=55`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --period=5m --strategy=trend_ema --trend_ema=210`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --period=5m --strategy=trend_ema --trend_ema=200`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --period=7m --strategy=boll`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --period=7m --strategy=boll --bollinger_size=60`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --period=7m --strategy=boll --bollinger_sell_touch_distance_pct=0.5`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --period=7m --strategy=boll --bollinger_breakout_size_violation_pct`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --strategy=ta_macd_ext --period=7m --default_ma_type=TEMA -- ema_short_period=16 --ema_long_period=39`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --verbose --strategy=ta_macd_ext --period=7m --default_ma_type=DEMA`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --strategy=ta_macd_ext --period=7m --default_ma_type=DEMA -- ema_short_period=16 --ema_long_period=39 --currency_capital=100`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --strategy=ta_macd_ext --period=7m --default_ma_type=SMA`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --strategy=ta_macd_ext --period=7m --default_ma_type=EMA`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --strategy=espend_stoch_rsi --period=5m --k_period=9 --d_period=9 - -rsi_period=42 --stochastic_period=42`

* `./zenbot.sh sim binance.BTC-USDC --currency_capital=100 --days=7 --verbose --strategy=espend_stoch_rsi --period=15m`

* `./zenbot.sh trade binance.BTC-USDC --manual --period=5m --strategy=trend_ema --deposit=50 --debug --exact_buy_orders --exact_sell_orders --markdown_buy_pct=1 --markup_sell_pct=1`
