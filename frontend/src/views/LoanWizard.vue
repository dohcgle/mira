<script setup>
import { ref, computed, watch } from 'vue' // 'computed' va 'watch'ni qo'shdik
import { useRouter } from 'vue-router'
import { vMaska } from "maska/vue" // Oxiriga /vue qo'shildi
import { authStore } from '../store/auth'
import api from '../api'

const router = useRouter()


const currentStep = ref(1)

const steps = [
    { id: 1, label: 'Mijoz', icon: '👤' },
    { id: 2, label: 'Kredit', icon: '💰' },
    { id: 3, label: 'Moliyaviy holat', icon: '📊' },
    { id: 4, label: 'Garov', icon: '🏠' }
]

const formData = ref({
    client_info: {
        fish: 'ANNAZAROV KAXRAMAN SADULLAYEVICH',
        fish_inisiali: 'K.S.ANNAZAROV',
        tugilgan_sana: '02.02.1987',
        jinsi: 'ERKAK',
        telefon: '+998901234567',
        pasport: 'AA1234567',
        jshshir: '31002873680015',
        pasport_berilgan_sana: '02.02.2017',
        pasport_amal_qilish: '02.02.2027',
        pasport_berilgan_joy: 'TOSHKENT SHAHAR ICHKI ISHLAR BOSHQARMASI',
        contacts: [
            { telefon: '', qarindoshlik: '' },
            { telefon: '', qarindoshlik: '' }
        ]
    },

    loan_details: {
        shartnoma_raqami: '№310-TR', 
        shartnoma_sana: '03.04.2026', 
        boshlanish_sana: '03.04.2026', 
        tugash_sana: '03.04.2027',
        kredit_turi: '', 
        grafik_turi: '', 
        kredit_summasi: 45000000, 
        kredit_summasi_soz: '', 
        foiz_stavkasi: 55, 
        foiz_stavkasi_soz: '',
        kredit_muddati: 36, 
        kredit_muddati_soz: '', 
        oylik_tolov: 1700000, 
        oylik_tolov_soz: ''
    },

    financial: {
        ish_muassasa: 'TOSHKENT SHAHAR ICHKI ISHLAR BOSHQARMASI',
        ish_manzil: 'Beruniy ko\'chasi 1B-uy',
        ish_lavozim: 'Operator',
        aloqa_uy_tel: '',
        aloqa_ish_tel: '',
        aloqa_uyali_tel: '',
        daromad_asosiy: 4500000,
        daromad_orindosh: 0,
        daromad_boshqa: 0,
        daromad_jami: 0,
        daromad_jami_soz: '',
        xarajat_kommunal: 680000,
        xarajat_oilaviy: 0,
        xarajat_boshqa: 0,
        xarajat_jami: 0,
        xarajat_jami_soz: '',
        majburiyatlar: '',
    },

    collateral: {
        garov_egasi: 'self',
        avto: {
            yil: 2022,
            nomi: 'CHEVROLET COBALT',
            rang: 'Oq',
            kuzov: 'XWBJA69VERA108471',
            davlat_raqami: '01A123AA',
            manzil: 'SAMARQAND SHAHAR YUGUNAKIY KOCHASI',
            shassi: 'RAQAMSIZ',
            dvigatel: 'B15D213241352MTAX0118',
            jshshir: '31002873680015',
            kuzov_turi: 'SEDAN',
            texpasport: 'AAF123456789',
            texpasport_sana: '02.02.2022',
            bahosi: 125000000,
            bahosi_soz: '',
        },
        mulk: {
            turi: '',
            nomi: 'YAKKA TARTIBDAGI UY-JOY',
            umumiy_yer_maydoni: '704',
            qurilish_osti_maydoni: '149.81',
            umumiy_foydali_maydoni: '213.72',
            yashash_maydoni: '213.72',
            manzili: 'KALTAMINAR KO\'CHASI 1B-UY',
            reestr_raqami: '',
            kadastr_raqami: '01.04.2026 y. №23:08:40:01:04:0357',
            egasi_fish: '',
            bahosi: 0,
            bahosi_soz: '',
        },
        sugurta: {
            kompaniya: '',
            summa: 0,
            summa_soz: ''
        },
        owner: {
            fish: '',
            fish_inisiali: '',
            tugilgan_sana: '',
            jinsi: '',
            telefon: '',
            pasport: '',
            jshshir: '',
            pasport_berilgan_sana: '',
            pasport_amal_qilish: '',
            pasport_berilgan_joy: '',
        },
        ishonchnoma: {
            notarius_fish: '',
            notarius_address: '',
            notarius_reestr_raqami: '',
            notarius_berilgan_sana: ''
        },
        types: [], // Tanlangan garov turlari (massiv)
    }
    // ... qolganlari
})

// 1. Qadam to'g'ri to'ldirilganini tekshirish (Computed)
const isStepValid = computed(() => {
    if (currentStep.value === 1) {
        // F.I.SH va Pasport to'ldirilgan bo'lsa true qaytaradi
        return formData.value.client_info.fish.length > 5 && formData.value.client_info.pasport.length >= 7
    }
    if (currentStep.value === 2) {
        return formData.value.loan_details.summa > 0
    }
    return true
})

