# Made by SG-Products

# Импортируем нужные библиотеки
import discord
from discord.ext import commands
import random
import sys
from asyncio import sleep
from discord.ui import Button, View
import json

# Делаем ембед
def create_embed(title, description, footer):
    embed = discord.Embed(title=title, description=description, color=0x000001)
    embed.set_footer(text=footer)
    return embed

# Сохраняемся
def save_user_data():
    pass

# Отправка ембеда
async def send_embed(ctx, title, description, footer="Информация"):
    title = f'```{title}```'
    description = f'```{description}```'
    embed = create_embed(title, description, footer)
    await ctx.send(embed=embed)

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
          await sleep(5)
          await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"Мой префикс: {prefix}"))
          await sleep(5)
          await bot.change_presence(status=discord.Status.online, activity=discord.Game("Мы с гхс мир...?"))
          await sleep(5)

# Делаем комманду для зарабатывания $REDCOIN
@bot.command()
async def click(ctx):
    user_id = ctx.author.id
    if user_id not in user_data:
        user_data[user_id] = {"points": 0, "level": 1}
    
    click_points = random.randint(1, 5)
    user_data[user_id]["points"] += click_points
        
    save_user_data()
    
    await send_embed(ctx, "Тапаешь ты, тапаю я......", f"Вы получили {click_points} $REDCOIN!")

# Делаем комманду для покупки нового уровня
@bot.command()
async def levelup(ctx):
    user_id = ctx.author.id
    if user_id not in user_data:
        user_data[user_id] = {"points": 0, "level": 1, "zvanie": "Обычный"}

    level_cost = user_data[user_id]["level"] * 10
    if user_data[user_id]["points"] >= level_cost:
        user_data[user_id]["points"] -= level_cost
        user_data[user_id]["level"] += 1
        await send_embed(ctx, "Поздравляем!", f"Поздравляем! Вы прокачали уровень до {user_data[user_id]['level']}!")
    else:
        await send_embed(ctx, "Недостаточно средств", f"Вам нужно еще {level_cost - user_data[user_id]['points']} $REDCOIN для прокачки уровня.")

# Делаем комманду для просмотра сколько у нас $REDCOIN'ов и уровень'
@bot.command()
async def stats(ctx):
    user_id = ctx.author.id
    if user_id in user_data:
        points = user_data[user_id]["points"]
        level = user_data[user_id]["level"]
        zvanie = user_data[user_id].get("zvanie", "Обычный")
        await send_embed(ctx, "Статистика", f"Ваш баланс $REDCOIN: {points}\nВаш уровень: {level}\nВаши звания: {zvanie}")
    else:
        await send_embed(ctx, "Информация", "У вас еще нет $REDCOIN. Используйте команду .click!")

# Делаем комманду для мониторинга статуса листинга
@bot.command()
async def listing_status(ctx):
	if status_listing == True:
		await send_embed(ctx, "Статус листинга", f"Статус листинга: :white_check_mark:")
	elif status_listing == False:
		await send_embed(ctx, "Статус листинга", f"Статус листинга: :x:")
	else:
		await send_embed(ctx, "Статус листинга", f"Не возможно узнать статус листинга.")

# Делаем комманду для листинга (фейк)
@bot.command()
async def listing(ctx):
	if status_listing == False:
		await ctx.send(f'Листинг не доступен. Что-бы проверить статус введите комманду: **.listing_status**')
		await send_embed(ctx, "Листинг", "Листинг не доступен. Что-бы проверить статус введиье комманду: **.listing_status**")
	elif status_listing == True:
		await send_embed(ctx, "Листинг", "# Листинг $REDCOIN уже тут: <https://only-fans.uk/red228kombat>")
	else:
		await send_embed(ctx, "Листинг", "Листинг не доступен.")

# Делаем комманду для узнавания курса $REDCOIN
@bot.command()
async def exchange_rate(ctx):
	await send_embed(ctx, "Курс $REDCOIN", ":bar_chart: Сегодняшний курс $REDCOIN: 1 $REDCOIN = 0,429₽")

# Делаем комманду для кика пидора с гхс
@bot.command()
async def ghs_kick(ctx, member: discord.Member, *, reason="Причина не указана"):
    if not ctx.author.guild_permissions.administrator:
        return await send_embed(ctx, "Ошибка", f'<@{ctx.author.id}> у вас нет прав!', "Кик пользователя")
    
    await member.kick(reason=reason)
    await send_embed(ctx, "Успешно", f'{member.display_name} был успешно кикнут.\nПричина: {reason}', "Кик пользователя")

