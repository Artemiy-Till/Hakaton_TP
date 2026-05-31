import os

class FileManager:
    def __init__(self):
        if not os.path.exists("output"):
            os.mkdir("output")

        if not os.path.exists("broken_files"):
            os.mkdir("broken_files")

    def move_file(self, file_path, category):
        category_path = "output/" + category

        if not os.path.exists(category_path):
            os.mkdir(category_path)

        file_name = os.path.basename(file_path)
        new_path = category_path + "/" + file_name

        os.rename(file_path, new_path)

        return new_path

    def move_broken_file(self, file_path):
        file_name = os.path.basename(file_path)
        new_path = "broken_files/" + file_name

        os.rename(file_path, new_path)

        return new_path
