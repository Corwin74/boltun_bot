import random
from environs import Env

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow_api import detect_intent_text

REPLY_ENABLE_INTENTS = ['Приветствие', 'Default Fallback Intent']


def echo(event, vk_api, project_id, enabled_intents):
    reply = detect_intent_text(
        event.user_id,
        event.text,
        'ru',
        project_id=project_id
    )
    if reply.query_result.intent.display_name in enabled_intents:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply.query_result.fulfillment_text,
            random_id=random.randint(1,1000)
        )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_api_token = env('VK_API_TOKEN')
    project_id = env('PROJECT_ID')
    vk_session = vk.VkApi(token=vk_api_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, project_id, REPLY_ENABLE_INTENTS)
