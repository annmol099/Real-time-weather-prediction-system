// ===== SIMPLE HOVER EFFECTS =====
document.querySelectorAll('.card, .day-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-10px)';
    });
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
    });
});

// ===== BUTTON LOADING =====
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
        const btn = form.querySelector('button');
        btn.style.opacity = '0.7';
        btn.textContent = 'Loading...';
    });
});