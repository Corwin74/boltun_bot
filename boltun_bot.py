import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from dialog_flow_api import detect_intent_texts

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class DialogFlowBot():
    def __init__(self, project_id):
        self.project_id = project_id

    def echo(self, update, context):
        reply = detect_intent_texts(update.message.chat.id, [update.message.text], 'ru', self.project_id)
        if replyresponse.query_result.intent.display_name
        update.message.reply_text(reply)

    def start(self, update, context):
        """Send a message when the command /start is issued."""
        user = update.effective_user
        update.message.reply_markdown_v2(
            fr'Здравствуйте {user.mention_markdown_v2()}\!',
            reply_markup=ForceReply(selective=True),
        )

    def help_command(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

def main():

    env = Env()
    env.read_env()

    tlgm_token_bot = env('TLGM_TOKEN_BOT')
    project_id = env('PROJECT_ID')

    df_bot = DialogFlowBot(project_id)

    updater = Updater(tlgm_token_bot)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", df_bot.start))
    dispatcher.add_handler(CommandHandler("help", df_bot.help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, df_bot.echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
