import json
from environs import Env
from dialog_flow_api import create_intent, list_intents_names

BULK_MIN_NUMBER = 11


def main():
    env = Env()
    env.read_env()

    project_id = env('PROJECT_ID')

    with open("questions.json", "r", encoding='utf-8') as _:
        intents = json.loads(_.read())
    intents_names = list(intents.keys())
    intents_number = len(intents_names)
    selected_intents_names = intents_names
    if intents_number < BULK_MIN_NUMBER:
        print('В файле содержатся следующие события:\n')
        for count, intent in enumerate(intents.keys(), 1):
            print(f'{count}. {intent}')
        correct_answers = [str(x) for x in range(1, intents_number+1)]
        correct_answers.append('a')
        while not (choice := input(f'Какое событие добавить?'
                                   f'(1-{intents_number})'
                                   ', "a" - Добавить все: ')
                   ) in correct_answers:
            pass
        if not choice == 'a':
            selected_intents_names = [intents_names[int(choice)-1]]
    exist_intents_names = list_intents_names(project_id)
    for intent_name in selected_intents_names:
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
