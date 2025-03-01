# -*- coding: utf-8 -*-
"""Qdrant_Vectorestor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10cGDsQ879_005pn3jSTbA1BD24z_lXkZ
"""

api-key="5KCuzIx5YGcAj_2AEwjl4nPv08-8UHxLjE4ziJXQRRl7-2XnUuEyow"
url=curl \
    -X GET 'https://63ac2483-f9a4-4b62-b6bb-8c130dd117a8.us-east4-0.gcp.cloud.qdrant.io:6333' \
    --header 'api-key: 5KCuzIx5YGcAj_2AEwjl4nPv08-8UHxLjE4ziJXQRRl7-2XnUuEyow'

!pip install langchain qdrant_client openai tiktoken

!pip install langchain-qdrant --q

!pip install langchain_community --q

from langchain_community.document_loaders import TextLoader,PyPDFLoader
# from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import CharacterTextSplitter

from langchain_community.embeddings import HuggingFaceBgeEmbeddings

!pip install pypdf --q

loader = PyPDFLoader("/content/drive/MyDrive/Docs/hh/Gemini.pdf")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# embeddings = OpenAIEmbeddings()

!pip install sentence_transformers --q

model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

import qdrant_client
import os
from langchain.vectorstores import Qdrant

#Client
client = qdrant_client.QdrantClient(
        "https://63ac2483-f9a4-4b62-b6bb-8c130dd117a8.us-east4-0.gcp.cloud.qdrant.io:6333",
        api_key="5KCuzIx5YGcAj_2AEwjl4nPv08-8UHxLjE4ziJXQRRl7-2XnUuEyow"
    )

# create collection
collection="my_collection1"

collection_config = qdrant_client.http.models.VectorParams(
        size=1024, # 768 for instructor-xl, 1536 for OpenAI
        distance=qdrant_client.http.models.Distance.COSINE
    )

client.recreate_collection(
    collection_name=collection,
    vectors_config=collection_config
)

vectorstore = Qdrant(
        client=client,
        collection_name=collection,
        embeddings=embeddings
    )

vectorstore.add_documents(docs)

vectorstore.similarity_search_with_score("tell me about the performance of Gemini modles?")[0]