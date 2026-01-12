import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Tu función de siempre, la misma que tenías en runbot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    WEB_APP_URL = "https://cotizados.vercel.app/"
    web_app_info = WebAppInfo(url=WEB_APP_URL)
    keyboard = [[InlineKeyboardButton("🚀 Abrir Cotizados", web_app=web_app_info)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"¡Hola {user_first_name}! 👇 Abre la app aquí:",
        reply_markup=reply_markup
    )

# ESTA ES LA MAGIA: Una vista que Telegram visitará
@csrf_exempt
async def telegram_webhook(request):
    if request.method == 'POST':
        # 1. Obtenemos el token de forma segura
        token = os.getenv('TELEGRAM_TOKEN')
        
        # 2. Construimos la app (igual que antes)
        app = ApplicationBuilder().token(token).build()
        
        # 3. Agregamos el manejador
        app.add_handler(CommandHandler("start", start))
        
        # 4. Procesamos los datos que nos envió Telegram
        try:
            body = json.loads(request.body)
            update = Update.de_json(body, app.bot)
            
            # Inicializamos la app y procesamos el update
            await app.initialize()
            await app.process_update(update)
            await app.shutdown()
            
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'status': 'invalid request'}, status=400)