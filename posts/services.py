import json

from google.cloud import language_v1
from google.oauth2 import service_account
from django.conf import settings


def check_text_inappropriateness(text) -> bool:
    key_data = json.loads(settings.GOOGLE_APPLICATION_CREDENTIALS_JSON)
    credentials = service_account.Credentials.from_service_account_info(key_data)
    client = language_v1.LanguageServiceClient(credentials=credentials)

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    print(response)
    for sentence in response.sentences:
        if sentence.sentiment.score < -0.3:
            return True

    return False
