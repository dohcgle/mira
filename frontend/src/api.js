import axios from 'axios'
import { authStore } from './store/auth'
import router from './router'

// Markaziy API obyekti
const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json'
    }
})

// So'rov ketishidan oldin (Interceptor)
api.interceptors.request.use(config => {
    // Agar bizda token bo'lsa, uni har doim Headerga qo'shish
    if (authStore.accessToken) {
        config.headers.Authorization = `Bearer ${authStore.accessToken}`
    }
    return config
}, error => {
    return Promise.reject(error)
})

// Javob kelganda (Xatolikni tekshirish)
api.interceptors.response.use(response => {
    return response
}, error => {
    // Agar Token muddati o'tgan bo'lsa (401 xatosi) -> Login sahifasiga qaytarish
    if (error.response && error.response.status === 401) {
        authStore.logout()
        router.push('/login')
    }
    return Promise.reject(error)
})

export default api
