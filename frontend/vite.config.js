import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    // Output to the Frappe app's public folder
    outDir: '../cambo_pos_retail_app/public/frontend',
    emptyOutDir: true,
    lib: {
      entry: path.resolve(__dirname, 'src/main.js'),
      name: 'Frontend',
      formats: ['umd'],
      fileName: (format) => `frontend_app.js`,
    },
  },
  define: {
    'process.env': {}
  }
})
