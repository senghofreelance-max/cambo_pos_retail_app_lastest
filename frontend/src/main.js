import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// createApp(App).mount('#app')

const initVueApp = (selector) => {
    createApp(App).mount(selector);
}
console.log(initVueApp)

// Explicitly attach to window for UMD reliability
window.initVueApp = initVueApp;

console.log(window.initVueApp)