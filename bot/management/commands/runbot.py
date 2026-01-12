from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    
    # --- TU URL REAL DE VERCEL ---
    WEB_APP_URL = "https://cotizados.vercel.app/" 

    # 1. Definimos que el botón abrirá una Web App
    web_app_info = WebAppInfo(url=WEB_APP_URL)

    # 2. Creamos el botón
    # Texto: "🚀 Abrir Cotizados"
    keyboard = [
        [InlineKeyboardButton("🚀 Abrir Cotizados", web_app=web_app_info)]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 3. Enviamos el mensaje con el botón
    await update.message.reply_text(
        f"¡Hola {user_first_name}! 👋\n\nToca el botón de abajo para ver las tasas y usar la calculadora:",
        reply_markup=reply_markup
    )

class Command(BaseCommand):
    help = 'Ejecuta el bot de Telegram con Web App'

    def handle(self, *args, **options):
        # Leemos el token de tu archivo .env (vía settings.py)
        token = settings.TELEGRAM_TOKEN
        
        if not token:
            self.stdout.write(self.style.ERROR("Error: No hay token en el .env"))
            return

        self.stdout.write(self.style.SUCCESS("Bot de Cotizados iniciado... 🚀"))
        
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.run_polling()