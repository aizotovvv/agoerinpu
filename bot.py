import asyncio
from mcstatus import JavaServer
from telegram import Bot

# ==================== НАСТРОЙКИ ====================
TELEGRAM_TOKEN = "8984052950:AAGgYMhL7Vy51W5OaT1OWaCKF0lLJ8Jqsek"
CHAT_ID = -1001700915161
SERVER_ADDRESS = "play4.eternalzero.cloud:26369"
CHECK_INTERVAL = 15
# ====================================================

bot = Bot(token=TELEGRAM_TOKEN)
is_online = False

async def check_server():
    global is_online
    print("Бот запущен и отслеживает статус сервера...")
    
    while True:
        try:
            # В новых версиях используется JavaServer вместо MinecraftServer
            server = await JavaServer.async_lookup(SERVER_ADDRESS)
            status = await server.async_status()
            
            if not is_online:
                is_online = True
                msg = f"🟢 Сервер EternalZero запущен!\n\nИгроков онлайн: {status.players.online}/{status.players.max}"
                await bot.send_message(chat_id=CHAT_ID, text=msg)
                print("Уведомление о старте отправлено.")
                
        except Exception:
            if is_online:
                is_online = False
                msg = "🔴 Сервер выключен или перезагружается."
                await bot.send_message(chat_id=CHAT_ID, text=msg)
                print("Сервер выключился.")
                
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    asyncio.run(check_server())
