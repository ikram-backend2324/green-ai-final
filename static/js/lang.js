// Language persistence — saves to both sessionStorage and cookie
// so Django can read it server-side

function getLang() {
    return sessionStorage.getItem('greenai_lang') || getCookie('greenai_lang') || 'en';
}

function setLang(lang) {
    sessionStorage.setItem('greenai_lang', lang);
    // Save to cookie so Django can read it
    document.cookie = `greenai_lang=${lang};path=/;max-age=86400`;

    applyTranslations(lang);

    const labels = { en: 'EN', ru: 'RU', uz: 'UZ' };
    const el = document.getElementById('currentLang');
    if (el) el.textContent = labels[lang] || 'EN';

    document.querySelectorAll('.lang-option').forEach(function (btn) {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    // Update all "Optimize" links to include ?lang=xx
    updateOptimizeLinks(lang);
}

function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
}

function updateOptimizeLinks(lang) {
    document.querySelectorAll('a[href*="/optimization/run/"]').forEach(function(link) {
        const url = new URL(link.href);
        url.searchParams.set('lang', lang);
        link.href = url.toString();
    });
}

function toggleLangMenu() {
    const menu = document.getElementById('langMenu');
    const btn = document.getElementById('langToggle');
    if (!menu) return;
    const isOpen = menu.classList.contains('open');
    menu.classList.toggle('open', !isOpen);
    btn.classList.toggle('open', !isOpen);
}

document.addEventListener('click', function (e) {
    const switcher = document.querySelector('.lang-switcher');
    if (switcher && !switcher.contains(e.target)) {
        const menu = document.getElementById('langMenu');
        const btn = document.getElementById('langToggle');
        if (menu) menu.classList.remove('open');
        if (btn) btn.classList.remove('open');
    }
});