class EmailMessage:
    def __init__(self, file_name, raw_text, subject="", sender=""):
        self.file_name = file_name
        self.raw_text = raw_text
        self.subject = subject
        self.sender = sender
