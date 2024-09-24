import asyncio
import os
from datetime import datetime
from typing import List, TypedDict
import aiohttp
from langchain_community.vectorstores import Chroma
from langchain_postgres import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()



class Category(TypedDict):
    id:         int;
    name:       str;
    image:      str;
    creationAt: datetime;
    updatedAt:  datetime;


class Product(TypedDict):
    id:          int;
    title:       str;
    price:       int;
    description: str;
    images:      List[str];
    creationAt:  datetime
    updatedAt:   datetime;
    category:    Category;





async def getProducts() -> List[Product]:
    api_url = 'https://api.escuelajs.co/api/v1/products'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            products = await response.json()
    return products

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embedding_function = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

async def add_to_chroma():
    products = await getProducts()
    print(f"Fetched {len(products)} products")
    db = PGVector(
        embeddings=embedding_function,
        collection_name=os.environ['COLLECTION_NAME'],
        connection=os.environ['DB_CONNECTION_STRING'],
        use_jsonb=True,
    )

        
    documents = [
            Document(
                id= str(product["id"]),
                page_content=f"{product['title']}\n{product['description']}",
                metadata={
                    "id": str(product["id"]),
                    "title": product["title"],
                    "description": product["description"],
                    "price": product["price"],
                    "category": product["category"],
                    "images": product["images"],
                    "creationAt": product["creationAt"],
                    "updatedAt": product["updatedAt"]
                }
            ) for product in products
        ]

    document_ids = [doc.metadata["id"] for doc in documents]

    db.add_documents(documents, ids=document_ids)

vector_store = PGVector(
    embeddings=embedding_function,
    collection_name=os.environ['COLLECTION_NAME'],
    connection=os.environ['DB_CONNECTION_STRING'],
    use_jsonb=True,
)
