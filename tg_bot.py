import neural_process
import file_process
import config
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes


# Функция, которая вызывается при отправке файла
async def handle_file(update: Update, context: CallbackContext):
    audio = update.message.audio
    print(audio.mime_type)
    # Сохраняем аудиофайл локально и получаем путь сохранения
    file = await context.bot.get_file(audio.file_id)
    f_name = audio.file_name
    local_file_path = file_process.save_audio_file(f_name, file.file_path)
    # Отправляем сообщение о успешном сохранении аудиофайла
    await update.message.reply_text(
        f"Подождите немного, я в ускоренном темпе прослушаю аудиофайл {f_name} и отправлю вам текстовую "
        f"расшифровку с переводом."
    )
    # проверяем файл на длительность
    status = True
    status_dur = True
    try:
        file_dur = file_process.file_duration_check(local_file_path)
        if file_dur > 600:
            status_dur = False
    except Exception as e:
        print(f"Возникла ошибка: {e}")
        status_dur = False

    # Получаем перевод

    trance_text = 'в эту переменную сохраняется текст транскрибации с переводом'
    if status_dur:
        try:
            start_time = time.time()
            trance_text = neural_process.final_process(local_file_path, f_name)
        except Exception as e:
            print(f"Возникла ошибка: {e}")
            status = False
    else:
        status = False
        await update.message.reply_text(
            f"Сожалею, но возникла ошибка обработки файла. Длительность файла не должна превышать десять минут."
        )

    if status:
        # Сохраняем вывод в текстовый файл
        tx_file_path = file_process.save_text_to_file(f_name, trance_text)
        end_time = time.time()
        process_time = round(end_time - start_time, 2)
        await update.message.reply_text(
            f"Перевод готов! Ловите файл с переводом. Затраченное время: {process_time} сек.  "
        )
        # Отправляем текстовый файл
        with open(tx_file_path, "rb") as document:
            await context.bot.send_document(chat_id=update.message.chat_id, document=document)

    else:
        file_process.delete_file(local_file_path)
        if status_dur:
            await update.message.reply_text(
                f"Сожалею, но возникла ошибка обработки файла. Пожалуйста, убедитесь что файл имеет правильный аудиоформат."
            )

# Функция для команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Привет! Добро пожаловать! Нравится песня, но ты не знаешь о чем она? Я могу перевести песню с любого языка '
        'на русский за считанные секунды, просто скинь аудио файл в чат. ')


# Функция для команды / help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"{user.mention_html()}, я могу перевести песню с любого языка на русский, просто скинь аудио файл в чат.",
        reply_markup=ForceReply(selective=False),
    )


# Запускаем бота
def main():
    # Токен  бота
    application = Application.builder().token(config.tg_key).build()
    # Регистрируем обработчик для команды /start
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # Регистрируем обработчик для приема файлов
    application.add_handler(MessageHandler(filters.AUDIO, handle_file))
    # Запускаем бота
    application.run_polling()
    # Останавливаем бота при нажатии Ctrl+C
    application.idle()


if __name__ == '__main__':
    main()
