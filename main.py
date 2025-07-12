from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cozepy import Coze, TokenAuth, Stream, WorkflowEvent, WorkflowEventType, COZE_CN_BASE_URL
import json

app = FastAPI()

# CORS 跨域支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求体模型
class PromptRequest(BaseModel):
    prompt: str
    style: str = ""
    size: str = "medium"

# 🧠 请替换为你自己的 token 和 workflow ID
COZE_API_TOKEN = "cztei_q3kDZqtvYl4GTO4HBo27u6t5PbZnxyboGdhkI9G6K6oVGY63Mfsei9xPxzGOTrEaH"
WORKFLOW_ID = "7523050470983663631"

# 初始化客户端
coze = Coze(auth=TokenAuth(token=COZE_API_TOKEN), base_url=COZE_CN_BASE_URL)

@app.post("/generate-image")
async def generate_image(req: PromptRequest):
    try:
        # 构造提示词
        enhanced_prompt = f"{req.style + ': ' if req.style else ''}{req.prompt}. 高清，细节丰富，视觉吸引力强"
        print("✨ 调用 Prompt:", enhanced_prompt)

        # 发起 Coze 工作流调用（流式）
        stream = coze.workflows.runs.stream(
            workflow_id=WORKFLOW_ID,
            parameters={"input": enhanced_prompt}
        )

        for event in stream:
            print("📨 收到事件：", event.event)
            if event.event == WorkflowEventType.MESSAGE:
                # 安全获取 content 内容（字符串形式）
                content = (
                    event.message.get("content")
                    if isinstance(event.message, dict)
                    else getattr(event.message, "content", None)
                )
                print("📦 message content:", content)

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
                        print("❌ JSON解析失败:", e)

            elif event.event == WorkflowEventType.ERROR:
                print("❌ 工作流报错:", event.error)
                return {"success": False, "error": event.error.message}

            elif event.event == WorkflowEventType.INTERRUPT:
                # 自动 resume
                stream = coze.workflows.runs.resume(
                    workflow_id=WORKFLOW_ID,
                    event_id=event.interrupt.interrupt_data.event_id,
                    resume_data="继续",
                    interrupt_type=event.interrupt.interrupt_data.type,
                )
                return await generate_image(req)

        # 如果没有任何消息事件带输出
        return {
            "success": False,
            "error": "未能获取图片链接"
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

# ✅ 本地运行入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
