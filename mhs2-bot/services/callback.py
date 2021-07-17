from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from services.monster_info import render_info, monster_names

def render(bot, text, mode):
    bot.callback_query.edit_message_text(render_info(text, mode))

def query(bot, text, mode):
    names = map(lambda name: name.split()[-1], monster_names(text))
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(name, callback_data = 'render {} {}'.format(name, mode))] for name in names
    ])
    bot.callback_query.edit_message_text('請選擇魔物：', reply_markup = reply_markup)

def switch(bot, method, text, mode):
    return {
        'render': render,
        'query': query
    }[method](bot, text, mode)

def callback(bot, update):
    method, text, mode = [str(x) for x in bot.callback_query.data.split()]
    switch(bot, method, text, mode)
