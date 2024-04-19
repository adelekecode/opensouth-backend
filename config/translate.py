import boto3
import os



session = boto3.Session(
    "translate", region_name=os.getenv("region"),
    aws_access_key_id=os.getenv("mail_access_id"),
    aws_secret_access_key=os.getenv("mail_secret_key")
)








class TranslationMiddleware:
    
    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        response = self.get_response(request)
        if response.status_code == 200 and response.data:
            self.translate_response(response)

        return response

    def translate_response(self, response):
        if isinstance(response.data, dict):

            self.translate_dict(response.data)

    def translate_dict(self, data):
        for key, value in data.items():

            if isinstance(value, str):
                translated_text = self.translate_text(value)
                data[key] = translated_text

            elif isinstance(value, dict):
                self.translate_dict(value)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.translate_dict(item)

    def translate_text(self, text, target_language="en"):
        
  
        response = session.translate_text(
            Text=text,
            SourceLanguageCode='fr',
            TargetLanguageCode=target_language
        )

        translated_text = response['TranslatedText']

        return translated_text
