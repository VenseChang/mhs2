import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from dotenv import load_dotenv
load_dotenv()

# ----------------
from services.callback import callback, monster
from services.sr_nest import monsters, render_sr_info
from services.monster_info import render_info, monster_names

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi!\n輸入魔物的關鍵字，就可以查到相關資料~\n\n感謝廣大巴友們共同彙整的資訊\nhttps://forum.gamer.com.tw/C.php?bsn=5786&snA=162396")

def help(update, context):
    """Send a message when the command /help is issued."""
    message = "/eggs： 蛋紋樣式一欄表"
    update.message.reply_text(message, parse_mode = ParseMode.MARKDOWN)

def echo(update, context):
    """Echo the user message."""
    reply_markup = None
    text = update.message.text
    total = len(monster_names(text))
    if total == 0:
        message = '查無符合名稱的魔物！'
    elif total == 1:
        message = render_info(text, 'fuzzy')
    elif total <= 10:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('模糊搜尋', callback_data = 'render {} fuzzy 0'.format(text))],
            [InlineKeyboardButton('精準搜尋', callback_data = 'query {} precise 0'.format(text))]
        ])
        message = '符合結果共 {}筆，請選擇搜尋方式：'.format(total)
    else:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('精準搜尋', callback_data = 'query {} precise 0'.format(text))]])
        message = '符合筆數過多（{}筆），只支援精準搜索：'.format(total)
    update.message.reply_text(message, reply_markup = reply_markup)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def eggs(update, context):
    url = 'https://github.com/VenseChang/mhs2/blob/master/data/images/eggs.jpeg?raw=true'
    caption = '資料來源：[【攻略】分享蛋紋樣式一欄表](https://forum.gamer.com.tw/C.php?bsn=5786&snA=162432&tnum=1&subbsn=11)\n由版友 sailpg4（小傲雪）整理'
    update.message.reply_photo(url,
                               caption = caption,
                               parse_mode = ParseMode.MARKDOWN_V2)

def sr(update, context):
    command = '/sr'
    text = update.message.text.strip()
    name = None if text == command else text.split()[1]

    if name is None:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('依地形', callback_data = 'nest {} nest 0'.format(name))],
            [InlineKeyboardButton('依魔物', callback_data = 'nest {} monsters 0'.format(name))]
        ])
        update.message.reply_text('ＳＲ巢穴全魔物資料，請選擇搜尋方式：', reply_markup = reply_markup)
    else:
        monster(update, name, 'monsters')

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("eggs", eggs))
    dp.add_handler(CommandHandler("sr", sr))

    updater.dispatcher.add_handler(CallbackQueryHandler(callback))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(os.getenv('WEBHOOK_URL') + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
