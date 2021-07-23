from sqlalchemy import create_engine

DB_URL = 'postgresql://ilhamnyto:Dec101298er@localhost:5432/skripsi'
engine = create_engine(DB_URL, echo=False)
