from math import ceil

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from services.monster_info import render_info, monster_names
from services.global_variables import RECORD_PER_PAGE

def pages(text, mode, page, total):
    buttons = []
    page = int(page)
    total_page = ceil(total / RECORD_PER_PAGE) - 1
    if page != 0:
        buttons.append(InlineKeyboardButton('⬅️ 上一頁', callback_data = 'query {} {} {}'.format(text, mode, page - 1)))
    if page != total_page:
        buttons.append(InlineKeyboardButton('下一頁 ➡️', callback_data = 'query {} {} {}'.format(text, mode, page + 1)))
    return buttons


def render(bot, text, mode, page = None):
    bot.callback_query.edit_message_text(render_info(text, mode))

def query(bot, text, mode, page):
    start, end = int(page) * RECORD_PER_PAGE, (int(page) + 1) * RECORD_PER_PAGE
    names = list(map(lambda name: name.split()[-1], monster_names(text)))
    markups = [[InlineKeyboardButton(name, callback_data = 'render {} {} 0'.format(name, mode))] for name in names[start:end]]
    markups.append(pages(text, mode, page, len(names)))
    reply_markup = InlineKeyboardMarkup(markups)
    bot.callback_query.edit_message_text('請選擇魔物：', reply_markup = reply_markup)

def switch(bot, method, text, mode, page):
    return {
        'render': render,
        'query': query
    }[method](bot, text, mode, page)

def callback(bot, update):
    method, text, mode, page = [str(x) for x in bot.callback_query.data.split()]
    switch(bot, method, text, mode, page)
