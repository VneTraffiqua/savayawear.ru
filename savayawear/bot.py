import logging
from environs import Env
import phonenumbers
from enum import Enum
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

logger = logging.getLogger(__name__)


# Определяем константы этапов разговора
class ConversationPoints(Enum):
    MENU = 0
    PROMO_PROGRAM = 1
    ENTER_NAME = 2
    ENTER_PHONE_NUMBER = 3
    ENTER_PHOTO = 4
    DOWNLOAD_PHOTO = 5
    SUCCESS = 6
    EXIT_FROM_PROMO = 7
    QUESTION_FOR_MANAGER = 8
    SEND_QUESTION_TO_MANAGER = 9


NAME, PHONE_NUMBER, PHOTO, DOWNLOAD_PHOTO, SUCCESS = range(5)
QUESTION, RESENT_QUESTION = range(2)


def start(update, _):
    """Информация о том, что может сделать этот бот"""
    user = update.effective_user
    start_choices_keyboard = [
            ['Акция: 200р. за отзыв'], ['Savayawear в сети'],
            ['Задать вопрос']
    ]
    reply_markup = ReplyKeyboardMarkup(start_choices_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
            fr'Привет, {user.first_name} {user.last_name}, отлично выглядишь!'
            fr' Это чат-бот savayawear. Чем могу помочь?',
            reply_markup=reply_markup
    )


def promotion(update, context):
    user = update.effective_user
    choices_keyboard = [['Участвовать в акции'], ['Savayawear в сети', 'Задать вопрос']]
    reply_markup = ReplyKeyboardMarkup(choices_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
        fr'{user.first_name} {user.last_name}, ага, два листа с Москвой захотел?! Ну ладно, тогда щелкай учавствовать в акции',
        reply_markup=reply_markup
    )
    return NAME


def get_customer_name(update: Update, context: CallbackContext):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал Имя пользователя
    logger.info("%s %s нажал: %s", user.first_name, user.last_name, update.message.text)
    update.message.reply_text(
    'Введите ваше имя и фамилию, или отправь /cancel, если передумал.',
    reply_markup=ReplyKeyboardRemove(),
    )
    return PHONE_NUMBER


def get_phonenumber(update: Update, context: CallbackContext):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал фио пользователя
    logger.info("Имя и фамилия %s: %s", user.username, update.message.text)
    update.message.reply_text(
            'Введите номер телефона, или отправь /cancel, если передумал.',
            reply_markup=ReplyKeyboardRemove(),
    )
    return PHOTO


def enter_number_again(update: Update, context: CallbackContext):
    # определяем пользователя
    user = update.message.from_user

    update.message.reply_text('Введите корректный номер телефона в международном формате. Например +79181234567')
    validate_phonenumber
    return PHOTO # get_phonenumber(update, context)


def validate_phonenumber(update: Update, context: CallbackContext):
    phonenumber = update.message.text

    try:
        pure_phonenumber = phonenumbers.parse(
            phonenumber, 'RU'
        )
    except phonenumbers.phonenumberutil.NumberParseException:
        return enter_number_again(update, context)

    if not phonenumbers.is_valid_number(pure_phonenumber):
        return enter_number_again(update, context)
    # if context.user_data.get('name'):  # если ввод номера произошел при заказе
    #     save_user_choice(update, context)
    #     return
    else:
        return PHOTO


def send_information_to_manager(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Менеджер скоро свяжется с вами...'
    )

    return start(update, context)


