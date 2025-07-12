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
            <h1 class="nav-title">🎨 AI 图像生成器</h1>
          </div>
          <div class="nav-right">
            <span class="user-info">欢迎，{{ currentUser.username }}</span>
            <button @click="handleLogout" class="logout-btn">退出登录</button>
          </div>
        </div>
      </header>

      <!-- 主内容区域 -->
      <main class="main-content">
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
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

// 页面状态
const currentPage = ref('login') // 'login', 'register', 'main'
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

// 登录处理
const handleLogin = async () => {
  if (loginForm.password.length < 6) {
    alert("密码至少需要6位字符");
    return;
  }

  loginLoading.value = true;

  try {
    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email: loginForm.email,
        password: loginForm.password
      })
    });

    const data = await res.json();
    if (data.success) {
      currentUser.value = {
        username: data.username,
        email: loginForm.email
      };
      currentPage.value = "main";
      loginForm.email = "";
      loginForm.password = "";
    } else {
      alert(data.error || "登录失败");
    }
  } catch (err) {
    alert("登录请求失败：" + err.message);
  } finally {
    loginLoading.value = false;
  }
};


// 注册处理
const handleRegister = async () => {
  if (registerForm.password !== registerForm.confirmPassword) {
    alert("两次输入的密码不一致");
    return;
  }

  if (registerForm.password.length < 6) {
    alert("密码至少需要6位字符");
    return;
  }

  registerLoading.value = true;

  try {
    const res = await fetch("http://localhost:8000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: registerForm.username,
        email: registerForm.email,
        password: registerForm.password
      })
    });

    const data = await res.json();
    if (data.success) {
      currentUser.value = {
        username: registerForm.username,
        email: registerForm.email
      };
      currentPage.value = "main";

      Object.keys(registerForm).forEach(key => {
        registerForm[key] = "";
      });
    } else {
      alert(data.error || "注册失败");
    }
  } catch (err) {
    alert("注册请求失败：" + err.message);
  } finally {
    registerLoading.value = false;
  }
};


// 退出登录
const handleLogout = () => {
  currentUser.value = { username: '', email: '' }
  currentPage.value = 'login'
  // 清空生成的内容
  imageUrl.value = ''
  prompt.value = ''
  imageHistory.value = []
}

// 生成图片
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

// 下载图片
const downloadImage = () => {
  const link = document.createElement('a')
  link.href = imageUrl.value
  link.download = `ai-image-${Date.now()}.png`
  link.click()
}

// 分享图片
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

// 保存到历史记录
const saveToHistory = () => {
  if (imageUrl.value && currentPrompt.value) {
    imageHistory.value.unshift({
      url: imageUrl.value,
      prompt: currentPrompt.value,
      style: style.value,
      size: size.value,
      timestamp: new Date().toLocaleString()
    })

    // 限制历史记录数量
    if (imageHistory.value.length > 20) {
      imageHistory.value = imageHistory.value.slice(0, 20)
    }

    alert('已保存到历史记录！')
  }
}

// 选择历史图片
const selectHistoryImage = (item) => {
  imageUrl.value = item.url
  currentPrompt.value = item.prompt
  prompt.value = item.prompt
  style.value = item.style
  size.value = item.size
}
</script>

<style scoped>
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

.nav-title {
  font-size: 1.5rem;
  font-weight: bold;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
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

/* 主内容区域 */
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

/* 控制面板 */
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

/* 历史记录 */
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

/* 结果面板 */
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

/* 加载状态 */
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

/* 结果展示 */
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

/* 空状态 */
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

/* 响应式设计 */
@media (max-width: 1200px) {
  .content-container {
    grid-template-columns: 350px 1fr;
    gap: 20px;
  }
}

@media (max-width: 968px) {
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
}
</style>