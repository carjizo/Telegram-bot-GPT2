import os
import logging
# from turtle import update #report bot events   
import telegram
import sys
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from chatbot_brain import ChatbotBrain
from transformers import MarianMTModel, MarianTokenizer


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s," 
)
logger = logging.getLogger()


TOKEN = os.getenv("TOKEN") #create an environment variable. pwershell = $env:TOKEN="token code", cmd = set TOKEN=token code
mode = os.getenv("MODE")

if mode == "dev":
    #Acceso local (desarrollo)
    def run(updater):
        updater.start_polling()#preguntando por mensajes entrantes
        print("BOT RUN...")
        updater.idle() #cerrar el proceso

elif mode == "prod":
    #Acceso HEROKU (producción)
    def run(updater):
        PORT = int(os.environ.get("PORT", "80"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
        # updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
else:
    logger.info("No se especificó el MODE.")
    sys.exit()



tokenizer_en_t_es = MarianTokenizer.from_pretrained(
    "Helsinki-NLP/opus-mt-en-ROMANCE"
)
model_en_t_es = MarianMTModel.from_pretrained(
    "Helsinki-NLP/opus-mt-en-ROMANCE")


tokenizer_es_t_en = MarianTokenizer.from_pretrained(
    "Helsinki-NLP/opus-mt-ROMANCE-en"
)
model_es_t_en = MarianMTModel.from_pretrained(
    "Helsinki-NLP/opus-mt-ROMANCE-en")


contexto = """who are you?
My name is Pequenin, I'm a robot from the future, I'm trapped \
in a teddy bear, I hate people and I love to wet people, Hector \
Pulido is my master, I am very grumpy, and I'm in the Hector twitch chat"""

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

def eng_to_spanish(text):
    src_text = [">>es<< {}".format(text)]
    translated = model_en_t_es.generate(
        **tokenizer_en_t_es.prepare_seq2seq_batch(src_text, return_tensors="pt")
    )
    tgt_text = [
        tokenizer_en_t_es.decode(t, skip_special_tokens=True)
        for t in translated
    ]

    return tgt_text[0]


def esp_to_english(text):
    src_text = [">>es<< {}".format(text)]
    translated = model_es_t_en.generate(
        **tokenizer_es_t_en.prepare_seq2seq_batch(src_text, return_tensors="pt")
    )
    tgt_text = [
        tokenizer_es_t_en.decode(t, skip_special_tokens=True)
        for t in translated
    ]

    return tgt_text[0]


def start(update, context):
    # print(update)
    logger.info(f"El usuario {update.effective_user['username']}, ha iniciado una conversación")
    name = update.effective_user['first_name']
    update.message.reply_text(f"Hola {name} yo soy tu bot.")

def random_number(update, context):
    user_id = update.effective_user['id']
    logger.info(f"El usuario {user_id}, ha solicitado un número aleatorio.")
    number = random.randint(0,10)
    context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=f"<b>Número</b> aleatorio: \n{number}")

def echo(update, context):
    user_id = update.effective_user['id']
    logger.info(f"El usuario {user_id}, ha enviado un mensaje de texto")
    text = update.message.text #guardamos mensaje
    output = chatbot.talk(text)
    context.bot.sendMessage(
        chat_id=user_id,
        # parse_mode = "MarkdownV2",
        # text = f"*Escribiste:*\n_{respuesta}_"
        text = f"{output}"
        )



if __name__ == '__main__':
    #obtain bot info
    myBot = telegram.Bot(token= TOKEN) 
    # print(myBot.getMe())    


#connect Updater with our bot
updater = Updater(myBot.token, use_context=True)

#create a receive and transmit info, dispatcher
dp = updater.dispatcher
#create handler
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("random", random_number))
dp.add_handler(MessageHandler(Filters.text, echo))

run(updater)

