import nltk

#old
# def chunker(text: str, length=400, overlap=80) -> list:
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = start + length
#         chunks.append(text[start:end])
#         start = end - overlap

#     return chunks

#Fix 2: Preserve Sentences
nltk.download('punkt')


def chunker(text: str, length=400, overlap=80) -> list:
    sentence = nltk.sent_tokenize(text)
    chunks = []
    current = ""
    for s in sentence:
        if len(current) + len(s) < length:
            current += " " + s
        else:
            chunks.append(current.strip())
            current = current[-overlap:] + s
    if current:
        chunks.append(current)

    return chunks