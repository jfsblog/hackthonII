// ====================================
// 1. 響應式網頁設計 (RWD) 漢堡選單的開關邏輯
// ====================================
const hamburger = document.getElementById('hamburger'); // 取得漢堡圖示 (觸發按鈕)
const navMenu = document.getElementById('navMenu');     // 取得導覽選單區塊

// 監聽漢堡圖示的點擊事件
hamburger.addEventListener('click', () => {
    // 點擊時切換漢堡圖示的 'active' 狀態 (用於改變圖示樣式，例如變成 X)
    hamburger.classList.toggle('active');
    
    // ⭐ 漢堡選單無法展開的可能原因：CSS 中 .navMenu.active 的樣式設定遺失
    // 點擊時切換導覽選單的 'active' 狀態 (用於顯示/隱藏選單)
    navMenu.classList.toggle('active');
});

// 點擊選單項目後，自動關閉已展開的選單 (優化手機和平板的使用體驗)
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        // 移除漢堡圖示和導覽選單的 'active' 狀態，將選單關閉
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});


// ====================================
// 2. 媒體畫廊：主顯示區塊的媒體內容切換邏輯 (解決初始化時無法顯示媒體的問題)
// ====================================
const mainMediaViewer = document.getElementById('mainMediaViewer');       // 主媒體顯示區塊 (大型圖片或影片)
// const thumbnails = document.querySelectorAll('.thumbnail-gallery-scroll img'); // 所有縮圖列表

function switchMedia(mediaType, mediaSrc) {
    // 1. 清空主顯示區塊目前的內容
    mainMediaViewer.innerHTML = '';
    
    let mediaElement;

    if (mediaType === 'video') {
        // 媒體類型為影片：創建 <video> 元素
        mediaElement = document.createElement('video');
        mediaElement.src = mediaSrc;
        mediaElement.controls = true; // 啟用影片播放控制列
        
        // 遊戲平台/商品頁面常見的影片自動播放設定
        mediaElement.autoplay = true;       // 自動播放
        mediaElement.loop = true;           // 循環播放
        mediaElement.muted = true;          // 預設靜音 (符合瀏覽器自動播放政策)
        mediaElement.playsinline = true;   // 允許在行動裝置上行內播放
        
    } else if (mediaType === 'image') {
        // 媒體類型為圖片：創建 <img> 元素
        mediaElement = document.createElement('img');
        mediaElement.src = mediaSrc;
    }
    
    // 2. 如果成功創建了媒體元素，則將其加入到主顯示區塊中
    if (mediaElement) {
        mainMediaViewer.appendChild(mediaElement);
    }
}

// ====================================
// 3. 監聽所有縮圖的點擊事件 (媒體內容切換的主要觸發點)
// ====================================
const thumbnails = document.querySelectorAll('.thumbnail-item');

thumbnails.forEach(thumb => {
    thumb.addEventListener('click', () => {
        // 移除這行：const img = thumb.querySelector('img'); 
        // ✅ 修正：直接從父層元素 thumb (div.thumbnail-item) 上獲取屬性
        const mediaType = thumb.getAttribute('data-media-type');
        const mediaSrc = thumb.getAttribute('data-media-src');

        switchMedia(mediaType, mediaSrc);

        thumbnails.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
    });
});

// ====================================
// 4. 頁面初始化：確保頁面載入時主顯示區塊有內容顯示
// ====================================
if (thumbnails.length > 0) {
    const defaultThumb = thumbnails[0];                        // 取得第一個縮圖作為預設媒體
    const defaultType = defaultThumb.getAttribute('data-media-type');
    const defaultSrc = defaultThumb.getAttribute('data-media-src');
    
    // 將第一個縮圖設為 active 狀態
    defaultThumb.classList.add('active');
    
    // 載入並顯示預設的第一個媒體 (通常是影片或封面圖)
    switchMedia(defaultType, defaultSrc);
}


// ====================================
// 4. TOC
// ====================================
document.addEventListener("DOMContentLoaded", function() {
    // ===== 收合/展開 h2 =====
    const headers = document.querySelectorAll(".content-section h2");

    headers.forEach(h2 => {
        const content = h2.nextElementSibling;

        // 若預設開啟
        if(content.classList.contains("open")) {
            content.style.maxHeight = content.scrollHeight + "px";
            h2.classList.add("active");
        }

        h2.addEventListener("click", () => {
            content.classList.toggle("open");
            h2.classList.toggle("active");

            if (content.classList.contains("open")) {
                content.style.maxHeight = content.scrollHeight + "px";
            } else {
                content.style.maxHeight = 0;
            }
        });
    });

    // ===== 生成 TOC =====
    const toc = document.getElementById("toc");
    if (toc) {
        toc.innerHTML = ""; // 先清空
        const title = document.createElement("h3");
        title.textContent = "內容索引";
        toc.appendChild(title);
        const ul = document.createElement("ul");
        headers.forEach((h2, i) => {
            if (!h2.id) h2.id = "section-" + i;
            const li = document.createElement("li");
            const a = document.createElement("a");
            a.href = "#" + h2.id;
            a.textContent = h2.textContent;
            li.appendChild(a);
            ul.appendChild(li);
        });
        toc.appendChild(ul);
    }
});


// ====================================
// TopBtn
// ====================================

const scrollBtn = document.getElementById("scrollTopBtn");

// 滾動時顯示或隱藏按鈕
window.addEventListener("scroll", () => {
    if (window.scrollY > 200) { // 滾動超過 200px 顯示
        scrollBtn.style.display = "block";
    } else {
        scrollBtn.style.display = "none";
    }
});

// 點擊捲回頂部
scrollBtn.addEventListener("click", () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});
