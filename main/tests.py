import unittest
from django.test import RequestFactory
from config.translate import TranslationMiddleware


class TranslationMiddlewareTestCase(unittest.TestCase):

    def test_translate_text(self):
        middleware = TranslationMiddleware(None)
        text = "Hello world"
        translated_text = middleware.translate_text(text, "fr")
        self.assertEqual(translated_text, "Hello world")

    def test_get_target_language(self):
        middleware = TranslationMiddleware(None)
        factory = RequestFactory()
        request = factory.get('/test/')
        request.META['REMOTE_ADDR'] = '192.168.1.1'
        target_language = middleware.get_target_language(request)
        self.assertEqual(target_language, "fr")

    def test_translate_response(self):
        middleware = TranslationMiddleware(None)
        response_data = {
            "title": "Bonjour le monde",
            "content": {
                "subtitle": "Comment ça va?",
                "body": "C'est un beau jour"
            }
        }
        target_language = "en"
        middleware.translate_response(response_data, target_language)
        self.assertEqual(response_data['title'], "Hello world")
        self.assertEqual(response_data['content']['subtitle'], "How are you?")
        self.assertEqual(response_data['content']['body'], "It's a beautiful day")

if __name__ == '__main__':
    unittest.main()
