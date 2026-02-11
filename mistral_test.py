import os
from mistralai import Mistral
import io
import pandas
from dotenv import load_dotenv


load_dotenv("mistralai_api_key.env")

api_key = os.environ["MISTRAL_API_KEY"]

file_path = 'VocabList.pdf'

client = Mistral(api_key=api_key)


uploaded_pdf = client.files.upload(
    file={
        "file_name": file_path,
        "content": open(file_path, "rb"),
    },
    purpose="ocr"
)

retrieved_file = client.files.retrieve(file_id=uploaded_pdf.id)

signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": signed_url.url,
    },
    table_format="markdown",
    # extract_header=True, # default is False
    # extract_footer=True, # default is False
    include_image_base64=True
)

for page in ocr_response.pages:
    if page.tables:
        for table in page.tables:
            df = pandas.read_table(io.StringIO(table.content), sep="|", skipinitialspace=True)
            df = df.dropna(axis=1, how="all")
            df.to_csv("out.csv", index=False)