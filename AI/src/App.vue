<template>
  <div class="app">
    <!-- 登录页面 -->
    <div v-if="currentPage === 'login'" class="page-container">
      <div class="auth-container">
        <div class="auth-card">
          <div class="auth-header">
            <h1 class="auth-title">🎨 AI 图像生成器</h1>
            <p class="auth-subtitle">登录您的账户</p>
          </div>

          <form @submit.prevent="handleLogin" class="auth-form">
            <div class="form-group">
              <label class="label">邮箱</label>
              <input
                v-model="loginForm.email"
                type="email"
                placeholder="请输入您的邮箱"
                class="input"
                required
              />
            </div>

            <div class="form-group">
              <label class="label">密码</label>
              <input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入您的密码"
                class="input"
                required
              />
            </div>

            <button type="submit" class="auth-btn" :disabled="loginLoading">
              <span v-if="!loginLoading">🚀 登录</span>
              <span v-else class="loading-text">
                <span class="spinner"></span>
                登录中...
              </span>
            </button>
          </form>

          <div class="auth-footer">
            <p>还没有账户？
              <button @click="currentPage = 'register'" class="link-btn">立即注册</button>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 注册页面 -->
    <div v-if="currentPage === 'register'" class="page-container">
      <div class="auth-container">
        <div class="auth-card">
          <div class="auth-header">
            <h1 class="auth-title">🎨 AI 图像生成器</h1>
            <p class="auth-subtitle">创建新账户</p>
          </div>

          <form @submit.prevent="handleRegister" class="auth-form">
            <div class="form-group">
              <label class="label">用户名</label>
              <input
                v-model="registerForm.username"
                type="text"
                placeholder="请输入用户名"
                class="input"
                required
              />
            </div>

            <div class="form-group">
              <label class="label">邮箱</label>
              <input
                v-model="registerForm.email"
                type="email"
                placeholder="请输入您的邮箱"
                class="input"
                required
              />
            </div>

            <div class="form-group">
              <label class="label">密码</label>
              <input
                v-model="registerForm.password"
                type="password"
                placeholder="请输入密码（至少6位）"
                class="input"
                required
                minlength="6"
              />
            </div>

            <div class="form-group">
              <label class="label">确认密码</label>
              <input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="请再次输入密码"
                class="input"
                required
              />
            </div>

            <button type="submit" class="auth-btn" :disabled="registerLoading">
              <span v-if="!registerLoading">✨ 注册</span>
              <span v-else class="loading-text">
                <span class="spinner"></span>
                注册中...
              </span>
            </button>
          </form>

          <div class="auth-footer">
            <p>已有账户？
              <button @click="currentPage = 'login'" class="link-btn">立即登录</button>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 主应用页面 -->
    <div v-if="currentPage === 'main'" class="main-app">
      <!-- 顶部导航栏 -->
      <header class="navbar">
        <div class="nav-container">
          <div class="nav-left">
            <h1 class="nav-title">🎨 AI 创作助手</h1>
            <!-- 功能切换标签 -->
            <div class="nav-tabs">
              <button
                @click="activeTab = 'image'"
                class="nav-tab"
                :class="{ active: activeTab === 'image' }"
              >
                🖼️ 图像生成
              </button>
              <button
                @click="activeTab = 'chat'"
                class="nav-tab"
                :class="{ active: activeTab === 'chat' }"
              >
                💬 AI 聊天
              </button>
            </div>
          </div>
          <div class="nav-right">
            <span class="user-info">欢迎，{{ currentUser.username }}</span>
            <button @click="handleLogout" class="logout-btn">退出登录</button>
          </div>
        </div>
      </header>

      <!-- 图像生成模块 -->
      <main v-if="activeTab === 'image'" class="main-content">
        <div class="content-container">
          <!-- 左侧控制面板 -->
          <div class="control-panel">
            <div class="panel-card">
              <h2 class="panel-title">创作设置</h2>

              <form @submit.prevent="generateImage" class="generator-form">
                <div class="form-group">
                  <label class="label">
                    <span class="icon">✨</span>
                    提示词 Prompt
                  </label>
                  <textarea
                    v-model="prompt"
                    placeholder="请详细描述你想生成的图像内容..."
                    class="textarea"
                    rows="4"
                  ></textarea>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label class="label">
                      <span class="icon">🎭</span>
                      风格 Style
                    </label>
                    <select v-model="style" class="select">
                      <option value="">无风格</option>
                      <option>油画风</option>
                      <option>赛博朋克</option>
                      <option>像素艺术</option>
                      <option>未来感</option>
                      <option>水彩画</option>
                      <option>素描风</option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label class="label">
                      <span class="icon">📐</span>
                      尺寸 Size
                    </label>
                    <select v-model="size" class="select">
                      <option value="small">256x256 (小)</option>
                      <option value="medium">512x512 (中)</option>
                      <option value="large">1024x1024 (大)</option>
                    </select>
                  </div>
                </div>

                <button
                  type="submit"
                  :disabled="loading || !prompt.trim()"
                  class="generate-btn"
                  :class="{ 'loading': loading, 'disabled': !prompt.trim() }"
                >
                  <span v-if="!loading">🚀 生成图片</span>
                  <span v-else class="loading-text">
                    <span class="spinner"></span>
                    AI创作中...
                  </span>
                </button>
              </form>
            </div>

            <!-- 历史记录 -->
            <div class="panel-card" v-if="imageHistory.length > 0">
              <h3 class="panel-subtitle">创作历史</h3>
              <div class="history-grid">
                <div
                  v-for="(item, index) in imageHistory.slice(0, 6)"
                  :key="index"
                  class="history-item"
                  @click="selectHistoryImage(item)"
                >
                  <img :src="item.url" :alt="item.prompt" class="history-image" />
                </div>
              </div>
            </div>
          </div>

          <!-- 右侧结果展示区域 -->
          <div class="result-panel">
            <!-- 加载状态 -->
            <div v-if="loading" class="loading-display">
              <div class="loading-animation">
                <div class="loading-spinner">
                  <div class="spinner-ring"></div>
                  <div class="spinner-emoji">🎨</div>
                </div>
                <h3 class="loading-title">AI正在创作中...</h3>
                <p class="loading-desc">请稍候，这可能需要几秒钟时间</p>
                <div class="progress-bar">
                  <div class="progress-fill"></div>
                </div>
              </div>
            </div>

            <!-- 结果展示 -->
            <div v-else-if="imageUrl" class="result-display">
              <div class="result-header">
                <h2 class="result-title">✅ 创作完成！</h2>
                <p class="result-prompt">{{ currentPrompt }}</p>
              </div>

              <div class="image-showcase">
                <img
                  :src="imageUrl"
                  alt="AI生成图像"
                  class="showcase-image"
                />
                <div class="image-overlay">
                  <div class="overlay-actions">
                    <button @click="downloadImage" class="overlay-btn">
                      📥 下载
                    </button>
                    <button @click="shareImage" class="overlay-btn">
                      🔗 分享
                    </button>
                    <button @click="saveToHistory" class="overlay-btn">
                      💾 保存
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 默认状态 -->
            <div v-else class="empty-state">
              <div class="empty-content">
                <div class="empty-icon">🎨</div>
                <h3 class="empty-title">开始你的AI创作之旅</h3>
                <p class="empty-desc">在左侧输入提示词，让AI为你创造独特的艺术作品</p>
                <div class="example-prompts">
                  <p class="example-title">试试这些提示词：</p>
                  <div class="example-tags">
                    <button
                      v-for="example in examplePrompts"
                      :key="example"
                      @click="prompt = example"
                      class="example-tag"
                    >
                      {{ example }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- AI聊天模块 -->
      <main v-if="activeTab === 'chat'" class="chat-main">
        <div class="chat-container">
          <!-- 聊天侧边栏 -->
          <div class="chat-sidebar">
            <div class="sidebar-header">
              <h3 class="sidebar-title">💬 对话历史</h3>
              <button @click="startNewChat" class="new-chat-btn">
                ➕ 新对话
              </button>
            </div>

            <div class="chat-list">
              <div
                v-for="(chat, index) in chatHistory"
                :key="index"
                @click="selectChat(index)"
                class="chat-item"
                :class="{ active: currentChatIndex === index }"
              >
                <div class="chat-preview">
                  <div class="chat-title">{{ chat.title || '新对话' }}</div>
                  <div class="chat-time">{{ formatTime(chat.timestamp) }}</div>
                </div>
                <button @click.stop="deleteChat(index)" class="delete-chat-btn">
                  🗑️
                </button>
              </div>
            </div>

            <!-- 聊天设置 -->
            <div class="chat-settings">
              <h4 class="settings-title">🤖 AI 设置</h4>
              <div class="setting-group">
                <label class="setting-label">AI 角色</label>
                <select v-model="aiRole" class="setting-select">
                  <option value="assistant">智能助手</option>
                  <option value="creative">创意伙伴</option>
                  <option value="teacher">知识导师</option>
                  <option value="friend">聊天朋友</option>
                </select>
              </div>
              <div class="setting-group">
                <label class="setting-label">回复风格</label>
                <select v-model="responseStyle" class="setting-select">
                  <option value="balanced">平衡</option>
                  <option value="creative">创意</option>
                  <option value="precise">精确</option>
                </select>
              </div>

              <div class="setting-group">
                <label class="setting-label">创造性 (Temperature)</label>
                <input
                  v-model.number="chatSettings.temperature"
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  class="setting-range"
                />
                <span class="setting-value">{{ chatSettings.temperature }}</span>
              </div>

              <div class="setting-group">
                <label class="setting-label">多样性 (Top-p)</label>
                <input
                  v-model.number="chatSettings.topP"
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  class="setting-range"
                />
                <span class="setting-value">{{ chatSettings.topP }}</span>
              </div>

              <div class="setting-group">
                <label class="setting-label">历史长度</label>
                <select v-model="chatSettings.historyLength" class="setting-select">
                  <option value="1">1轮对话</option>
                  <option value="3">3轮对话</option>
                  <option value="5">5轮对话</option>
                  <option value="10">10轮对话</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 聊天主区域 -->
          <div class="chat-content">
            <!-- 聊天头部 -->
            <div class="chat-header">
              <div class="chat-info">
                <h2 class="chat-title">{{ getCurrentChatTitle() }}</h2>
                <p class="chat-subtitle">{{ getAiRoleDescription() }}</p>
              </div>
              <div class="chat-actions">
                <button @click="clearCurrentChat" class="action-btn">
                  🗑️ 清空对话
                </button>
                <button @click="exportChat" class="action-btn">
                  📤 导出对话
                </button>
              </div>
            </div>

            <!-- 消息列表 -->
            <div class="messages-container" ref="messagesContainer">
              <div class="messages-list">
                <!-- 欢迎消息 -->
                <div v-if="getCurrentMessages().length === 0" class="welcome-message">
                  <div class="welcome-content">
                    <div class="welcome-icon">🤖</div>
                    <h3 class="welcome-title">你好！我是你的AI助手</h3>
                    <p class="welcome-desc">我可以帮你解答问题、创意写作、学习辅导等。有什么我可以帮助你的吗？</p>
                    <div class="quick-questions">
                      <button
                        v-for="question in quickQuestions"
                        :key="question"
                        @click="sendMessage(question)"
                        class="quick-question-btn"
                      >
                        {{ question }}
                      </button>
                    </div>
                  </div>
                </div>

                <!-- 聊天消息 -->
                <div
                  v-for="(message, index) in getCurrentMessages()"
                  :key="index"
                  class="message"
                  :class="{ 'user-message': message.role === 'user', 'ai-message': message.role === 'assistant' }"
                >
                  <div class="message-avatar">
                    <span v-if="message.role === 'user'">👤</span>
                    <span v-else>🤖</span>
                  </div>
                  <div class="message-content">
                    <div class="message-text" v-html="formatMessage(message.content)"></div>
                    <div class="message-time">{{ formatMessageTime(message.timestamp) }}</div>
                  </div>
                  <div class="message-actions" v-if="message.role === 'assistant'">
                    <button @click="copyMessage(message.content)" class="message-action-btn" title="复制">
                      📋
                    </button>
                    <button @click="likeMessage(index)" class="message-action-btn" title="点赞">
                      👍
                    </button>
                  </div>
                </div>

                <!-- AI正在输入 -->
                <div v-if="chatLoading" class="message ai-message typing">
                  <div class="message-avatar">
                    <span>🤖</span>
                  </div>
                  <div class="message-content">
                    <div class="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 输入区域 -->
            <div class="chat-input-area">
              <div class="input-container">
                <textarea
                  v-model="chatInput"
                  @keydown="handleKeyDown"
                  placeholder="输入你的消息... (Shift+Enter换行，Enter发送)"
                  class="chat-input"
                  rows="1"
                  ref="chatInputRef"
                ></textarea>
                <div class="input-actions">
                  <button
                    @click="sendMessage()"
                    :disabled="!chatInput.trim() || chatLoading"
                    class="send-btn"
                  >
                    <span v-if="!chatLoading">🚀</span>
                    <span v-else class="spinner"></span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, onMounted } from 'vue'

