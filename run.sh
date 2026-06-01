#!/bin/bash

echo "Запуск проекта"

cd "$(dirname "$0")"

if [ ! -d "inbox" ]; then
    echo "Ошибка: папка inbox не найдена"
    exit 1
fi

if [ ! -f "src/main.py" ]; then
    echo "Ошибка: файл src/main.py не найден"
    exit 1
fi

if [ ! -d "logs" ]; then
    mkdir logs
fi

echo "Папка inbox найдена"
echo "Файл src/main.py найден"
echo "Запускаю программу"

python src/main.py > logs/run_output.log 2>&1

if [ $? -eq 0 ]; then
    echo "Программа завершилась успешно"
    echo "Вывод программы сохранён в logs/run_output.log"
else
    echo "Произошла ошибка при запуске программы"
    echo "Подробности ошибки сохранены в logs/run_output.log"
    exit 1
fi
