import telebot
import speech_recognition as sr
from gtts import gTTS
import datetime
import wikipedia
import pywhatkit
import requests
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


bot = telebot.TeleBot('6056324190:AAEcmOve_HrKvIBD33GzztSCQ4m_W2Zdgfw')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Olá. Eu sou a Nemu, um bot que pode te ajudar com informações e músicas. Fale algo para mim!")



#------------------------------------------------------------------------

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    comando = message.text.lower()
    try:
#-----------------------------------------------------------------------
# -------------------------INFORMA AS HORAS          

        if 'horas' in comando:
            hora = datetime.datetime.now().strftime('%H:%M')
            bot.send_message(message.chat.id, hora)
            tts = gTTS(text='Agora são ' + hora, lang='pt')
            tts.save('horas.mp3')
            audio = open('horas.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)

#-----------------------------------------------------------------------            
#-----------------BREVE CONTEUDO DE UM TERMO NA WIKIPEDIA

        elif 'procure por' in comando:
            procurar = comando.replace('procure por', '')
            wikipedia.set_lang('pt')
            resultado = wikipedia.summary(procurar,5)
            print(resultado)
            bot.send_message(message.chat.id, resultado)
            tts = gTTS(text=resultado, lang='pt')
            tts.save('resultado.mp3')
            audio = open('resultado.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)

#---------------------------------------------------------------------------------
#------------------REESCRITA INEFICIENTE DE TEXTOS

        elif 'reescrever' in comando:
            words = nltk.word_tokenize(comando.lower())
            stop_words = set(stopwords.words('portuguese'))
            filtered_words = [word for word in words if word not in stop_words]
            stemmer = SnowballStemmer('portuguese')
            stemmed_words = [stemmer.stem(word) for word in filtered_words]
            rewritten_text = ' '.join(stemmed_words)

            bot.send_message(message.chat.id, rewritten_text)
#-----------------------------------------------------------------------
# --------------------TOCA MUSICA NO YOUTUBE            

        elif 'toque' in comando:
            musica = comando.replace('toque','')
            resultado = pywhatkit.playonyt(musica)
            tts = gTTS(text='Tocando música', lang='pt')
            tts.save('tocando.mp3')
            audio = open('tocando.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)
#-----------------------------------------------------------------------  


        
        else:
            bot.reply_to(message, 'Não entendi o que você quis dizer. Tente novamente!')


    except Exception as e:
        bot.reply_to(message, f'Ocorreu um erro: {e}')



bot.polling()