// 页面状态
const currentPage = ref('login') // 'login', 'register', 'main'
const activeTab = ref('image') // 'image', 'chat'
const currentUser = ref({ username: '', email: '' })

// 登录表单
const loginForm = reactive({
  email: '',
  password: ''
})
const loginLoading = ref(false)

// 注册表单
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})
const registerLoading = ref(false)

// AI生成相关
const prompt = ref('')
const style = ref('')
const size = ref('medium')
const imageUrl = ref('')
const currentPrompt = ref('')
const loading = ref(false)
const error = ref('')
const imageHistory = ref([])

// 示例提示词
const examplePrompts = [
  '一只可爱的小猫在花园里玩耍',
  '未来城市的夜景，霓虹灯闪烁',
  '宁静的湖泊，倒映着夕阳',
  '神秘的森林，阳光透过树叶'
]

// AI聊天相关
const chatHistory = ref([])
const currentChatIndex = ref(-1)
const chatInput = ref('')
const chatLoading = ref(false)
const messagesContainer = ref(null)
const chatInputRef = ref(null)
const aiRole = ref('assistant')
const responseStyle = ref('balanced')

const chatSettings = reactive({
  temperature: 0.5,
  topP: 0.5,
  maxTokens: 2000,
  historyLength: 5
})

// 快速问题
const quickQuestions = [
  '你好，请介绍一下自己',
  '帮我写一首关于春天的诗',
  '解释一下人工智能的原理',
  '推荐几本好书给我'
]

