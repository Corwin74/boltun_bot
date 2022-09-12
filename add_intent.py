import json
from environs import Env
from dialog_flow_api import create_intent, list_intents_names


def main():
    env = Env()
    env.read_env()

    project_id = env('PROJECT_ID')

    with open("questions.json", "r", encoding='utf-8') as _:
        intents = json.loads(_.read())
    intents_names = list(intents.keys())
    exist_intents_names = list_intents_names(project_id)
    for intent_name in intents_names:
        if intent_name in exist_intents_names:
            print(f'Событие "{intent_name}" уже существует!')
            continue
        intent = intents[intent_name]
        create_intent(
                    project_id,
                    intent_name,
                    intent['questions'],
                    [intent['answer']]
        )


if __name__ == '__main__':
    main()
