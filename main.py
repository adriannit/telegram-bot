# pyright: reportMissingImports=false

from array import array
import sys
from hass import Hass
from qbittorrent import Qbitorrent
import configparser
import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.bot import Bot, BotCommand

# logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

### Parse the config file ###

# Let's see if we can open the config file.
config = configparser.ConfigParser()
try:
    with open('telegram-bot.conf') as f:
        config.read_file(f)
except IOError as err:
    log.error("Something wrong occured with the config file: %s",err)
    sys.exit(1)

# Check if telegram is configured
for key in ['token', 'base_url']:
    if not config.has_option('telegram', key):
        log.error("Missing Telegram " + key + " in config file")
        sys.exit(2)

# Get enabled plugins if not sent then it's disabled
HASS_ENABLED = config.getboolean('homeassistant','enabled', fallback=False)
QBITORRENT_ENABLED = config.getboolean('qbitorrent','enabled', fallback=False)

# Check if plugins have at least the config values set
if HASS_ENABLED:
    for key in ['token', 'url']:
        if not config.has_option('homeassistant', key):
            log.error("Missing HomeAssistant " + key + " in config file")
            sys.exit(2)
if QBITORRENT_ENABLED:
    for key in ['host', 'username', 'password']:
        if not config.has_option('qbitorrent', key):
            log.error("Missing qBitorrent " + key + " in config file")
            sys.exit(2)

# Get all the config values
HASS = {}
TELEGRAM = {}
QBITORRENT = {}

HASS['URL']     = config['homeassistant']['url']
HASS['TOKEN']   = config['homeassistant']['token']

TELEGRAM['TOKEN'] = config['telegram']['token']

QBITORRENT['USERNAME']  = config['qbitorrent']['username']
QBITORRENT['PASSWORD']  = config['qbitorrent']['password']
QBITORRENT['HOST']      = config['qbitorrent']['host']

# HASS object
hass = Hass(HASS['URL'], HASS['TOKEN'])

#qbitorrent object
qbitorrent = Qbitorrent(QBITORRENT['HOST'], QBITORRENT['USERNAME'], QBITORRENT['PASSWORD'])

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def temp_dormitor(update: Update, context: CallbackContext) -> None:
    message = hass.get_state('sensor.tasmotatemphum_dht11_temperature')
    update.message.reply_text('Temperatura dormitor: ' + message)

def torrent_stats(update: Update, context: CallbackContext) -> None:
    message = qbitorrent.statistics()
    update.message.reply_text(message)

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TELEGRAM['TOKEN'])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("temp_dormitor", temp_dormitor))
    dispatcher.add_handler(CommandHandler("torrent_stats", torrent_stats))

    command = [BotCommand("temp_dormitor","temperatura dormitor"),BotCommand("torrent_stats", "statistici qBitorrent")]
    bot = Bot(TELEGRAM['TOKEN'])
    bot.set_my_commands(command)

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()