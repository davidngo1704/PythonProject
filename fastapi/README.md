.\.venv\Scripts\activate

pip install -r requirements.txt

pip install fastapi uvicorn

uvicorn main:app --reload