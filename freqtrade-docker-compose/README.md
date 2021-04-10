# freqtrade-docker-compose


wget https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml

docker-compose pull
# Create user directory structure
docker-compose run --rm freqtrade create-userdir --userdir user_data

# Create user directory structure
docker-compose run --rm freqtrade create-userdir --userdir user_data

# create config.json using docker-compose
docker-compose run --rm freqtrade new-config --config user_data/config.json


# use strategies from freqtrade-strategies library
git clone https://github.com/freqtrade/freqtrade-strategies
mv freqtrade-strategies/user_data/strategies/berlinguyinca/* /user_data/strategies/

# use ObeliskRSI_v6_1 strategy
mv strategies/* /user_data/strategies/

# use USDT config - configure exchange key/secret, telegram token, etc
mv config.json /user_data/

# Create user directory structure
docker-compose run --rm freqtrade trade --strategy BbandRsi
