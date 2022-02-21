from chatbot_brain import ChatbotBrain


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



while True:
    inputText = (input('>>'))
    if inputText:
        output = chatbot.talk(inputText)
        print(output)
    else:
        print("Hola, encantado de conocerte")
    # context += inputText + '\n'
    
    
