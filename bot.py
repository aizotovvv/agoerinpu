Python 3.14.7 (tags/v3.14.7:823f032, Aug  5 2026, 10:51:32) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
import asyncio
import logging
from mcstatus import MinecraftServer
from telegram import Bot

# ==================== НАСТРОЙКИ ====================
# 1. Токен бота от @BotFather (в кавычках)
TELEGRAM_TOKEN = "8984052950:AAGgYMhL7Vy51W5OaT1OWaCKF0lLJ8Jqsek"

# 2. ID вашей группы Telegram (число со знаком минус)
CHAT_ID = -1001700915161

# 3. IP и порт вашего сервера на EternalZero
SERVER_ADDRESS = "play4.eternalzero.cloud:26369"

# 4. Интервал проверки сервера в секундах
CHECK_INTERVAL = 20
# ====================================================

logging.basicConfig(
...     format="%(asctime)s - %(levelname)s - %(message)s",
...     level=logging.INFO
... )
... 
... bot = Bot(token=TELEGRAM_TOKEN)
... is_online = False
... 
... async def check_server():
...     global is_online
...     logging.info("Бот отслеживания сервера EternalZero успешно запущен...")
...     
...     while True:
...         try:
...             # Запрос статуса сервера Minecraft
...             server = await MinecraftServer.async_lookup(SERVER_ADDRESS)
...             status = await server.async_status()
...             
...             # Если сервер был выключен, а теперь ответил
...             if not is_online:
...                 is_online = True
...                 msg = (
...                     "🟢 **Сервер EternalZero запущен!**\n\n"
...                     f"🎮 Игроков онлайн: **{status.players.online}/{status.players.max}**\n"
...                     f"📌 Версия: `{status.version.name}`"
...                 )
...                 await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
...                 logging.info("Сервер запустился. Уведомление отправлено в группу.")
...                 
...         except Exception:
...             # Если сервер недоступен (выключен или перезагружается)
...             if is_online:
...                 is_online = False
...                 msg = "🔴 **Сервер выключен или перезагружается.**"
...                 await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')
...                 logging.info("Сервер выключен.")
...                 
...         await asyncio.sleep(CHECK_INTERVAL)
... 
... if __name__ == '__main__':
