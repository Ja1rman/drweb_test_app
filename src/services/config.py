import yaml

with open("configs/config.yml", "r") as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(e)

DB_NAME = config['db_name']
DB_USER = config['db_user']
DB_PASSWORD = config['db_password']
DB_HOST = config['db_host']
DB_PORT = config['db_port']
APP_HOST = config['app_host']
APP_PORT = config['app_port']