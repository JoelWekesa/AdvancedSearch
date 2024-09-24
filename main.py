from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from search.setup import add_to_chroma, vector_store

from search.search import SearchParams

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "API is up and running"
    }

@app.get("/search")
async def searchResults(params: Annotated[SearchParams, Query()]):

    try:
        results = vector_store.similarity_search(query=params.query, k=params.k)

        response = [result.metadata for result in results]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred in performing the search, {e}")
    
@app.on_event("startup")
async def startup_event():
    await add_to_chroma()