// 登录处理
const handleLogin = async () => {
  if (loginForm.password.length < 6) {
    alert('密码至少需要6位字符')
    return
  }

  loginLoading.value = true

  // 模拟登录API调用
  setTimeout(() => {
    currentUser.value = {
      username: loginForm.email.split('@')[0],
      email: loginForm.email
    }
    currentPage.value = 'main'
    loginLoading.value = false

    // 初始化聊天
    initializeChat()

    // 清空表单
    loginForm.email = ''
    loginForm.password = ''
  }, 1500)
}

// 注册处理
const handleRegister = async () => {
  if (registerForm.password !== registerForm.confirmPassword) {
    alert('两次输入的密码不一致')
    return
  }

  if (registerForm.password.length < 6) {
    alert('密码至少需要6位字符')
    return
  }

  registerLoading.value = true

  // 模拟注册API调用
  setTimeout(() => {
    currentUser.value = {
      username: registerForm.username,
      email: registerForm.email
    }
    currentPage.value = 'main'
    registerLoading.value = false

    // 初始化聊天
    initializeChat()

    // 清空表单
    Object.keys(registerForm).forEach(key => {
      registerForm[key] = ''
    })
  }, 1500)
}

// 退出登录
const handleLogout = () => {
  currentUser.value = { username: '', email: '' }
  currentPage.value = 'login'
  activeTab.value = 'image'
  // 清空所有数据
  imageUrl.value = ''
  prompt.value = ''
  imageHistory.value = []
  chatHistory.value = []
  currentChatIndex.value = -1
}

