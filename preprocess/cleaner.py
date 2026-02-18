import unicodedata
import re
import ftfy
import json


def clean_text(text: str) -> str:
    # Fix broken encoding (â‚¬, Ã©, etc.)
    try:
        text = json.loads(f'"{text}"')
    except:
        pass
    
    text = ftfy.fix_text(text)


    # Normalize unicode
    text = unicodedata.normalize("NFKC", text)

    # Lowercase
    text = text.lower()

    # Remove junk characters (keep currency)
    text = re.sub(r"[\x00-\x1F\x7F]", " ", text)

    # Normalize spaces
    text = " ".join(text.split())

    return text.strip()
