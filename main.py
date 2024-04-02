import json
import config
import requests
import database
from aiogram import *
import functions as func

db = database.ORM()
bot = Bot(config.TOKEN)
dp = Dispatcher(bot)

# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)

@dp.message_handler(commands=['start'])
async def check_money(message: types.Message):
    await message.answer(db.add_user(message.from_user.id))
    await message.answer(config.start)


@dp.message_handler(commands=['check'])
async def check_money(message: types.Message):
    
        mes = await message.answer('⚠️ Запрашиваю данные...')
        values = func.get_coins()
        await mes.edit_text('Получил курсы монет')

        user_money = db.get_buy(message.from_user.id)
        
        page_values = ""
        for coin in values:
            page_values += f'{coin[0][:3]} | $ {coin[1]}\n'

        rub = func.get_rub()

        await mes.edit_text('Считаю проценты монет')
        all_procent = 0
        for coin in values:
            try: 
                buy = user_money.get(coin[0])
                for i in range(len(buy)):
                    all_procent += (coin[1] / buy[i][1] * 100)
            except:
                ...


        await mes.edit_text('Считаю твои средства')
        page_money = ''
        um = 0
        for coin in values:
            try:
                for i in range(len(user_money.get(coin[0]))):
                    um += user_money.get(coin[0])[i][0]
                page_money += f"<code>{coin[0][:3]}</code> = ${rub * um * coin[1]:.2f} | {um} 🪙 | {all_procent - 100:.2f}%\n" if um is not None else ''
            except:
                pass
            

        # Получение баланса пользователя
        # coin, amount, buy = db.get_user_money(message.from_user.id)
        # await mes.edit_text('Вспоминаю твой кошелёк')
        # Считаем кол-во средств в долларах
        # usd_bitcoin = float(f'{bitcoin_value * (float(amount)):.4f}')

        # Вычисляем процент
        # await mes.edit_text('Рассчитываем процент для монет...')
        # procent = usd_bitcoin/buy*100-100
        # await mes.delete()

        # {usd_bitcoin}/{buy}*100-100
        await mes.delete()
        await bot.send_photo(chat_id=message.from_user.id, 
                             photo=open('logotype.png', 'rb').read(), 
                             caption=f'<pre>{page_values}</pre>\nВаш баланс:\n{page_money}',
                             parse_mode='HTML')


@dp.message_handler(commands=['delete'])
async def check_money(message: types.Message):
    money = message.text.replace('/delete ', '')
    money_exist = db.get_user_money(message.from_user.id)
    money_exist[money] = None
    db.update_user_money(money_exist, message.from_user.id)
    await message.answer('Ваш баланс обновлён!')

@dp.message_handler(commands=['change'])
async def check_money(message: types.Message):
    try:
        money = message.text.replace('/change ', '').split('\n')
        money_exist = db.get_user_money(message.from_user.id)

        for data in money:
            money_exist[data.split()[0]] = float(data.split()[1])

        db.update_user_money(money_exist, message.from_user.id)
        await message.answer('Ваш баланс обновлён!')
    except Exception as e:
        print(e)
        await message.answer(config.error_mes, parse_mode='HTML')


@dp.message_handler(commands=['buy'])
async def buy_money(message: types.Message):
    try:
        coin, money, price = message.text.replace('/buy ', '').split(' ')
        amount = db.get_buy(message.from_user.id)
        amount.get(coin).append([float(money), float(price)])
        # print(array)
        db.add_buy(amount=amount, user_id=message.from_user.id)
        await message.answer(f'На кошелёк {coin} добавлено {money} с ценой покупки {price}')

    except Exception as e:
        await message.answer(f'Не удалось обработать команду.\nОшибка: <pre>{e}</pre>\n\nПроверьте правильность сообщения',
                             parse_mode='HTML')

@dp.message_handler(commands=['help'])
async def check_money(message: types.Message):
    if len(message.text) > 6:
        await message.answer(config.help_command.get(
        message.text.replace('/help ', '')
    ), parse_mode='HTML')
    else:
        await message.answer(config.help)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)