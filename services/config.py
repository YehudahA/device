import json


class ConfigSettings:
    def __init__(self, server_address: str):
        self.server_address = server_address


class ConfigService:
    settings: ConfigSettings = None

    def get_config(self):
        if not self.settings:
            self.settings = ConfigService.__parse()

        return self.settings

    def __parse():
        j = open('./config.json',)

        data = json.load(j)

        config = ConfigSettings(data['serverAddress'])

        return config
