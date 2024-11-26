import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# Инициализируйте приложение Django ASGI заранее, чтобы AppRegistry
# был заполнен до импорта кода, который может импортировать модели ORM.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Пока только HTTP. (Позже мы можем добавить другие протоколы.)
})
