import faiss
import numpy as np
index = None
chunks_store =[]
def create_index(embeddings,chunks):
    global index,chunks_store
    dim =len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    chunks_store =chunks
    print("FAISS index created successfully")
    print("Total chunks stored :",len(chunks_store))
def search (query_embedding,k=3):
    global index
    if index is None:
        return ["please upload a pdf first."]
    D,I =index.search(np.array([query_embedding],dtype=np.float32), k)
    return [chunks_store[i] for i in I[0]]    
   