from telegram.ext import Updater
from telegram.error import(TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
import requests
import string
from bs4 import BeautifulSoup
from commands import Commands
from tokens import bottoken

t = bottoken
updater = Updater(token=t.token("live"))
dispatcher = updater.dispatcher
commands = Commands

from telegram.ext import CommandHandler
start_handler = CommandHandler('aboutme', commands.aboutme)
dispatcher.add_handler(start_handler)
cmd_handler = CommandHandler('cmd', commands.commands)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('supported', commands.supported)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('st', commands.straitstimes)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('today', commands.todayonline)
dispatcher.add_handler(cmd_handler)
cmd_handler = CommandHandler('cna', commands.cna)
dispatcher.add_handler(cmd_handler)

updater.start_polling()
