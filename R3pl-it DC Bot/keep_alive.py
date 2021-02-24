#BO KOMUT BOTUNUZU AKTİF TUTMANIZI SAĞLAR YANİ SOL TARAFTA ÇIKAN SİTE BENZERİ ŞEY BU KOMUT SAYESİNDE ÇALIŞIR
from flask import Flask
from threading import Thread

app = Flask('')

#BU KISMA HELLO I AM ALİVE! YERİNE SOL ÜSTTE YAZMASINI İSTEDİĞİNİZ ŞEYİ YAZABİLİRSİNİZ MERAK ETMEYİN KOMUTU BOZMAZ
@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()