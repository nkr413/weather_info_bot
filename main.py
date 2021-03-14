import telebot, requests

token = "1640367472:AAHzMg8kXOsIDoL4aLtBzmiBcBcsWiVI1TM"
bot = telebot.TeleBot(token, parse_mode=None)

api_keyOne = "4d71e2ca78b19770ec229c75b21db70c"
api_keyTwo = "a6ef7ec1f6c949ab82e7f582bac77c48"

base = {
	"country_name": "", "main_temp": "", "feels_temp": "", "humidity": "",
	"speed": "", "deg": "", "cloud": ""
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Отправьте мне название города и получите погоду")

@bot.message_handler(content_types=['text'])
def send_text(message):
	txt = message.text.lower()
	
	try:
		temp = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + txt + "&units=metric&appid=" + api_keyOne).json()
		geo = requests.get("https://api.opencagedata.com/geocode/v1/json?q=" + txt + "&key=" + api_keyTwo).json()

		base["country_name"] = f"Локация:  {(geo['results'][0]['formatted'])}\n\n"
		base["main_temp"] = f"Температура:  {(temp['main']['temp'])}°C\n"
		base["feels_like"] = f"Ощущается:  {(temp['main']['feels_like'])}°C\n"
		base["humidity"] = f"Влажность:  {(temp['main']['humidity'])}%\n"
		base["speed"] = f"Скор. ветра:  {(temp['wind']['speed'])}метр/сек\n"
		base["deg"] = f"Направ. ветра:  {(temp['wind']['deg'])}град\n"
		base["cloud"] = f"Облачность:  {(temp['clouds']['all'])}%\n"
		icon = 'http://openweathermap.org/img/wn/' + temp['weather'][0]['icon'] + '@2x.png'
		result = ""

		for key, value in base.items(): result += value
		bot.send_photo(message.chat.id, icon, caption=result)

	except:
		bot.send_message(message.chat.id, "Такой город не найден, введите пожалуйста правильно")

bot.polling()