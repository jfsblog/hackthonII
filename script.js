const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

// 監聽漢堡圖示點擊事件
hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// 點擊選單項目後自動關閉選單 (RWD 體驗優化)
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});