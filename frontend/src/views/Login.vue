<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../store/auth'
import api from '../api'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)

const togglePassword = () => {
    showPassword.value = !showPassword.value
}

const handleLogin = async () => {
    error.value = ''
    loading.value = true
    try {
        const response = await api.post('/auth/login/', {
            username: username.value,
            password: password.value
        })

        const data = response.data
        authStore.setAuth(data.access, data.role, data.username)
        router.push('/')
    } catch (err) {
        if (err.response && err.response.data) {
            error.value = err.response.data.detail || "Login yoki parol xato!"
        } else {
            error.value = "Serverga ulanib bo'lmadi! Iltimos qaytadan urinib ko'ring."
        }
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="login-wrapper min-h-screen flex items-center justify-center p-6 bg-[#0f1014]">
        <!-- Animated Background Blur Blobs -->
        <div class="fixed inset-0 overflow-hidden -z-10">
            <div class="blob blob-1"></div>
            <div class="blob blob-2"></div>
        </div>

        <div class="max-w-[480px] w-full">
            <div class="glass-container p-12 rounded-[3rem] border border-white/5 shadow-[0_32px_64px_-16px_rgba(0,0,0,0.6)] backdrop-blur-xl bg-white/[0.02]">
                <div class="text-center mb-12">
                    <div class="inline-flex items-center justify-center w-24 h-24 rounded-3xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-blue-400 p-[2px] shadow-2xl shadow-indigo-500/30 mb-8 transform hover:rotate-6 transition-transform duration-500">
                        <div class="w-full h-full bg-[#0f1014] rounded-[22px] flex items-center justify-center">
                             <span class="text-4xl font-black bg-gradient-to-r from-white to-white/70 bg-clip-text text-transparent">M</span>
                        </div>
                    </div>
                    <h2 class="text-4xl font-black text-white tracking-tight mb-3">Xush kelibsiz</h2>
                    <p class="text-slate-400 font-bold tracking-wide uppercase text-[10px]">Mira Kredit Boshqaruv Tizimi</p>
                </div>
                
                <transition name="fade">
                    <div v-if="error" class="mb-8 p-5 bg-red-500/10 border border-red-500/20 rounded-2xl flex items-center gap-4 animate-shake">
                        <span class="text-red-400 text-xl">⚡</span>
                        <div class="text-sm font-bold text-red-100">{{ error }}</div>
                    </div>
                </transition>

                <form @submit.prevent="handleLogin" class="space-y-8">
                    <div class="space-y-4">
                        <div class="relative group">
                            <label class="absolute -top-3 left-4 px-2 bg-[#121319] text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] group-focus-within:text-indigo-400 transition-colors">Username</label>
                            <input v-model="username" type="text" 
                                class="w-full px-6 py-5 bg-[#121319]/50 border-2 border-white/5 rounded-2xl text-white outline-none focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/10 transition-all font-bold text-lg hover:border-white/10"
                                required placeholder="Tizim logini">
                        </div>

                        <div class="relative group">
                            <label class="absolute -top-3 left-4 px-2 bg-[#121319] text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] group-focus-within:text-indigo-400 transition-colors">Password</label>
                            <div class="relative">
                                <input v-model="password" :type="showPassword ? 'text' : 'password'" 
                                    class="w-full px-6 py-5 bg-[#121319]/50 border-2 border-white/5 rounded-2xl text-white outline-none focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/10 transition-all font-bold text-lg hover:border-white/10 pr-16"
                                    required placeholder="••••••••">
                                
                                <button type="button" @click="togglePassword" 
                                    class="absolute right-5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-white p-2 transition-colors">
                                    <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
                                </button>
                            </div>
                        </div>
                    </div>

                    <button type="submit" 
                        :disabled="loading"
                        class="w-full py-5 bg-gradient-to-r from-indigo-600 via-indigo-500 to-indigo-600 bg-[length:200%_auto] text-white rounded-3xl font-black text-lg shadow-[0_20px_40px_-12px_rgba(79,70,229,0.4)] hover:bg-[100%_center] hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:scale-100 flex items-center justify-center gap-3">
                        <span v-if="loading" class="animate-spin text-2xl px-1">◌</span>
                        <span v-if="loading">Kutilmoqda...</span>
                        <span v-else>TIZIMGA KIRISH</span>
                    </button>
                </form>

                <div class="mt-12 pt-8 border-t border-white/5 text-center">
                    <p class="text-slate-500 text-[10px] font-black uppercase tracking-[0.3em]">Mira Ecosystem v1.2</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@200;400;600;800&display=swap');

.login-wrapper {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.glass-container {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
}

.blob {
    position: absolute;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.15;
    z-index: -10;
}

.blob-1 {
    background: #4f46e5;
    top: -200px;
    left: -200px;
    animation: move 20s infinite alternate;
}

.blob-2 {
    background: #2563eb;
    bottom: -200px;
    right: -200px;
    animation: move 25s infinite alternate-reverse;
}

@keyframes move {
    from { transform: translate(0, 0) scale(1); }
    to { transform: translate(100px, 100px) scale(1.2); }
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.5s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.animate-shake {
    animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes shake {
    10%, 90% { transform: translate3d(-1px, 0, 0); }
    20%, 80% { transform: translate3d(2px, 0, 0); }
    30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
    40%, 60% { transform: translate3d(4px, 0, 0); }
}
</style>
