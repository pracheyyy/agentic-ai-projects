from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_document(transcript: str, video_id: str) -> Document:
    """
    Convert the YouTube transcript into a LangChain Document.
    """

    document = Document(
        page_content=transcript,
        metadata={
            "source": "youtube",
            "video_id": video_id
        }
    )

    return document


def split_document(document: Document):
    """
    Split the document into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents([document])

    return chunks