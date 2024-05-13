from src.utils.file_operations import construct_path, file_to_dict
from src.utils.validator import validate_of_type

CONFIG_FILE_PATH = construct_path("src/config.json")

class Config():
    _instance = None

    def __init__(self) -> None:
        if Config._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of Config.")
        
        config_data = file_to_dict(CONFIG_FILE_PATH)
        
        self.BOT_TOKEN = config_data.get("token", None)
        self.PREFIX = config_data.get("prefix", None)
        self.OWNER_ID = config_data.get("owner_id", None)
        self.API_KEY = config_data.get("api_key", None)

        try:
            validate_of_type(self.BOT_TOKEN, str, "token")
            validate_of_type(self.PREFIX, str, "prefix")
            validate_of_type(self.API_KEY, str, "api_key")
        except ValueError as e:
            raise RuntimeError(f"An error occured while initializing config: {e}")

    @staticmethod
    def get_instance() -> 'Config':
        if Config._instance is None:
            Config._instance = Config()
        return Config._instance