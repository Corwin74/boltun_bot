import json
from environs import Env
from dialog_flow_api import create_intent

INTENT = 'Устройство на работу'
env = Env()
env.read_env()

project_id = env('PROJECT_ID')

with open("questions.json", "r") as _:
    file_contents = _.read()
print('\tВ файле содержатся следующие события:\n')
for count, intent in enumerate(json.loads(file_contents).keys(), 1):
    print(f'\t{count}. {intent}')
'''
intent_q_and_a = json.loads(file_contents)[INTENT]
create_intent(
              project_id, INTENT,
              intent_q_and_a['questions'],
              [intent_q_and_a['answer']]
)
'''

