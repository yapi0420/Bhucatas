import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://121.43.27.209:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      // ✅ 新增：代理图片请求到后端
      '/uploads': {
        target: 'http://121.43.27.209:8000',
        changeOrigin: true
      }
    }
  }
})