from google.cloud import dialogflow


def detect_intent_text(session_id, text, language_code, project_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    return session_client.detect_intent(
        request={"session": session, "query_input": query_input}
        )


def list_intents_names(project_id):

    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    return [intent.display_name for intent in
            intents_client.list_intents(request={"parent": parent})]


def create_intent(
                  project_id,
                  display_name,
                  training_phrases_parts,
                  message_texts
                  ):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
                               display_name=display_name,
                               training_phrases=training_phrases,
                               messages=[message]
    )

    return intents_client.create_intent(
                                request={"parent": parent, "intent": intent}
                                )
