document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const darkModeCSS = document.getElementById('dark-mode-css');
    const html = document.documentElement;

    // Initialize theme
    const currentTheme = localStorage.getItem('theme') || 'light';
    if (currentTheme === 'dark') {
        html.setAttribute('data-theme', 'dark');
        darkModeCSS.disabled = false;
    } else {
        darkModeCSS.disabled = true;
    }

    // Toggle theme
    themeToggle.addEventListener('click', function() {
        if (html.getAttribute('data-theme') === 'dark') {
            html.setAttribute('data-theme', 'light');
            darkModeCSS.disabled = true;
            localStorage.setItem('theme', 'light');
        } else {
            html.setAttribute('data-theme', 'dark');
            darkModeCSS.disabled = false;
            localStorage.setItem('theme', 'dark');
        }
    });
});