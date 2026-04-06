
def get_text_loaded(source_type: str):
    if source_type == "url":
        from app.ingestion.loader.url import load as load_url
        return load_url

    elif source_type == "text":
        from app.ingestion.loader.text import load_text
        return load_text

    elif source_type == "directory":
        from app.ingestion.loader.directory import load_directory
        return load_directory
    
    elif source_type == "file":
        from app.ingestion.loader.file import load_file
        return load_file

    else:
        raise ValueError("Invalid source type")