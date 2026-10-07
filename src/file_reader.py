import fitz


def extract_text(file_path):

    if file_path.endswith(".pdf"):

        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text


    elif file_path.endswith(".txt"):

        with open(file_path, "r", encoding="utf-8") as file:

            return file.read()


    else:

        raise ValueError("Only PDF and TXT files are supported.")