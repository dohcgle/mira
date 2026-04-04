<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import { authStore } from '../store/auth'

const loans = ref([])
const loading = ref(true)
const searchQuery = ref('')
const role = authStore.userRole

const fetchLoans = async () => {
    loading.value = true
    try {
        const response = await api.get('/loans/')
        loans.value = response.data
    } catch (err) {
        console.error("Xatolik:", err)
    } finally {
        loading.value = false
    }
}

const filteredLoans = computed(() => {
    if (!searchQuery.value) return loans.value
    const q = searchQuery.value.toLowerCase()
    return loans.value.filter(loan =>
        loan.data?.client_info?.fish?.toLowerCase().includes(q) ||
        loan.branch?.toLowerCase().includes(q) ||
        loan.id.toString().includes(q)
    )
})

const getStatusClass = (status) => {
    const classes = {
        'new': 'text-blue-600',
        'moderation': 'text-amber-600',
        'approved': 'text-green-600',
        'rejected': 'text-red-600'
    }
    return classes[status] || 'text-slate-600'
}

const getStatusLabel = (status) => {
    const labels = {
        'new': 'Yangi',
        'moderation': 'Moderatsiya',
        'approved': 'Tasdiqlangan',
        'rejected': 'Rad etilgan'
    }
    return labels[status] || status
}

const pageTitle = computed(() => {
    if (role === 'operator') return 'Mening arizalarim'
    if (role === 'moderator') return 'Tasdiqlash kutilmoqda'
    if (role === 'direktor') return 'Direktor tasdiqlashi'
    return 'Shartnomalar ro\'yxati'
})

onMounted(fetchLoans)
</script>

<template>
    <div class="space-y-6">
        <!-- Header -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div>
                <h1 class="text-2xl font-black text-slate-800 tracking-tight">{{ pageTitle }}</h1>
                <p class="text-slate-400 text-xs font-bold uppercase tracking-widest mt-1">Barcha kredit arizalari bazasi</p>
            </div>
            <div class="relative max-w-md w-full">
                <span class="absolute inset-y-0 left-4 flex items-center text-slate-400">🔍</span>
                <input v-model="searchQuery" type="text"
                    placeholder="ID yoki FISH bo'yicha qidirish..."
                    class="w-full pl-12 pr-6 py-3 bg-white border border-slate-200 rounded-xl focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/5 transition-all outline-none font-bold text-slate-600 text-sm">
            </div>
        </div>

        <!-- Jiddiy Bank Jadvali -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <table class="w-full border-collapse">
                <thead>
                    <tr class="bg-slate-50 border-b border-slate-200 text-left">
                        <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest border-r border-slate-200 w-20 text-center">ID</th>
                        <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest border-r border-slate-200">Holat</th>
                        <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest border-r border-slate-200">Mijoz (F.I.SH)</th>
                        <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest border-r border-slate-200">Filial</th>
                        <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest border-r border-slate-200">Kredit summasi</th>
                        <th class="px-6 py-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Sana</th>
                    </tr>
                </thead>
                <tbody v-if="!loading">
                    <tr v-for="loan in filteredLoans" :key="loan.id"
                        class="hover:bg-indigo-50/30 transition-colors border-b border-slate-100 last:border-0 group">
                        
                        <!-- ID -->
                        <td class="px-6 py-4 border-r border-slate-100 text-center">
                            <RouterLink :to="`/contracts/${loan.id}`" 
                                class="font-black text-indigo-600 hover:text-indigo-800 transition-colors block">
                                #{{ loan.id }}
                            </RouterLink>
                        </td>

                        <!-- Holat -->
                        <td class="px-6 py-4 border-r border-slate-100">
                            <span :class="getStatusClass(loan.status)" class="text-[10px] font-black uppercase tracking-widest">
                                ● {{ getStatusLabel(loan.status) }}
                            </span>
                        </td>

                        <!-- Mijoz -->
                        <td class="px-6 py-4 border-r border-slate-100">
                            <div class="flex flex-col">
                                <span class="font-bold text-slate-700 text-sm">{{ loan.data?.client_info?.fish }}</span>
                                <span class="text-[9px] text-slate-400 font-bold uppercase mt-0.5">{{ loan.data?.client_info?.pasport }}</span>
                            </div>
                        </td>

                        <!-- Filial -->
                        <td class="px-6 py-4 border-r border-slate-100 font-bold text-slate-500 text-xs">
                            {{ loan.branch }}
                        </td>

                        <!-- Summa -->
                        <td class="px-6 py-4 border-r border-slate-100">
                            <div class="flex flex-col text-right sm:text-left">
                                <span class="font-black text-slate-800 text-sm">{{ loan.data?.loan_details?.kredit_summasi?.toLocaleString() }} UZS</span>
                                <span class="text-[9px] text-indigo-500 font-black uppercase tracking-tighter">{{ loan.data?.loan_details?.kredit_muddati }} oy</span>
                            </div>
                        </td>

                        <!-- Sana -->
                        <td class="px-6 py-4 text-[11px] font-bold text-slate-400">
                            {{ new Date(loan.created_at).toLocaleDateString('uz-UZ') }}
                        </td>
                    </tr>

                    <!-- Bo'sh holat -->
                    <tr v-if="filteredLoans.length === 0">
                        <td colspan="6" class="py-20 text-center">
                            <div class="flex flex-col items-center opacity-30">
                                <span class="text-4xl mb-2">📂</span>
                                <p class="text-[10px] font-black uppercase tracking-widest">Ma'lumot mavjud emas</p>
                            </div>
                        </td>
                    </tr>
                </tbody>

                <!-- Loading -->
                <tbody v-else>
                    <tr v-for="i in 5" :key="i" class="animate-pulse">
                        <td v-for="j in 6" :key="j" class="px-6 py-6 border border-slate-50 bg-slate-50/50"></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
/* Bank uslubida qat'iy borderlar */
table {
    border-spacing: 0;
}
</style>
