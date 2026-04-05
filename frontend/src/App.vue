<script setup>
import { ref, onMounted, watch } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { authStore } from './store/auth'
import api from './api'

const router = useRouter()
const profile = ref({
  filial: '',
  filial_fish: '',
  fish: ''
})

const fetchProfile = async () => {
  if (authStore.isAuthenticated) {
    try {
      const response = await api.get('/profile/')
      if (response.data) {
        profile.value = response.data
      }
    } catch (err) {
      console.error('Profil yuklashda xatolik:', err)
    }
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

onMounted(fetchProfile)

// Tizimga kirish/chiqishni kuzatish
watch(() => authStore.isAuthenticated, (newVal) => {
  if (newVal) fetchProfile()
})
</script>

<template>
  <div class="min-h-screen bg-[#f0f2f5] flex">
    <!-- Sidebar (Serious Bank Style) -->
    <aside v-if="authStore.isAuthenticated" 
      class="w-64 bg-[#001529] text-white flex flex-col shadow-2xl relative z-20">
      
      <!-- App Logo Section -->
      <div class="p-6 bg-[#002140] border-b border-slate-700 flex items-center gap-3">
        <div class="w-8 h-8 bg-indigo-600 rounded flex items-center justify-center font-black text-xl shadow-lg shadow-indigo-900/50">M</div>
        <div>
          <div class="text-lg font-black tracking-tighter leading-none">MIRA</div>
          <div class="text-[9px] text-indigo-400 font-bold uppercase tracking-widest mt-1">Loan Management</div>
        </div>
      </div>

      <!-- User Information Section -->
      <div class="p-5 border-b border-slate-800 bg-[#001529]">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded bg-slate-700 flex items-center justify-center text-lg font-black border border-slate-600 text-indigo-300">
            {{ authStore.username?.charAt(0).toUpperCase() }}
          </div>
          <div class="overflow-hidden">
            <div class="text-xs font-black truncate text-slate-100 uppercase" :title="profile.filial_fish">{{ profile.filial_fish || authStore.username }}</div>
            <div class="text-[9px] text-slate-400 font-bold uppercase mt-0.5">{{ authStore.userRole }}</div>
          </div>
        </div>
        
        <!-- Branch Status -->
        <div class="bg-indigo-950/40 p-2 rounded border border-indigo-900/50 flex flex-col gap-1">
          <span class="text-[8px] text-indigo-400 font-black uppercase tracking-widest">Filial:</span>
          <span class="text-[10px] font-bold text-slate-200 truncate">{{ profile.filial || 'Markaziy' }}</span>
        </div>
      </div>

      <!-- Navigation Menu -->
      <nav class="flex-1 py-4 overflow-y-auto custom-scrollbar">
        <div class="px-3 mb-2 text-[9px] font-black text-slate-500 uppercase tracking-widest">Asosiy menyu</div>
        
        <RouterLink v-if="authStore.userRole === 'operator'"
          to="/loan-wizard" 
          class="nav-item group"
          active-class="nav-item-active">
          <span class="text-base">💰</span> 
          <span>Kredit arizasi</span>
        </RouterLink>

        <RouterLink to="/contracts" 
          class="nav-item group"
          active-class="nav-item-active">
          <span class="text-base">📜</span> 
          <span>Shartnomalar reestri</span>
        </RouterLink>
      </nav>

      <!-- System Footer -->
      <div class="p-4 border-t border-slate-800 bg-[#001529]">
        <button @click="handleLogout" 
          class="w-full py-2.5 bg-slate-800/50 text-slate-400 hover:bg-red-900 hover:text-white border border-slate-700/50 rounded transition-all duration-300 font-black text-[10px] uppercase tracking-widest flex items-center justify-center gap-2 group">
          <span class="group-hover:rotate-180 transition-transform duration-500">🚪</span> 
          Tizimdan chiqish
        </button>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col min-w-0">
      <!-- Top Navbar -->
      <header v-if="authStore.isAuthenticated" 
        class="h-14 bg-white border-b border-slate-300 flex items-center justify-between px-6 shadow-sm relative z-10">
        
        <div class="flex items-center gap-2">
            <span class="text-slate-400 hidden lg:inline text-xs font-bold">Tizim holati:</span>
            <span class="flex items-center gap-1.5 px-2 py-0.5 bg-emerald-50 text-emerald-600 rounded text-[9px] font-black uppercase tracking-wider border border-emerald-100">
                <span class="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span> Offline emas
            </span>
        </div>
        
        <div class="flex items-center gap-4">
          <div class="flex flex-col text-right pr-4 border-r border-slate-200">
            <span class="text-[11px] font-black text-slate-800 leading-none uppercase">{{ profile.filial_fish || authStore.username }}</span>
            <span class="text-[8px] font-bold text-slate-400 uppercase tracking-widest mt-1">{{ profile.filial }}</span>
          </div>
          <div class="text-xs font-black text-slate-400 group cursor-default" title="Foydalanuvchi roli">
            #{{ authStore.userRole?.toUpperCase() }}
          </div>
        </div>
      </header>

      <!-- Page Content Content Area -->
      <div class="flex-1 overflow-auto bg-[#f0f2f5] p-6 lg:p-10">
        <div class="bg-white rounded shadow-md border border-slate-200 min-h-full">
          <RouterView />
        </div>
      </div>
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background-color: #f0f2f5;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  margin: 4px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
  color: #a0aec0;
  transition: all 0.3s;
}

.nav-item:hover {
  color: white;
  background-color: rgba(255, 255, 255, 0.05);
}

.nav-item-active {
  color: white;
  background-color: #1890ff !important;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.35);
}

/* Custom Scrollbar for Sidebar */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #2d3748;
  border-radius: 10px;
}
</style>
