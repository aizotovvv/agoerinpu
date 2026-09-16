import asyncio
import os
from aiohttp import web
from mcstatus import JavaServer
from telegram import Bot

# ==================== НАСТРОЙКИ ====================
TELEGRAM_TOKEN = "8984052950:AAGgYMhL7Vy51W5OaT1OWaCKF0lLJ8Jqsek"
CHAT_ID = -1001700915161  # Ваш ID группы
SERVER_ADDRESS = "play4.eternalzero.cloud:26369"
CHECK_INTERVAL = 15
# ====================================================

bot = Bot(token=TELEGRAM_TOKEN)
is_online = False

# Заглушка веб-сервера для Render (чтобы процесс не перезапускался по таймауту)
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Веб-сервер запущен на порту {port}")

async def check_server():
    global is_online
    print("Бот запущен и отслеживает статус сервера...")
    
    while True:
        try:
            server = await JavaServer.async_lookup(SERVER_ADDRESS)
            status = await server.async_status()
            
            # Отправка ТОЛЬКО если сервер был оффлайн, а стал онлайн
            if not is_online:
                is_online = True
                msg = f"🟢 Сервер EternalZero запущен!\n\nИгроков онлайн: {status.players.online}/{status.players.max}"
                await bot.send_message(chat_id=CHAT_ID, text=msg)
                print("Статус изменился: ОНЛАЙН. Уведомление отправлено.")
                
        except Exception as e:
            # Отправка ТОЛЬКО если сервер был онлайн, а стал оффлайн
            if is_online:
                is_online = False
                try:
                    msg = "🔴 Сервер выключен или перезагружается."
                    await bot.send_message(chat_id=CHAT_ID, text=msg)
                    print("Статус изменился: ОФФЛАЙН. Уведомление отправлено.")
                except Exception as send_error:
                    print(f"Ошибка отправки в Telegram: {send_error}")
            else:
                # Если сервер и так оффлайн, просто молча ждем
                pass
                
        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    # Запускаем и веб-сервер для Render, и сам мониторинг параллельно
    await start_dummy_server()
    await check_server()

if __name__ == '__main__':
    asyncio.run(main())
