import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sys
import getpass

# Настройки бота
TOKEN = "ВАШ_TELEGRAM_BOT_TOKEN"
AUTHORIZED_USERS = [123456789]  # Замените на ваш User ID

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user.id not in AUTHORIZED_USERS:
        await update.message.reply_text('⛔ Доступ запрещен')
        return
    
    response = (
        f'🔒 Авторизация пройдена\n'
        f'💻 Управление компьютером {getpass.getuser()}\n\n'
        '🚀 Команды:\n'
        '/shutdown - Выключить ПК\n'
        '/reboot - Перезагрузка\n'
        '/sleep - Спящий режим'
    )
    await update.message.reply_text(response)

def execute_command(command: str) -> str:
    if sys.platform == 'win32':
        commands = {
            'shutdown': 'shutdown /s /t 0',
            'reboot': 'shutdown /r /t 0',
            'sleep': 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0'
        }
    else:
        commands = {
            'shutdown': 'sudo shutdown -h now',
            'reboot': 'sudo shutdown -r now',
            'sleep': 'systemctl suspend'
        }
    os.system(commands[command])
    return f'Команда {command} выполнена'

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_command(update, 'shutdown')

async def reboot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_command(update, 'reboot')

async def sleep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_command(update, 'sleep')

async def handle_command(update: Update, command: str):
    if update.effective_user.id not in AUTHORIZED_USERS:
        await update.message.reply_text('⛔ Доступ запрещен')
        return
    
    try:
        result = execute_command(command)
        await update.message.reply_text(f'✅ {result}')
    except Exception as e:
        await update.message.reply_text(f'❌ Ошибка: {str(e)}')

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("shutdown", shutdown))
    application.add_handler(CommandHandler("reboot", reboot))
    application.add_handler(CommandHandler("sleep", sleep))

    application.run_polling()

if __name__ == "__main__":
    main()