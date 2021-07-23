from math import ceil

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from services.monster_info import render_info, monster_names
from services.sr_nest import nests, monsters, render_sr_info
from services.global_variables import RECORD_PER_PAGE

def paginations(action, text, mode, page, total):
    buttons = []
    page = int(page)
    total_page = ceil(total / RECORD_PER_PAGE) - 1
    if page != 0:
        buttons.append(InlineKeyboardButton('⬅️ 上一頁', callback_data = '{} {} {} {}'.format(action, text, mode, page - 1)))
    if page != total_page:
        buttons.append(InlineKeyboardButton('下一頁 ➡️', callback_data = '{} {} {} {}'.format(action, text, mode, page + 1)))
    return buttons

def button_render(action, result, text, mode, page, names):
    start, end = int(page) * RECORD_PER_PAGE, (int(page) + 1) * RECORD_PER_PAGE
    markups = [[InlineKeyboardButton(name, callback_data = '{} {} {} 0'.format(result, name, mode))] for name in names[start:end]]
    markups.append(paginations(action, text, mode, page, len(names)))
    return InlineKeyboardMarkup(markups)

def render(bot, text, mode, page = None):
    bot.callback_query.edit_message_text(render_info(text, mode))

def query(bot, text, mode, page):
    datas = list(map(lambda name: name.split()[-1], monster_names(text)))
    bot.callback_query.edit_message_text('請選擇魔物：', reply_markup = button_render('query', 'render', text, mode, page, datas))

def nest(bot, text, mode, page):
    if mode == 'nest':
        message = '請選擇地區：'
        datas   = nests()
    else:
        message = '請選擇魔物：'
        datas   = monsters()
    bot.callback_query.edit_message_text(message, reply_markup = button_render('nest', 'nest_data', text, mode, page, datas))

def nest_data(bot, text, mode, page = None):
    reply_markup = None
    if mode == 'monsters':
        buttons = [[InlineKeyboardButton('魔物資訊', callback_data = 'toggle_nest_info {} monsters 0'.format(text))]]
        reply_markup = InlineKeyboardMarkup(buttons)
    output = render_sr_info(text, mode)
    bot.callback_query.edit_message_text(output, reply_markup = reply_markup)

def monster(bot, text, mode, page = None):
    datas = list(filter(lambda name: text in name ,monsters()))
    if page is None:
        bot.message.reply_text('請選擇魔物：', reply_markup = button_render('monster', 'nest_data', text, mode, 0, datas))
    else:
        bot.callback_query.edit_message_text('請選擇魔物：', reply_markup = button_render('monster', 'nest_data', text, mode, page, datas))

def toggle_nest_info(bot, text, mode, page = None):
    if mode == 'monsters':
        mode = 'nest_info'
        message = render_info(text, 'precise')
        buttons = [[InlineKeyboardButton('巢穴資訊', callback_data = 'toggle_nest_info {} {} 0'.format(text, mode))]]
    else:
        mode = 'monsters'
        message = render_sr_info(text, 'monsters')
        buttons = [[InlineKeyboardButton('魔物資訊', callback_data = 'toggle_nest_info {} {} 0'.format(text, mode))]]
    bot.callback_query.edit_message_text(message, reply_markup = InlineKeyboardMarkup(buttons))

def switch(bot, method, text, mode, page):
    return {
        'render': render,
        'query': query,
        'nest': nest,
        'nest_data': nest_data,
        'monster': monster,
        'toggle_nest_info': toggle_nest_info
    }[method](bot, text, mode, page)

def callback(bot, update):
    method, text, mode, page = [str(x) for x in bot.callback_query.data.split()]
    switch(bot, method, text, mode, page)
