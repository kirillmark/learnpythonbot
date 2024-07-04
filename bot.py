import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from anketa import anketa_start, anketa_name, anketa_rating, anketa_comment, anketa_skip, anketa_dontknow
from handlers import (greet_user, guess_number, send_cat_picture, user_coordinates,
                        talk_to_me, check_user_photo)
from jobs import send_hello

import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    jq = mybot.job_queue
    jq.run_repeating(send_hello, interval=5)

    dp = mybot.dispatcher

    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)
        ],
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "rating": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)],
            "comment": [
                CommandHandler('skip', anketa_skip),
                MessageHandler(Filters.text, anketa_comment)
            ]
        },
        fallbacks=[
            MessageHandler(
                Filters.text | Filters.video | Filters.photo | Filters.document
                | Filters.location, anketa_dontknow
            )
        ]
    )
    dp.add_handler(anketa)

    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()