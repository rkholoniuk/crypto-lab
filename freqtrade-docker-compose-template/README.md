# freqtrade-docker-compose

docker-compose build
# Create user directory structure
docker-compose run --rm freqtrade create-userdir --userdir user_data

# create config.json using docker-compose
docker-compose run --rm freqtrade new-config --config user_data/config.json


# use strategies from freqtrade-strategies library
git clone https://github.com/freqtrade/freqtrade-strategies
mv freqtrade-strategies/user_data/strategies/berlinguyinca/* /user_data/strategies/

# use ObeliskRSI_v6_1 strategy
mv strategies/* ./user_data/strategies/

# use USDT config - configure exchange key/secret, telegram token, etc
mv config.json ./user_data/

# Create user directory structure
docker-compose run --rm freqtrade trade --strategy BbandRsi

# Backtesting
docker-compose run --rm freqtrade download-data -t 1h --timerange 20210310-20210410" or days 60
docker-compose run --rm freqtrade download-data --pairs ETH/BTC --exchange binance --days 5 -t 
docker-compose run --rm freqtrade backtesting --config user_data/config.json --strategy SampleStrategy --timerange 20190801-20191001 -i 5m
docker-compose run --rm freqtrade plot-dataframe --strategy AwesomeStrategy -p BTC/ETH --timerange=20180801-20180805


# Data analysis using docker compose
docker-compose -f docker/docker-compose-jupyter.yml up
https://127.0.0.1:8888/lab
docker-compose -f docker/docker-compose-jupyter.yml build --no-cache



# freqtrade-docker-compose-template
Steps : 
1. create .env file - use as referance .env-sample

TEMPLATE_DIR=template_dir  - do not edit

Specify user data directory freqtrade user-dir parameter
USER_DATA_DIR=user_data_test

Specify db file
DB_FILE=tradesv3_ichi.sqlite

Specify Strategy to be used. Note the stratagy should be copied into USER_DATA_DIR
STRATEGY_NAME=Obelisk_Ichimoku_Slow_v1_1

Specify config file
CONFIG_FILE_NAME=config_ichi.json

Specify Binance api key
EXCHANGE_KEY=abc_key_ichi

Specify Binance api secret
EXCHANGE_SECRET=abc_secret_ichi

Specify Telegram token
TELEGRAM_TOKEN=telegram_token_ichi

Specify Telegram chat id
TELEGRAM_CHAT_ID=telegram_chat_ichi

2. run setup.sh script

3. Copy the Strategy into USER_DATA_DIR

4. docker-compose up