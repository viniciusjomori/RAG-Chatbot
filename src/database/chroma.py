import chromadb
from openai import OpenAI
from src.util.string import chunk_text

llm = OpenAI()

class ChromaRepository:
    def __init__(self, db_name, collection_name, model='text-embedding-3-small'):
        self.db_name = db_name
        self.collection_name = collection_name
        self.db = chromadb.PersistentClient(path=db_name)
        self.collection = self.db.get_or_create_collection(name=collection_name)
        self.model = model
    
    def get_embedding(self, chunks: list) -> list:
        result = llm.embeddings.create(
            model=self.model,
            input=chunks
        )
        return [item.embedding for item in result.data]

    def create_collection(self, text: str, chunk_size: int, overlap: int):
        chunks = chunk_text(text, chunk_size, overlap)
        embbedings = self.get_embedding(chunks)

        self.collection.add(
            embeddings=embbedings,
            documents=chunks,
            ids=[str(id) for id in range(len(embbedings))]
        )
    
    def retrieve(self, query, results):
        query_embeddings = self.get_embedding([query])
        result = self.collection.query(
            query_embeddings=query_embeddings,
            n_results=results
        )

        return result['documents'][0]