import os
import logging
from dotenv import load_dotenv
import telebot
from telebot import types
import requests

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


ROLE_NAME = "ОбзорщикВалют"
ROLE_PROMPT = (
    "Ты — ассистент финансового аналитика."
)
DISCLAIMER = (
    "⚠️ Это не является инвестиционной рекомендацией. "
    "Примите самостоятельное решение с учётом ваших рисков."
)


def main_menu_kb() -> types.ReplyKeyboardMarkup:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📌 О боте", "🆘 Помощь")
    kb.row("📈 Что умею", "💬 FAQ")
    return kb


@bot.message_handler(commands=["start"])
def handle_start(message: telebot.types.Message):
    user = message.from_user
    text = (
        f"Привет, <b>{user.first_name or 'коллега'}</b>! 👋\n"
        f"Я — {ROLE_NAME}. Помогу с обзором различных валют и возможно подготовлю шаблоны.\n"
        f"Нажмите кнопки ниже или введите команду /help."
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu_kb())
@bot.message_handler(commands=["help"])
def handle_help(message: telebot.types.Message):
    help_text = (
        "<b>Команды</b>:\n"
        "/start — приветствие\n"
        "/help — список команд\n"
        "/about — о боте и роли\n"
        "/capabilities — что умеет\n"
        "/faq — частые вопросы\n"
        "/ping — проверка доступности\n"
    )
    bot.reply_to(message, help_text)
@bot.message_handler(commands=["about"])
def handle_about(message: telebot.types.Message):
    text = (
        f"<b>{ROLE_NAME}</b> — ваш финансовый ассистент в безграничном ивнестиционном мире. "
        "Могу структурировать вопросы по компаниям/сектору, накинуть шаблон мини-разбора, дать текущую цену BTC "
        "и подготовить списки уточняющих пунктов.\n\n"
        f"{DISCLAIMER}"
    )
    bot.reply_to(message, text)
@bot.message_handler(commands=["capabilities"])
def handle_capabilities(message: telebot.types.Message):
    text = (
        "<b>Что умею </b>:\n"
        "• Отвечать на базовые вопросы вежливо и структурированно\n"
        "• Давать шаблон мини-анализа компании (без живых данных)\n"
        "• Готовить список уточняющих вопросов для исследования\n"
        "• Выводить FAQ\n\n"
        "В следующих практиках добавим API/LLM/графики."
    )
    bot.reply_to(message, text)
@bot.message_handler(commands=["faq"])
def handle_faq(message: telebot.types.Message):
    text = (
        "<b>FAQ</b>\n"
        "• Комиссии/цены? — Бот учебный, не торгует и денег не берёт.\n"
        "• Откуда данные? — На этой паре без внешних API; позднее подключим источники.\n"
        "• Даёшь советы? — Нет. Бот помогает структурировать мысли и запросы.\n\n"
        f"{DISCLAIMER}"
    )
    bot.reply_to(message, text)
@bot.message_handler(commands=["ping"])
def handle_ping(message: telebot.types.Message):
    bot.reply_to(message, "pong ✅")



@bot.message_handler(func=lambda m: m.text in ["📌 О боте", "🆘 Помощь", "📈 Что умею", "💬 FAQ"])
def handle_buttons(message: telebot.types.Message):
    mapping = {
        "📌 О боте": handle_about,
        "🆘 Помощь": handle_help,
        "📈 Что умею": handle_capabilities,
        "💬 FAQ": handle_faq,
    }
    return mapping[message.text](message)



def mini_analysis_template(ticker: str, company: str | None = None) -> str:
    """
    Возвращает каркас мини-анализа без реальных котировок.
    Данные подставим на следующих практиках.
    """
    company_name = company or ticker.upper()
    return (
        f"<b>Мини-анализ: {company_name} ({ticker.upper()})</b>\n"
        "1) Бизнес-модель: [кратко]\n"
        "2) Сегменты и выручка: [сегменты/регион]\n"
        "3) Рост и маржинальность: [динамика, факторы]\n"
        "4) Катализаторы/риски: [вверх/вниз]\n"
        "5) Валюта/долг/дивиденды: [кратко]\n"
        "6) Конкуренты/оценка: [мультипликаторы позже]\n\n"
        f"{DISCLAIMER}"
    )
