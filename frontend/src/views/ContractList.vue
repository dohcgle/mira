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
        loan.data?.client_info?.fish_inisiali?.toLowerCase().includes(q) ||
        loan.data?.administrative?.filial?.toLowerCase().includes(q) ||
        loan.id.toString().includes(q)
    )
})

const getStatusClass = (status) => {
    const classes = {
        'new': 'status-new',
        'moderation': 'status-moderation',
        'approved': 'status-approved',
        'rejected': 'status-rejected'
    }
    return classes[status] || ''
}

const getStatusLabel = (status) => {
    const labels = {
        'new': 'YANGI',
        'moderation': 'MODERATSIYA',
        'approved': 'TASDIQLANGAN',
        'rejected': 'RAD ETILGAN'
    }
    return labels[status] || status.toUpperCase()
}

const getCollateralIcon = (type) => {
    const icons = {
        'avto': '🚗',
        'mulk': '🏠',
        'sugurta': '📄',
        'tilla': '💍'
    }
    return icons[type] || '📦'
}

const getOwnerIcon = (type) => {
    const icons = {
        'self': '👤',
        'other': '👥',
        'ishonchnoma': '📜'
    }
    return icons[type] || '❔'
}

const pageTitle = computed(() => {
    if (role === 'operator') return 'MENING ARIZALARIM'
    if (role === 'moderator') return 'TASDIQLASH KUTILMOQDA'
    if (role === 'direktor') return 'DIREKTOR TASDIQLASHI'
    return 'SHARTNOMALAR REESTRI'
})

onMounted(fetchLoans)
</script>

<template>
    <div class="px-6 py-4 space-y-4 bg-[#f4f7f9] min-h-screen">
        <!-- Dashboard Header -->
        <div class="flex flex-col md:flex-row md:items-end justify-between border-b-2 border-slate-300 pb-4 gap-4">
            <div>
                <h1 class="text-xl font-bold text-slate-800 tracking-tight flex items-center gap-2">
                    <span class="w-2 h-6 bg-indigo-700 rounded-sm"></span>
                    {{ pageTitle }}
                </h1>
                <p class="text-[10px] text-slate-500 font-bold tracking-widest mt-0.5">MIRA LOAN MANAGEMENT SYSTEM v1.0</p>
            </div>
            
            <div class="flex items-center gap-3">
                <div class="relative group">
                    <span class="absolute inset-y-0 left-3 flex items-center text-slate-400 text-xs">🔍</span>
                    <input v-model="searchQuery" type="text"
                        placeholder="Reestr bo'yicha qidiruv..."
                        class="pl-9 pr-4 py-1.5 bg-white border border-slate-300 rounded shadow-inner focus:border-indigo-600 focus:ring-1 focus:ring-indigo-200 outline-none font-bold text-slate-700 text-xs w-64 transition-all">
                </div>
                <button @click="fetchLoans" class="p-1.5 bg-white border border-slate-300 rounded hover:bg-slate-50 text-slate-600 shadow-sm" title="Yangilash">
                    🔄
                </button>
            </div>
        </div>

        <!-- Oracle APEX Style Data Grid -->
        <div class="bg-white border border-slate-300 shadow-lg rounded-sm overflow-hidden">
            <div class="overflow-x-auto">
                <table class="grid-table w-full border-collapse">
                    <thead>
                        <tr>
                            <th class="w-16 text-center">ID</th>
                            <th class="w-32">HOLAT</th>
                            <th>MIJOZ (INISIALI)</th>
                            <th class="w-28">PASPORT</th>
                            <th class="w-32">KREDIT TURI</th>
                            <th class="w-40 text-right">SUMMA (UZS)</th>
                            <th class="w-24 text-center">GAROV</th>
                            <th class="w-20 text-center">EGASI</th>
                            <th class="w-36">FILIAL</th>
                            <th class="w-28 text-center">SANA</th>
                        </tr>
                    </thead>
                    <tbody v-if="!loading">
                        <tr v-for="loan in filteredLoans" :key="loan.id" 
                            class="row-link group"
                            @click="$router.push(`/contracts/${loan.id}`)">
                            
                            <!-- ID -->
                            <td class="text-center font-bold text-indigo-700 bg-slate-50/50">
                                #{{ loan.id }}
                            </td>

                            <!-- Holat -->
                            <td>
                                <div :class="getStatusClass(loan.status)" class="status-badge">
                                    {{ getStatusLabel(loan.status) }}
                                </div>
                            </td>

                            <!-- Mijoz -->
                            <td class="font-bold text-slate-800 text-[11px] uppercase truncate max-w-[200px]">
                                {{ loan.data?.client_info?.fish_inisiali || loan.data?.client_info?.fish }}
                            </td>

                            <!-- Pasport -->
                            <td class="font-semibold text-slate-600 text-[10px] tracking-tighter">
                                {{ loan.data?.client_info?.pasport }}
                            </td>

                            <!-- Kredit Turi -->
                            <td class="text-[10px] font-black text-slate-500 italic">
                                {{ loan.data?.loan_details?.kredit_turi?.toUpperCase() }}
                            </td>

                            <!-- Summa -->
                            <td class="text-right font-black text-slate-900 text-[12px] bg-indigo-50/20">
                                {{ loan.data?.loan_details?.kredit_summasi?.toLocaleString() }}
                            </td>

                            <!-- Garov Turlari -->
                            <td class="text-center">
                                <div class="flex justify-center gap-1.5">
                                    <span v-for="type in loan.data?.collateral?.types" :key="type" 
                                          :title="type" class="text-xs filter grayscale group-hover:grayscale-0 transition-all">
                                        {{ getCollateralIcon(type) }}
                                    </span>
                                    <span v-if="!loan.data?.collateral?.types?.length" class="text-slate-300">—</span>
                                </div>
                            </td>

                            <!-- Garov Egasi -->
                            <td class="text-center">
                                <span v-if="loan.data?.collateral?.garov_egasi" 
                                      :title="loan.data.collateral.garov_egasi" class="text-xs">
                                    {{ getOwnerIcon(loan.data.collateral.garov_egasi) }}
                                </span>
                                <span v-else class="text-slate-300">—</span>
                            </td>

                            <!-- Filial -->
                            <td class="text-[10px] font-bold text-slate-600 border-l border-slate-100">
                                {{ loan.data?.administrative?.filial || '—' }}
                            </td>

                            <!-- Shartnoma Sana -->
                            <td class="text-[10px] font-bold text-slate-400 text-center bg-slate-50/30">
                                {{ loan.data?.loan_details?.shartnoma_sana || new Date(loan.created_at).toLocaleDateString('uz-UZ') }}
                            </td>
                        </tr>

                        <!-- Bo'sh holat -->
                        <tr v-if="filteredLoans.length === 0">
                            <td colspan="10" class="py-32 text-center bg-slate-50">
                                <h3 class="text-slate-400 font-black uppercase tracking-[0.2em] text-sm">Ma'lumot topilmadi</h3>
                                <p class="text-[10px] text-slate-300 mt-2">Qidiruv parametrlarini o'zgartirib ko'ring</p>
                            </td>
                        </tr>
                    </tbody>

                    <!-- Skeleton Loading -->
                    <tbody v-else>
                        <tr v-for="i in 12" :key="i">
                            <td v-for="j in 10" :key="j" class="py-3 bg-white border border-slate-200">
                                <div class="h-2 bg-slate-100 rounded w-full animate-pulse"></div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Footer Info -->
        <div class="flex justify-between items-center text-[10px] font-bold text-slate-400 uppercase tracking-widest px-2">
            <div>JAMI ARIZALAR: {{ filteredLoans.length }}</div>
            <div>Hozirgi vaqt: {{ new Date().toLocaleString('uz-UZ') }}</div>
        </div>
    </div>
