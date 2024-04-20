import boto3
import os
from public.models import ClientIP
import json

class TranslationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 200:
            target_language = self.get_target_language(request)
            self.translate_response(response, target_language)
        return response

    def translate_response(self, response, target_language):
        self.translate_dict(response, target_language)

    def translate_dict(self, data, target_language):
        if isinstance(data, dict):
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
            client_ip = ClientIP.objects.filter(ip_address=ip).first()

            if client_ip:
                return client_ip.lang
            else:
                return "fr"
            
        except ClientIP.DoesNotExist:
            return "fr"

    # def translate_text(self, text, target_language):
    #     session = boto3.Session(
    #         "translate", 
    #         region_name=os.getenv("region")
    #     )
        
    #     try:
    #         response = session.translate_text(
    #             Text=text,
    #             SourceLanguageCode='en',
    #             TargetLanguageCode=target_language
    #         )
    #         return response['TranslatedText']
    #     except Exception:
    #         return text
        
    def translate_text(self, text, target_language):

        session = boto3.Session(
        region_name=os.getenv("region"),
        aws_access_key_id=os.getenv("mail_access_id"),
        aws_secret_access_key=os.getenv("mail_secret_key")

        )
    
        translate_client = session.client('translate')
    
        try:
            response = translate_client.translate_text(
                Text=text,
                SourceLanguageCode='en',
                TargetLanguageCode=target_language
            )
            translated_text = response['TranslatedText']
            
            return translated_text
        except Exception as e:
            print(f"Translation error: {e}")
            return text
