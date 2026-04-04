<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'
import { authStore } from '../store/auth'

const route = useRoute()
const router = useRouter()
const loan = ref(null)
const loading = ref(true)
const role = authStore.userRole

const fetchLoan = async () => {
    loading.value = true
    try {
        const response = await api.get(`/loans/${route.params.id}/`)
        loan.value = response.data
    } catch (err) {
        console.error("Xatolik:", err)
        alert("Ariza topilmadi!")
        router.push('/contracts')
    } finally {
        loading.value = false
    }
}

const updateStatus = async (action) => {
    if (!confirm(`Haqiqatan ham ushbu arizani ${action === 'approve' ? 'tasdiqlamoqchimisiz' : 'rad etmoqchimisiz'}?`)) return
    try {
        await api.patch(`/loans/${loan.value.id}/status/`, { action })
        await fetchLoan()
    } catch (e) {
        alert(e.response?.data?.error || 'Xatolik yuz berdi!')
    }
}

const openDoc = (template) => {
    window.open(`/api/loans/${loan.value.id}/doc/${template}/`, '_blank')
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

const getStatusClass = (status) => {
    const classes = {
        'new': 'bg-blue-50 text-blue-600 border-blue-200',
        'moderation': 'bg-amber-50 text-amber-600 border-amber-200',
        'approved': 'bg-green-50 text-green-600 border-green-200',
        'rejected': 'bg-red-50 text-red-600 border-red-200'
    }
    return classes[status] || 'bg-slate-50 text-slate-600'
}

onMounted(fetchLoan)
</script>

<template>
    <div class="max-w-6xl mx-auto space-y-8 pb-20">
        
        <!-- Yuqori panel: Navigatsiya va Status -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100">
            <div class="flex items-center gap-6">
                <button @click="router.push('/contracts')" class="w-12 h-12 rounded-2xl bg-slate-50 flex items-center justify-center text-slate-400 hover:bg-slate-900 hover:text-white transition-all shadow-sm">
                    ←
                </button>
                <div>
                    <h1 class="text-2xl font-black text-slate-800 tracking-tight">Ariza ma'lumotlari</h1>
                    <p class="text-slate-400 font-bold text-xs uppercase tracking-widest mt-0.5">ID: #{{ route.params.id }}</p>
                </div>
            </div>

            <div v-if="loan" class="flex flex-wrap items-center gap-3">
                <!-- Status -->
                <span :class="getStatusClass(loan.status)" class="px-6 py-3 rounded-2xl border-2 font-black text-xs uppercase tracking-[0.1em]">
                    {{ getStatusLabel(loan.status) }}
                </span>

                <!-- MODERATOR BOSHQARUVI -->
                <template v-if="role === 'moderator' && loan.status === 'new'">
                    <button @click="updateStatus('approve')" class="px-6 py-3 rounded-2xl bg-green-500 text-white font-black text-xs uppercase tracking-widest shadow-lg shadow-green-200 hover:bg-green-600 transition-all">
                        ✓ Tasdiqlash
                    </button>
                    <button @click="updateStatus('reject')" class="px-6 py-3 rounded-2xl bg-white border-2 border-red-100 text-red-500 font-black text-xs uppercase tracking-widest hover:border-red-500 transition-all">
                        ✕ Rad etish
                    </button>
                </template>

                <!-- DIREKTOR BOSHQARUVI -->
                <template v-if="role === 'direktor' && loan.status === 'moderation'">
                    <button @click="updateStatus('approve')" class="px-6 py-3 rounded-2xl bg-indigo-600 text-white font-black text-xs uppercase tracking-widest shadow-lg shadow-indigo-200 hover:bg-indigo-700 transition-all">
                        ✓ Yakuniy Tasdiq
                    </button>
                    <button @click="updateStatus('reject')" class="px-6 py-3 rounded-2xl bg-white border-2 border-red-100 text-red-500 font-black text-xs uppercase tracking-widest hover:border-red-500 transition-all">
                        ✕ Rad etish
                    </button>
                </template>
            </div>
        </div>

        <div v-if="!loading && loan" class="grid grid-cols-1 xl:grid-cols-4 gap-8">
            
            <!-- Ma'lumotlar jadvali -->
            <div class="xl:col-span-3 space-y-8">
                
                <!-- 1. Mijoz shaxsiy ma'lumotlari -->
                <div class="bg-white rounded-[2.5rem] overflow-hidden shadow-sm border border-slate-100">
                    <div class="bg-slate-50 px-8 py-5 border-b border-slate-100 flex items-center justify-between">
                        <h3 class="font-black text-slate-800 uppercase text-xs tracking-widest">Mijoz shaxsiy ma'lumotlari</h3>
                        <span class="text-[10px] font-bold text-slate-400">1-BO'LIM</span>
                    </div>
                    <table class="w-full text-sm">
                        <tbody>
                            <tr v-for="(val, label) in {
                                'To\'liq F.I.SH': loan.data.client_info?.fish,
                                'Pasport seriya va raqami': loan.data.client_info?.pasport,
                                'INN raqami': loan.data.client_info?.inn,
                                'Telefon raqami': loan.data.client_info?.phone,
                                'Doimiy ro\'yxatdan otan manzili': loan.data.client_info?.address,
                                'Haqiqiy yashash manzili': loan.data.client_info?.lived_address
                            }" :key="label" class="border-b border-slate-50 last:border-0">
                                <td class="px-8 py-4 bg-slate-50/50 w-1/3 font-black text-slate-400 uppercase text-[10px] tracking-wider">{{ label }}</td>
                                <td class="px-8 py-4 font-bold text-slate-700">{{ val || '—' }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- 2. Kredit shartlari -->
                <div class="bg-white rounded-[2.5rem] overflow-hidden shadow-sm border border-slate-100">
                    <div class="bg-slate-50 px-8 py-5 border-b border-slate-100 flex items-center justify-between">
                        <h3 class="font-black text-slate-800 uppercase text-xs tracking-widest">Kredit shartlari va ma'lumotlari</h3>
                        <span class="text-[10px] font-bold text-slate-400">2-BO'LIM</span>
                    </div>
                    <table class="w-full text-sm">
                        <tbody>
                            <tr v-for="(val, label) in {
                                'Shartnoma raqami': loan.data.loan_details?.shartnoma_raqami,
                                'Shartnoma sanasi': loan.data.loan_details?.shartnoma_sana,
                                'Kredit summasi': loan.data.loan_details?.kredit_summasi?.toLocaleString() + ' so\'m',
                                'Kredit muddati': loan.data.loan_details?.kredit_muddati + ' oy',
                                'Yillik foiz stavkasi': loan.data.loan_details?.foiz_stavkasi + '%',
                                'Kredit maqsadi': loan.data.loan_details?.kredit_maqsadi
                            }" :key="label" class="border-b border-slate-50 last:border-0">
                                <td class="px-8 py-4 bg-slate-50/50 w-1/3 font-black text-slate-400 uppercase text-[10px] tracking-wider">{{ label }}</td>
                                <td class="px-8 py-4 font-bold text-slate-700">{{ val || '—' }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- 3. Garov ta'minoti -->
                <div class="bg-white rounded-[2.5rem] overflow-hidden shadow-sm border border-slate-100">
                    <div class="bg-slate-50 px-8 py-5 border-b border-slate-100 flex items-center justify-between">
                        <h3 class="font-black text-slate-800 uppercase text-xs tracking-widest">Garov ta'minoti detallari</h3>
                        <span class="text-[10px] font-bold text-slate-400">3-BO'LIM</span>
                    </div>
                    <!-- Garov turlari -->
                    <div class="p-8 border-b border-slate-50 flex gap-3">
                        <span v-for="type in (Array.isArray(loan.data.collateral?.types) ? loan.data.collateral.types : [])" :key="type"
                            class="px-5 py-2 rounded-xl bg-indigo-50 text-indigo-600 font-black text-[10px] uppercase tracking-widest border border-indigo-100">
                            {{ type === 'avto' ? '🚗 Avtomobil' : type === 'mulk' ? '🏠 Ko\'chmas mulk' : '🛡️ Sug\'urta' }}
                        </span>
                    </div>
                    <!-- Alohida garov ma'lumotlari bo'lsa (Misol: Avto) -->
                    <div v-if="loan.data.collateral?.avto" class="px-8 py-6 bg-slate-50/30">
                        <div class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4">Avtomobil ma'lumotlari:</div>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                            <div v-for="(v, l) in {
                                'Markasi': loan.data.collateral.avto.markasi,
                                'Davlat raqami': loan.data.collateral.avto.dav_raqami,
                                'Ishlab chiqarilgan yili': loan.data.collateral.avto.yil,
                                'Dvigatel raqami': loan.data.collateral.avto.dvigatel_raqami
                            }" :key="l">
                                <p class="text-[9px] font-bold text-slate-400 uppercase">{{ l }}</p>
                                <p class="font-bold text-slate-800 text-sm mt-1">{{ v || '—' }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- O'ng panel: Hujjatlar va Tizim -->
            <div class="space-y-8">
                
                <!-- HUJJATLAR (Faol faqat approved bo'lganda yoki direktor bo'lganda) -->
                <div class="bg-indigo-900 rounded-[2.5rem] p-8 text-white shadow-2xl shadow-indigo-100 relative overflow-hidden">
                    <!-- Bezak uchun sub'ektiv element -->
                    <div class="absolute -top-10 -right-10 w-32 h-32 bg-white/5 rounded-full blur-3xl"></div>
                    
                    <h3 class="text-xs font-black uppercase tracking-[0.2em] opacity-60 mb-8 flex items-center gap-3">
                        <span class="w-2 h-2 rounded-full bg-indigo-300 animate-pulse"></span>
                        Rasmiy hujjatlar
                    </h3>
                    
                    <div v-if="loan.status === 'approved' || role === 'direktor'" class="space-y-3">
                        <button v-for="(label, key) in {
                            'buyruq': 'Buyruq (HTML/PDF)',
                            'dalolatnoma': 'Dalolatnoma (HTML/PDF)',
                            'protokol': 'Protokol (HTML/PDF)',
                            'shartnoma': 'Shartnoma (HTML/PDF)',
                            'xulosa': 'Xulosa (HTML/PDF)',
                            'grafik': 'Grafik (HTML/PDF)'
                        }" :key="key" @click="openDoc(key)"
                        class="w-full text-left px-6 py-4 rounded-2xl bg-white/10 hover:bg-white/20 border border-white/5 hover:border-white/20 transition-all group flex items-center justify-between backdrop-blur-sm">
                            <span class="text-[11px] font-bold tracking-wide group-hover:translate-x-1 transition-transform">{{ label }}</span>
                            <span class="opacity-30 group-hover:opacity-100 group-hover:translate-x-1 transition-all font-black text-sm">→</span>
                        </button>
                    </div>
                    <div v-else class="py-12 text-center border-2 border-dashed border-white/10 rounded-3xl">
                        <p class="text-[10px] font-black uppercase tracking-widest opacity-30">Hujjatlar yopiq</p>
                    </div>
                </div>

                <!-- Foydalanuvchi ma'lumotlari -->
                <div class="bg-white rounded-[2.5rem] p-8 shadow-sm border border-slate-100">
                    <h3 class="text-xs font-black uppercase tracking-[0.2em] text-slate-400 mb-6">Ijrochi ma'lumotlari</h3>
                    <div class="flex items-center gap-4 mb-6">
                        <div class="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center text-white font-black">
                            {{ loan.operator_fish?.charAt(0) }}
                        </div>
                        <div>
                            <p class="font-black text-slate-800 text-sm">{{ loan.operator_fish }}</p>
                            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{{ loan.branch }}</p>
                        </div>
                    </div>
                    <div class="pt-6 border-t border-slate-50 space-y-4">
                        <div class="flex flex-col">
                            <label class="text-[9px] font-black text-slate-400 uppercase tracking-widest">Yaratilgan vaqt:</label>
                            <span class="text-xs font-bold text-slate-600 mt-1">{{ new Date(loan.created_at).toLocaleString('uz-UZ') }}</span>
                        </div>
                    </div>
                </div>

            </div>

        </div>

    </div>
</template>

<style scoped>
/* Rasmiy ko'rinish uchun qat'iy uslublar */
table td {
    vertical-align: middle;
}
</style>
