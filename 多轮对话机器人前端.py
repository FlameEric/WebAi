import requests
import streamlit as st

st.title("🐋多轮对话聊天机器人")

# 设置侧边栏
# with 上下文管理器，主要用于资源管理，确保资源在使用后被正确释放
# 一般在文件读写中  with open() as f:   不管文件操作是否正确 最后都会正确关闭文件
with st.sidebar:
    st.title("Chatbot")
    sys_prompt = st.text_input("系统提示词", value="你是一个非常可爱的助手")
    history_len = st.slider("历史对话保留轮数", 1, 10, 3)
    temperature = st.slider("LLM采样温度", 0.01, 1.0, 0.5, 0.01)
    top_p = st.slider("LLM采样概率", 0.01, 1.0, 0.5, 0.01)
    max_tokens = st.slider("LLM最大token数量", 64, 4096, 512)
    stream = st.checkbox("是否流式输出", value=True)
    st.button("清空历史信息")


if 'history' not in st.session_state:
    st.session_state.history = []

for dic in st.session_state.history:
    st.chat_message(dic["role"]).markdown(dic["content"])

# 配置主页聊天框
if input := st.chat_input("来和我聊天吧"):
    st.session_state.history.append({"role":"user", "content":input})
    with st.chat_message("user"):
        st.markdown(input)

    # 向后端发起请求
    backend_url = " http://127.0.0.1:8000/chat"
    data = {
        "query": input,
        "sys_prompt": sys_prompt,
        "history": st.session_state.history,
        "history_len": history_len,
        "temperature":temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }
    response = requests.post(backend_url, json=data, stream=True)

    # 对请求的结果进行判断
    if response.status_code == 200:
        # 因为要响应流式输出，所以我先使用占位符占位，再一点点码字
        ai_placeholder = st.chat_message("assistant")
        ai_text = ai_placeholder.markdown("")
        chunks = ""
        if stream:
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                chunks += chunk
                ai_text.markdown(chunks)
        else:
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                chunks += chunk
            ai_text.markdown(chunks)

        # 存储ai信息到历史信息列表中
        st.session_state.history.append({"role":"assistant", "content":chunks})
    else:
        st.error("请求失败")
