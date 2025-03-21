from src.database.chroma import ChromaRepository
from src.util import pdf
from src.util import directory

if __name__ == '__main__':
    db_path = './data/db'

    if directory.is_dir(db_path) == False:
        repository = ChromaRepository(db_path, 'academia')
        text = pdf.extract_text('data/E-book-de-Musculacao-Tiagonutri.pdf')

        repository.create_collection(
            text=text,
            chunk_size=1000,
            overlap=0
        )