import os

from TelegramBot import TelegramBot


token = os.getenv("TOKEN") #create an environment variable. pwershell = $env:TOKEN="token code", cmd = set TOKEN=token code

telegrambot = TelegramBot(
    token,
)


if __name__ == '__main__':
    telegrambot.run()