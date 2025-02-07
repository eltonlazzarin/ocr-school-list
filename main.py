import json
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_textract.type_defs import DetectDocumentTextResponseTypeDef

def detect_file_text(file_name: str = "lista-material-escolar.jpeg") -> None:
    client = boto3.client("textract")
    file_path = Path(__file__).parent / "images" / file_name
    
    if not file_path.exists():
        print(f"File {file_path} not found.")
        return

    try:
        with file_path.open("rb") as f:
            document_bytes = f.read()
        response = client.detect_document_text(Document={"Bytes": document_bytes})
        Path("response.json").write_text(json.dumps(response, indent=4))
    except ClientError as e:
        print(f"Error processing document: {e}")

def get_lines() -> list[str]:
    response_file = Path("response.json")
    
    if not response_file.exists():
        detect_file_text()
        if not response_file.exists():
            return []
    
    try:
        data: DetectDocumentTextResponseTypeDef = json.loads(response_file.read_text())
        return [block["Text"] for block in data.get("Blocks", []) if block.get("BlockType") == "LINE"]
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading response file: {e}")
        return []

if __name__ == "__main__":
    for line in get_lines():
        print(line)
