import boto3
import os
from public.models import ClientIP




class TranslationMiddleware:

    def session(self):
        session = boto3.Session(
            "translate", region_name=os.getenv("region"),
            aws_access_key_id=os.getenv("mail_access_id"),
            aws_secret_access_key=os.getenv("mail_secret_key")
        )

        return session

    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 200 and response.data:
            target_language = self.get_target_language(request)
            self.translate_response(response, target_language)

        return response

    def translate_response(self, response, target_language):
        if isinstance(response.data, dict):
            self.translate_dict(response.data, target_language)

    def translate_dict(self, data, target_language):
        for key, value in data.items():
            if isinstance(value, str):
                translated_text = self.translate_text(value, target_language)
                data[key] = translated_text
            elif isinstance(value, dict):
                self.translate_dict(value, target_language)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.translate_dict(item, target_language)


    def get_target_language(self, request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            client_ip = ClientIP.objects.get(ip_address=ip)
        except ClientIP.DoesNotExist:
            client_ip = ClientIP(ip_address=ip)
            client_ip.save()

        return client_ip.lang

        
        

    def translate_text(self, text, target_language="en"):
        
  
        response = self.session.translate_text(
            Text=text,
            SourceLanguageCode='fr',
            TargetLanguageCode=target_language
        )
        if response.status_code == 200:

            translated_text = response['TranslatedText']

            return translated_text
        else:
            return text
