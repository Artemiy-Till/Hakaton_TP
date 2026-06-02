import os
from email_message import EmailMessage
class MailReader:
    def read(self, message):
        if os.path.isfile(message):
            if self.imageMessage(message):
                raise ValueError("Изображение")
            if os.path.getsize(message) == 0:
                raise ValueError("В файле ничего нет, он пустой")
            try:
                openMessage = open(message, "r", encoding="utf-8")
                messageText = openMessage.read()
                openMessage.close()
            except UnicodeDecodeError:
                raise ValueError("Файл ошибочный")
        else:
            raise ValueError("Сообщение не является отдельным файлом или его нет")
        subject = self.findSubject(messageText)
        sender = self.findSender(messageText)
        return EmailMessage(
            file_name = os.path.basename(message),
            raw_text = messageText,
            subject = subject,
            sender = sender )
    def imageMessage(self, message):
        image = False
        table = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
        low = message.lower()
        for types in table:
            if low.endswith(types):
                image = True
                break
        return image
    def findSender(self, messageText):
        lines = messageText.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("From:"):
                return line[5:].strip()
            if line.startswith("От кого:"):
                return line[8:].strip()
            if line.startswith("Ot kogo:"):
                return line[8:].strip()
        return ""
    def findSubject(self, messageText):
        lines = messageText.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("Subject:"):
                return line[8:].strip()
            if line.startswith("Тема:"):
                return line[5:].strip()
            if line.startswith("Tema:"):
                return line[5:].strip()
        return ""
