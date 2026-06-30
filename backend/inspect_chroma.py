"""
Script de inspección detallada de ChromaDB.

Uso:
    cd backend
    uv run python inspect_chroma.py

Objetivos:
- Mostrar cuántos chunks tiene cada documento.
- Mostrar un preview de TODOS los chunks.
- Reconstruir el documento completo para validar que el loader
  realmente obtuvo el artículo y no solo el menú.
"""

from collections import defaultdict

from app.rag.vectorstore import get_vectorstore


def main() -> None:
    vs = get_vectorstore()

    total = vs._collection.count()

    print("\n" + "=" * 100)
    print(f"Total de chunks en ChromaDB: {total}")
    print("=" * 100)

    if total == 0:
        print("La colección está vacía.")
        return

    raw = vs._collection.get(include=["documents", "metadatas"])

    # Agrupar chunks por fuente
    docs_by_source = defaultdict(list)

    for content, metadata in zip(raw["documents"], raw["metadatas"]):
        source = metadata.get("source", "desconocido")
        docs_by_source[source].append(content)

    print(f"\nFuentes encontradas: {len(docs_by_source)}\n")

    # Inspeccionar cada documento
    for source, chunks in docs_by_source.items():

        print("=" * 100)
        print(f"FUENTE: {source}")
        print(f"Cantidad de chunks: {len(chunks)}")
        print("=" * 100)

        # Mostrar todos los chunks
        for idx, chunk in enumerate(chunks, start=1):

            print(f"\n--- Chunk {idx}/{len(chunks)}")
            print(f"Longitud: {len(chunk)} caracteres")

            preview = chunk.replace("\n", " ")[:400]

            print(preview)

        # Reconstrucción del documento completo
        full_text = "\n".join(chunks)

        print("\n" + "-" * 100)
        print("RESUMEN DEL DOCUMENTO RECONSTRUIDO")
        print("-" * 100)
        print(f"Longitud total: {len(full_text)} caracteres")

        print("\nPrimeros 1000 caracteres:\n")
        print(full_text[:1000])

        print("\nÚltimos 1000 caracteres:\n")
        print(full_text[-1000:])

        print("\n\n")

    print("=" * 100)
    print("Fin de la inspección")
    print("=" * 100)


if __name__ == "__main__":
    main()