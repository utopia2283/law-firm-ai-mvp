from datetime import datetime
import json
import os

def load_json(filename):
    path = os.path.join(os.getcwd(), 'mock_data', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

templates = load_json('templates.json')

def handler(request):
    if request.method == 'POST':
        try:
            data = request.get_json()
            user_msg = data.get('message', '')
            
            msg_lower = user_msg.lower()
            
            if '法律' in user_msg or 'law' in msg_lower:
                content = '根據香港法例第1條公司法第十四款，公司章程細則一經登記，公司即成為合法法人組織，得以公司名義進行各項法律行為。如需更詳細的法律意見，請聯絡我們的專業團隊。'
            elif '破產' in user_msg:
                content = '根據香港法例第30條破產條例第六款，債權人可向高等法院提交破產呈請，須證明債務人無力償還到期債務。本系統可協助您查閱相關法例及案例。'
            elif '案例' in user_msg or '案件' in user_msg:
                content = '以下是相關案例：\n\n【HCA 1234/2023】張三 訴 李四\n案件類型：民事合約糾紛\n裁決：被告人須退還款項港幣五百萬元\n\n【HCMA 567/2024】王某 訴 香港某銀行\n案件類型：銀行服務糾紛\n裁決：上訴被駁回'
            elif '會議' in user_msg or 'meeting' in msg_lower:
                content = '請上傳會議錄音或文字記錄，我將為您：\n1. 進行語音轉寫\n2. 萃取重點\n3. 歸納決議\n4. 生成標準會議記錄\n\n支援格式：MP3, M4A, WAV, TXT'
            elif '判詞' in user_msg or '裁決' in user_msg:
                content = templates['judgment_template']['sample']
            elif '律師信' in user_msg:
                content = templates['lawyer_letter_template']['sample']
            elif '你好' in user_msg or 'hi' in msg_lower:
                content = '您好！我是東風 AI 法律助理，很高興為您服務。我可以協助您：\n\n• 查詢香港法例及案例\n• 生成法律文件草稿\n• 分析案件要點\n• 撰寫律師信及判詞\n\n請告訴我您需要什麼幫助？'
            else:
                content = f'感謝您的提問。根據您提出的內容，我正在分析並從我們的知識庫中搜尋相關資料。\n\n建議您可以嘗試：\n• 查詢特定法例（如：公司法、破產條例）\n• 搜尋相關案例\n• 要求生成法律文件草稿'
            
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"role": "assistant", "content": content})
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }
    
    return {"statusCode": 405, "body": "Method not allowed"}
