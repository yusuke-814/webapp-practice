from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import Base, engine, get_db
from models import Message

# デーブル作成
# 検証用のため、本番ではAlembicなどのマイグレーションツールを使用してください
Base.metadata.create_all(bind=engine)

app = FastAPI()

# React (localhost:3000)からのアクセスを許可
# 本番環境では具体的なドメインを指定するか、より厳格なCORSポリシーを設定する必要がある
# 将来的にBearer Tokenなどの認証ヘッダを使う可能性を考慮し、Authorizationを許可している
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.get("/api/message")
def get_message(db: Session = Depends(get_db)):
    msg = db.query(Message).first()
    if msg:
        return {"message": msg.text}
    else:
        new_msg = Message(text="Hello from PostgreSQL + SQLAlchemy!")
        db.add(new_msg)
        db.commit()
        db.refresh(new_msg)
        return {"message": new_msg.text}