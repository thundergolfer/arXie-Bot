import os


class Config():
    def __init__(self):
        self.ENV = os.getenv("ENV", "DEV")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.slack_token = os.getenv("SLACK_TOKEN", "")
        self.project_id = os.getenv('PROJECT_ID', 'arxie-bot')  # for G Cloud
        # db_token is defaulted for dependent tests
        self.db_token = os.getenv('ARXIE_DB_TOKEN', 'apian cleft dogs cats t fuss')
        self.apiai_token = os.getenv('APIAI_TOKEN', '')


config = Config()
