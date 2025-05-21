from qdrant_utils import get_client, create_collection, upsert_vectors, search_vectors
import numpy as np

COLLECTION_NAME = "demo_collection"
VECTOR_SIZE = 4

if __name__ == "__main__":
    client = get_client()
    create_collection(client, COLLECTION_NAME, VECTOR_SIZE)

    # Example: Insert 10 random vectors
    vectors = np.random.rand(10, VECTOR_SIZE).tolist()
    payloads = [{"label": f"item_{i}"} for i in range(10)]
    upsert_vectors(client, COLLECTION_NAME, vectors, payloads)
    print(f"Inserted {len(vectors)} vectors.")

    # Example: Search for similar vectors to a random query
    query_vector = np.random.rand(VECTOR_SIZE).tolist()
    results = search_vectors(client, COLLECTION_NAME, query_vector, top_k=3)
    print("Search results:")
    for hit in results:
        print(f"ID: {hit.id}, Score: {hit.score}, Payload: {hit.payload}") 