def photo(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал пол пользователя
    logger.info("телефон %s: %s", user.username, update.message.text)
    # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
    update.message.reply_text(
        'Хорошо. Пришли мне свой скрин с отзывом, чтоб я зарегестрировал '
        'Вас в акции, или отправь /skip, если передумал.',
        reply_markup=ReplyKeyboardRemove(),
    )
    # переходим к этапу `DOWNLOAD_PHOTO`
    return DOWNLOAD_PHOTO


def skip(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал сведения о фото
    logger.info("Пользователь %s не заполнил форму участия в акции.", user.first_name)
    # Отвечаем на сообщение с пропущенной фотографией
    update.message.reply_text(
        'Держу пари, ты передумаешь!\n'
        'Для перехода в главное меню, введите команду /start'
    )
    # завершаем цикл
    return ConversationHandler.END


def download_photo(update, context):
    # определяем пользователя
    user = update.message.from_user
    # захватываем фото
    try:
        photo_file = update.message.photo[-1].get_file()
    except IndexError:
        photo_file = update.message.document.get_file()
    print(photo_file)
    # скачиваем фото
    photo_file.download(f'./media/{user.id}-{user.first_name}_photo.jpg')
    # Пишем в журнал сведения о фото
    logger.info("Фотография %s: %s", user.first_name, f'{user.first_name}_photo.jpg')
    # Отвечаем на сообщение с фото
    update.message.reply_text(
        'Великолепно! Я зарегистрировал вас в Акции '
        ' С вами свяжется наш менеджер..'
    )
    # Заканчиваем разговор.
    return SUCCESS


def question(update: Update, context: CallbackContext):
    # определяем пользователя
    update.message.reply_text(
        text=f"Задайте свой вопрос:",
        reply_markup=ReplyKeyboardRemove()
    )
    return QUESTION
    # dispatcher.add_handler(MessageHandler(Filters.text),
    #                        forward_to_speaker(update, context))
    # return dispatcher.add_handler(MessageHandler(Filters.text), forward_to_speaker(update, context))


def forward_to_manager(update: Update, context: CallbackContext):
    env = Env()
    env.read_env()
    tg_chat_id = env.str('TG_CHAT_ID')
    question = update.message.text
    print(question)
    update.message.forward(chat_id=tg_chat_id)
    update.message.reply_text(
        text='Сообщение отправлено, ждем ответа менеджера...'
    )
    user_id = update.message.from_user.id
    return RESENT_QUESTION


def answer(update: Update, context: CallbackContext) -> None:
    env = Env()
    env.read_env()
    tg_chat_id = env.str('TG_CHAT_ID')
    user_id = update.message.from_user.id
    # print(update.message.reply_to_message.text)
    # print(update.message.reply_to_message.forward_from.id)
    # print(update.message.reply_to_message.forward_from.first_name)
    if user_id == tg_chat_id:
        print(user_id, '==', tg_chat_id)
        return None
    print(user_id, update.message.text)
    update.message.forward(chat_id=update.message.reply_to_message.forward_from.id)
    return ConversationHandler.END


def say_reply(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Что бы продолжить диалог с менеджером, необходимо ответить на его сообщение, или отправь /cancel, если передумал.'
    )
    return QUESTION


# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться.'
        ' Для возврата в главное меню нажмите /start.',
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END


if __name__ == '__main__':
    logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
    )
    env = Env()
    env.read_env()
    tg_token = env.str('TG_TOKEN')
    tg_logger_token = env.str('TELEGRAM_LOGGER_TOKEN')
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(tg_token)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher
    # Добавляем обработчик разговоров `conv_handler`
    # dispatcher.add_handler(MessageHandler(Filters.text(['Задать вопрос']), question))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text(['Акция: 200р. за отзыв']) & ~Filters.command, promotion))
    question_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.text(['Задать вопрос']), question)
        ],
        states={
            QUESTION: [MessageHandler(Filters.text & ~Filters.command, forward_to_manager)],
            RESENT_QUESTION: [MessageHandler(Filters.reply & ~Filters.command, answer), MessageHandler(Filters.text, say_reply)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.text(['Участвовать в акции']), get_customer_name),
        ],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_customer_name)],
            PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, get_phonenumber)],
            # PHONE_VALIDATOR: [MessageHandler(Filters.text, validate_phonenumber)],
            PHOTO: [MessageHandler(Filters.regex('^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'), photo)],
            DOWNLOAD_PHOTO: [MessageHandler(Filters.photo | Filters.document, download_photo), CommandHandler('cancel', skip)],
            SUCCESS: [send_information_to_manager]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(question_handler)
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.reply & ~Filters.command, answer))
    # Запуск бота
    updater.start_polling()
    updater.idle()