// 图像生成相关函数
const generateImage = async () => {
  loading.value = true
  imageUrl.value = ''
  currentPrompt.value = prompt.value

  try {
    const res = await fetch("http://localhost:8000/generate-image", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt: prompt.value,
        style: style.value,
        size: size.value,
      }),
    });

    const data = await res.json();
    if (data.success) {
      imageUrl.value = data.imageUrl;
    } else {
      error.value = data.error || "生成失败";
      alert(error.value)
    }
  } catch (e) {
    error.value = "请求出错：" + e.message;
    alert(error.value)
  } finally {
    loading.value = false;
  }
}

const downloadImage = () => {
  const link = document.createElement('a')
  link.href = imageUrl.value
  link.download = `ai-image-${Date.now()}.png`
  link.click()
}

const shareImage = async () => {
  if (navigator.share) {
    try {
      await navigator.share({
        title: 'AI生成的图像',
        text: `看看我用AI生成的这张图片！提示词：${currentPrompt.value}`,
        url: imageUrl.value
      })
    } catch (err) {
      console.log('分享失败:', err)
    }
  } else {
    navigator.clipboard.writeText(imageUrl.value)
    alert('图片链接已复制到剪贴板！')
  }
}

const saveToHistory = () => {
  if (imageUrl.value && currentPrompt.value) {
    imageHistory.value.unshift({
      url: imageUrl.value,
      prompt: currentPrompt.value,
      style: style.value,
      size: size.value,
      timestamp: new Date().toLocaleString()
    })

    if (imageHistory.value.length > 20) {
      imageHistory.value = imageHistory.value.slice(0, 20)
    }

    alert('已保存到历史记录！')
  }
}

