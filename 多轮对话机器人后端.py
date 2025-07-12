from fastapi import FastAPI, Body
from typing import List
from openai import AsyncOpenAI      # 没有openai的同学安装一下
from fastapi.responses import StreamingResponse

# 初始化openAI的客户端
aclient = AsyncOpenAI(
    api_key="sk-ewdmpwshnxrruamvtuhhciedifmrjynsckrjurnjnaxzquue",
    base_url="https://api.siliconflow.cn/v1"
)

# 初始化会话历史列表
message = []

# 初始化FastAPI应用
app = FastAPI()

# 为根路径添加路由
@app.get("/")
async def root():
    return {"message": "欢迎来到我的聊天机器人系统，请使用/chat开启聊天"}

# 为/chat添加路由
"""
FastAPI默认会将路径参数或查询参数 作为函数的参数
http://127.0.0.1/8000/name=swy?pwd=123456
但是在前端我们使用requests库请求的时候，发送的是JSON数据，
所以在这里我们接收参数需要使用Body来接收。
"""
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
    # 根据历史会话的保留长度，决定history的内容
    if history_len > 0:
        history = history[-2 * history_len:]    # 利用切片从总会话历史中，截取指定长度

    # 将历史会话放到message列表中，作为参数传给大模型
    message.clear()
    # message.append(("system", sys_prompt))
    message.append({"role": "system", "content":sys_prompt})
    message.extend(history)
    message.append({"role": "user", "content":query})
    """
    在openAI中 身份 system 和 user
    在langchain框架下 身份 可以是system ai  assistant  和 user human
    """

    # 接收到前端传来的参数，向大模型发起请求
    response = await aclient.chat.completions.create(
        model="Qwen/Qwen3-8B",
        messages=message,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True     # 开启流式输出
    )

    # 开启流式输出后，需要响应流式输出
    async def generate_response():
        async for chunk in response:
            # 按块提取 大模型的回复内容
            chunk_msg = chunk.choices[0].delta.content
            if chunk_msg:
                yield chunk_msg
    # 以文本形式，流式输出大模型回复
    return StreamingResponse(generate_response(), media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    """
    有三种特殊的IP地址
    localhost       本机
    127.0.0.1       本机
    0.0.0.0         本机 也可以 外部计算机访问
    """
    uvicorn.run(app)


"""
多轮对话，保留历史信息
用户：你是谁？
AI： 我是豆包
用户：你能做什么？
AI： 我什么都可以
用户：我上个问题问的是什么？
AI： 你问的的问题是 “你能做什么？”

在前天讲到的COZE对话流中，你见到的 会话历史 就是这块内容

将用户输入 和 会话历史 同时交给大模型处理的优点是什么？
会话历史是不是都要保存？都传给大模型？有几种策略？
1. 都保存   token受不了
2. 指定轮数 例如：只将最近的3轮、5轮对话传给大模型
3. 模型总结历史信息，将总结的历史信息 和 用户输入再传给大模型
"""