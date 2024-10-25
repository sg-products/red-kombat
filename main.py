# Made by SG-Products

# Импортируем нужные библиотеки
import discord
from discord.ext import commands
import random
import sys
import json
from asyncio import sleep

# Загрузка данных пользователей из файла JSON
def load_user_data():
    global user_data
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}
        
load_user_data()

# Сохранение данных пользователей в файл JSON
def save_user_data():
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file)

# Обновление данных пользователя в файле JSON
def update_user_data():
    save_user_data()

# Токен, префикс и тд.
prefix = '.'
token = 'your_token_here'
owner_id = '916723526696841217'

# Импортируем интенты
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Делаем статус листинга
status_listing = False

# Статус бота
status_bot_text = "Статус бота: :x: Проект временно приостановлен для получения обновлений. Причина: Блокировка Discord в Российской Федерации."

# Делаем префикс
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

# Место для хранения даты о пользователе
user_data = {}
# Делаем ивент что-бы узнать когда бот будет готов к работе
@bot.event
async def on_ready():
    print(f'Тихо зашёл как {bot.user}')
    
    while True:
          await bot.change_presence(status=discord.Status.online, activity=discord.Game("Собираем деньги на мозги для реда"))
          await sleep(15)
          await bot.change_presence(status=discord.Status.online, activity=discord.Game("Мой префикс: ."))

# Делаем комманду для зарабатывания $REDCOIN
@bot.command()
async def click(ctx):
    user_id = ctx.author.id
    if user_id not in user_data:
        user_data[user_id] = {"points": 0, "level": 1}
    
    click_points = random.randint(1, 5)
    user_data[user_id]["points"] += click_points

    await ctx.send(f'Вы кликнули и получили {click_points} $REDCOIN! Всего $REDCOIN: {user_data[user_id]["points"]}')

# Делаем комманду для покупки нового уровня
@bot.command()
async def levelup(ctx):
    user_id = ctx.author.id
    if user_id not in user_data:
        user_data[user_id] = {"points": 0, "level": 1, "zvanie": 'Обычный'}
    
    if user_data[user_id]["points"] >= user_data[user_id]["level"] * 10:
        user_data[user_id]["points"] -= user_data[user_id]["level"] * 10
        user_data[user_id]["level"] += 1
        await ctx.send(f'Поздравляем! Вы прокачали уровень до {user_data[user_id]["level"]}!')
    else:
        await ctx.send(f'Вам нужно еще {user_data[user_id]["level"] * 100 - user_data[user_id]["points"]} $REDCOIN для прокачки уровня.')

# Делаем комманду для просмотра сколько у нас $REDCOIN'ов и уровень'
@bot.command()
async def stats(ctx):
    user_id = ctx.author.id
    if user_id in user_data:
        points = user_data[user_id]["points"]
        level = user_data[user_id]["level"]
        zvanie = user_data[user_id]["zvanie"]
        await ctx.send(f'Ваш баланс $REDCOIN: {points}\nВаш уровень: {level}\nВаши звания: {zvanie}')
    else:
        await ctx.send(f'У вас еще нет $REDCOIN. Используйте команду **.click**!')

# Делаем комманду для мониторинга статуса листинга
@bot.command()
async def listing_status(ctx):
	if status_listing == True:
		await ctx.send(f'Статус листинга: :white_check_mark:')
	elif status_listing == False:
		await ctx.send(f'Статус листинга: :x:')
	else:
		await ctx.send(f'Невозможно узнать статус листинга.')

# Делаем комманду для листинга (фейк)
@bot.command()
async def listing(ctx):
	if status_listing == False:
		await ctx.send(f'Листинг не доступен. Что-бы проверить статус введите комманду: **.listing_status**')
	elif status_listing == True:
		await ctx.send(f'# Листинг $REDCOIN уже тут: <https://only-fans.uk/red228kombat>')
	else:
		await ctx.send(f'Ошибка листинга.')

# Делаем комманду для узнавания курса $REDCOIN
@bot.command()
async def exchange_rate(ctx):
	await ctx.send(f':bar_chart: Сегодняшний курс $REDCOIN: 1 $REDCOIN = 0,429₽')

