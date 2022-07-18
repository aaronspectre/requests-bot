import json
import requests
from aiogram import Bot, Dispatcher, executor, types


BOT_TOKEN = '5316381275:AAF5wpb3Xf2lLQspDLedThfMOTyui4SQy1U'
domain = 'https://bid.pythonanywhere.com/api/create'
bot = Bot(token = BOT_TOKEN)
dispatch = Dispatcher(bot)


credentials = dict()


@dispatch.message_handler(commands = ['start', 'help'])
async def start(message: types.Message):
	credentials[message['from']['id']] = dict()
	credentials[message['from']['id']]['restriction'] = False
	keyboard = types.InlineKeyboardMarkup(row_width = 3)
	keyboard.row(
		types.InlineKeyboardButton(text = "🇬🇧", callback_data = "language_en"),
		types.InlineKeyboardButton(text = '🇷🇺', callback_data = "language_ru"),
		types.InlineKeyboardButton(text = '🇺🇿', callback_data = "language_uz"))
	await message.reply('🇬🇧 Please choose language\n🇺🇿 Iltimos tilni tanlang\n🇷🇺 Пожалуйста выберите язык', reply_markup = keyboard)



@dispatch.message_handler()
async def default_answer(message: types.Message):
	if credentials[message['from']['id']]['restriction'] == False:
		return

	credentials[message['from']['id']]['restriction'] = False
	credentials[message['from']['id']]['name'] = message.text
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

	if credentials[message['from']['id']]['language'] == 'ru':
		keyboard.add(types.KeyboardButton('☎️ Отправить', request_contact = True))
		await message.answer('Отправьте пожалуйста ваш номер телефона', reply_markup = keyboard)
	elif credentials[message['from']['id']]['language'] == 'en':
		keyboard.add(types.KeyboardButton('☎️ Share', request_contact = True))
		await message.answer('Please send your phone number', reply_markup = keyboard)
	elif credentials[message['from']['id']]['language'] == 'ru':
		keyboard.add(types.KeyboardButton("☎️ Jo'natish", request_contact = True))
		await message.answer("Iltimos telefon raqamingizni jo'nating", reply_markup = keyboard)



@dispatch.message_handler(content_types = types.ContentType.CONTACT)
async def contact(message: types.Message):
	credentials[message['from']['id']]['phone'] = message.contact.phone_number
	print(credentials[message['from']['id']])

	if credentials[message['from']['id']]['language'] == 'ru':
		template = f"Заявка отправлена:\n\nИмя: {credentials[message['from']['id']]['name']}\nТелефон: {credentials[message['from']['id']]['phone']}"
	elif credentials[message['from']['id']]['language'] == 'en':
		template = f"Application sent:\n\nName: {credentials[message['from']['id']]['name']}\nPhone: {credentials[message['from']['id']]['phone']}"
	elif credentials[message['from']['id']]['language'] == 'ru':
		template = f"Arizangiz jonatildi:\n\nIsm: {credentials[message['from']['id']]['name']}\nTelefon raqam: {credentials[message['from']['id']]['phone']}"

	request = requests.post(domain, data = json.dumps(credentials[message['from']['id']]))
	if (request.status_code == 200):
		await message.answer(template, reply_markup = types.ReplyKeyboardRemove())
	else:
		await message.answer(':(')



@dispatch.callback_query_handler(lambda data: "language" in data.data)
async def language(call: types.CallbackQuery):
	credentials[call['from']['id']]['restriction'] = True
	await call.answer()
	if 'en' in call.data:
		credentials[call['from']['id']]['language'] = 'en'
		await call.message.answer('Please send your full name')
	elif 'ru' in call.data:
		credentials[call['from']['id']]['language'] = 'ru'
		await call.message.answer('Пожалуйста отправьте ваше полное имя')
	elif 'uz' in call.data:
		credentials[call['from']['id']]['language'] = 'uz'
		await call.message.answer("Iltimos to'liq ismingizni jo'nating")


if __name__ == '__main__':
	executor.start_polling(dispatch)