mkdir -p daily_simulaions_results

cd ../zenbot/
./zenbot.sh backfill binance.BNB-USDT --days 1
# ./zenbot.sh backfill binance.BTC-USDT --days 1

./zenbot.sh sim binance.BNB-USDT --verbose --strategy bollinger --days 1|| true
./zenbot.sh sim binance.BNB-USDT --verbose --period=7m --strategy=bollinger --days 1|| true

./zenbot.sh sim binance.BNB-USDT --verbose --period=7m --strategy=sar --days 1|| true
./zenbot.sh sim binance.BNB-USDT --verbose --strategy=crossover_vwap --days 1|| true

./zenbot.sh sim binance.BNB-USDT --verbose --strategy momentum --days 1 || true
./zenbot.sh sim binance.BNB-USDT --verbose --strategy macd --days 1 || true

./zenbot.sh sim binance.BNB-USDT --period=5m --strategy=trend_ema  --markdown_buy_pct=2 --markup_sell_pct=2 --verbose --days 1 || true

# ./zenbot.sh sim binance.BNB-USDT --currency_capital=100 --days=1 --verbose --period=5m --strategy=trend_ema --trend_ema=55 

cd -
eval "$(pyenv init -)"
python simulations_results_cleaner.py

mv *.csv daily_simulaions_results/
jupyter notebook