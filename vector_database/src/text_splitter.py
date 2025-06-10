from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from vector_database.src.utils import load_config
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
from dotenv import load_dotenv
load_dotenv()


def sentence_based_chunking(text, chunk_size=800):

    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

config = load_config()
chunking_config = config['document_processing']['chunking']
chunk_size = chunking_config.get('chunk_size', 512)
chunk_overlap = chunking_config.get('chunk_overlap', 50)

def chunk_documents(documents):
    all_chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
    )

    filtered_docs = [
        doc for doc in documents
        if doc is not None and (
            (isinstance(doc, dict) and 'page_content' in doc) or
            hasattr(doc, 'page_content')
        )
    ]

    for doc in filtered_docs:
        metadata = {
            "source": doc.metadata.get("file_path", "unknown"),
            "file_type": doc.metadata.get("file_type", "unknown")
        }
        try:
            content = doc['page_content'] if isinstance(doc, dict) else doc.page_content
            metadata = doc['metadata'] if isinstance(doc, dict) else getattr(doc, 'metadata', {})

            sentence_chunks = sentence_based_chunking(content, chunk_size=1000)

            sentence_docs = [
                Document(page_content=chunk, metadata=metadata)
                for chunk in sentence_chunks
            ]

            final_chunks = splitter.split_documents(sentence_docs)
            all_chunks.extend(final_chunks)
        
        except Exception as e:
            file_path = metadata.get('file_path', 'unknown') if metadata else 'unknown'
            print(f'Chunking failed for {file_path} = {e}')
        
    return all_chunks