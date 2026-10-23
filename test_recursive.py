from app.rag.chunker import recursive_chunking

with open(
    "app/data/documents/sample.txt",
    "r",
    encoding="utf-8"
) as file:

    text = file.read()

chunks = recursive_chunking(text)

for i, chunk in enumerate(chunks):
    print()
    print("Chunk", i+1)
    print(chunk)