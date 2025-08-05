import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

llm = OpenRouterClient(api_key=OPENROUTER_API_KEY)
BACKGROUND = 0

site_context = (
    "В AI Talent Hub университета ИТМО доступны две магистратурные программы:\n"
    "1. 'AI' — техническое направление (машинное обучение, нейросети, алгоритмы).\n"
    "2. 'AI Product' — продуктовый трек (продуктовый менеджмент, аналитика, запуск AI-продуктов).\n"
    "Обе программы включают выборные дисциплины, проектную работу и работу с наставником."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ Команда /start получена")
    await update.message.reply_text(
        "Привет! Я ITMO AI Master's Helper. Помогу тебе выбрать между двумя магистратурами ИТМО:\n"
        "— *AI* (техническая)\n"
        "— *AI Product* (продуктовая)\n\n"
        "Задай вопрос или введи /recommend, чтобы получить персональный совет.",
        parse_mode="Markdown"
    )


async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Расскажи немного о себе — образование, опыт, интересы:")
    return BACKGROUND

async def handle_background(update: Update, context: ContextTypes.DEFAULT_TYPE):
    background = update.message.text
    question = (
        f"Вот бэкграунд абитуриента: {background}\n"
        f"Посоветуй, какое направление подойдёт лучше — AI или AI Product, и почему. "
        f"Если можно, предложи 3–4 подходящих курса."
    )
    await update.message.reply_text("Секунду, думаю…")
    response = llm.generate_answer(question, site_context)
    await update.message.reply_text(response)
    return ConversationHandler.END

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.reply_text("Думаю над ответом…")
    response = llm.generate_answer(question, site_context)
    await update.message.reply_text(response)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Окей, отменено.")
    return ConversationHandler.END

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("recommend", recommend))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("recommend", recommend)],
        states={BACKGROUND: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_background)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    await app.initialize()
    await app.start()