const selectHistoryImage = (item) => {
  imageUrl.value = item.url
  currentPrompt.value = item.prompt
  prompt.value = item.prompt
  style.value = item.style
  size.value = item.size
}

// AI聊天相关函数
const initializeChat = () => {
  if (chatHistory.value.length === 0) {
    startNewChat()
  }
}

const startNewChat = () => {
  const newChat = {
    id: Date.now(),
    title: '',
    messages: [],
    timestamp: new Date()
  }
  chatHistory.value.unshift(newChat)
  currentChatIndex.value = 0
}

const selectChat = (index) => {
  currentChatIndex.value = index
  nextTick(() => {
    scrollToBottom()
  })
}

const deleteChat = (index) => {
  if (confirm('确定要删除这个对话吗？')) {
    chatHistory.value.splice(index, 1)
    if (currentChatIndex.value === index) {
      currentChatIndex.value = chatHistory.value.length > 0 ? 0 : -1
    } else if (currentChatIndex.value > index) {
      currentChatIndex.value--
    }

    if (chatHistory.value.length === 0) {
      startNewChat()
    }
  }
}

const getCurrentMessages = () => {
  if (currentChatIndex.value >= 0 && chatHistory.value[currentChatIndex.value]) {
    return chatHistory.value[currentChatIndex.value].messages
  }
  return []
}

const getCurrentChatTitle = () => {
  if (currentChatIndex.value >= 0 && chatHistory.value[currentChatIndex.value]) {
    return chatHistory.value[currentChatIndex.value].title || '新对话'
  }
  return '新对话'
}

const getAiRoleDescription = () => {
  const descriptions = {
    assistant: '我是你的智能助手，可以帮你解答各种问题',
    creative: '我是你的创意伙伴，一起探索无限可能',
    teacher: '我是你的知识导师，帮你学习和成长',
    friend: '我是你的聊天朋友，随时陪你聊天'
  }
  return descriptions[aiRole.value] || descriptions.assistant
}

const sendMessage = async (message = null) => {
  const messageText = message || chatInput.value.trim()
  if (!messageText || chatLoading.value) return

  // 确保有当前对话
  if (currentChatIndex.value < 0) {
    startNewChat()
  }

  const currentChat = chatHistory.value[currentChatIndex.value]

  // 添加用户消息
  const userMessage = {
    role: 'user',
    content: messageText,
    timestamp: new Date()
  }
  currentChat.messages.push(userMessage)

  // 设置对话标题（如果是第一条消息）
  if (!currentChat.title && messageText.length > 0) {
    currentChat.title = messageText.length > 20 ? messageText.substring(0, 20) + '...' : messageText
  }

  chatInput.value = ''
  chatLoading.value = true

  nextTick(() => {
    scrollToBottom()
  })

  try {
    // 准备历史对话数据
    const history = currentChat.messages
      .filter(msg => msg.role !== 'system')
      .slice(-10) // 只取最近10条消息作为历史
      .map(msg => ({
        role: msg.role,
        content: msg.content
      }))

    // 获取系统提示词
    const systemPrompt = getSystemPrompt()

    // 调用后端API
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: messageText,
        sys_prompt: systemPrompt,
        history: history.slice(0, -1), // 排除当前用户消息
        history_len: Math.min(5, Math.floor(history.length / 2)), // 历史长度
        temperature: getTemperature(),
        top_p: getTopP(),
        max_tokens: 2000
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    // 创建AI消息对象
    const aiMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date()
    }
    currentChat.messages.push(aiMessage)

    // 处理流式响应
    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })
      aiMessage.content += chunk

      // 实时更新UI
      nextTick(() => {
        scrollToBottom()
      })
    }

    chatLoading.value = false

  } catch (error) {
    console.error('发送消息失败:', error)
    chatLoading.value = false

    // 添加错误消息
    const errorMessage = {
      role: 'assistant',
      content: '抱歉，我现在无法回复。请检查网络连接或稍后再试。',
      timestamp: new Date(),
      isError: true
    }
    currentChat.messages.push(errorMessage)

    nextTick(() => {
      scrollToBottom()
    })
  }
}

