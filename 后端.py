from fastapi import FastAPI, Body
from typing import List
from openai import AsyncOpenAI      # 安装openai库
from fastapi.responses import StreamingResponse
import requests  # 用于图片生成API的请求

# 初始化openAI的客户端
aclient = AsyncOpenAI(
    api_key="sk-ewdmpwshnxrruamvtuhhciedifmrjynsckrjurnjnaxzquue",  # 填写你自己的API密钥
    base_url="https://api.openai.com/v1"  # 根据你使用的API调整URL
)

# 初始化会话历史列表
message = []

# 初始化FastAPI应用
app = FastAPI()

# 为根路径添加路由
@app.get("/")
async def root():
    return {"message": "欢迎来到我的聊天机器人和图片生成系统，请使用/chat开启聊天，/generate_image生成图片"}

# 为/chat添加路由（聊天功能）
@app.post("/chat")
async def chat(query: str = Body(..., description="用户输入"),
               sys_prompt: str = Body("你是一个有用的助手", description="系统提示词"),
               history: List = Body([], description="历史对话"),
               history_len: int = Body(1, description="保留历史对话的轮数"),
               temperature: float = Body(0.5, description="LLM采样温度"),
               top_p: float = Body(0.5, description="LLM采样概率"),
               max_tokens: int = Body(None, description="LLM最大token数量")
               ):
    global message
    if history_len > 0:
        history = history[-2 * history_len:]

    message.clear()
    message.append({"role": "system", "content": sys_prompt})
    message.extend(history)
    message.append({"role": "user", "content": query})

    # 接收到前端传来的参数，向大模型发起请求
    response = await aclient.chat.completions.create(
        model="Qwen/Qwen3-8B",  # 使用你想要的GPT模型
        messages=message,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True
    )

    # 开启流式输出后，需要响应流式输出
    async def generate_response():
        async for chunk in response:
            chunk_msg = chunk.choices[0].delta.content
            if chunk_msg:
                yield chunk_msg

    # 以文本形式，流式输出大模型回复
    return StreamingResponse(generate_response(), media_type="text/plain")


# 为/generate_image添加路由（图片生成功能）
@app.post("/generate_image")
async def generate_image(prompt: str = Body(..., description="生成图片的文案")):
    # 使用DALL·E或其他图像生成API生成图片
    # 以下是一个使用OpenAI API调用DALL·E生成图片的例子，你可以根据自己的需求进行调整
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers={"Authorization": "Bearer sk-your-api-key-here"},
            json={
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024"
            }
        )
        response_data = response.json()
        image_url = response_data['data'][0]['url']
        return {"image_url": image_url}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
