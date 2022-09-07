import logging
from environs import Env

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dialog_flow_api import detect_intent_text
from tlgm_logger import TlgmLogsHandler


logger = logging.getLogger(__file__)


def send_reply(update, context):
    reply = detect_intent_text(
                                update.message.chat.id,
                                update.message.text,
                                'ru',
                                context.bot_data['df_project_id']
    )
    update.message.reply_text(reply.query_result.fulfillment_text)


def start(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте {user.mention_markdown_v2()}\!',
    )


def error_handler(update, context):
    logger.exception('Exception', exc_info=context.error)


def main():
    logging.basicConfig(
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.INFO
    )

    env = Env()
    env.read_env()
    tlgm_token_bot = env('TLGM_TOKEN_BOT')

    updater = Updater(tlgm_token_bot)
    dispatcher = updater.dispatcher

    dispatcher.bot_data['admin_tlgm_chat_id'] = env('ADMIN_TLGM_CHAT_ID')
    dispatcher.bot_data['df_project_id'] = env('DF_PROJECT_ID')

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, send_reply))

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        '%H:%M:%S',
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(TlgmLogsHandler(
                                      updater.bot,
                                      env('ADMIN_TLGM_CHAT_ID'),
                                      formatter
                                     )
                      )
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
