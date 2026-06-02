#!/bin/bash

echo "Запуск проекта"

cd "$(dirname "$0")"

if [ ! -f "main.py" ]; then
    echo "Ошибка: файл main.py не найден"
    exit 1
fi

if [ ! -d "inbox" ]; then
    echo "Ошибка: папка inbox не найдена"
    exit 1
fi

if [ ! -f "tests" ]; then
    echo "Ошибка: файл tests.py не найден"
    exit 1
fi

if [ ! -d "logs" ]; then
    mkdir logs
fi

echo "Файл main.py найден"
echo "Папка inbox найдена"
echo "Файл tests найден"

echo "Запускаю тесты"

python3 -m pytest tests.py > logs/tests_output.log 2>&1

if [ $? -eq 0 ]; then
    echo "Тесты прошли успешно"
    echo "Результат тестов сохранён в logs/tests_output.log"
else
    echo "Тесты не прошли"
    echo "Подробности ошибки сохранены в logs/tests_output.log"
    exit 1
fi

echo "Запускаю основную программу"

python3 main.py > logs/run_output.log 2>&1

if [ $? -eq 0 ]; then
    echo "Программа завершилась успешно"
    echo "Вывод программы сохранён в logs/run_output.log"
else
    echo "Произошла ошибка при запуске программы"
    echo "Подробности ошибки сохранены в logs/run_output.log"
    exit 1
fi
