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
    intents_number = len(intents_names)
    print('В файле содержатся следующие события:\n')
    for count, intent in enumerate(intents.keys(), 1):
        print(f'{count}. {intent}')
    while not (choice := input(f'Какое событие добавить? (1-{intents_number})'))\
                            in [str(x) for x in range(1, intents_number+1)]:
        pass

    intent_name = intents_names[int(choice)-1]
    intent = intents[intent_name]
    if intent_name in list_intents_names(project_id):
        print(f'Событие "{intent_name}" уже существует!')
        return
    create_intent(
                project_id,
                intent_name,
                intent['questions'],
                [intent['answer']]
    )


if __name__ == '__main__':
    main()
