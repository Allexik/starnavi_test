import json

from google.cloud import language_v2
from google.oauth2 import service_account

import vertexai
from vertexai.generative_models import GenerativeModel

from django.conf import settings

_key_data = json.loads(settings.GOOGLE_APPLICATION_CREDENTIALS_JSON)
_credentials = service_account.Credentials.from_service_account_info(_key_data)


def check_text_inappropriateness(text) -> bool:
    client = language_v2.LanguageServiceClient(credentials=_credentials)

    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)

    for sentence in response.sentences:
        if sentence.sentiment.score < -0.3:
            return True

    return False


def generate_comment_answer(post_title, post_content, comment_content) -> str:
    vertexai.init(
        project=settings.GCP_PROJECT_ID,
        location=settings.GCP_MODELS_LOCATION,
        credentials=_credentials
    )
    model = GenerativeModel("gemini-1.5-flash-001")

    response = model.generate_content(f"""
    [Post title]: 
    
    {post_title}
    
    [Post content]: 
    
    {post_content}
    
    [Comment to the post]: 
    
    {comment_content}
    
    [Prompt]: 
    
    Provide a response to the comment above based on the post title and content.
    If there are no info to answer it, provide a general response.
    """)

    answer = response.candidates[0].content.text

    return answer
