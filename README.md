# 法律樓 AI 系統 MVP | Law Firm AI System MVP

![Status](https://img.shields.io/badge/status-MVP-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Vercel](https://img.shields.io/badge/Vercel-Ready-black)

律師樓內部 AI 系統，用於法律文件自動化處理。

## 功能 | Features

- 💬 **AI 法律助理** - Telegram Bot 風格介面
- 📜 **法例查詢** - RAG 知識庫即時檢索香港法例
- ⚖️ **案例分析** - 智能分析案件要點及法律爭議
- 📝 **文件生成** - 自動生成判詞、律師信
- 📊 **BI 數據大屏** - 視覺化系統使用統計
- 🔐 **管理後台** - 檔案管理、用戶權限控制

## 部署 | Deployment

### Vercel (推薦)

1. Fork 此專案
2. 在 [Vercel](https://vercel.com) Import 專案
3. Deploy！

```bash
# 或者使用 Vercel CLI
npm i -g vercel
vercel
```

### 本地運行

```bash
pip install -r requirements.txt
python app.py
# 打开 http://localhost:5000
```

## 架構 | Architecture

```
├── api/                  # Vercel Serverless Functions
│   ├── chat.py          # AI 聊天接口
│   ├── dashboard.py    # 數據大屏接口
│   ├── files.py         # 檔案管理接口
│   └── generate.py      # 文檔生成接口
├── public/              # 靜態文件
│   ├── index.html
│   ├── style.css
│   └── app.js
├── mock_data/           # 模擬數據
│   ├── hk_laws.json     # 香港法例
│   ├── sample_cases.json # 案例
│   └── templates.json   # 範本
├── vercel.json          # Vercel 配置
└── requirements.txt     # Python 依賴
```

## 技術棧 | Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JS
- **Backend**: Python Serverless (Vercel)
- **Design**: Dark Luxury Theme (#0a0a0f + #d4af37)

## 聲明 | Disclaimer

此為 MVP 演示版本，所有 AI 回應為模擬數據，僅供展示用途。

---
Made with ♥ for Hong Kong Legal Industry
