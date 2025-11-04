from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uvicorn
from deepseek import DeepSeekChat  # Your model wrapper

# Database Models
Base = declarative_base()

class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True)
    user_query = Column(Text)
    bot_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Database Setup (with connection pooling)
DATABASE_URL = "postgresql://user:password@localhost/proddb"
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI()
model = DeepSeekChat()  # Initialize your model

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    db = SessionLocal()
    try:
        # Generate response (with timeout safety)
        try:
            response = model.generate(request.prompt)
        except Exception as model_error:
            raise HTTPException(
                status_code=503,
                detail=f"Model service unavailable: {str(model_error)}"
            )
        
        # Log to database
        log = ChatLog(
            user_query=request.prompt,
            bot_response=response
        )
        db.add(log)
        db.commit()
        
        return {
            "response": response,
            "timestamp": log.timestamp.isoformat()
        }
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    finally:
        db.close()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=300  # Important for model inference
    )