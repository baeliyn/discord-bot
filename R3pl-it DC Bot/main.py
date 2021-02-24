#IMPORTLAR

#DİSCORD KOMUTLARINI İMPORT EDER
import discord
#.ENV GİBİ BAŞKA DOSYALARDAN TOKEN VS. ÇEKMENİZİ SAĞLAR
import os
#ALINTILARI ÇEKMENİZ VE JSONA DÖNÜŞTÜRMENİZ VS. DURUMLARINA YARAYAN BİR KOMUTTUR
import requests
import json
#BİR ŞEYİ RASTGELE OLARAK SEÇMEYE YARAYAN BİR PYHTON KOMUDUDUR
import random
#REPLİT'İN DATABASESİNİ İMPORT EDER
from replit import db
#KEEP ALİVE'Yİ ÇEKER
from keep_alive import keep_alive

#CLIENT
client = discord.Client()

#... WORDSLER DENDİĞİNDE STARTER ...LERİ/LARI GÖNDER
sad_words = ["üzgünüm", "depresyondayım", "mutsuzum", "sinirliyim", "acınası bir haldeyim", "çok üzgünüm"]

starter_encouragements = [
  "sen muhteşem birisisin!",
  "sakın kendini üzme.",
  "mutlu kalmak zordur seni anlayabiliyorum ama kendini üzme"
]


yey_words = ["yey", "YEY", "Yey"]

starter_yey = [
  "YEEEEEY!",
  "yeeeeeeey!:yum: ",
]

#BOTUN CEVAP VERMESİNİN AÇILIP KAPATILMASININ DATABASE TARAFI
if "responding" not in db.keys():
  db["responding"] = True

#ALINTININ ÇEKİLMESİ
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

#ÜZGÜNÜM (SAD WORDS KISMINDA DENİLEN KELİMELERİ VE CEVAPLARINI BELİRLEMİŞTİK) EKLE-ÇIKARIN FUNCTİONLARINI OLUŞTURUYORUZ
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

