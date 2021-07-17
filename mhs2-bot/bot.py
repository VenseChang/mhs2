import logging
from urllib.request import urlopen
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import json

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = ''

url = 'https://raw.githubusercontent.com/VenseChang/mhs2/master/data/data.json'
datas = json.loads(urlopen(url).read())

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi!\n輸入魔物的關鍵字，就可以查到相關資料~\n\n感謝廣大巴友們共同彙整的資訊\nhttps://forum.gamer.com.tw/C.php?bsn=5786&snA=162396")

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    output = ""
    text = update.message.text
    targets = list(filter(lambda name: text in name , datas.keys()))
    for target in targets:
        data = datas[target]
        output += "No. {}\n".format(data['no'])
        output += "名稱：         {}\n".format(' / '.join(filter(lambda x: x, [data['name']['zh-hant'], data['name']['en']])))
        output += "可孵蛋?       {}\n".format('O' if data['egg'] or False else 'X')
        output += "普通狀態： {}\n".format(data['normal'])
        if 'angry' in data:
            output += "生氣狀態： {}\n".format(data['angry'])
        if 'nest' in data:
            output += "歸巢加成： {}\n".format(data['nest'])
        if 'weakness' in data:
            output += "弱點屬性： {}\n".format(data['weakness'])
        if len(data['parts']) > 0:
            output += "部位破壞：\n"
            if 'head' in data['parts']:
                output += "・ 頭    ： {}\n".format(data['parts']['head'])
            if 'body' in data['parts']:
                output += "・ 身體： {}\n".format(data['parts']['body'])
            if 'wing' in data['parts']:
                output += "・ 翅膀： {}\n".format(data['parts']['wing'])
            if 'abdomen' in data['parts']:
                output += "・ 腹部： {}\n".format(data['parts']['abdomen'])
            if 'feet' in data['parts']:
                output += "・ 腳    ： {}\n".format(data['parts']['feet'])
            if 'tail' in data['parts']:
                output += "・ 尾巴： {}\n".format(data['parts']['tail'])
        if len(targets) > 1:
            output += "\n"
    if len(output) == 0:
        output = "您輸入的關鍵字找不到對應的魔物"
    update.message.reply_text(output)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

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

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://vense-mhs2.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
