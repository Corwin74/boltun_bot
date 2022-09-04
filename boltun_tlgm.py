import logging
import traceback
import html
import json

from telegram import ForceReply, ParseMode, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from environs import Env
from dialog_flow_api import detect_intent_text

REPLY_ENABLE_INTENTS = ['Приветствие', 'Default Fallback Intent']

logger = logging.getLogger(__file__)


class DialogFlowBot():
    def __init__(self, project_id, enabled_intents, admin_chat_id):
        self.project_id = project_id
        self.enabled_intents = enabled_intents
        self.admin_chat_id = admin_chat_id

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
        user = update.effective_user
        update.message.reply_markdown_v2(
            fr'Здравствуйте {user.mention_markdown_v2()}\!',
            reply_markup=ForceReply(selective=True),
        )

    def help_command(self, update, context):
        update.message.reply_text('Help!')

    def error_handler(self, update, context):
        logger.error(
                     msg="Исключение при обработке сообщения:",
                     exc_info=context.error
        )

        tb_list = traceback.format_exception(
                                             None,
                                             context.error,
                                             context.error.__traceback__
        )
        tb_string = ''.join(tb_list)

        update_str = update.to_dict()\
            if isinstance(update, Update) else str(update)
        message = (
         f'Возникло исключение при обработке сообщения.\n'
         f'<pre>update = '
         f'{html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
         '</pre>\n\n'
         f'<pre>context.chat_data = '
         f'{html.escape(str(context.chat_data))}</pre>\n\n'
         f'<pre>context.user_data ='
         f'{html.escape(str(context.user_data))}</pre>\n\n'
         f'<pre>{html.escape(tb_string)}</pre>'
        )

        context.bot.send_message(
                                 chat_id=self.admin_chat_id,
                                 text=message,
                                 parse_mode=ParseMode.HTML
        )

    def bad_command(self, _, context):
        """Вызывает ошибку, чтобы вызвать обработчик ошибок."""
        context.bot.wrong_method_name()


def main():
    logging.basicConfig(
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                level=logging.INFO
    )

    env = Env()
    env.read_env()
    tlgm_token_bot = env('TLGM_TOKEN_BOT')
    project_id = env('PROJECT_ID')
    admin_tlgm_chat_id = env('ADMIN_TLGM_CHAT_ID')

    df_bot = DialogFlowBot(
                           project_id,
                           REPLY_ENABLE_INTENTS,
                           admin_tlgm_chat_id
    )

    updater = Updater(tlgm_token_bot)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", df_bot.start))
    dispatcher.add_handler(CommandHandler("help", df_bot.help_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, df_bot.echo))
    dispatcher.add_handler(CommandHandler('bad_command', df_bot.bad_command))

    dispatcher.add_error_handler(df_bot.error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
