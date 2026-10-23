from app.rag.chunker import sliding_window_chunking

text = "A" * 2000

chunks = sliding_window_chunking(text)

print("Total Chunks:", len(chunks))

for chunk in chunks:
    print(len(chunk))