// 获取系统提示词
const getSystemPrompt = () => {
  const prompts = {
    assistant: '你是一个有用、准确、诚实的AI助手。请用中文回答问题，提供有帮助的信息。',
    creative: '你是一个富有创意的AI伙伴。请用富有想象力和创造性的方式回答问题，同时保持准确性。',
    teacher: '你是一个耐心的知识导师。请用教育性的方式回答问题，提供详细的解释和例子。',
    friend: '你是一个友好的聊天伙伴。请用轻松、友好的语气回答问题，就像和朋友聊天一样。'
  }
  return prompts[aiRole.value] || prompts.assistant
}

// 获取温度参数
const getTemperature = () => {
  return chatSettings.temperature
}

// 获取top_p参数
const getTopP = () => {
  return chatSettings.topP
}

const handleKeyDown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const clearCurrentChat = () => {
  if (confirm('确定要清空当前对话吗？')) {
    if (currentChatIndex.value >= 0) {
      chatHistory.value[currentChatIndex.value].messages = []
    }
  }
}

const exportChat = () => {
  if (currentChatIndex.value >= 0) {
    const chat = chatHistory.value[currentChatIndex.value]
    const chatText = chat.messages.map(msg =>
      `${msg.role === 'user' ? '用户' : 'AI'}: ${msg.content}`
    ).join('\n\n')

    const blob = new Blob([chatText], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `chat-${chat.title || 'conversation'}-${new Date().toISOString().split('T')[0]}.txt`
    link.click()
    URL.revokeObjectURL(url)
  }
}

const copyMessage = (content) => {
  navigator.clipboard.writeText(content)
  alert('消息已复制到剪贴板！')
}

const likeMessage = (index) => {
  // 这里可以实现点赞功能
  alert('感谢你的反馈！')
}

const formatMessage = (content) => {
  // 简单的消息格式化（支持换行）
  return content.replace(/\n/g, '<br>')
}

const formatTime = (timestamp) => {
  const now = new Date()
  const time = new Date(timestamp)
  const diff = now - time

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return time.toLocaleDateString()
}

const formatMessageTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 组件挂载时初始化
onMounted(() => {
  // 可以在这里加载用户数据
})
</script>

<style scoped>
/* 保持原有样式，添加新的聊天相关样式 */

/* 全局样式 */
* {
  box-sizing: border-box;
}

.app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
}

/* 页面容器 */
.page-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

/* 认证页面样式 */
.auth-container {
  width: 100%;
  max-width: 450px;
}

.auth-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-title {
  font-size: 2.2rem;
  font-weight: bold;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
}

.auth-subtitle {
  color: #666;
  font-size: 1.1rem;
  margin: 0;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 25px;
}

.auth-btn {
  padding: 15px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.auth-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.auth-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  color: #666;
}

.link-btn {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-weight: 600;
  text-decoration: underline;
}

.link-btn:hover {
  color: #764ba2;
}

/* 主应用样式 */
.main-app {
  min-height: 100vh;
  background: #f8fafc;
}

/* 导航栏 */
.navbar {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 0 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 30px;
}