#BOT GİRİŞ YAPTIĞI ZAMAN (ACTİVİTY NORMALDE BU KOMUT TARZI İÇİN KULLANILAMIYOR AMA BEN KENDİM YAZARAK BİR TANE OLUŞTURDUM)
@client.event
async def on_ready():
    activity = discord.Game(name="!yardım", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print("Aktif!")

#MESAJLARI TANIMLIYORUZ VE MESAJ SAHİBİNİN BOT OLMAMASINI SÖYLÜYORUZ
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
#ALINTI MESAJLARINI APIDEN ÇEKİP !alıntı YAZINCA ATMASINI SAĞLIYORUZ
  if msg.startswith('!alıntı'):
    quote = get_quote()
    await message.channel.send(quote)

#BU KISIMDA ARRAY ŞEKLİNDE DEĞİŞTİRİLEBİLİR VE DEĞİŞTİRİLEMEZ 1 TANE KELİMEYE CEVAP VEREN SA-AS KOMUDU YAPTIK
#NAPİM YAZINCA BİR YAZI ATAN DÜZ BİR PİNG PONG
  if msg.startswith('napim'):
      await message.channel.send("yalnız napim demenin modası geçmedi mi")
#YUKARIDA BELİRLEDİĞİMİZ YEY WORDSLER GELİNCE STARTER WORDSLERİ ATAR
  if any(word in msg for word in yey_words):
        await message.channel.send(random.choice(starter_yey))
#EĞER SUNUCUNUZ BUNLARA İZİN VERMİYORSA YEY WORDS,STARTER YEYS VE BU KOMUTLARI SİLEBİLİRSİNİZ


#CEVAP VERMEYİ KONTROL EDEREK MOTİVASYON MESAJI EKLEME VE SİLMENİN KOMTLARINI YAZIYORUZ
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
#YENİ MORAL EKLEME KOMUDU
  if msg.startswith("!yeni-moral"):
    encouraging_message = msg.split("!yeni-moral ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("Yeni Motive Edici Mesaj Eklendi.")
#MORAL CEVAPLARINDAN BİRİNİ !sil __ YAZARAK SİLME KOMUDU
  if msg.startswith("!sil-moral"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("!sil-moral",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
#MORAL CEVAPLARINI LİSTELEME KOMUDU
  if msg.startswith("!liste-moral"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

#CEVAP VERMEYİ AÇIP KAPATMA KOMUDU
  if msg.startswith("!cevap-verme"):
    value = msg.split("!cevap-verme ",1)[1]

    if value.lower() == "aç":
      db["responding"] = True
      await message.channel.send("Cevap Verme Açıldı.")
    if value.lower() == "kapat":
      db["responding"] = False
      await message.channel.send("Cevap Verme Kapatıldı.")


#YARDIM KOMUDU
    if msg.startswith("!yardım"):
    embed=discord.Embed(title="PRASTY CODE", url="https://discord.gg/UruBEetE", description="Githubımı kullandığınız için teşekkür ederim :) umarım eğlenirsiniz", color=0x992d22)

    embed.set_author(name="-- ད ⁸⁷¹ｉmａｍㄠ --", url="http://theias.xyz/", icon_url="https://cdn.discordapp.com/attachments/806112454470795267/808345984731578379/1664606672481286_c5_720x720.jpeg")

    embed.add_field(name="`!yardım`", value="cavalleria.py'nin yapabileceklerini atar", inline=True)

    embed.add_field(name="`!alıntı`", value="size rastgele bir motivasyon alıntısı atar(İngilizce)", inline=True)

    embed.add_field(name="`üzgünüm/!yeni-moral/!sil-moral/!liste-moral`", value="en iyi kısmı ise bota kod kullanmadan ekleme yapabilmenizdir botun size üzgün olmanız durumunda söylediği sözlere ekleme yapmak istiyorsanız tek yazmanız gereken !yeni .... şeklinde motive edici sözünüzü yazmaktır eğer yazdığınız sözü iptal etmek istiyorsanız !sil ... şeklinde ... kısmına silmek istediğiniz motive edici sözün listedeki numarasını yazmaktır yani !sil 1 gibi (Moral ekleme çıkarma veya listeleme işlemleri sadece yetkililer tarafından kullanılabilir)", inline=False)

    embed.add_field(name="`!cevap-verme kapat/!cevap-verme aç`", value="eğer botun size motive edici cevaplar veya duyurular atması sizi sinir ettiyse tek yazmanız gereken !cevap-verme kapat'dır eğer bot size motive edici sözleri söylemiyorsa birisi bu komutu kapatmıştır tek yapmanız gereken !cevap-verme aç yazarak açmaktır :) (Bu Komut Sadece Yetkililer Tarafından Kullanılabilir)", inline=False)


    embed.set_footer(text="İYİ EĞLENCELER / PRASTY / THEİA")
    await message.channel.send(embed=embed)


#SADECE YETKİLİLERİN KULLANMASINI İSTEDİĞİNİZ KOMUTLAR İÇİN BU KOD YAPISINDA YETKİSİNİ KONTROL ETME KOMUTU KULLANILAMADIĞI İÇİN SUNUCUNUZUN KÜFÜR ENGELLEYİCİ BOTUNA KULLANILMASINI 
#İSTEMEDİĞİNİZ KOMUTLARI EKLEYİN VE BU SAYEDE İNSANLAR BU KOMUTLARI KULLANAMAYACAKTIR EĞER KÜFÜR ENGELLEYİCİ BOTUNUZ YOKSA O ZAAN PİNG PONG TÜRÜNDE BU KOMUTLAR YAZILDIĞINDA YETKİLİ
#DEĞİLSEN VE BİR DAHA KULLANIRSAN BANLANIRSIN VEYA KİCKLENİRSİN ŞEKLİNDE BİR YAZI ÇIKARTTIRABİLİRSİNİZ BU DURUMDA KULLANAYACAKLARDIR

keep_alive()
client.run(os.getenv('TOKEN'))