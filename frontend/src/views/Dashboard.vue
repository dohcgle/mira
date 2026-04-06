<template>
  <div class="space-y-8 p-4 md:p-8 animate-in fade-in duration-700">
    <!-- Header Section -->
    <header class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-slate-800 tracking-tight">Dashboard Overview</h1>
        <p class="text-slate-500 mt-1">Welcome back, <span class="font-semibold text-indigo-600">{{ username }}</span>. Here's what's happening with your loans today.</p>
      </div>
      <div class="flex items-center gap-3">
        <router-link to="/loan-wizard" 
          class="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-xl font-medium transition-all shadow-lg shadow-indigo-200 active:scale-95">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Yangi ariza
        </router-link>
      </div>
    </header>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="stat in stats" :key="stat.label" 
        class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group">
        <div class="flex items-center justify-between">
          <div :class="stat.iconBg" class="p-3 rounded-2xl transition-colors duration-300">
            <component :is="stat.icon" class="h-6 w-6 text-white" />
          </div>
          <span class="text-xs font-bold px-2.5 py-1 rounded-full text-indigo-700 bg-indigo-50 group-hover:bg-indigo-100 transition-colors">
            +12% vs last month
          </span>
        </div>
        <div class="mt-4">
          <p class="text-sm font-medium text-slate-500">{{ stat.label }}</p>
          <p class="text-2xl font-bold text-slate-800 mt-1">{{ stat.value }}</p>
        </div>
      </div>
    </div>

    <!-- Quick Actions & Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Quick Navigation -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm">
          <h2 class="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Tizim funksiyalari
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <router-link to="/loan-wizard" class="group flex items-center p-4 rounded-2xl bg-slate-50 hover:bg-white border border-transparent hover:border-indigo-100 hover:shadow-md transition-all">
              <div class="bg-indigo-100 p-3 rounded-xl group-hover:bg-indigo-600 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-600 group-hover:text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div class="ml-4 text-left">
                <p class="font-bold text-slate-800">Mikroqarz hujjatlarini yaratish</p>
                <p class="text-sm text-slate-500">Yangi ariza to'ldirish va PDF generatsiya</p>
              </div>
            </router-link>

            <router-link to="/contracts" class="group flex items-center p-4 rounded-2xl bg-slate-50 hover:bg-white border border-transparent hover:border-indigo-100 hover:shadow-md transition-all">
              <div class="bg-blue-100 p-3 rounded-xl group-hover:bg-blue-600 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600 group-hover:text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                </svg>
              </div>
              <div class="ml-4 text-left">
                <p class="font-bold text-slate-800">Barcha shartnomalar ro'yxati</p>
                <p class="text-sm text-slate-500">Tizimdagi barcha arizalar va ularning holati</p>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Custom Illustration Card -->
        <div class="relative overflow-hidden bg-gradient-to-br from-indigo-700 to-violet-800 p-8 rounded-3xl text-white shadow-xl shadow-indigo-200">
          <div class="relative z-10 max-w-sm">
            <h3 class="text-2xl font-bold mb-2">Tezkor Hujjat Yaratish</h3>
            <p class="opacity-90 mb-6">Mijoz ma'lumotlarini kiriting va bir soniyada shartnoma, grafik va buyruqlarni tayyorlang.</p>
            <router-link to="/loan-wizard" class="inline-flex py-3 px-6 rounded-xl bg-white text-indigo-700 font-bold hover:bg-opacity-90 transition-all active:scale-95 shadow-lg">
              Hoziroq boshlash
            </router-link>
          </div>
          <div class="absolute -right-10 -bottom-10 opacity-20 transform -rotate-12">
            <svg class="w-64 h-64" viewBox="0 0 200 200" fill="currentColor">
               <path d="M 40, 40 L 160, 40 L 160, 160 L 40, 160 Z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Right Sidebar: Info -->
      <div class="space-y-6">
        <div class="bg-slate-900 p-8 rounded-3xl text-white shadow-xl">
          <h2 class="text-lg font-bold mb-4 flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Tizim holati
          </h2>
          <div class="space-y-4 text-sm opacity-80">
            <div class="flex justify-between border-b border-white/10 pb-2">
              <span>Foydalanuvchi:</span>
              <span class="font-mono">{{ username }}</span>
            </div>
            <div class="flex justify-between border-b border-white/10 pb-2">
              <span>Roli:</span>
              <span class="uppercase tracking-wider font-bold">{{ role }}</span>
            </div>
            <div class="flex justify-between border-b border-white/10 pb-2">
              <span>Filial:</span>
              <span>Toshkent Bosh Ofisi</span>
            </div>
            <div class="flex justify-between pt-2">
              <span>Versiya:</span>
              <span class="bg-white/20 px-2 py-0.5 rounded">v2.4.0</span>
            </div>
          </div>
          <button @click="logout" class="w-full mt-8 py-3 rounded-2xl bg-white/10 hover:bg-red-500/20 text-white font-medium border border-white/10 hover:border-red-500/50 transition-all">
            Chiqish
          </button>
        </div>

        <div class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
          <h2 class="font-bold text-slate-800 mb-4">Tezkor maslahat</h2>
          <p class="text-sm text-slate-500 leading-relaxed italic">
            "Hujjatlarni chop etishdan oldin mijozning JSHSHIR (PINFL) va pasport seriyasini qayta tekshirib olishni tafsiya etamiz."
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { authStore } from '@/store/auth';
import { useRouter } from 'vue-router';

const router = useRouter();

const username = computed(() => authStore.username || 'Admin');
const role = computed(() => authStore.role || 'Operator');

const logout = () => {
  authStore.logout();
  router.push('/login');
};

const stats = [
  { 
    label: 'Jami arizalar', 
    value: '1,280', 
    iconBg: 'bg-indigo-500', 
    icon: {
      template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>`
    }
  },
  { 
    label: 'Tasdiqlangan', 
    value: '942', 
    iconBg: 'bg-green-500', 
    icon: {
      template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>`
    }
  },
  { 
    label: 'Moderatsiyada', 
    value: '12', 
    iconBg: 'bg-amber-500', 
    icon: {
      template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`
    }
  },
  { 
    label: 'Rad etilgan', 
    value: '326', 
    iconBg: 'bg-red-500', 
    icon: {
      template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>`
    }
  }
];
</script>

<style scoped>
.animate-in {
  animation-duration: 0.5s;
}
</style>
