import json
from environs import Env
from dialog_flow_api import create_intent

env = Env()
env.read_env()

project_id = env('PROJECT_ID')

with open("questions.json", "r", encoding='utf-8') as _:
    intents = json.loads(_.read())
intents_names = list(intents.keys())
intents_number = len(intents_names)
print('\tВ файле содержатся следующие события:\n')
for count, intent in enumerate(intents.keys(), 1):
    print(f'\t{count}. {intent}')
while not (choice := input(f'Какое событие добавить? (1-{intents_number})'))\
                in [str(x) for x in range(1, intents_number+1)]:
    pass
intent = intents[intents_names[int(choice)-1]]
create_intent(
              project_id, intents_names[int(choice)-1],
              intent['questions'],
              [intent['answer']]
)