</template>

<style scoped>
/* Oracle APEX Data Grid Style CSS */
.grid-table {
    border-collapse: collapse;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.grid-table thead tr {
    background-color: #f0f3f6;
    border-bottom: 2px solid #cbd5e0;
}

.grid-table th {
    padding: 10px 12px;
    text-align: left;
    font-size: 10px;
    font-weight: 800;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border: 1px solid #d1d9e3;
    white-space: nowrap;
}

.grid-table td {
    padding: 8px 12px;
    border: 1px solid #e2e8f0;
    transition: all 0.2s;
}

.row-link {
    cursor: pointer;
}

.row-link:hover td {
    background-color: #f1f5f9 !important;
    border-color: #cbd5e0;
}

/* Status Badges */
.status-badge {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 2px;
    font-size: 9px;
    font-weight: 900;
    letter-spacing: 0.5px;
    border: 1px solid currentColor;
}

.status-new { color: #2563eb; background: #eff6ff; }
.status-moderation { color: #d97706; background: #fffbeb; }
.status-approved { color: #059669; background: #ecfdf5; }
.status-rejected { color: #dc2626; background: #fef2f2; }

/* Scrollbar Style */
.overflow-x-auto::-webkit-scrollbar {
    height: 8px;
}
.overflow-x-auto::-webkit-scrollbar-track {
    background: #edf2f7;
}
.overflow-x-auto::-webkit-scrollbar-thumb {
    background: #cbd5e0;
    border-radius: 0;
}
.overflow-x-auto::-webkit-scrollbar-thumb:hover {
    background: #a0aec0;
}
</style>
