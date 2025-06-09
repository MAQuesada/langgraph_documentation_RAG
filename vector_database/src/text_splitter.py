from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_files(input_dir, chunk_size=500, chunk_overlap=50):
    input_dir = Path(input_dir)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
        )
    
    chunks_with_metadata = []

    for txt_file in input_dir.glob('*.txt'):
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        splits = splitter.split_text(content)
        chunks_with_metadata.extend([{
            "content" : chunk,
            "source" : txt_file.name
        } for chunk in splits])

        return chunks_with_metadata
