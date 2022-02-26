import logging
# from turtle import update #report bot events   
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from ChatbotBrain import ChatbotBrain


contexto = """who are you?
My name is bot, I'm a robot from the future, I'm trapped \
in a teddy bear, I hate people and I love to wet people, Carlos \
Jiménez is my master, I am very grumpy, and I'm in the carjiso twitch chat"""

translation_artifacts_english = {"Disagreement": "Discord"}

translation_artifacts_spanish = {
    "pequenina": "Pequeñin",
    "osito de peluche": "Oso Teddy",
    "profesor": "Maestro",
}

chatbot = ChatbotBrain(
    contexto,
    translation_artifacts_english,
    translation_artifacts_spanish,
    "microsoft/DialoGPT-large",
    "microsoft/DialoGPT-large",
    True,
    True,
)

class TelegramBot:
    def __init__(
        self,
        token, 
    ):

        self.token = token
        self.config = logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        )
        self.logger = logging.getLogger()
        self.myBot = telegram.Bot(self.token) 
        


    def start(self, update, context):
        # print(update)
        self.logger.info(f"El usuario {update.effective_user['username']}, ha iniciado una conversación")
        name = update.effective_user['first_name']
        update.message.reply_text(f"Hola {name} yo soy tu bot.")

    def echo(self, update, context):
        user_id = update.effective_user['id']
        self.logger.info(f"El usuario {user_id}, ha enviado un mensaje de texto")
        text = update.message.text #guardamos mensaje
        with open("./archivos/emojis.txt", "r", encoding="utf-8") as f:
            for line in f:
                if text == line:
                    context.bot.sendMessage(
                    chat_id=user_id,
                    # parse_mode = "MarkdownV2",
                    # text = f"*Escribiste:*\n_{respuesta}_"
                    text = f"{line}"
                    )  

                output = chatbot.talk(text)
                context.bot.sendMessage(
                chat_id=user_id,
                # parse_mode = "MarkdownV2",
                # text = f"*Escribiste:*\n_{respuesta}_"
                text = f"{output}"
                )   
        

    def run(self):
        
        updater = Updater(self.myBot.token, use_context=True)
        #create a receive and transmit info, dispatcher
        dp = updater.dispatcher
        #create handler
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(MessageHandler(Filters.text, self.echo))

        updater.start_polling()#preguntando por mensajes entrantes
        print("BOT RUN...")
        updater.idle() #cerrar el proceso