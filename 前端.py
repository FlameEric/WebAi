import streamlit as st
import requests

# 页面选择（模拟页面路由）
st.set_page_config(page_title="AI智能文案图片生成器")
if "page" not in st.session_state:
    st.session_state.page = "登录"

# 页面切换函数
def switch_page(page_name):
    st.session_state.page = page_name

# 侧边栏导航
with st.sidebar:
    st.title("📄 页面导航")
    if st.session_state.page != "登录":
        st.button("🔐 登录", on_click=lambda: switch_page("登录"))
    if st.session_state.page != "注册":
        st.button("📝 注册", on_click=lambda: switch_page("注册"))
    if st.session_state.page != "文案生成":
        st.button("🎨 文案图片生成", on_click=lambda: switch_page("文案生成"))
    if st.session_state.page != "AI聊天":
        st.button("🤖 AI助手聊天", on_click=lambda: switch_page("AI聊天"))

# -------------------- 页面内容 ------------------------

# 登录页面
if st.session_state.page == "登录":
    st.title("🔐 登录")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        # 简单模拟验证
        if username == "admin" and password == "123456":
            st.success("登录成功！")
            switch_page("文案生成")
        else:
            st.error("用户名或密码错误")

# 注册页面
elif st.session_state.page == "注册":
    st.title("📝 注册")
    username = st.text_input("新用户名")
    password = st.text_input("新密码", type="password")
    confirm = st.text_input("确认密码", type="password")
    if st.button("注册"):
        if password != confirm:
            st.warning("两次密码不一致")
        elif username and password:
            st.success(f"用户 {username} 注册成功！")
            switch_page("登录")
        else:
            st.error("请填写完整信息")

# 文案图片生成功能页面
elif st.session_state.page == "文案生成":
    st.title("🎨 AI文案图片生成器")
    text_input = st.text_area("请输入你要生成图片的文案内容：", height=100)
    if st.button("生成图片"):
        # 示例调用后端接口（需要你后端支持）
        response = requests.post("http://127.0.0.1:8000/generate", json={"text": text_input})
        if response.status_code == 200:
            img_url = response.json().get("image_url")
            st.image(img_url, caption="生成结果")
        else:
            st.error("图片生成失败")

# AI聊天页面
elif st.session_state.page == "AI聊天":
    st.title("🤖 AI助手聊天界面")

    with st.sidebar:
        st.subheader("参数设置")
        sys_prompt = st.text_input("系统提示词", value="你是一个聪明的助手")
        history_len = st.slider("历史对话轮数", 1, 10, 3)
        temperature = st.slider("温度", 0.01, 1.0, 0.5, 0.01)
        top_p = st.slider("top_p", 0.01, 1.0, 0.5, 0.01)
        max_tokens = st.slider("最大Token数", 64, 4096, 512)
        stream = st.checkbox("流式输出", value=True)
        if st.button("清空聊天记录"):
            st.session_state.history = []

    if "history" not in st.session_state:
        st.session_state.history = []

    for dic in st.session_state.history:
        st.chat_message(dic["role"]).markdown(dic["content"])

    if input := st.chat_input("请输入问题开始聊天..."):
        st.session_state.history.append({"role": "user", "content": input})
        with st.chat_message("user"):
            st.markdown(input)

        # 后端对话接口
        backend_url = "http://127.0.0.1:8000/chat"
        data = {
            "query": input,
            "sys_prompt": sys_prompt,
            "history": st.session_state.history[-history_len:],  # 控制长度
            "history_len": history_len,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens
        }

        response = requests.post(backend_url, json=data, stream=True)
        ai_placeholder = st.chat_message("assistant")
        ai_text = ai_placeholder.markdown("")
        chunks = ""
        if response.status_code == 200:
            if stream:
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    chunks += chunk
                    ai_text.markdown(chunks)
            else:
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    chunks += chunk
                ai_text.markdown(chunks)
            st.session_state.history.append({"role": "assistant", "content": chunks})
        else:
            st.error("请求失败")