def clarifying_questions(domain: str = "акции") -> str:
    return (
        f"<b>Уточняющие вопросы ({domain})</b>\n"
        "• Горизонт: трейдинг/инвестирование? Срок?\n"
        "• Риск-профиль: консервативный/умеренный/агрессивный?\n"
        "• Валюта портфеля: RUB/USD/EUR?\n"
        "• Ограничения: ликвидность, комиссии, налоги?\n"
        "• Секторные приоритеты/исключения?\n"
        "• Нужны ли ESG/дивиденды?\n"
    )


def get_fx_rates():
    # url = "https://api.exchangerate.host/latest?base=USD&symbols=RUB,EUR"
    # resp = requests.get(url, timeout=10)
    # data = resp.json()
    # usd_rub = data["rates"]["RUB"]
    # eur_usd = data["rates"]["EUR"]
    btc_usd = requests.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD", timeout=10).json().get("USD")
    eth_usd = requests.get("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD", timeout=10).json().get("USD")

    return btc_usd, eth_usd
@bot.message_handler(commands=["fx"])
def handle_fx(message):
    try:
        btc_usd, eth_usd = get_fx_rates()
        text = (
            f"📊 <b>Курсы монет</b>\n"
            f"1 BTC = {btc_usd:.2f} USD\n"
            f"1 ETH = {eth_usd:.2f} USD\n\n"
            f"{DISCLAIMER}"
        )
    except Exception:
        text = "Не удалось загрузить данные о курсах валют."
    bot.reply_to(message, text)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
def get_finance_news():
    api_key = "your_api_key_here"
    url = f"https://min-api.cryptocompare.com/data/v2/news/?lang=EN&api_key={api_key}"
    resp = requests.get(url)
    data = resp.json()
    return [article["title"] for article in data.get("Data", [])[:3]]
@bot.message_handler(commands=["news"])
def handle_news(message):
    try:
        headlines = get_finance_news()
        text = "📰 <b>Последние новости</b>\n" + "\n".join([f"• {h}" for h in headlines])
    except Exception:
        text = "Не удалось загрузить новости."
    bot.reply_to(message, text)


# @bot.message_handler(commands=["report"])
# def handle_report(message):
#     return


@bot.message_handler(content_types=["text"])
def handle_text(message: telebot.types.Message):
    text = (message.text or "").strip()

    if "курс" in text or "btc" in text or "eth" in text:
        return handle_fx(message)
    if "новост" in text or "рынок" in text or "экономик" in text:
        return handle_news(message)

    if text.lower() in ["биткоин", "курс биткоина", "курс bitcoin", "bitcoin"]:
        bot.reply_to(message, "скоро будет")
        return

    # 1) Каркас мини-анализа по тикеру: "анализ AAPL" / "разбор SBER"
    if text.lower().startswith(("анализ ", "разбор ")):
        parts = text.split()
        if len(parts) >= 2:
            ticker = parts[1]
            bot.reply_to(message, mini_analysis_template(ticker))
            return
        else:
            bot.reply_to(message, "Укажите тикер: например, «анализ AAPL».")
            return
    # 2) Уточняющие вопросы: "что спросить у клиента" / "что уточнить?"
    if "что уточнить" in text.lower() or "что спросить" in text.lower():
        bot.reply_to(message, clarifying_questions("акции"))
        return
    # 3) Короткие запросы вида "помоги с идеей", "с чего начать"
    if "идея" in text.lower() or "с чего начать" in text.lower():
        bot.reply_to(message,
            "Опишите цель (доход/дивиденды/защита), срок и риски. "
            "Я предложу план исследования и список данных, которые запросим позже."
        )
        return
    # 4) По умолчанию — вежливый структурный ответ в стиле роли
    reply = (
        f"{ROLE_PROMPT}\n\n"
        "Опишите, пожалуйста, задачу подробнее (тикер/сектор/цель/срок/ограничения), "
        "и я подготовлю каркас разбора или список уточнений."
    )
    bot.reply_to(message, reply)




if __name__ == "__main__":
    bot.infinity_polling(timeout=10, long_polling_timeout=5)