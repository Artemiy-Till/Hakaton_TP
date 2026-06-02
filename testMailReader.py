import pytest
import os
from mail_reader import MailReader

class TestMailReader:
    @pytest.fixture
    def reader(self):
        return MailReader()
    def test_image(self, reader, tmp_path):
        message = os.path.join(tmp_path, "scooter.jpeg")
        with open(message, "w", encoding="utf-8") as file:
            file.write("scooterrr")
        with pytest.raises(ValueError) as error:
            reader.read(message)
        assert str(error.value) == "Изображение"
    def test_empty(self, reader, tmp_path):
        message = os.path.join(tmp_path, "vozduh.txt")
        with open(message, "w", encoding="utf-8") as file:
            file.write("")
        with pytest.raises(ValueError) as error:
            reader.read(str(message))
        assert str(error.value) == "В файле ничего нет, он пустой"
    def test_engText(self, reader, tmp_path):
        message = os.path.join(tmp_path, "engText.txt")
        text = """From: students.com
        Subject: происшествие на шаболовской
        На территории очень много велосипедов"""
        with open(message, "w", encoding="utf-8") as file:
            file.write(text)
        res = reader.read(message)
        assert res.file_name == "engText.txt"
        assert res.sender == "students.com"
        assert res.subject == "происшествие на шаболовской"
    def test_rusText(self, reader, tmp_path):
        message = os.path.join(tmp_path, "rusText.txt")
        text = """От кого: матан.com
        Тема: скоро экзамен
        я ненавижу интегралы"""
        with open(message, "w", encoding="utf-8") as file:
            file.write(text)
        res = reader.read(message)
        assert res.file_name == "rusText.txt"
        assert res.sender == "матан.com"
        assert res.subject == "скоро экзамен"
    def test_translitText(self, reader, tmp_path):
        message = os.path.join(tmp_path, "translitText.txt")
        text = """Ot kogo: studentochki.com
        Tema: pomogite skoro sessia"""
        with open(message, "w", encoding="utf-8") as file:
            file.write(text)
        res = reader.read(message)
        assert res.file_name == "translitText.txt"
        assert res.sender == "studentochki.com"
        assert res.subject == "pomogite skoro sessia"
    def test_noSender(self, reader, tmp_path):
        message = os.path.join(tmp_path, "withoutSender.txt")
        text = "Subject: ляляляля"
        with open(message, "w", encoding="utf-8") as file:
            file.write(text)
        res = reader.read(message)
        assert res.file_name == "withoutSender.txt"
        assert res.sender == ""
        assert res.subject == "ляляляля"
    def test_noSubject(self, reader, tmp_path):
        message = os.path.join(tmp_path, "withoutSubject.txt")
        text = "От кого: ychebka.ru"
        with open(message, "w", encoding="utf-8") as file:
            file.write(text)
        res = reader.read(message)
        assert res.file_name == "withoutSubject.txt"
        assert res.sender == "ychebka.ru"
        assert res.subject == ""
    def test_noSenderNoSubject(self, reader, tmp_path):
        message = os.path.join(tmp_path, "nothing.txt")
        text = "ааа"
        with open(message, "w", encoding="utf-8") as file:
            file.write(text)
        res = reader.read(message)
        assert res.file_name == "nothing.txt"
        assert res.sender == ""
        assert res.subject == ""
    def test_Error(self, reader, tmp_path):
        message = os.path.join(tmp_path, "nothing.txt")
        text = "aaa"
        with pytest.raises(ValueError) as error:
            reader.read(message)
        assert str(error.value) == "Сообщение не является отдельным файлом или его нет"
