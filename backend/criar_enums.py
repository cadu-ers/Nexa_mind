from src.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("CREATE TYPE tipo_arquivo_enum AS ENUM ('pdf', 'pptx', 'docx', 'txt', 'md', 'outro')"))
    conn.execute(text("CREATE TYPE dificuldade_enum AS ENUM ('facil', 'medio', 'dificil')"))
    conn.execute(text("CREATE TYPE papel_mensagem_enum AS ENUM ('usuario', 'assistente')"))
    conn.commit()

print('ENUMs criados com sucesso!')