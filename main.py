from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cozepy import Coze, TokenAuth, Stream, WorkflowEvent, WorkflowEventType, COZE_CN_BASE_URL
import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from passlib.hash import bcrypt

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------- 数据库配置 ----------------------
DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

# ---------------------- 数据模型 ----------------------
class PromptRequest(BaseModel):
    prompt: str
    style: str = ""
    size: str = "medium"

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# ---------------------- Coze 配置 ----------------------
COZE_API_TOKEN = "cztei_q3kDZqtvYl4GTO4HBo27u6t5PbZnxyboGdhkI9G6K6oVGY63Mfsei9xPxzGOTrEaH"
WORKFLOW_ID = "7523050470983663631"
coze = Coze(auth=TokenAuth(token=COZE_API_TOKEN), base_url=COZE_CN_BASE_URL)

# ---------------------- 注册接口 ----------------------
@app.post("/register")
def register(user: RegisterRequest):
    db = SessionLocal()
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="邮箱已注册")
    hashed_pwd = bcrypt.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pwd)
    db.add(db_user)
    db.commit()
    return {"success": True, "message": "注册成功"}

# ---------------------- 登录接口 ----------------------
@app.post("/login")
def login(user: LoginRequest):
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not bcrypt.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    return {"success": True, "message": "登录成功", "user": {"id": db_user.id, "username": db_user.username}}

# ---------------------- 图像生成接口 ----------------------
@app.post("/generate-image")
async def generate_image(req: PromptRequest):
    try:
        enhanced_prompt = f"{req.style + ': ' if req.style else ''}{req.prompt}. 高清，细节丰富，视觉吸引力强"
        print("\u2728 Prompt:", enhanced_prompt)

        stream = coze.workflows.runs.stream(
            workflow_id=WORKFLOW_ID,
            parameters={"input": enhanced_prompt}
        )

        for event in stream:
            print("\ud83d\udce8 事件：", event.event)
            if event.event == WorkflowEventType.MESSAGE:
                content = (
                    event.message.get("content")
                    if isinstance(event.message, dict)
                    else getattr(event.message, "content", None)
                )
                print("\ud83d\udce6 content:", content)

                if content:
                    try:
                        parsed = json.loads(content)
                        image_url = parsed.get("output")
                        if image_url:
                            return {
                                "success": True,
                                "imageUrl": image_url,
                                "prompt": enhanced_prompt
                            }
                    except Exception as e:
                        print("\u274c JSON解析失败:", e)

            elif event.event == WorkflowEventType.ERROR:
                print("\u274c 错误:", event.error)
                return {"success": False, "error": event.error.message}

            elif event.event == WorkflowEventType.INTERRUPT:
                stream = coze.workflows.runs.resume(
                    workflow_id=WORKFLOW_ID,
                    event_id=event.interrupt.interrupt_data.event_id,
                    resume_data="继续",
                    interrupt_type=event.interrupt.interrupt_data.type,
                )
                return await generate_image(req)

        return {"success": False, "error": "未能获取图片链接"}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

# ---------------------- 启动 ----------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
