import os

class FileManager:
    def __init__(self):
        if not os.path.exists("output"):
            os.mkdir("output")

        if not os.path.exists("broken_files"):
            os.mkdir("broken_files")

    def copy_file(self, file_path, category):
        category_path = "output/" + category

        if not os.path.exists(category_path):
            os.mkdir(category_path)

        file_name = os.path.basename(file_path)
        new_path = category_path + "/" + file_name

        old_file = open(file_path, "r", encoding="utf-8")
        text = old_file.read()
        old_file.close()

        new_file = open(new_path, "w", encoding="utf-8")
        new_file.write(text)
        new_file.close()

        return new_path

    def copy_broken_file(self, file_path):
        file_name = os.path.basename(file_path)
        new_path = "broken_files/" + file_name

        old_file = open(file_path, "r", encoding="utf-8")
        text = old_file.read()
        old_file.close()

        new_file = open(new_path, "w", encoding="utf-8")
        new_file.write(text)
        new_file.close()

        return new_path
