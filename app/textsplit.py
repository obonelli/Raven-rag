from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)

def split_text(text: str):
    return list(splitter.split_text(text))
