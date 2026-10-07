def read_file(file_path):

    try:

        with open(file_path, "r", encoding="utf-8") as file:

            return file.read()

    except FileNotFoundError:

        print("File Not Found.")

        return None