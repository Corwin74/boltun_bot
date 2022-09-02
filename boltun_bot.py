import logging

from telegram import ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from environs import Env
from dialog_flow_api import detect_intent_text

REPLY_ENABLE_INTENTS = ['Приветствие', 'Default Fallback Intent']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class DialogFlowBot():
    def __init__(self, project_id, enabled_intents):
        self.project_id = project_id
        self.enabled_intents = enabled_intents

    def echo(self, update, context):
        reply = detect_intent_text(
                                    update.message.chat.id,
                                    update.message.text,
                                    'ru',
                                    self.project_id
        )
        if reply.query_result.intent.display_name in self.enabled_intents:
            update.message.reply_text(reply.query_result.fulfillment_text)

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

    df_bot = DialogFlowBot(project_id, REPLY_ENABLE_INTENTS)

    updater = Updater(tlgm_token_bot)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", df_bot.start))
    dispatcher.add_handler(CommandHandler("help", df_bot.help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, df_bot.echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
