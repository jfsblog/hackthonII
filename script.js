// Sticky nav
const nav = document.getElementById('main-nav');
const header = document.getElementById('main-header');
// 請確保 header 這個元素確實存在，不然會報錯
const headerHeight = header ? header.offsetHeight : 0; 


window.addEventListener('scroll', () => {
    if(window.scrollY >= headerHeight){
        nav.classList.add('fixed');
    } else {
        nav.classList.remove('fixed');
    }
});

// Back to top
const backtotop = document.getElementById("backtotop");
window.addEventListener('scroll', () => {
    backtotop.style.display = (window.scrollY > 300) ? "block" : "none";
});
backtotop.onclick = () => {
    window.scrollTo({top:0, behavior:'smooth'});
};

// Hamburger
function toggleNav() {
    // 這個函式已經正確地切換了 #main-nav 上的 responsive 類別
    nav.classList.toggle("responsive");
}