import json
from environs import Env
from dialog_flow_api import create_intent

INTENT = 'Устройство на работу'
env = Env()
env.read_env()

project_id = env('PROJECT_ID')

with open("questions.json", "r") as _:
    file_contents = _.read()
intent_q_and_a = json.loads(file_contents)[INTENT]
create_intent(
              project_id, INTENT,
              intent_q_and_a['questions'],
              [intent_q_and_a['answer']]
)