# Делаем комманду для инвайта бота на другой сервер
@bot.command()
async def invite(ctx):
	await ctx.send(f'<https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot+applications.commands&permissions=8>')

# Делаем комманду для показа авторов проекта
@bot.command()
async def credits(ctx):
    await send_embed(ctx, "Авторы проекта", "Кодеры: sgysh3nka, dudethatwas_79324, squake.xp, вся команда SG-Products.\nОсобенная благодарность: MSC Empire, kartohka000")

# Делаем комманду для узнавания статуса бота
@bot.command()
async def status(ctx):
	await ctx.send(status_bot_text)

# Делаем комманду для бана пидора с гхс
@bot.command()
async def ghs_ban(ctx, member: discord.Member, *, reason="Причина не указана"):
    if not ctx.author.guild_permissions.administrator:
        return await send_embed(ctx, "Ошибка", f'<@{ctx.author.id}> у вас нет прав!', "Бан пользователя")
    
    await member.ban(reason=reason)
    await send_embed(ctx, "Успешно", f'{member.display_name} был успешно забанен.\nПричина: {reason}', "Бан пользователя")

# Делаем комманду для отправления сообщения от лица бота
@bot.command()
async def say(ctx, *, message):
    if not ctx.author.guild_permissions.administrator:
        return await send_embed(ctx, "Ошибка", f'<@{ctx.author.id}> у вас нет прав!', "Отправка сообщения")
    
    await ctx.send(message)
    print(f"Сообщение отправлено через бота: {message}. Кто сделал: {ctx.author}")

# Добавляем деньги самому себе >:)
@bot.command()
async def addown(ctx, money):
    s = ctx.author
    if not str(s.id) == owner_id:
        await ctx.send('Вы не можете использовать эту команду.')
        return
    
    money = int(money)
    user_data[owner_id]["points"] += money
    
    
    await ctx.send(f'Успешно добавлено {money} $REDCOIN к балансу.')

# Комманда с всякой нужной инфой (хелп)
@bot.command()
async def help(ctx):
	await send_embed(ctx, "Помощь", f'# Red Kombat by SG-Products\n# Комманды:\n# Тапалка:\n.click\n.levelup\n.stats\n# Листинг и тд.:\n.listing\n.listing_status\n.exchange_rate\n# Модерация:\n.ghs_ban\n.ghs_kick\n.say\n# Для создателя:\n.addown\n# Магазин:\n.shop\n.buy\n# Другое:\n.status\n.invite\n.credits', "Комманды")

# Магазин званий
@bot.command()
async def shop(ctx):
	await send_embed(ctx, "Убежище реда", '# Товары:\n1. Звание "Отчим реда"\n2. Звание "босс гхс"', "Магазин")

# Система покупки звания
@bot.command()
async def buy(ctx, zvaniebuy: int):
    user_id = ctx.author.id
    if user_id not in user_data:
        user_data[user_id] = {"points": 0, "level": 1, "zvanie": "Обычный"}

    if zvaniebuy == 1:
        if user_data[user_id]["points"] >= 10:
            user_data[user_id]["points"] -= 10
            user_data[user_id]["zvanie"] = "Отчим реда"
            await send_embed(ctx, "Покупка успешна", 'Вы успешно купили звание "Отчим реда"!', "Магазин")
        else:
            await send_embed(ctx, "Ошибка", "Не достаточно средств для покупки звания 'Отчим реда'.", "Магазин")
    elif zvaniebuy == 2:
        if user_data[user_id]["points"] >= 100:
            user_data[user_id]["points"] -= 100
            user_data[user_id]["zvanie"] = "Босс гхс"
            await send_embed(ctx, "Покупка успешна", 'Вы успешно купили звание "Босс гхс"!', "Магазин")
        else:
            await send_embed(ctx, "Ошибка", "Не достаточно средств для покупки звания 'Босс гхс'.", "Магазин")
    else:
        await send_embed(ctx, "Ошибка", "Неверный номер товара.", "Магазин")

# Выходим
@bot.event
async def on_disconnect():
    sys.exit()

# Запускаем наше чудо
bot.run(token)
