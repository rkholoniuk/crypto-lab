cd ../zenbot/
./zenbot.sh sim binance.ETH-USDT --strategy bollinger --days 1|| true
./zenbot.sh sim binance.ETH-USDT --strategy cci_srsi --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy crossover_vwap --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy dema --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy forex_analytics --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy macd --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy momentum --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy neural --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy noop --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy rsi --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy sar --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy speed --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy srsi_macd --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy stddev --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy ta_ema --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy ta_macd --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy ta_macd_ext --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy ta_trix --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy trend_ema --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy ta_ppo --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy ta_ultosc --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy trendline --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy trust_distrust --days 1 || true
./zenbot.sh sim binance.ETH-USDT --strategy wavetrend --days 1 || true
cd -
./venv/bin/python simulations_results_cleaner.py