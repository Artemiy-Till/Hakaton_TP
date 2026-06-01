import os
from file_manager import FileManager

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
