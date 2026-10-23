from app.rag.chunker import fixed_chunking

text = """
Machine Learning is a field of AI.

Supervised learning uses labelled data.

Deep learning uses neural networks.

Transformers power modern LLMs.
""" * 50

chunks = fixed_chunking(text)

print("Chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print()
    print(f"Chunk {i+1}")
    print(chunk[:100])