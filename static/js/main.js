/**
 * Wanderlust Tour & Travel - Master Frontend Logic
 * Warm Boutique & Earthy Aesthetic Edition
 */

(function () {
    'use strict';

    // ==========================================
    // Theme Manager (Light / Dark Earthy Mode)
    // ==========================================
    const THEME_KEY = 'wanderlust_theme';

    function getPreferredTheme() {
        const saved = localStorage.getItem(THEME_KEY);
        if (saved) return saved;
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(THEME_KEY, theme);

        const isDark = theme === 'dark';
        const buttons = [
            document.getElementById('desktopThemeToggle'),
            document.getElementById('mobileThemeToggle')
        ];

        buttons.forEach(btn => {
            if (!btn) return;
            btn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
            btn.setAttribute('title', isDark ? 'Switch to light mode' : 'Switch to dark mode');
        });
    }

    function toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme') || 'light';
        const next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
    }

    // Initialize Theme immediately on DOM ready
    document.addEventListener('DOMContentLoaded', function () {
        applyTheme(getPreferredTheme());

        const desktopToggle = document.getElementById('desktopThemeToggle');
        const mobileToggle = document.getElementById('mobileThemeToggle');

        if (desktopToggle) desktopToggle.addEventListener('click', toggleTheme);
        if (mobileToggle) mobileToggle.addEventListener('click', toggleTheme);

        // Listen for OS system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (!localStorage.getItem(THEME_KEY)) {
                applyTheme(e.matches ? 'dark' : 'light');
            }
        });

        // ==========================================
        // Sticky Navbar Effect
        // ==========================================
        const navbar = document.querySelector('.navbar-custom');
        function handleNavbarScroll() {
            if (!navbar) return;
            if (window.scrollY > 40) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        }
        window.addEventListener('scroll', handleNavbarScroll, { passive: true });
        handleNavbarScroll();

        // ==========================================
        // Back to Top Button
        // ==========================================
        const backToTopBtn = document.getElementById('back-to-top');
        if (backToTopBtn) {
            window.addEventListener('scroll', function () {
                if (window.scrollY > 350) {
                    backToTopBtn.classList.add('show');
                } else {
                    backToTopBtn.classList.remove('show');
                }
            }, { passive: true });

            backToTopBtn.addEventListener('click', function () {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }

        // ==========================================
        // Bootstrap Tooltips & Popovers
        // ==========================================
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (el) {
                return new bootstrap.Tooltip(el);
            });
        }

        // ==========================================
        // Smooth Anchor Scrolling for on-page links
        // ==========================================
        document.querySelectorAll('a[href^="#"]:not([data-bs-toggle])').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const targetId = this.getAttribute('href');
                if (targetId && targetId !== '#') {
                    const targetEl = document.querySelector(targetId);
                    if (targetEl) {
                        e.preventDefault();
                        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }
            });
        });
    });
})();
