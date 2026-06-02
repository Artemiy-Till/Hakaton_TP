import os
import pytest

from mail_classifier import MailClassifier
from mail_reader import MailReader
from file_manager import FileManager
from email_message import EmailMessage


class TestMailClassifier:
    @pytest.fixture
    def classifier(self):
        return MailClassifier()

    @pytest.mark.parametrize(
        "subject,sender,body,expected",
        [
            (
                "Срочно: новости о ШДА",
                "dsvarch@hes.ru",
                "Произошел критический инцидент, нужна срочная помощь, у велосипеда пропало колесо",
                "important",
            ),
            (
                "Проблема с ноутбуком",
                "konstantin@hes.com",
                "На территории ВЭШ замечен человек не с макбкуком, нужна замена оборудования",
                "hardware",
            ),
            (
                "Ошибка в приложении HES APP",
                "user@hes.com",
                "Программа не запускается, появляется код ошибки",
                "software",
            ),
            (
                "Запрос доступа",
                "employee@hes.com",
                "Нужно выдать права в GitLab и VPN",
                "access",
            ),
            (
                "Плановые технические работы",
                "zakG@hes.com",
                "Уведомление о регламентных работах по кондиционерам, сегодня воздух проветривается специалистами",
                "info",
            ),
            (
                "Вы выиграли приз",
                "subo@hes.com",
                "Перейдите по ссылке и получите пересдачу",
                "spam",
            ),
            (
                "Перенос созвона по поводу B2G AI SAAS product",
                "alekseyPersh@hes.com",
                "Предлагаю встретиться завтра и обсудить статус задач в дрынкыте",
                "meetings",
            ),
            (
                "Правки в документации",
                "polinaSm@hes.com",
                "Нужно внести правки в курсовой проект",
                "docs",
            ),
            (
                "Счёт на оплату",
                "finance@hes.com",
                "Просим оплатить ИУП по договору",
                "finance",
            ),
            (
                "Консультация и немного юмора",
                "kar@hes.com",
                "Был у меня один случай",
                "inbox",
            ),
        ],
    )
    def test_classifies_known_categories(self, classifier, subject, sender, body, expected):
        result = classifier.classify(subject, sender, body)

        assert result == expected

    def test_empty_email_goes_to_inbox(self, classifier):
        result = classifier.classify(
            subject="",
            sender="",
            body="",
        )

        assert result == "inbox"

    def test_case_insensitive_classification(self, classifier):
        result = classifier.classify(
            subject="URGENT SERVER DOWN",
            sender="ADMIN@COMPANY.COM",
            body="Critical problem",
        )

        assert result == "important"

    def test_all_output_folders_are_supported(self, classifier):
        expected_folders = {
            "spam",
            "important",
            "access",
            "meetings",
            "hardware",
            "docs",
            "info",
            "software",
            "finance",
            "inbox",
        }

        assert set(classifier.rules.keys()) == expected_folders

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

class TestFileManager:
    def test_move_file_creates_category_folder_and_moves_file(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        inbox = tmp_path / "inbox"
        inbox.mkdir()

        source_file = inbox / "mail_001.txt"
        source_file.write_text("test email", encoding="utf-8")

        manager = FileManager()
        new_path = manager.move_file(str(source_file), "software")

        assert new_path == "output/software/mail_001.txt"
        assert not source_file.exists()
        assert os.path.exists("output/software/mail_001.txt")

    def test_move_broken_file_moves_file_to_broken_files(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        inbox = tmp_path / "inbox"
        inbox.mkdir()

        source_file = inbox / "broken_mail.txt"
        source_file.write_text("broken email", encoding="utf-8")

        manager = FileManager()
        new_path = manager.move_broken_file(str(source_file))

        assert new_path == "broken_files/broken_mail.txt"
        assert not source_file.exists()
        assert os.path.exists("broken_files/broken_mail.txt")
