from django.contrib import admin
from django.urls import path
from bot.views import telegram_webhook # Importa tu vista

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta será la dirección donde Telegram tocará la puerta
    path('webhook/', telegram_webhook, name='telegram_webhook'),
]
