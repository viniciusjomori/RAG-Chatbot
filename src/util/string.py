def chunk_text(text: str, chunk_size: int = 100, overlap: int = 0):
    chunks = []
    start = 0

    while True:
        end = min(start+chunk_size, len(text))

        chunk = text[start:end]
        chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap
    
    return chunks