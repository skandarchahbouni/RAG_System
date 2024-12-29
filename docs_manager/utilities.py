import os, magic


def readtext(path):
    path = path.rstrip()
    path = path.replace(" \n", "")
    path = path.replace("%0A", "")
    relative_path = path
    filename = os.path.abspath(relative_path)
    filetype = magic.from_file(filename, mime=True)
    print(f"\nEmbedding {filename} as {filetype}")
    text = ""
    if filetype == "application/pdf":
        print("PDF not supported yet")
    if filetype == "text/plain":
        with open(filename, "rb") as f:
            text = f.read().decode("utf-8")
    if filetype == "text/html":
        with open(filename, "rb") as f:
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text()
    if os.path.exists(filename) and filename.find("content/") > -1:
        os.remove(filename)
    return text
