from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from cozepy import Coze, TokenAuth, Stream, WorkflowEvent, WorkflowEventType, COZE_CN_BASE_URL
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from passlib.hash import bcrypt
from openai import AsyncOpenAI
from typing import List
import json
import traceback

# ---------------------- FastAPI 初始化 ----------------------
app = FastAPI()

# ---------------------- CORS 配置 ----------------------
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

# ---------------------- Coze 图像生成配置 ----------------------
COZE_API_TOKEN = "cztei_qnlW1gt55C2Nj3eBUr3nLB0HO0TL00TMEkSmcW76QKAdJKTb3h0Xjv4O8bpFbTtOs"

WORKFLOW_ID = "7523050470983663631"
coze = Coze(auth=TokenAuth(token=COZE_API_TOKEN), base_url=COZE_CN_BASE_URL)

# ---------------------- OpenAI 聊天模型配置 ----------------------
aclient = AsyncOpenAI(
    api_key="sk-ewdmpwshnxrruamvtuhhciedifmrjynsckrjurnjnaxzquue",
    base_url="https://api.siliconflow.cn/v1"
)
message = []

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
    return {"success": True, "message": "登录成功", "username": db_user.username}

# ---------------------- 图像生成接口 ----------------------
@app.post("/generate-image")
async def generate_image(req: PromptRequest):
    try:
        enhanced_prompt = f"{req.style + ': ' if req.style else ''}{req.prompt}. 高清，细节丰富，视觉吸引力强"
        stream = coze.workflows.runs.stream(
            workflow_id=WORKFLOW_ID,
            parameters={"input": enhanced_prompt}
        )

        for event in stream:
            if event.event == WorkflowEventType.MESSAGE:
                content = (
                    event.message.get("content")
                    if isinstance(event.message, dict)
                    else getattr(event.message, "content", None)
                )
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
        traceback.print_exc()
        return {"success": False, "error": str(e)}

# ---------------------- 聊天接口 ----------------------
@app.post("/chat")
async def chat(query: str = Body(...),
               sys_prompt: str = Body("你是一个有用的助手"),
               history: List = Body([], description="历史对话"),
               history_len: int = Body(1),
               temperature: float = Body(0.5),
               top_p: float = Body(0.5),
               max_tokens: int = Body(None)):

    global message
    message.clear()
    message.append({"role": "system", "content": sys_prompt})
    message.extend(history[-2 * history_len:])
    message.append({"role": "user", "content": query})

    response = await aclient.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=message,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True
    )

    async def generate_response():
        async for chunk in response:
            chunk_msg = chunk.choices[0].delta.content
            if chunk_msg:
                yield chunk_msg

    return StreamingResponse(generate_response(), media_type="text/plain")

# ---------------------- 启动 ----------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
