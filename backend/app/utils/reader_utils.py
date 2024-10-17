from pypdf import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=750,
    chunk_overlap=50,
    length_function=len,
)


def pdf_to_document(filepath):
    pdf_reader = PdfReader(filepath)
    raw_text = ""
    for i, page in enumerate(pdf_reader.pages):
        content = page.extract_text()
        if content:
            raw_text += content
    texts = text_splitter.split_text(raw_text)
    documents = []
    for text in texts:
        documents.append(Document(
            page_content=text,
            metadata={"source": filepath},
        ))
    return documents


def text_to_document(filepath):
    loader = TextLoader(filepath)
    text_document = loader.load()
    documents = text_splitter.split_documents(text_document)
    return documents
