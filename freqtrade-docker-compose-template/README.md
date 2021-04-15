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