import logging
import random
import time
from environs import Env


import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import VkApiError

import telegram

from dialog_flow_api import detect_intent_text


SLEEP_TIME = 10

logger = logging.getLogger(__file__)


class TlgmLogsHandler(logging.Handler):

    def __init__(self, token, chat_id, formatter):
        super().__init__()
        self.bot = telegram.Bot(token=token)
        self.admin_chat_id = chat_id
        self.setFormatter(formatter)

    def emit(self, record):
        self.bot.send_message(
                         chat_id=self.admin_chat_id,
                         text=self.formatter.format(record)
        )


def echo(event, vk_api, project_id):
    reply = detect_intent_text(
        event.user_id,
        event.text,
        'ru',
        project_id=project_id
    )
    if not reply.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )

def main():
    env = Env()
    env.read_env()
    vk_api_token = env('VK_API_TOKEN')
    project_id = env('PROJECT_ID')
    admin_tlgm_chat_id = env('ADMIN_TLGM_CHAT_ID')
    tlgm_token_bot = env('TLGM_TOKEN_BOT')

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        '%H:%M:%S',
    )
    logger.setLevel(logging.INFO)
    logger.addHandler(TlgmLogsHandler(
                                      tlgm_token_bot,
                                      admin_tlgm_chat_id,
                                      formatter
                                     )
                      )

    vk_session = vk.VkApi(token=vk_api_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info('VK_bot started!')
    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api, project_id)
        except VkApiError as exception:
            logger.exception(exception)
            time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
