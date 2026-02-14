// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function() {
    var toggle = document.getElementById('navToggle');
    var links = document.getElementById('navLinks');
    if (toggle && links) {
        toggle.addEventListener('click', function() {
            links.classList.toggle('open');
        });
    }

    // Dark mode toggle
    var themeToggle = document.getElementById('themeToggle');
    var html = document.documentElement;
    var saved = localStorage.getItem('theme');
    if (saved) {
        html.setAttribute('data-theme', saved);
        updateToggleIcon(saved);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            var current = html.getAttribute('data-theme');
            var next = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
            updateToggleIcon(next);
        });
    }

    function updateToggleIcon(theme) {
        if (themeToggle) {
            themeToggle.textContent = theme === 'dark' ? '\u2600' : '\u263E';
        }
    }

    // Box detail toggle
    window.toggleBoxDetail = function(purchaseId) {
        var row = document.getElementById('box-detail-' + purchaseId);
        if (row) {
            row.style.display = row.style.display === 'none' ? '' : 'none';
        }
    };

    // Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s';
            setTimeout(function() { alert.remove(); }, 300);
        }, 5000);
    });
});