.nav-title {
  font-size: 1.5rem;
  font-weight: bold;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.nav-tabs {
  display: flex;
  gap: 5px;
}

.nav-tab {
  padding: 8px 16px;
  background: none;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  color: #64748b;
  transition: all 0.2s;
}

.nav-tab:hover {
  background: #f1f5f9;
  color: #334155;
}

.nav-tab.active {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  color: #64748b;
  font-weight: 500;
}

.logout-btn {
  padding: 8px 16px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #dc2626;
}

/* 图像生成模块样式（保持原有样式） */
.main-content {
  padding: 30px 20px;
}

.content-container {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 30px;
  min-height: calc(100vh - 130px);
}

.control-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel-card {
  background: white;
  border-radius: 16px;
  padding: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.panel-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 20px;
  margin-top: 0;
}

.panel-subtitle {
  font-size: 1.1rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 15px;
  margin-top: 0;
}

.generator-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #374151;
  font-size: 0.95rem;
}

.icon {
  font-size: 1.1rem;
}

.input, .select, .textarea {
  padding: 12px 15px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: white;
}

.input:focus, .select:focus, .textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.textarea {
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
}

.generate-btn {
  padding: 15px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.generate-btn:hover:not(.disabled):not(.loading) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.generate-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.history-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.history-item {
  aspect-ratio: 1;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}

.history-item:hover {
  transform: scale(1.05);
}

.history-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.result-panel {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.loading-display {
  text-align: center;
  padding: 60px 40px;
}

.loading-animation {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 25px;
}

.loading-spinner {
  position: relative;
  width: 100px;
  height: 100px;
}

.spinner-ring {
  width: 100px;
  height: 100px;
  border: 6px solid #f1f5f9;
  border-top: 6px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner-emoji {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 2.5rem;
}

.loading-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.loading-desc {
  color: #64748b;
  margin: 0;
}

.progress-bar {
  width: 200px;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(45deg, #667eea, #764ba2);
  animation: progress 2s ease-in-out infinite;
}

.result-display {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.result-header {
  padding: 25px 25px 0;
  text-align: center;
}

.result-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #059669;
  margin-bottom: 8px;
  margin-top: 0;
}

.result-prompt {
  color: #64748b;
  margin: 0;
  font-style: italic;
}

.image-showcase {
  flex: 1;
  padding: 20px 25px 25px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.showcase-image {
  max-width: 100%;
  max-height: 100%;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
}

.image-overlay {
  position: absolute;
  top: 20px;
  left: 25px;
  right: 25px;
  bottom: 25px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-showcase:hover .image-overlay {
  opacity: 1;
}

.overlay-actions {
  display: flex;
  gap: 15px;
}

.overlay-btn {
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.9);
  color: #1e293b;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.overlay-btn:hover {
  background: white;
  transform: translateY(-2px);
}

.empty-state {
  text-align: center;
  padding: 80px 40px;
}

.empty-content {
  max-width: 400px;
  margin: 0 auto;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 10px;
  margin-top: 0;
}

.empty-desc {
  color: #64748b;
  margin-bottom: 30px;
  line-height: 1.6;
}

.example-prompts {
  text-align: left;
}

.example-title {
  font-weight: 600;
  color: #374151;
  margin-bottom: 15px;
}

.example-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.example-tag {
  padding: 8px 12px;
  background: #f1f5f9;
  color: #475569;
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.example-tag:hover {
  background: #e2e8f0;
  color: #1e293b;
}

/* AI聊天模块样式 */
.chat-main {
  height: calc(100vh - 70px);
  padding: 20px;
}

.chat-container {
  max-width: 1400px;
  margin: 0 auto;
  height: 100%;
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 20px;
}

/* 聊天侧边栏 */
.chat-sidebar {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.new-chat-btn {
  padding: 6px 12px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.new-chat-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.chat-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 5px;
}

.chat-item:hover {
  background: #f8fafc;
}

.chat-item.active {
  background: #e0e7ff;
  border-left: 3px solid #667eea;
}

.chat-preview {
  flex: 1;
  min-width: 0;
}

.chat-title {
  font-weight: 500;
  color: #1e293b;
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 2px;
}

.chat-time {
  font-size: 0.8rem;
  color: #64748b;
}

.delete-chat-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  opacity: 0;
  transition: all 0.2s;
}

.chat-item:hover .delete-chat-btn {
  opacity: 1;
}

.delete-chat-btn:hover {
  background: #fee2e2;
}

.chat-settings {
  padding: 20px;
  border-top: 1px solid #e2e8f0;
}

.settings-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 15px;
  margin-top: 0;
}

.setting-group {
  margin-bottom: 15px;
  position: relative;
}

.setting-label {
  display: block;
  font-size: 0.9rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 5px;
}

.setting-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9rem;
  background: white;
}

/* 聊天主区域 */
.chat-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chat-info h2 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
  margin-top: 0;
}

.chat-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
}

.chat-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  padding: 8px 12px;
  background: #f8fafc;
  color: #475569;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

/* 消息区域 */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.welcome-message {
  text-align: center;
  padding: 40px 20px;
}

.welcome-content {
  max-width: 500px;
  margin: 0 auto;
}

.welcome-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.welcome-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 10px;
  margin-top: 0;
}

.welcome-desc {
  color: #64748b;
  margin-bottom: 30px;
  line-height: 1.6;
}

.quick-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.quick-question-btn {
  padding: 10px 16px;
  background: #f8fafc;
  color: #475569;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-question-btn:hover {
  background: #e2e8f0;
  color: #1e293b;
}

/* 消息样式 */
.message {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.user-message .message-avatar {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
}

.message-content {
  flex: 1;
  max-width: 70%;
}

.user-message .message-content {
  text-align: right;
}

.message-text {
  background: #f8fafc;
  padding: 12px 16px;
  border-radius: 16px;
  line-height: 1.5;
  color: #1e293b;
}

.user-message .message-text {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
}

.message-time {
  font-size: 0.8rem;
  color: #94a3b8;
  margin-top: 4px;
}

.message-actions {
  display: flex;
  gap: 5px;
  margin-top: 5px;
  opacity: 0;
  transition: opacity 0.2s;
}

.message:hover .message-actions {
  opacity: 1;
}

.message-action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.message-action-btn:hover {
  background: #f1f5f9;
}

/* 正在输入动画 */
.typing .message-text {
  padding: 16px 20px;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  align-items: center;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #94a3b8;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

/* 输入区域 */
.chat-input-area {
  padding: 20px;
  border-top: 1px solid #e2e8f0;
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.chat-input {
  flex: 1;
  min-height: 44px;
  max-height: 120px;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  font-family: inherit;
  resize: none;
  transition: all 0.2s ease;
}

.chat-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-actions {
  display: flex;
  align-items: flex-end;
}

.send-btn {
  width: 44px;
  height: 44px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 通用样式 */
.loading-text {
  display: flex;
  align-items: center;
  gap: 10px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 动画 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes progress {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(0%); }
  100% { transform: translateX(100%); }
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .content-container {
    grid-template-columns: 350px 1fr;
    gap: 20px;
  }

  .chat-container {
    grid-template-columns: 280px 1fr;
  }
}

@media (max-width: 968px) {
  .nav-left {
    gap: 15px;
  }

  .nav-tabs {
    display: none;
  }

  .content-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .control-panel {
    order: 2;
  }

  .result-panel {
    order: 1;
    min-height: 400px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .nav-container {
    padding: 0 15px;
  }

  .main-content {
    padding: 20px 15px;
  }

  .chat-container {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .chat-sidebar {
    order: 2;
    height: auto;
  }

  .chat-content {
    order: 1;
    height: 60vh;
  }
}

@media (max-width: 640px) {
  .auth-card {
    padding: 30px 25px;
  }

  .overlay-actions {
    flex-direction: column;
  }

  .history-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .chat-main {
    padding: 15px;
  }

  .chat-container {
    gap: 10px;
  }

  .sidebar-header {
    padding: 15px;
  }

  .chat-header {
    padding: 15px;
  }

  .messages-container {
    padding: 15px;
  }

  .chat-input-area {
    padding: 15px;
  }

  .quick-questions {
    flex-direction: column;
  }

  .quick-question-btn {
    width: 100%;
    text-align: center;
  }

  .message-content {
    max-width: 85%;
  }

  .chat-actions {
    flex-direction: column;
    gap: 5px;
  }

  .action-btn {
    font-size: 0.8rem;
    padding: 6px 10px;
  }
}

.setting-range {
  width: 100%;
  margin: 5px 0;
}

.setting-value {
  font-size: 0.8rem;
  color: #64748b;
  float: right;
}

.setting-group {
  margin-bottom: 15px;
  position: relative;
}
</style>