from django.utils.deprecation import MiddlewareMixin

class LogPostRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST':
            # Логи для отладки
            print("POST request body:", request.body)
            print("POST request data:", request.POST)