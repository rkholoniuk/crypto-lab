#!/bin/bash

TEMPLATE_DIR=template_dir
DB_FILE=tradesv3_default.sqlite
STRATEGY_NAME=Sample
CONFIG_FILE_NAME=config.json
EXCHANGE_KEY=default_key_value
EXCHANGE_SECRET=default_secret_value
USER_DATA_DIR=user_data_dir

if [ -f .env ]; then

    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
    # Show variables
    echo $DB_FILE
    echo $STRATEGY_NAME
    echo $CONFIG_FILE_NAME
    echo $EXCHANGE_KEY
    echo $EXCHANGE_SECRET
    echo $USER_DATA_DIR
fi

docker-compose run --rm freqtrade create-userdir --user-data-dir $USER_DATA_DIR

cp ./$TEMPLATE_DIR/config.json $CONFIG_FILE_NAME

config_file_name=./$USER_DATA_DIR/$CONFIG_FILE_NAME
db_file_path=./$USER_DATA_DIR/$DB_FILE

echo $config_file_name
echo $db_file_path


if [[ -n $EXCHANGE_KEY ]];then
    sed -i -e "s/exchange-key/$EXCHANGE_KEY/g" $CONFIG_FILE_NAME
fi

if [[ -n $EXCHANGE_SECRET ]];then
    sed -i -e "s/exchange-secret/$EXCHANGE_SECRET/g" $CONFIG_FILE_NAME
fi

if [[ -n $TELEGRAM_TOKEN ]];then
    sed -i -e "s/telegram-token/$TELEGRAM_TOKEN/g" $CONFIG_FILE_NAME
fi

if [[ -n $TELEGRAM_CHAT_ID ]];then
    sed -i -e "s/telegram-chat_id/$TELEGRAM_CHAT_ID/g" $CONFIG_FILE_NAME
fi

cp $CONFIG_FILE_NAME $config_file_name
touch $db_file_path



