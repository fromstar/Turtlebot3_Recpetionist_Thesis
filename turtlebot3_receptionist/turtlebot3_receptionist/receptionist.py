from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from turtlebot3_receptionist.navigation import navigation
from turtlebot3_receptionist.tlg_bot import *

CHAT_ID = "225206858"
TOKEN = "6593779673:AAEhgaWl0lbV5oEYm7H3IduHtv5z2Ta7C_k"

def thread_populate():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("list", list_command))
    dp.add_handler(CommandHandler("queue", queue_command))
    dp.add_handler(CommandHandler("delete", delete_command))
    dp.add_handler(CommandHandler("recap", user_recap_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.voice,limit_access))
    dp.add_handler(MessageHandler(Filters.text,limit_access))  
    updater.start_polling()
    updater.idle()

def thread_unpopulate():
    while True:
        if len(pending_tasks)>0:
            navigation()
            sleep(5)

def main():
    executor = ThreadPoolExecutor(max_workers=2)
    a = executor.submit(thread_populate)
    b = executor.submit(thread_unpopulate)
if __name__ == "__main__":
    main()