# Делаем комманду для кика пидора с гхс
@bot.command()
async def ghs_kick(ctx, member : discord.Member, *, reason):
	s = ctx.author
	if not s.guild_permissions.administrator:
		return await ctx.channel.send(f'<@{s.id}> у тебя нету прав!')
	if reason == None:
		await member.kick(reason="Причина для бана пидора с гхс не указана.")
	await member.kick(reason=reason)
	await ctx.send(f'Пидор с гхс был успешно кикнут.')
	print("Был кикнут пидор с гхс! Причина:" , reason, "Кто сделал:" ,s)

# Делаем комманду для инвайта бота на другой сервер
@bot.command()
async def invite(ctx):
	await ctx.send(f'<https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot+applications.commands&permissions=8>')

# Делаем комманду для показа авторов проекта
@bot.command()
async def credits(ctx):
	await ctx.send(f'Кодеры: sgysh3nka, dudethatwas_79324, squake.xp, вся комманда SG-Products.\nОсобенное спасибо: MSC Empire, kartohka000')

# Делаем комманду для узнавания статуса бота
@bot.command()
async def status(ctx):
	await ctx.send(status_bot_text)

# Делаем комманду для бана пидора с гхс
@bot.command()
async def ghs_ban(ctx, member : discord.Member, *, reason):
	s = ctx.author
	if not s.guild_permissions.administrator:
		return await ctx.send(f'<@{s.id}> у тебя нету прав!')
	if reason == None:
		await member.ban(reason="Причина для бана пидора с гхс не указана.")
	await member.ban(reason=reason)
	await ctx.send(f'Пидор с гхс был успешно кикнут.')
	print("Был забанен пидор с гхс! Причина:" ,reason, "Кто сделал:" ,s)

# Делаем комманду для отправления сообщения от лица бота
@bot.command()
async def say(ctx, *, message):
	s = ctx.author
	if not s.guild_permissions.administrator:
		return await ctx.send(f'<@{s.id}> у тебя нету прав!')
	await ctx.send(message)
	print("Было отправлено сообщение через бота (say)! Сообщение:" ,message, "Кто сделал:" ,s)

# Добавляем деньги самому себе >:)
@bot.command()
async def addown(ctx, money):
    s = ctx.author
    if not str(s.id) == owner_id:
        await ctx.send('Вы не можете использовать эту команду.')
        return
    
    money = int(money)
    user_data[owner_id]["points"] += money
    
    save_user_data()
    
    await ctx.send(f'Успешно добавлено {money} $REDCOIN к балансу.')

# Делаем магазин
@bot.command()
async def shop(ctx):
	await ctx.send(f'Добро пожаловать в бункер реда!\nВот наши товары:\n1. Звание "Отчим реда" - 10 $REDCOIN\n2. Звание "Босс гхс" - 100 $REDCOIN\n-# p.s: что-бы что-то купить напиши **.buy** и номер предмета.')

# Покупка званий
@bot.command()
async def buy(ctx, zvaniebuy: int):
	user_id = ctx.author.id
	if zvaniebuy == '1':
		if user_data[user_id]["points"] >= '10':
			user_data[user_id]["points"] -= '10'
			user_data[user_id]["zvanie"] == 'Отчим реда'
				
			await ctx.send(f'Вы успешно купили звание "Отчим реда"!')
		else:
			await ctx.send(f'Не достаточно средств для покупки звания "Отчим реда".')
	elif zvaniebuy == '2':
		if user_data[user_id]["points"] >= '100':
			user_data[user_id]["points"] -= '100'
			user_data[user_id]["zvanie"] == 'Босс гхс'
			
			save_user_data()
			
			await ctx.send(f'Вы успешно купили звание "Босс гхс"!')
		else:
			await ctx.send(f'Не достаточно средств для покупки звания "Босс гхс".')

# Выходим
@bot.event
async def on_disconnect():
    update_user_data()
    sys.exit()

# Запускаем наше чудо
bot.run(token)
