"""Chunk the help articles and store them in a local Chroma vector store."""
import pathlib
import chromadb

CHUNK_CHARS = 600


def chunk(text: str, size: int = CHUNK_CHARS):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, current = [], ""
    for p in paragraphs:
        if current and len(current) + len(p) > size:
            chunks.append(current)
            current = p
        else:
            current = f"{current}\n\n{p}".strip()
    if current:
        chunks.append(current)
    return chunks


def main():
    client = chromadb.PersistentClient(path="chroma_db")
    try:
        client.delete_collection("help_center")
    except Exception:
        pass
    collection = client.create_collection("help_center")

    ids, docs, metas = [], [], []
    for path in sorted(pathlib.Path("kb").glob("*.md")):
        for i, c in enumerate(chunk(path.read_text(encoding="utf-8"))):
            ids.append(f"{path.stem}-{i}")
            docs.append(c)
            metas.append({"source": path.name})
    collection.add(ids=ids, documents=docs, metadatas=metas)
    print(f"Indexed {len(docs)} chunks from {len(set(m['source'] for m in metas))} articles")


if __name__ == "__main__":
    main()
