import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, PointStruct

QDRANT_HOST = os.getenv('QDRANT_HOST', 'localhost')
QDRANT_PORT = int(os.getenv('QDRANT_PORT', 6333))


def get_client():
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def create_collection(client, collection_name, vector_size, distance="Cosine"):
    collections = client.get_collections().collections
    if collection_name not in [c.name for c in collections]:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance)
        )


def upsert_vectors(client, collection_name, vectors, payloads=None):
    points = [
        PointStruct(
            id=i,
            vector=vec,
            payload=payloads[i] if payloads else None
        )
        for i, vec in enumerate(vectors)
    ]
    client.upsert(collection_name=collection_name, points=points)


def search_vectors(client, collection_name, query_vector, top_k=5, filter_payload=None):
    return client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        query_filter=filter_payload
    ) 