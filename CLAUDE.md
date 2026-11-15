# 太陽電玩組件庫：給 Claude 的工作說明

這是 Ching（太陽電玩）的網頁組件庫。只要 Ching 請你設計、製作或修改任何網頁（教學網站、教學總站、8591 工具、交易機器人儀表板、後台），**先從這裡取用組件**，不要從零自己寫外觀。

## Ching 的設計要求（一定要遵守）
- 要「專業、高級、不花俏」：參考 Vercel、Linear、Stripe、Apple 的質感。
- 禁止：置中標題＋三張一樣的 icon 卡片、紫藍色漸層、到處發光、表情符號裝飾、每塊都同一種圓角卡片。
- 一頁只用一個亮點（一種動態效果或一道晨曦金光），其他保持安靜。
- 所有介面文字用繁體中文，回覆 Ching 也只用繁體中文。
- 只能上下捲動，任何寬度（手機 320px）都不能出現左右捲動；表格在手機上改卡片。
- 一次做完整：載入中、空資料、錯誤、手機版、深淺色都要處理。
- 改動前先說計畫，Ching 確認後才建立或傳送檔案。

## 資料夾
- `core/tokens.css`：設計變數（顏色、字級、間距、圓角）。唯一重點色是 `--sun`（晨曦金）。淺色預設，系統深色或 `data-theme="dark"` 時切深色。
- `core/base.css`：基礎樣式與共用元件（`.btn` `.btn-primary` `.btn-sun` `.btn-ghost` `.badge` `.kbd` `.input` `.select` `.textarea` `.field` `.label` `.hint` `.panel` `.section` `.section-head` `.container` `.num`）。
- `components/*.html`：組件「片段」（只有自己的 style、標記、script），開頭註解寫名稱、分類、說明、來源、適用、高度。**要改組件就改這裡。**
- `dist/*.html`：建置後的完整單一 HTML，可直接開啟或整份複製使用。
- `templates/*.html`：多個組件組成的整頁範本（目前有 `landing.html` 首頁範本）。
- `components.json`：所有組件的清單，先讀它挑組件。
- `index.html`：預覽目錄頁（給 Ching 看的）。
- `originals/`：從 Magic UI、shadcn/ui 抓下來的原始 React 程式碼（MIT 授權，附 LICENSE），改寫新組件時拿來參考。

## 怎麼用
1. 讀 `components.json`，依 Ching 的需求挑組件（對外頁面挑「對外／通用」，工具頁挑「自用／通用」）。
2. 組一頁時：一份 `tokens.css` + `base.css`，再依序貼上各組件片段的內容。各組件的 class 與 id 都有自己的前綴，不會互相衝突。
3. 依真實內容改文字與資料；顏色一律用變數，不要寫死色碼。
4. 完成後用瀏覽器在 360px 與 1280px 各檢查一次，確認沒有橫向捲動、沒有錯誤。

## 新增組件
1. 在 `components/` 新增片段，開頭照現有格式寫註解；class 用 2～3 個字母的專屬前綴。
2. 若改寫自開源專案，把原始碼放進 `originals/<專案>/` 並保留授權檔；只收可商用的授權（MIT、Apache 等）。21st 上的組件授權各不相同，取用前要確認。
3. 執行 `python3 build.py` 重新產生 `dist/`、`templates/`、`components.json`、`index.html`。
4. 提交並推送。

## 21st
21st.dev 可免費搜尋組件，但免費帳號每天只能取得 2 次組件程式碼。優先從原本就公開的開源專案（Magic UI、shadcn/ui、Origin UI 等）取得，真的只有 21st 有的才動用每日額度。
