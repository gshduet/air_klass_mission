from functools        import wraps
from django.http      import JsonResponse

from accounts.models     import User

def login_decorator(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = access_token['user_id']
            request.user = User.objects.get(id=payload['id'])

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

        return func(self, request, *args, **kwargs)

    return wrapper