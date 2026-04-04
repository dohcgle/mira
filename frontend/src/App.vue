<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { authStore } from './store/auth'

const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 flex">
    <!-- Sidebar (Faqat tizimga kirilganda ko'rinadi) -->
    <aside v-if="authStore.isAuthenticated" class="w-64 bg-slate-900 text-white flex-col hidden md:flex">
      <div class="p-6 bg-indigo-600">
        <div class="text-2xl font-black">Mira</div>
        <div class="flex items-center gap-2 mt-2">
          <span class="text-indigo-200 text-sm font-bold">{{ authStore.username }}</span>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider"
            :class="{
              'bg-blue-400 text-blue-900': authStore.userRole === 'operator',
              'bg-amber-400 text-amber-900': authStore.userRole === 'moderator',
              'bg-emerald-400 text-emerald-900': authStore.userRole === 'direktor'
            }">
            {{ authStore.userRole }}
          </span>
        </div>
      </div>
      <nav class="flex-1 p-4 space-y-1">
        <!-- Faqat operator uchun: Kredit olish -->
        <RouterLink v-if="authStore.userRole === 'operator'"
          to="/loan-wizard" class="block p-3 rounded-xl hover:bg-slate-800 transition-all flex items-center gap-3 font-semibold">
          <span>💰</span> Kredit olish
        </RouterLink>

        <!-- Barcha guruhlar uchun: Shartnomalar -->
        <RouterLink to="/contracts" class="block p-3 rounded-xl hover:bg-slate-800 transition-all flex items-center gap-3 font-semibold">
          <span>🧾</span> Shartnomalar
        </RouterLink>
      </nav>
      <div class="p-4 border-t border-slate-800">
        <button @click="handleLogout" class="w-full p-2 bg-slate-800 rounded-lg hover:bg-red-500 transition-all font-bold">
          Chiqish
        </button>
      </div>
    </aside>

    <!-- Asosiy qism -->
    <main class="flex-1 flex flex-col">
      <!-- Navbar (Faqat tizimga kirilganda ko'rinadi) -->
      <header v-if="authStore.isAuthenticated" class="h-20 bg-white border-b border-slate-100 flex items-center justify-between px-10 shadow-sm">
        <h2 class="text-2xl font-black text-slate-800 tracking-tight uppercase">Mira <span class="text-indigo-600">Admin</span></h2>
        
        <div class="flex items-center gap-6">
          <!-- Foydalanuvchi ma'lumotlari -->
          <div class="flex items-center gap-4 pr-6 border-r border-slate-200">
            <div class="flex flex-col text-right">
              <span class="text-sm font-black text-slate-800 leading-none capitalize">{{ authStore.username }}</span>
              <span class="text-[10px] font-bold text-indigo-500 uppercase tracking-widest mt-1.5">{{ authStore.userRole }}</span>
            </div>
            <div class="w-11 h-11 rounded-2xl bg-indigo-50 flex items-center justify-center text-indigo-600 font-black text-lg shadow-sm border border-indigo-100">
              {{ authStore.username?.charAt(0).toUpperCase() }}
            </div>
          </div>
          
          <!-- Chiqish tugmasi -->
          <button @click="handleLogout" 
            class="group flex items-center gap-2.5 px-5 py-2.5 bg-red-50 text-red-600 rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-red-600 hover:text-white transition-all active:scale-95 shadow-sm">
            <span>🚪</span> Chiqish
          </button>
        </div>
      </header>

      <!-- Sahifa mazmuni -->
      <div class="p-8 h-full overflow-y-auto">
        <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-100 p-10 min-h-[calc(100vh-160px)]">
          <RouterView />
        </div>
      </div>
    </main>
  </div>
</template>

<style>
/* Bu yerda hamma global stillar Tailwind tomonidan boshqariladi */
body {
  margin: 0;
  font-family: 'Inter', sans-serif;
}
</style>
