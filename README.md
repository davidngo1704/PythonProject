.\.venv\Scripts\activate

pip install fastapi uvicorn

uvicorn fastapi.main:app --reload