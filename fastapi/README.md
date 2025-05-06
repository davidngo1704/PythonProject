.\.venv\Scripts\activate

cd .\fastapi

uvicorn app.main:app --reload

pip install -r requirements.txt

pip install fastapi uvicorn

