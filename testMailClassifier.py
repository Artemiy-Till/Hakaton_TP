mport os
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