const nextStep = () => {
    if (currentStep.value < 5) {
        currentStep.value++
    }
}

const prevStep = () => { if (currentStep.value > 1) currentStep.value-- }
const saveForm = async () => {
    try {
        const response = await api.post('/loans/', formData.value)
        alert('Ariza muvaffaqiyatli saqlandi!')
        router.push('/contracts')
    } catch (err) {
        alert('Saqlashda xatolik yuz berdi: ' + (err.response?.data ? JSON.stringify(err.response.data) : err.message));
    }
}

const toggleCollateralType = (type) => {
    const index = formData.value.collateral.types.indexOf(type);
    if (index === -1) {
        formData.value.collateral.types.push(type);
    } else {
        formData.value.collateral.types.splice(index, 1);
    }
}

// FISH yozilganda inisialni avtomat shakllantirish
const handleFishInput = (event, target) => {
    let val = event.target.value.toUpperCase();
    // O' va G' harflari uchun tutuq belgisini (apostrof) va bo'sh joyni qoldiramiz
    val = val.replace(/[^A-Z\s']+/g, '');
    target.fish = val;

    const parts = val.trim().split(/\s+/);
    if (parts.length >= 2) {
        const ignoreWords = ["O'GLI", "OG'LI", "OGLI", "QIZI"];
        const surname = parts[0];
        const initials = parts.slice(1)
            .filter(p => p.length > 0 && !ignoreWords.includes(p))
            .map(p => p.charAt(0) + '.')
            .join('');
        target.fish_inisiali = `${initials}${surname}`;
    } else {
        target.fish_inisiali = val;
    }
}
// Sonni o'zbek tilida so'z bilan yozish
const numberToWordsUz = (num) => {
    if (!num) return '';
    num = String(num).replace(/\s+/g, ''); // Bo'shliqlarni olib tashlaymiz (maska uchun)
    if (isNaN(num) || num === '') return '';
    if (num === '0') return 'nol';

    const ones = ['', 'bir', 'ikki', 'uch', 'to\'rt', 'besh', 'olti', 'yetti', 'sakkiz', 'to\'qqiz'];
    const tens = ['', 'o\'n', 'yigirma', 'o\'ttiz', 'qirq', 'ellik', 'oltmish', 'yetmish', 'sakson', 'to\'qson'];
    const units = ['', 'ming', 'million', 'milliard', 'trillion'];

    const convertChunk = (n) => {
        let res = '';
        if (n >= 100) {
            res += ones[Math.floor(n / 100)] + ' yuz ';
            n %= 100;
        }
        if (n >= 10) {
            res += tens[Math.floor(n / 10)] + ' ';
            n %= 10;
        }
        if (n > 0) {
            res += ones[n] + ' ';
        }
        return res;
    };

    let n = parseInt(num);
    let res = '';
    let unitIdx = 0;

    while (n > 0) {
        let chunk = n % 1000;
        if (chunk > 0) {
            res = convertChunk(chunk) + units[unitIdx] + ' ' + res;
        }
        n = Math.floor(n / 1000);
        unitIdx++;
    }

    return res.trim();
};

// Kredit ma'lumotlarini kuzatish va so'z bilan yozish
watch(() => formData.value.loan_details.kredit_summasi, (val) => {
    formData.value.loan_details.kredit_summasi_soz = numberToWordsUz(val);
});

watch(() => formData.value.loan_details.foiz_stavkasi, (val) => {
    formData.value.loan_details.foiz_stavkasi_soz = numberToWordsUz(val);
});

watch(() => formData.value.loan_details.kredit_muddati, (val) => {
    formData.value.loan_details.kredit_muddati_soz = numberToWordsUz(val);
});

watch(() => formData.value.loan_details.oylik_tolov, (val) => {
    formData.value.loan_details.oylik_tolov_soz = numberToWordsUz(val);
});

// Daromadlarni hisoblash
watch([
    () => formData.value.financial.daromad_asosiy,
    () => formData.value.financial.daromad_orindosh,
    () => formData.value.financial.daromad_boshqa
], () => {
    const v1 = parseInt(String(formData.value.financial.daromad_asosiy || 0).replace(/\s+/g, '')) || 0;
    const v2 = parseInt(String(formData.value.financial.daromad_orindosh || 0).replace(/\s+/g, '')) || 0;
    const v3 = parseInt(String(formData.value.financial.daromad_boshqa || 0).replace(/\s+/g, '')) || 0;
    formData.value.financial.daromad_jami = v1 + v2 + v3;
}, { immediate: true });

watch(() => formData.value.financial.daromad_jami, (val) => {
    formData.value.financial.daromad_jami_soz = numberToWordsUz(val);
});

// Xarajatlarni hisoblash
watch([
    () => formData.value.financial.xarajat_kommunal,
    () => formData.value.financial.xarajat_oilaviy,
    () => formData.value.financial.xarajat_boshqa
], () => {
    const v1 = parseInt(String(formData.value.financial.xarajat_kommunal || 0).replace(/\s+/g, '')) || 0;
    const v2 = parseInt(String(formData.value.financial.xarajat_oilaviy || 0).replace(/\s+/g, '')) || 0;
    const v3 = parseInt(String(formData.value.financial.xarajat_boshqa || 0).replace(/\s+/g, '')) || 0;
    formData.value.financial.xarajat_jami = v1 + v2 + v3;
}, { immediate: true });

watch(() => formData.value.financial.xarajat_jami, (val) => {
    formData.value.financial.xarajat_jami_soz = numberToWordsUz(val);
});

// Garov qiymatlarini kuzatish
watch(() => formData.value.collateral.avto.bahosi, (val) => {
    formData.value.collateral.avto.bahosi_soz = numberToWordsUz(val);
});

watch(() => formData.value.collateral.mulk.bahosi, (val) => {
    formData.value.collateral.mulk.bahosi_soz = numberToWordsUz(val);
});

watch(() => formData.value.collateral.sugurta.summa, (val) => {
    formData.value.collateral.sugurta.summa_soz = numberToWordsUz(val);
});

// Garov egasi 'Ozi' bo'lganda mijoz ma'lumotlarini nusxalash
watch([() => formData.value.collateral.garov_egasi, () => formData.value.client_info], ([newEgasi, newClient], [oldEgasi, oldClient]) => {
    if (newEgasi === 'self') {
        Object.keys(formData.value.collateral.owner).forEach(key => {
            if (newClient[key] !== undefined) {
                formData.value.collateral.owner[key] = newClient[key];
            }
        });
    } else if (newEgasi !== oldEgasi && (newEgasi === 'other' || newEgasi === 'ishonchnoma')) {
        // Turi o'zgarganda tozalash
        Object.keys(formData.value.collateral.owner).forEach(key => {
            formData.value.collateral.owner[key] = '';
        });
    }
}, { deep: true, immediate: true });

</script>

<template>
    <div class="max-w-10xl mx-auto px-4 py-8">
        <!-- Steplar (Indikatorlar) -->
        <div class="relative mb-12 max-w-4xl mx-auto">
            <!-- Bog'lovchi chiziq -->
            <div class="absolute top-5 left-0 w-full h-0.5 bg-slate-200 -z-0">
                <div class="h-full bg-indigo-600 transition-all duration-500"
                    :style="{ width: ((currentStep - 1) / (steps.length - 1) * 100) + '%' }"></div>
            </div>

            <div class="relative z-10 flex justify-between">
                <div v-for="step in steps" :key="step.id" class="flex flex-col items-center">
                    <div :class="['w-10 h-10 rounded-full flex items-center justify-center font-bold transition-all duration-300 border-4',
                        currentStep > step.id ? 'bg-indigo-600 border-indigo-600 text-white' :
                            currentStep === step.id ? 'bg-white border-indigo-600 text-indigo-600 shadow-md transform scale-110' :
                                'bg-slate-200 border-slate-200 text-slate-500']">
                        <span v-if="currentStep > step.id">✓</span>
                        <span v-else>{{ step.id }}</span>
                    </div>
                    <span :class="['mt-3 text-xs font-bold uppercase tracking-wider transition-colors duration-300',
                        currentStep >= step.id ? 'text-indigo-600' : 'text-slate-400']">
                        {{ step.label }}
                    </span>
                </div>
            </div>
        </div>

        <div class="bg-white p-10 rounded-3xl shadow-xl border border-slate-100 min-h-[400px] flex flex-col">

            <!-- 1-QADAM MIJOZ-->
            <div v-if="currentStep === 1">
                <h2 class="text-2xl font-bold mb-6 text-slate-800">👤 Shaxsiy ma'lumotlar</h2>
                <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">F.I.Sh.</label>
                        <input :value="formData.client_info.fish" @input="handleFishInput($event, formData.client_info)" type="text"
                            class="input-field" placeholder="MASALAN: ANVAR G'ANIYEV">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">F.I.Sh. inisiali</label>
                        <input v-model="formData.client_info.fish_inisiali" type="text" class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Tug'ilgan sana</label>
                        <input v-model="formData.client_info.tugilgan_sana" v-maska="'##.##.####'" type="text"
                            class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">JINSI</label>
                        <select v-model="formData.client_info.jinsi" class="input-field">
                            <option value="" disabled selected>Tanlang</option>
                            <option value="erkak">Erkak</option>
                            <option value="ayol">Ayol</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Telefon</label>
                        <input v-model="formData.client_info.telefon" v-maska="'+998 ## ### ## ##'" type="text"
                            class="input-field">
                    </div>
                </div>
                <!-- Pasport ma'lumotlari -->
                <div class="grid grid-cols-1 md:grid-cols-5 mt-4 gap-6">
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Pasport seriya va raqami</label>

                        <input v-model="formData.client_info.pasport"
                            v-maska="{ mask: '@@#######', preProcess: val => val.toUpperCase() }" type="text"
                            class="input-field" placeholder="AA1234567">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">JSHSHIR</label>
                        <input v-model="formData.client_info.jshshir" v-maska="'##############'" type="text"
                            class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Pasport berilgan sana</label>
                        <input v-model="formData.client_info.pasport_berilgan_sana" v-maska="'##.##.####'" type="text"
                            class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Pasport amal qilish muddati</label>
                        <input v-model="formData.client_info.pasport_amal_qilish" v-maska="'##.##.####'" type="text"
                            class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Pasport berilgan joy</label>
                        <input :value="formData.client_info.pasport_berilgan_joy"
                            @input="formData.client_info.pasport_berilgan_joy = $event.target.value.toUpperCase()"
                            type="text" class="input-field">
                    </div>
                </div>

                <!-- Bog'lanish uchun kontktlar -->
                <div class="grid grid-cols-1 md:grid-cols-2 mt-8 gap-8">
                    <div
                        class="bg-white p-10 rounded-3xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                        <h3 class="text-2xl font-bold text-slate-800 mb-6">1-shaxs</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Telefon</label>
                                <input v-model="formData.client_info.contacts[0].telefon" v-maska="'+998 ## ### ## ##'"
                                    type="text" class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Qarindoshlik darajasi</label>
                                <select v-model="formData.client_info.contacts[0].qarindoshlik" class="input-field">
                                    <option value="" disabled selected>Tanlang</option>
                                    <option value="ota">Ota</option>
                                    <option value="ona">Ona</option>
                                    <option value="aka">Aka</option>
                                    <option value="opa">Opa</option>
                                    <option value="uka">Uka</option>
                                    <option value="singil">Singil</option>
                                    <option value="turmush_ortoq">Turmush o'rtoq</option>
                                    <option value="farzand">Farzand</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div
                        class="bg-white p-10 rounded-3xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                        <h3 class="text-2xl font-bold text-slate-800 mb-6">2-shaxs</h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Telefon</label>
                                <input v-model="formData.client_info.contacts[1].telefon" v-maska="'+998 ## ### ## ##'"
                                    type="text" class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Qarindoshlik darajasi</label>
                                <select v-model="formData.client_info.contacts[1].qarindoshlik" class="input-field">
                                    <option value="" disabled selected>Tanlang</option>
                                    <option value="ota">Ota</option>
                                    <option value="ona">Ona</option>
                                    <option value="aka">Aka</option>
                                    <option value="opa">Opa</option>
                                    <option value="uka">Uka</option>
                                    <option value="singil">Singil</option>
                                    <option value="turmush_ortoq">Turmush o'rtoq</option>
                                    <option value="farzand">Farzand</option>
                                </select>
                            </div>
                        </div>
                    </div>

                </div>

            </div>

            <!-- 2-QADAM KREDIT-->
            <div v-else-if="currentStep === 2">
                <h2 class="text-2xl font-bold mb-6 text-slate-800">💰 Kredit ma'lumotlari</h2>
                <div class="grid grid-cols-1 md:grid-cols-6 gap-6">
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Shartnoma raqami</label>
                        <input :value="formData.loan_details.shartnoma_raqami"
                            @input="formData.loan_details.shartnoma_raqami = $event.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '')"
                            type="text" class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Shartnoma sanasi</label>
                        <input v-model="formData.loan_details.shartnoma_sana" v-maska="'##.##.####'" type="text"
                            class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Boshlanish sanasi</label>
                        <input v-model="formData.loan_details.boshlanish_sana" v-maska="'##.##.####'" type="text"
                            class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Tugash sanasi</label>
                        <input v-model="formData.loan_details.tugash_sana" v-maska="'##.##.####'" type="text"
                            class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Kredit turi</label>
                        <select v-model="formData.loan_details.kredit_turi" class="input-field">
                            <option value="" disabled selected>Tanlang</option>
                            <option value="mikroqarz">Mikroqarz</option>
                            <option value="mikrokredit">Mikrokredit</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Grafik turi</label>
                        <select v-model="formData.loan_details.grafik_turi" class="input-field">
                            <option value="" disabled selected>Tanlang</option>
                            <option value="annuitet">Annuitet</option>
                            <option value="differensial">Differensial</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mt-4">
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Kredit summasi</label>
                        <input v-model="formData.loan_details.kredit_summasi"
                            v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text" class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Kredit summasi soz bilan</label>
                        <input v-model="formData.loan_details.kredit_summasi_soz" type="text" class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Foiz stavkasi</label>
                        <input v-model="formData.loan_details.foiz_stavkasi" v-maska="'##'" type="text"
                            class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Foiz stavkasi soz bilan</label>
                        <input v-model="formData.loan_details.foiz_stavkasi_soz" type="text" class="input-field">
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mt-4">
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Kredit muddati</label>
                        <input v-model="formData.loan_details.kredit_muddati" v-maska="'##'" type="text"
                            class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Kredit muddati soz bilan</label>
                        <input v-model="formData.loan_details.kredit_muddati_soz" type="text" class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Oylik to'lov</label>
                        <input v-model="formData.loan_details.oylik_tolov"
                            v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text" class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Oylik to'lov soz bilan</label>
                        <input v-model="formData.loan_details.oylik_tolov_soz" type="text" class="input-field">
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-1 gap-6 mt-4">
                    <label class="block text-sm font-bold text-slate-600 mb-1">Grafik matni</label>
                    <textarea v-model="formData.loan_details.grafik_matni" class="input-field resize-y"
                        rows="10"></textarea>
                </div>

            </div>

            <!-- 3-QADAM MOLIYAVIY HOLAT -->
            <div v-else-if="currentStep === 3">
                <h2 class="text-2xl font-bold mb-6 text-slate-800">💰 Moliyaviy holat</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Ish Muassasa</label>
                        <input v-model="formData.financial.ish_muassasa" type="text" class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Ish lavozimi</label>
                        <input v-model="formData.financial.ish_lavozim" type="text" class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Ish joyi manzili</label>
                        <input v-model="formData.financial.ish_manzil" type="text" class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Aloqa Ish Telefon</label>
                        <input v-model="formData.financial.aloqa_ish_tel" v-maska="'+998 ## ###-##-##'" type="text" class="input-field">
                    </div>

                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Aloqa Uy Telefon</label>
                        <input v-model="formData.financial.aloqa_uy_tel" v-maska="'+998 ## ###-##-##'" type="text" class="input-field">
                    </div>
                    <div>
                        <label class="block text-sm font-bold text-slate-600 mb-1">Aloqa Uyali Telefon</label>
                        <input v-model="formData.financial.aloqa_uyali_tel" v-maska="'+998 ## ###-##-##'" type="text" class="input-field">
                    </div>
                </div>
                <!-- Daromad va xarajatlar -->
                <div class="grid grid-cols-1 md:grid-cols-2 mt-8 gap-8">
                    <div
                        class="bg-white p-10 rounded-3xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                        <h3 class="text-2xl font-bold text-slate-800 mb-6">DAROMADLAR</h3>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Asosiy daromad</label>
                                <input v-model="formData.financial.daromad_asosiy"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Orindosh daromad</label>
                                <input v-model="formData.financial.daromad_orindosh"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Boshqa daromad</label>
                                <input v-model="formData.financial.daromad_boshqa"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Jami daromad</label>
                                <input v-model="formData.financial.daromad_jami"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Jami daromad (so'z
                                    bilan)</label>
                                <input v-model="formData.financial.daromad_jami_soz" type="text" class="input-field">
                            </div>
                        </div>
                    </div>
                    <div
                        class="bg-white p-10 rounded-3xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                        <h3 class="text-2xl font-bold text-slate-800 mb-6">XARAJATLAR</h3>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Kommunal xarajatlar</label>
                                <input v-model="formData.financial.xarajat_kommunal"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Oilaviy xarajatlar</label>
                                <input v-model="formData.financial.xarajat_oilaviy"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Boshqa xarajatlar</label>
                                <input v-model="formData.financial.xarajat_boshqa"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Jami xarajatlar</label>
                                <input v-model="formData.financial.xarajat_jami"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Jami xarajatlar (so'z
                                    bilan)</label>
                                <input v-model="formData.financial.xarajat_jami_soz" type="text" class="input-field">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Majburiyatlar -->
                <div class="mt-8">
                    <label class="block text-sm font-bold text-slate-600 mb-2">MAJBURIYATLAR</label>
                    <textarea v-model="formData.financial.majburiyatlar" class="input-field resize-y" rows="2"
                        placeholder="Mavjud majburiyatlar haqida ma'lumot..."></textarea>
                </div>
            </div>

            <!-- 4-QADAM GAROV -->
            <div v-else-if="currentStep === 4">
                <h2 class="text-2xl font-bold mb-6 text-slate-800">🏠 Garov ma'lumotlari</h2>
                <!-- Garov egasini tanlash -->
                <div class="mb-8">
                    <label class="block text-sm font-bold text-slate-600 mb-3">Garov egasi</label>
                    <div class="flex flex-wrap gap-3">
                        <label
                            v-for="opt in [{ v: 'self', l: 'Ozi', i: '👤' }, { v: 'other', l: 'Boshqa', i: '👥' }, { v: 'ishonchnoma', l: 'Bosh ishonchnoma', i: '📜' }]"
                            :key="opt.v"
                            class="flex items-center gap-3 px-4 py-3 border-2 rounded-xl cursor-pointer transition-all"
                            :class="formData.collateral.garov_egasi === opt.v ? 'border-indigo-600 bg-indigo-50' : 'border-slate-100 hover:border-slate-200 bg-white'">
                            <input type="radio" v-model="formData.collateral.garov_egasi" :value="opt.v"
                                class="w-4 h-4 text-indigo-600">
                            <span class="text-xl">{{ opt.i }}</span>
                            <span class="font-bold text-slate-700">{{ opt.l }}</span>
                        </label>
                    </div>
                </div>

                <!-- Garov turini tanlash (Ko'p tanlash imkoniyati bilan) -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                    <div @click="toggleCollateralType('avto')"
                        :class="['p-6 rounded-2xl border-2 cursor-pointer transition-all flex flex-col items-center gap-4',
                            formData.collateral.types.includes('avto') ? 'border-indigo-600 bg-indigo-50 shadow-md transform scale-105' : 'border-slate-100 hover:border-slate-200 bg-white']">
                        <div class="flex items-center justify-center w-full">
                            <input type="checkbox" :checked="formData.collateral.types.includes('avto')"
                                class="w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 mr-auto">
                            <div
                                class="w-16 h-16 rounded-full bg-indigo-100 flex items-center justify-center text-3xl mx-auto">
                                🚗</div>
                            <div class="w-4 h-4 ml-auto invisible"></div> <!-- Alignment uchun -->
                        </div>
                        <div class="text-center">
                            <h3 class="font-bold text-slate-800">Avtomobil</h3>
                            <p class="text-xs text-slate-500">Yengil va yuk transporti</p>
                        </div>
                    </div>

                    <div @click="toggleCollateralType('mulk')"
                        :class="['p-6 rounded-2xl border-2 cursor-pointer transition-all flex flex-col items-center gap-4',
                            formData.collateral.types.includes('mulk') ? 'border-indigo-600 bg-indigo-50 shadow-md transform scale-105' : 'border-slate-100 hover:border-slate-200 bg-white']">
                        <div class="flex items-center justify-center w-full">
                            <input type="checkbox" :checked="formData.collateral.types.includes('mulk')"
                                class="w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 mr-auto">
                            <div
                                class="w-16 h-16 rounded-full bg-emerald-100 flex items-center justify-center text-3xl mx-auto">
                                🏠</div>
                            <div class="w-4 h-4 ml-auto invisible"></div> <!-- Alignment uchun -->
                        </div>
                        <div class="text-center">
                            <h3 class="font-bold text-slate-800">Ko'chmas mulk</h3>
                            <p class="text-xs text-slate-500">Uy-joy, bino, inshoot</p>
                        </div>
                    </div>

                    <div @click="toggleCollateralType('sugurta')"
                        :class="['p-6 rounded-2xl border-2 cursor-pointer transition-all flex flex-col items-center gap-4',
                            formData.collateral.types.includes('sugurta') ? 'border-indigo-600 bg-indigo-50 shadow-md transform scale-105' : 'border-slate-100 hover:border-slate-200 bg-white']">
                        <div class="flex items-center justify-center w-full">
                            <input type="checkbox" :checked="formData.collateral.types.includes('sugurta')"
                                class="w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 mr-auto">
                            <div
                                class="w-16 h-16 rounded-full bg-amber-100 flex items-center justify-center text-3xl mx-auto">
                                📄</div>
                            <div class="w-4 h-4 ml-auto invisible"></div> <!-- Alignment uchun -->
                        </div>
                        <div class="text-center">
                            <h3 class="font-bold text-slate-800">Sug'urta</h3>
                            <p class="text-xs text-slate-500">Sug'urta polisi/shartnomasi</p>
                        </div>
                    </div>
                </div>

                <div class="space-y-12">
                    <!-- Avtomobillar uchun maydonlar -->
                    <div v-if="formData.collateral.types.includes('avto')"
                        class="fade-in space-y-6 pt-6 border-t border-slate-100">
                        <h3 class="text-xl font-bold text-slate-700 flex items-center gap-2">🚗 Avtomobil ma'lumotlari
                        </h3>
                        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Nomi va modeli</label>
                                <input v-model="formData.collateral.avto.nomi" type="text" class="input-field"
                                    placeholder="MASALAN: COBALT">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Ishlab chiqarilgan
                                    yili</label>
                                <input v-model="formData.collateral.avto.yil" v-maska="'####'" type="text"
                                    class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Davlat raqami</label>
                                <input v-model="formData.collateral.avto.davlat_raqami"
                                    @input="formData.collateral.avto.davlat_raqami = $event.target.value.toUpperCase()"
                                    type="text" class="input-field" placeholder="01A123AA">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Rangi</label>
                                <input v-model="formData.collateral.avto.rang" type="text" class="input-field">
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Kuzov raqami</label>
                                <input v-model="formData.collateral.avto.kuzov"
                                    @input="formData.collateral.avto.kuzov = $event.target.value.toUpperCase()"
                                    type="text" class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Dvigatel raqami</label>
                                <input v-model="formData.collateral.avto.dvigatel"
                                    @input="formData.collateral.avto.dvigatel = $event.target.value.toUpperCase()"
                                    type="text" class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Shassi</label>
                                <input v-model="formData.collateral.avto.shassi"
                                    @input="formData.collateral.avto.shassi = $event.target.value.toUpperCase()"
                                    type="text" class="input-field">
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Texpasport seriya va
                                    raqami</label>
                                <input v-model="formData.collateral.avto.texpasport"
                                    @input="formData.collateral.avto.texpasport = $event.target.value.toUpperCase()"
                                    type="text" class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Texpasport berilgan
                                    sana</label>
                                <input v-model="formData.collateral.avto.texpasport_sana" v-maska="'##.##.####'"
                                    type="text" class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Baholangan qiymati</label>
                                <input v-model="formData.collateral.avto.bahosi"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Kuzov turi</label>
                                <select v-model="formData.collateral.avto.kuzov_turi" class="input-field">
                                    <option value="Sedan">Sedan</option>
                                    <option value="Xetchbek">Xetchbek</option>
                                    <option value="Universal">Universal</option>
                                    <option value="Yo'ltanlamas">Yo'ltanlamas</option>
                                    <option value="Boshqa">Boshqa</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Ko'chmas mulk uchun maydonlar -->
                    <div v-if="formData.collateral.types.includes('mulk')"
                        class="fade-in space-y-6 pt-6 border-t border-slate-100">
                        <h3 class="text-xl font-bold text-slate-700 flex items-center gap-2">🏠 Ko'chmas mulk
                            ma'lumotlari</h3>

                        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Mulk turi</label>
                                <select v-model="formData.collateral.mulk.turi" class="input-field">
                                    <option value="" disabled selected>Tanlang</option>
                                    <option value="xonadon">Xonadon</option>
                                    <option value="hovli">Hovli</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Mulk nomi</label>
                                <input v-model="formData.collateral.mulk.nomi" type="text" class="input-field"
                                    placeholder="MASALAN: YAKKA TARTIBDAGI UY-JOY">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Mulk manzili</label>
                                <input v-model="formData.collateral.mulk.manzili" type="text" class="input-field"
                                    placeholder="MASALAN: KALTAMINAR KO'CHASI 1B-UY">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Reestr raqami</label>
                                <input v-model="formData.collateral.mulk.reestr_raqami" type="text" class="input-field">
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Kadastr raqami</label>
                                <input v-model="formData.collateral.mulk.kadastr_raqami" type="text" class="input-field"
                                    placeholder="01.04.2026 y. №23:08:40...">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Umumiy yer maydoni</label>
                                <input v-model="formData.collateral.mulk.umumiy_yer_maydoni" type="text"
                                    class="input-field" placeholder="kv.m">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Qurilish osti maydoni</label>
                                <input v-model="formData.collateral.mulk.qurilish_osti_maydoni" type="text"
                                    class="input-field" placeholder="kv.m">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Umumiy foydali
                                    maydoni</label>
                                <input v-model="formData.collateral.mulk.umumiy_foydali_maydoni" type="text"
                                    class="input-field" placeholder="kv.m">
                            </div>
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Yashash maydoni</label>
                                <input v-model="formData.collateral.mulk.yashash_maydoni" type="text"
                                    class="input-field" placeholder="kv.m">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Baholangan qiymati</label>
                                <input v-model="formData.collateral.mulk.bahosi"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div class="md:col-span-2">
                                <label class="block text-sm font-bold text-slate-600 mb-1">Baholangan qiymati soz
                                    bilan</label>
                                <input v-model="formData.collateral.mulk.bahosi_soz" type="text" class="input-field">
                            </div>
                        </div>
                    </div>

                    <!-- Sug'urta -->
                    <div v-if="formData.collateral.types.includes('sugurta')"
                        class="fade-in space-y-6 pt-6 border-t border-slate-100">
                        <h3 class="text-xl font-bold text-slate-700 flex items-center gap-2">📄 Sug'urta ma'lumotlari
                        </h3>

                        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 text-left">
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Sug'urta kompaniyasi</label>
                                <input :value="formData.collateral.sugurta.kompaniya"
                                    @input="formData.collateral.sugurta.kompaniya = $event.target.value.toUpperCase()"
                                    type="text" class="input-field" placeholder="MASALAN: 'IMPEX INSURANCE'">
                            </div>
                            <div>
                                <label class="block text-sm font-bold text-slate-600 mb-1">Sug'urta summasi</label>
                                <input v-model="formData.collateral.sugurta.summa"
                                    v-maska="{ mask: '### ### ### ### ###', reversed: true }" type="text"
                                    class="input-field">
                            </div>
                            <div class="md:col-span-2">
                                <label class="block text-sm font-bold text-slate-600 mb-1">Sug'urta summasi soz
                                    bilan</label>
                                <input v-model="formData.collateral.sugurta.summa_soz" type="text" class="input-field">
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Garov egasi (Boshqa shaxs) ma'lumotlari -->
                <div
                    class="fade-in space-y-6 pt-6 border-t border-slate-100 mt-12">
                    <h3 class="text-xl font-bold text-slate-700 flex items-center gap-2">👤 Garov egasi ma'lumotlari</h3>
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 text-left">
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">F.I.Sh.</label>
                            <input :value="formData.collateral.owner.fish"
                                @input="handleFishInput($event, formData.collateral.owner)" type="text"
                                class="input-field" placeholder="MASALAN: ANVAR G'ANIYEV">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">F.I.Sh. inisiali</label>
                            <input v-model="formData.collateral.owner.fish_inisiali" type="text" class="input-field">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Tug'ilgan sana</label>
                            <input v-model="formData.collateral.owner.tugilgan_sana" v-maska="'##.##.####'" type="text"
                                class="input-field" placeholder="10.02.1987">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Jinsi</label>
                            <select v-model="formData.collateral.owner.jinsi" class="input-field">
                                <option value="" disabled selected>Tanlang</option>
                                <option value="erkak">Erkak</option>
                                <option value="ayol">Ayol</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Telefon</label>
                            <input v-model="formData.collateral.owner.telefon" v-maska="'+998 ## ### ## ##'" type="text"
                                class="input-field" placeholder="+998 90 971-01-11">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Pasport</label>
                            <input v-model="formData.collateral.owner.pasport"
                                v-maska="{ mask: '@@#######', preProcess: val => val.toUpperCase() }" type="text"
                                class="input-field" placeholder="AD1073617">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">JSHSHIR</label>
                            <input v-model="formData.collateral.owner.jshshir" v-maska="'##############'" type="text"
                                class="input-field" placeholder="31002873680015">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Pasport berilgan sana</label>
                            <input v-model="formData.collateral.owner.pasport_berilgan_sana" v-maska="'##.##.####'"
                                type="text" class="input-field" placeholder="10.02.1987">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Pasport amal qilish muddati</label>
                            <input v-model="formData.collateral.owner.pasport_amal_qilish" v-maska="'##.##.####'"
                                type="text" class="input-field" placeholder="10.02.1987">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Pasport berilgan joy</label>
                            <input :value="formData.collateral.owner.pasport_berilgan_joy"
                                @input="formData.collateral.owner.pasport_berilgan_joy = $event.target.value.toUpperCase()"
                                type="text" class="input-field">
                        </div>
                        </div>
                </div>

                <!-- Bosh ishonchnoma -->
                <div v-if="formData.collateral.garov_egasi === 'ishonchnoma'" 
                    class="fade-in space-y-6 pt-6 border-t border-slate-100 mt-12">
                    <h3 class="text-xl font-bold text-slate-700 flex items-center gap-2">📜 Bosh ishonchnoma ma'lumotlari</h3>
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 text-left">
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Notarius F.I.Sh.</label>
                            <input v-model="formData.collateral.ishonchnoma.notarius_fish"
                                @input="formData.collateral.ishonchnoma.notarius_fish = $event.target.value.toUpperCase()"
                                type="text" class="input-field">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Notarius manzili</label>
                            <input v-model="formData.collateral.ishonchnoma.notarius_address"
                                @input="formData.collateral.ishonchnoma.notarius_address = $event.target.value.toUpperCase()"
                                type="text" class="input-field">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Notarius reestr raqami</label>
                            <input v-model="formData.collateral.ishonchnoma.notarius_reestr_raqami"
                                @input="formData.collateral.ishonchnoma.notarius_reestr_raqami = $event.target.value.toUpperCase()"
                                type="text" class="input-field">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-600 mb-1">Ishonchnoma berilgan sana</label>
                            <input v-model="formData.collateral.ishonchnoma.notarius_berilgan_sana"
                                v-maska="'##.##.####'" type="text" class="input-field" placeholder="10.02.1987">
                        </div>
                    </div>
                 </div>
            </div>


            <!-- PASTA TUGMALAR -->
            <div class="mt-auto pt-10 flex justify-between">
                <button @click="prevStep" :disabled="currentStep === 1"
                    class="px-8 py-3 rounded-xl bg-slate-100 font-bold hover:bg-slate-200 disabled:opacity-30">
                    Orqaga
                </button>

                <!-- :disabled="!isStepValid" - mana shu qism tugmani qulflab qo'yadi -->
                <button v-if="currentStep < 4" @click="nextStep"
                    class="px-10 py-3 rounded-xl font-bold transition-all shadow-lg bg-indigo-600 text-white hover:bg-indigo-700">
                    Keyingisi
                </button>

                <button v-else @click="saveForm" class="px-10 py-3 rounded-xl bg-green-500 text-white font-bold">
                    Saqlash
                </button>
            </div>
        </div>
    </div>

    <!-- Live JSON Preview (Formaning eng pastiga qo'shiladi) -->
    <div class="mt-12 bg-slate-900 rounded-3xl p-8 shadow-2xl border border-slate-800 overflow-hidden">
        <div class="flex justify-between items-center mb-4 border-b border-slate-800 pb-4">
            <span class="text-slate-500 uppercase text-xs font-black tracking-[0.2em]">Jonli ma'lumotlar (Live
                JSON)</span>
            <div class="flex gap-1">
                <div class="w-2 h-2 rounded-full bg-red-500"></div>
                <div class="w-2 h-2 rounded-full bg-yellow-500"></div>
                <div class="w-2 h-2 rounded-full bg-green-500"></div>
            </div>
        </div>
        <!-- JSON ko'rinishi -->
        <pre
            class="text-emerald-400 font-mono text-sm overflow-x-auto leading-relaxed whitespace-pre-wrap break-all">{{ formData }}</pre>
    </div>

</template>
