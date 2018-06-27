#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY = range(2)

reply_keyboard = [['ETH Wallet', 'Refferal Link'],
                  ['My Balance', 'Refferal Balance'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def start(bot, update):
    keyboard = [[InlineKeyboardButton("Join Our Group", url = 'https://t.me/anbspecial')] ,
              [InlineKeyboardButton("Press Yes, If you have joined our group", callback_data='1')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('''Welcome to ANB referral program!
	
	Please join our annoucment channel and get 100 ANBP to proceed.''', reply_markup=reply_markup)

def button(bot, update):
    query = update.callback_query

    bot.send_message(text='''Thanks for joining our group.
	Press /Next to continue.''',chat_id=query.message.chat_id, message_id=query.message.message_id)
		
def next(bot, update):
    update.message.reply_text("Please provide your information by reply keyboard",reply_markup=markup)
    return CHOOSING

def ETH_Wallet(bot, update):
	update.message.reply_text('Please provide your ETH address')	
	return TYPING_REPLY

def Refferal_Link(bot, update):
	update.message.reply_text('your referral link is https://t.me/First1691bot?start=4125689')
	return CHOOSING

def My_Balance(bot, update):
	update.message.reply_text('your balance is')
	return CHOOSING
 
def Refferal_Balance(bot, update):
	update.message.reply_text('your ref balance is') 
	return CHOOSING

def received_information(bot, update, user_data):
    text = update.message.text # This is used to save user data
    update.message.reply_text("Your ETH address saved: ""{}".format(text.lower()))
    return CHOOSING

def done(bot, update, user_data):
    update.message.reply_text("Thanks for participating")
    return CHOOSING

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("605110748:AAFxkzGgG-qPVfHWJwqbi-6SA4RYvg0nUVQ")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
	
	
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('next', next)],

        states={
            CHOOSING: [
						RegexHandler('^ETH Wallet$',ETH_Wallet),
						RegexHandler('^Refferal Link$',Refferal_Link),
						RegexHandler('^My Balance$',My_Balance),
						RegexHandler('^Refferal Balance$',Refferal_Balance),
						],

            TYPING_REPLY: [
						MessageHandler(Filters.text,received_information,pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()