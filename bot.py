import json
import requests
from aiogram import Bot, Dispatcher, executor, types


BOT_TOKEN = '5316381275:AAF5wpb3Xf2lLQspDLedThfMOTyui4SQy1U'
domain = 'https://bid.pythonanywhere.com/api/create'
# domain = 'http://localhost:8000/api/create'
bot = Bot(token = BOT_TOKEN)
dispatch = Dispatcher(bot)


credentials = dict()
source_list = str()
channels_list = ['@Axbarot_live', '@TYUZBEK', '@shopirlar', '@YOL_YOLAKAY', '@Salomatlik_sirlari', '@Samarqand_Samarqandliklar_24', '@Uznext', '@Ginekologiya', '@UnchaMuncha', '@tezkorxabarlar', '@latifalar_uz', '@Onalar_kanali']
channels_list.sort()
for i in channels_list:
	source_list += f'{channels_list.index(i)+1}. {i}\n'

sources_ru = source_list + '\n\nИз какого источника вы нас нашли (отправьте номер источника)'
sources_en = source_list + '\n\nFrom which source you found us (send the number of source)'
sources_uz = source_list + '\n\nBizni qaysi manbadan topdingiz (manba raqamini yuboring)'


@dispatch.message_handler(commands = ['start', 'help', 'restart'])
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
	elif credentials[message['from']['id']]['language'] == 'uz':
		keyboard.add(types.KeyboardButton("☎️ Jo'natish", request_contact = True))
		await message.answer("Iltimos telefon raqamingizni jo'nating", reply_markup = keyboard)



@dispatch.message_handler(content_types = types.ContentType.CONTACT)
async def contact(message: types.Message):
	credentials[message['from']['id']]['phone'] = message.contact.phone_number

	keyboard = types.InlineKeyboardMarkup(row_width = 1)
	keyboard.add(types.InlineKeyboardButton(text = "Lactovita", callback_data = "product_Lactovita"))
	keyboard.add(types.InlineKeyboardButton(text = "Androgard", callback_data = "product_Androgard"))
	keyboard.add(types.InlineKeyboardButton(text = "Byuti Vit", callback_data = "product_Byuti Vit"))

	if credentials[message['from']['id']]['language'] == 'ru':
		await message.answer("Выберите продукт, который вас интересует", reply_markup = keyboard)
	elif credentials[message['from']['id']]['language'] == 'en':
		await message.answer("Choose the product you interested in", reply_markup = keyboard)
	elif credentials[message['from']['id']]['language'] == 'uz':
		await message.answer("Sizni qiziqtirgan maxsulotni tanlang", reply_markup = keyboard)



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




@dispatch.callback_query_handler(lambda data: "product" in data.data)
async def product(call: types.CallbackQuery):
	await call.answer()
	credentials[call['from']['id']]['product'] = call.data.split('product_')[1]

	keyboard = types.InlineKeyboardMarkup(row_width = 4)
	keyboard.row(
		types.InlineKeyboardButton(text = "1", callback_data = "source_1"),
		types.InlineKeyboardButton(text = '2', callback_data = "source_2"),
		types.InlineKeyboardButton(text = '3', callback_data = "source_3"),
		types.InlineKeyboardButton(text = '4', callback_data = "source_4"),
		types.InlineKeyboardButton(text = '5', callback_data = "source_5"),
		types.InlineKeyboardButton(text = '6', callback_data = "source_6"),
	)
	keyboard.row(
		types.InlineKeyboardButton(text = '7', callback_data = "source_7"),
		types.InlineKeyboardButton(text = '8', callback_data = "source_8"),
		types.InlineKeyboardButton(text = "9", callback_data = "source_9"),
		types.InlineKeyboardButton(text = '10', callback_data = "source_10"),
		types.InlineKeyboardButton(text = '11', callback_data = "source_11"),
		types.InlineKeyboardButton(text = '12', callback_data = "source_12"),
	)

	if credentials[call['from']['id']]['language'] == 'ru':
		await call.message.answer(sources_ru, reply_markup = keyboard)
	elif credentials[call['from']['id']]['language'] == 'en':
		await call.message.answer(sources_en, reply_markup = keyboard)
	elif credentials[call['from']['id']]['language'] == 'uz':
		await call.message.answer(sources_uz, reply_markup = keyboard)





@dispatch.callback_query_handler(lambda data: "source" in data.data)
async def source(call: types.CallbackQuery):
	await call.answer()
	credentials[call['from']['id']]['source'] = int(call.data.split('source_')[1])-1
	request = requests.post(domain, data = json.dumps(credentials[call['from']['id']]))
	if (request.status_code == 200):
		if credentials[call['from']['id']]['language'] == 'ru':
			template = f"Заявка отправлена:\n\nИмя: {credentials[call['from']['id']]['name']}\nТелефон: {credentials[call['from']['id']]['phone']}\nПродукт: {credentials[call['from']['id']]['product']}\nИсточник: {channels_list[credentials[call['from']['id']]['source']]}"
		elif credentials[call['from']['id']]['language'] == 'en':
			template = f"Application sent:\n\nName: {credentials[call['from']['id']]['name']}\nPhone: {credentials[call['from']['id']]['phone']}\nProduct: {credentials[call['from']['id']]['product']}\nSource: {channels_list[credentials[call['from']['id']]['source']]}"
		elif credentials[call['from']['id']]['language'] == 'uz':
			template = f"Arizangiz jonatildi:\n\nIsm: {credentials[call['from']['id']]['name']}\nTelefon raqam: {credentials[call['from']['id']]['phone']}\nMaxsulot: {credentials[call['from']['id']]['product']}\nManbada: {channels_list[credentials[call['from']['id']]['source']]}"
		await call.message.answer(template, reply_markup = types.ReplyKeyboardRemove())
	else:
		if credentials[call['from']['id']]['language'] == 'ru':
			await call.message.answer('Что-то пошло не так ☹️, повторите попытку позже')
		elif credentials[call['from']['id']]['language'] == 'en':
			await call.message.answer('Something went wrong ☹️, please try again later')
		elif credentials[call['from']['id']]['language'] == 'uz':
			await call.message.answer('Nimadir xato ketdi ☹️, keyinroq qayta urinib ko‘ring')


if __name__ == '__main__':
	executor.start_polling(dispatch)