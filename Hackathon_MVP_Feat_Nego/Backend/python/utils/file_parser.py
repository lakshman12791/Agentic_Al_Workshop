import os
import json
import csv

def parse_uploaded_file(file_path: str):
    _, ext = os.path.splitext(file_path)

    try:
        if ext == ".json":
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        elif ext == ".csv":
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)

        elif ext == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    except Exception as e:
        raise ValueError(f"Failed to parse {file_path}: {str(e)}")
