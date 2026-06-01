import os

from mail_reader import MailReader
from mail_classifier import MailClassifier
from file_manager import FileManager


if not os.path.exists("inbox"):
    print("Ошибка: папка inbox не найдена")
else:
    reader = MailReader()
    classifier = MailClassifier()
    file_manager = FileManager()

    processed = 0
    broken = 0
    categories = {}
    if not os.path.exists("logs"):
        os.mkdir("logs")

    log_file = open("logs/processing.log", "w", encoding="utf-8")

    files = sorted(os.listdir("inbox"))

    for file_name in files:
        file_path = "inbox/" + file_name

        if os.path.isfile(file_path):
            try:
                email = reader.read(file_path)
                category = classifier.classify(email.sender, email.subject, email.raw_text)
                new_path = file_manager.move_file(file_path, category)

                processed = processed + 1

                if category in categories:
                    categories[category] = categories[category] + 1
                else:
                    categories[category] = 1

                print("Обработан файл", file_name)
                print("Добавлен в папку", category)
                log_file.write(file_name + " -> " + category + "\n")




            except Exception as error:
                broken = broken + 1
                file_manager.move_broken_file(file_path)
                print("Плохой файл:", file_name)
                print("Причина:", error)
                log_file.write(file_name + " -> broken_files, reason: " + str(error) + "\n")




    print()
    print("Статистика")
    print("Обработано:", processed)
    print("Плохих файлов:", broken)

    print()
    print("Категории:")
    for category in categories:
        print(category, categories[category])
    log_file.close()
