# 法律樓 AI 系統 MVP

## 專案簡介

本案為法律樓 AI 系統之 MVP（Minimum Viable Product），展示 AI 輔助法律服務之核心功能。

## 功能列表

1. **自然語言查詢（NLU Query）** - 支援使用者以自然語言提問，系統解析語意並回應
2. **文件分析（Document Analysis）** - 上傳法律文件，AI 自動分析關鍵條款與風險點
3. **案例檢索（Case Retrieval）** - 快速搜尋相似案例與相關法條
4. **智慧分類（Smart Classification）** - 自動分類案件類型與法律領域
5. **術語解釋（Terminology Explainer）** - 查詢法律術語之定義與適用情境
6. **合約生成（Contract Drafting）** - 依據模板與輸入條件生成合約草稿
7. **法規更新（Regulation Updates）** - 追蹤最新法規異動並通知相關當事人
8. **會議紀錄（Meeting Minutes）** - 自動生成會議摘要與待辦事項
9. **翻譯服務（Translation Service）** - 中英雙語法律文件互譯
10. **行事曆整合（Calendar Integration）** - 與 Outlook/Google Calendar 同步庭期與期限
11. **收費計算（Fee Calculator）** - 依案件複雜度與時間估算律師費用

## 安裝方式

```bash
pip install -r requirements.txt
python app.py
```

啟動後開啟瀏覽器造訪：http://localhost:5000

## 系統架構

```
┌─────────────────────────────────────────┐
│            Frontend (Web UI)            │
├─────────────────────────────────────────┤
│            Flask API Server             │
│         (flask / flask-cors)            │
├─────────────────────────────────────────┤
│          AI Processing Layer            │
│  (NLU / Document Analysis / Search)     │
└─────────────────────────────────────────┘
```

## 演示說明

**注意：本 MVP 採用模擬資料（Mock Data）展示系統功能。所有 AI 回應均為預設回覆，實際整合大型語言模型（LLM）將於下一階段完成。**

---

*法律樓 AI 系統 MVP - 2026*
