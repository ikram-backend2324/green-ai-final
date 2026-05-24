// GreenAI — Main JS

document.addEventListener('DOMContentLoaded', function () {
    // Sidebar toggle
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    if (toggle && sidebar) {
        toggle.addEventListener('click', function () { sidebar.classList.toggle('open'); });
        document.addEventListener('click', function (e) {
            if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }

    // Current date
    const dateEl = document.getElementById('currentDate');
    if (dateEl) {
        const now = new Date();
        dateEl.textContent = now.toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });
    }

    // Auto-dismiss alerts
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(function () { alert.remove(); }, 500);
        }, 5000);
    });

    // Apply language on load
    const lang = getLang();
    applyTranslations(lang);
    const labels = { en: 'EN', ru: 'RU', uz: 'UZ' };
    const el = document.getElementById('currentLang');
    if (el) el.textContent = labels[lang] || 'EN';
    document.querySelectorAll('.lang-option').forEach(function (btn) {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });
    updateOptimizeLinks(lang);
});

// ── Translations ──────────────────────────────────────────────
const TRANSLATIONS = {
    en: {
        'Dashboard': 'Dashboard',
        'Energy Sources': 'Energy Sources',
        'AI Optimization': 'AI Optimization',
        'Analytics': 'Analytics',
        'Admin Panel': 'Admin Panel',
        'Admin': 'Admin',
        'User': 'User',
        'Total Energy Output': 'Total Energy Output',
        'CO₂ Saved': 'CO₂ Saved',
        'Avg Efficiency': 'Avg Efficiency',
        'Active Sources': 'Active Sources',
        'Add Energy Source': 'Add Energy Source',
        'Run AI Optimization': 'Run AI Optimization',
        'Recent Optimizations': 'Recent Optimizations',
        'Recent Energy Readings': 'Recent Energy Readings',
        'View all sources': 'View all sources →',
        'No energy sources yet.': 'No energy sources yet.',
        'No optimizations run yet.': 'No optimizations run yet.',
        'No readings recorded yet.': 'No readings recorded yet.',
        'Add Reading': 'Add Reading',
        'Back': 'Back',
        'Details': 'Details',
        'Optimize': 'Optimize',
        'View All': 'View All',
        'Source': 'Source',
        'Timestamp': 'Timestamp',
        'Output (kWh)': 'Output (kWh)',
        'Efficiency': 'Efficiency',
        'Save Reading': 'Save Reading',
        'Cancel': 'Cancel',
        'AI Recommendation': 'AI Recommendation',
        'Suggested Actions': 'Suggested Actions',
        'Raw AI Response': 'Raw AI Response',
        'Total Output': 'Total Output',
        'Optimizations Run': 'Optimizations Run',
        'Output Trend': 'Output Trend',
        'Output by Source Type': 'Output by Source Type',
        'AI Optimization for Green Energy': 'AI Optimization for Green Energy',
        'Welcome back': 'Welcome back',
        'Sign in to your account': 'Sign in to your account',
        'Username': 'Username',
        'Password': 'Password',
        'Sign In': 'Sign In',
        'Create Account': 'Create Account',
        'Join GreenAI and start optimizing': 'Join GreenAI and start optimizing',
        "Don't have an account?": "Don't have an account?",
        'Already have an account?': 'Already have an account?',
        'Email': 'Email',
        'Company': 'Company',
        'Confirm': 'Confirm',
        'Source Name': 'Source Name',
        'Source Type': 'Source Type',
        'Capacity (kW)': 'Capacity (kW)',
        'Status': 'Status',
        'Location': 'Location',
        'Installation Date': 'Installation Date',
        'Description': 'Description',
        'Create Source': 'Create Source',
        'New Energy Source': 'New Energy Source',
    },
    ru: {
        'Dashboard': 'Панель управления',
        'Energy Sources': 'Источники энергии',
        'AI Optimization': 'ИИ Оптимизация',
        'Analytics': 'Аналитика',
        'Admin Panel': 'Панель администратора',
        'Admin': 'Администратор',
        'User': 'Пользователь',
        'Total Energy Output': 'Общая выработка энергии',
        'CO₂ Saved': 'Сэкономлено CO₂',
        'Avg Efficiency': 'Средняя эффективность',
        'Active Sources': 'Активные источники',
        'Add Energy Source': 'Добавить источник',
        'Run AI Optimization': 'Запустить ИИ оптимизацию',
        'Recent Optimizations': 'Последние оптимизации',
        'Recent Energy Readings': 'Последние показания',
        'View all sources': 'Все источники →',
        'No energy sources yet.': 'Источники энергии не добавлены.',
        'No optimizations run yet.': 'Оптимизации ещё не запускались.',
        'No readings recorded yet.': 'Показания ещё не записаны.',
        'Add Reading': 'Добавить показание',
        'Back': 'Назад',
        'Details': 'Подробнее',
        'Optimize': 'Оптимизировать',
        'View All': 'Все',
        'Source': 'Источник',
        'Timestamp': 'Время',
        'Output (kWh)': 'Выработка (кВт·ч)',
        'Efficiency': 'Эффективность',
        'Save Reading': 'Сохранить показание',
        'Cancel': 'Отмена',
        'AI Recommendation': 'Рекомендация ИИ',
        'Suggested Actions': 'Предлагаемые действия',
        'Raw AI Response': 'Ответ ИИ (JSON)',
        'Total Output': 'Общая выработка',
        'Optimizations Run': 'Запущено оптимизаций',
        'Output Trend': 'Динамика выработки',
        'Output by Source Type': 'Выработка по типу источника',
        'AI Optimization for Green Energy': 'ИИ оптимизация зелёной энергетики',
        'Welcome back': 'Добро пожаловать',
        'Sign in to your account': 'Войдите в аккаунт',
        'Username': 'Имя пользователя',
        'Password': 'Пароль',
        'Sign In': 'Войти',
        'Create Account': 'Создать аккаунт',
        'Join GreenAI and start optimizing': 'Присоединитесь к GreenAI',
        "Don't have an account?": 'Нет аккаунта?',
        'Already have an account?': 'Уже есть аккаунт?',
        'Email': 'Электронная почта',
        'Company': 'Компания',
        'Confirm': 'Подтвердить',
        'Source Name': 'Название источника',
        'Source Type': 'Тип источника',
        'Capacity (kW)': 'Мощность (кВт)',
        'Status': 'Статус',
        'Location': 'Местоположение',
        'Installation Date': 'Дата установки',
        'Description': 'Описание',
        'Create Source': 'Создать источник',
        'New Energy Source': 'Новый источник энергии',
    },
    uz: {
        'Dashboard': 'Boshqaruv paneli',
        'Energy Sources': 'Energiya manbalari',
        'AI Optimization': 'AI Optimallashtirish',
        'Analytics': 'Tahlil',
        'Admin Panel': 'Admin panel',
        'Admin': 'Administrator',
        'User': 'Foydalanuvchi',
        'Total Energy Output': 'Jami energiya ishlab chiqarish',
        'CO₂ Saved': 'Tejab qolingan CO₂',
        'Avg Efficiency': "O'rtacha samaradorlik",
        'Active Sources': 'Faol manbalar',
        'Add Energy Source': "Energiya manbai qo'shish",
        'Run AI Optimization': 'AI optimallashtirish',
        'Recent Optimizations': "So'nggi optimallashtirishlar",
        'Recent Energy Readings': "So'nggi ko'rsatkichlar",
        'View all sources': 'Barcha manbalar →',
        'No energy sources yet.': "Energiya manbalari hali yo'q.",
        'No optimizations run yet.': 'Hali optimallashtirishlar amalga oshirilmagan.',
        'No readings recorded yet.': "Hali ko'rsatkichlar kiritilmagan.",
        'Add Reading': "Ko'rsatkich qo'shish",
        'Back': 'Orqaga',
        'Details': 'Batafsil',
        'Optimize': 'Optimallashtirish',
        'View All': 'Barchasi',
        'Source': 'Manba',
        'Timestamp': 'Vaqt',
        'Output (kWh)': 'Ishlab chiqarish (kVt/soat)',
        'Efficiency': 'Samaradorlik',
        'Save Reading': "Ko'rsatkichni saqlash",
        'Cancel': 'Bekor qilish',
        'AI Recommendation': 'AI tavsiyasi',
        'Suggested Actions': 'Tavsiya etilgan harakatlar',
        'Raw AI Response': 'AI javobi (JSON)',
        'Total Output': 'Jami ishlab chiqarish',
        'Optimizations Run': 'Optimallashtirishlar soni',
        'Output Trend': 'Ishlab chiqarish tendensiyasi',
        'Output by Source Type': "Manba turi bo'yicha ishlab chiqarish",
        'AI Optimization for Green Energy': "Yashil energiya uchun AI optimallashtirish",
        'Welcome back': 'Xush kelibsiz',
        'Sign in to your account': 'Hisobingizga kiring',
        'Username': 'Foydalanuvchi nomi',
        'Password': 'Parol',
        'Sign In': 'Kirish',
        'Create Account': 'Hisob yaratish',
        'Join GreenAI and start optimizing': "GreenAI'ga qo'shiling",
        "Don't have an account?": "Hisobingiz yo'qmi?",
        'Already have an account?': 'Hisobingiz bormi?',
        'Email': 'Elektron pochta',
        'Company': 'Kompaniya',
        'Confirm': 'Tasdiqlash',
        'Source Name': 'Manba nomi',
        'Source Type': 'Manba turi',
        'Capacity (kW)': 'Quvvat (kVt)',
        'Status': 'Holat',
        'Location': 'Joylashuv',
        'Installation Date': "O'rnatish sanasi",
        'Description': 'Tavsif',
        'Create Source': "Manba yaratish",
        'New Energy Source': "Yangi energiya manbai",
    }
};

function applyTranslations(lang) {
    const t = TRANSLATIONS[lang];
    if (!t) return;
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
        const key = el.dataset.i18n;
        if (t[key] !== undefined) el.textContent = t[key];
    });
    // Also translate placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
        const key = el.dataset.i18nPlaceholder;
        if (t[key] !== undefined) el.placeholder = t[key];
    });
}