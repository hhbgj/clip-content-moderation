<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>敏感图片检测</h1>
      </div>
      <nav>
        <ul>
          <li>
            <a href="#" class="active">敏感图片检测</a>
          </li>
        </ul>
      </nav>
    </aside>

    <main class="content">
      <section class="tab-content">
        <h2>敏感图片检测</h2>

        <div class="mode-select">
          <label><input type="radio" v-model="mode" value="file" /> 文件上传</label>
          <label><input type="radio" v-model="mode" value="url" /> URL</label>
        </div>

        <div v-if="mode === 'file'" class="input-area">
          <input type="file" @change="onFileChange" accept=".jpg,.jpeg,.png" />
        </div>

        <div v-if="mode === 'url'" class="input-area">
          <input type="text" v-model="imageUrl" placeholder="请输入图片 URL" />
        </div>

        <button @click="submitImage" class="submit-btn">检测敏感内容</button>

        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

        <div v-if="result" class="result">
          <h3>检测结果：</h3>
          <p :class="result.result ? 'flagged' : 'ok'">{{ result.result ? '⚠️ 疑似违规' : '✅ 未发现违规' }}</p>
          <p>最可能的类别：{{ result.label }}（{{ labelMap[result.label] }}），{{ result.score }}%</p>
          <div v-for="(score, name) in result.scores" :key="name" class="score-row">
            <span>{{ labelMap[name] || name }}</span>
            <progress :value="score" max="100"></progress>
            <span>{{ score }}%</span>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const mode = ref('file')
const imageFile = ref(null)
const imageUrl = ref('')
const result = ref(null)
const errorMessage = ref('')

const labelMap = {
  Normal: '正常',
  Porn: '色情',
  Terrorism: '暴恐',
  Violence: '暴力血腥',
}

const onFileChange = (e) => {
  imageFile.value = e.target.files[0]
  errorMessage.value = ''
}

const submitImage = async () => {
  result.value = null
  errorMessage.value = ''

  try {
    if (mode.value === 'file') {
      if (!imageFile.value) {
        errorMessage.value = '请上传图片文件'
        return
      }
      const formData = new FormData()
      formData.append('file', imageFile.value)
      const res = await fetch(`${API}/upload-image`, {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) throw new Error('请求失败')
      result.value = (await res.json()).payload
    } else if (mode.value === 'url') {
      if (!imageUrl.value.trim()) {
        errorMessage.value = '请输入图片 URL'
        return
      }
      const res = await fetch(`${API}/check-url`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: imageUrl.value }),
      })
      if (!res.ok) throw new Error('请求失败')
      result.value = (await res.json()).payload
    }
  } catch (err) {
    errorMessage.value = '检测失败，请检查网络或接口状态'
  }
}
</script>

<style scoped>
.flagged { color: #c0392b; font-weight: bold; }
.ok { color: #2e7d32; font-weight: bold; }
.score-row { display: flex; gap: .6rem; align-items: center; margin: .3rem 0; }
.score-row span:first-child { width: 5rem; }

html,
body,
#app {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Segoe UI', sans-serif;
  background-color: #f9f9f9;
  color: #333;
}

.app-layout {
  display: flex;
  height: 100%;
}

.sidebar {
  width: 200px;
  background-color: #f0f0f0;
  border-right: 1px solid #ccc;
  padding: 1.5rem;
  box-sizing: border-box;
}

.sidebar-header h1 {
  font-size: 1.4rem;
  margin-bottom: 1.5rem;
  color: #222;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li a {
  display: block;
  padding: 0.5rem;
  color: #333;
  text-decoration: none;
  border-radius: 4px;
}

.sidebar li a.active,
.sidebar li a:hover {
  background-color: #ddd;
}

.content {
  flex: 1;
  padding: 2rem 3rem;
  overflow-y: auto;
  box-sizing: border-box;
}

h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.mode-select label {
  margin-right: 1.5rem;
}

.input-area input {
  width: 100%;
  padding: 0.6rem;
  margin-top: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.submit-btn {
  margin-top: 1.5rem;
  padding: 0.7rem 2rem;
  background-color: #4a90e2;
  color: #fff;
  font-size: 1.1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #357ab8;
}

.result {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #f1f1f1;
  border-left: 5px solid #4a90e2;
  border-radius: 4px;
}

.result h3 {
  margin-top: 0;
}

progress {
  width: 100%;
  height: 20px;
  margin-top: 0.5rem;
}

.error-message {
  margin-top: 1rem;
  color: #d9534f;
  background-color: #fcebea;
  padding: 0.8rem;
  border-radius: 4px;
  border: 1px solid #f5c6cb;
}
</style>
