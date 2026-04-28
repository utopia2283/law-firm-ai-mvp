from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load mock data
def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), 'mock_data', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

hk_laws = load_json('hk_laws.json')
sample_cases = load_json('sample_cases.json')
templates = load_json('templates.json')

# In-memory session state
sessions = {
    'default': {
        'chat_history': [],
        'files': [
            {'name': '案件一_張三訴李四.pdf', 'size': '2.3MB', 'date': '2024-04-10', 'type': 'pdf'},
            {'name': '合作協議_2022.docx', 'size': '156KB', 'date': '2024-04-08', 'type': 'docx'},
            {'name': '會議錄音_20240412.m4a', 'size': '45MB', 'date': '2024-04-12', 'type': 'audio'},
        ],
        'users': [
            {'name': '陳律師', 'role': '資深律師', 'permission': 'admin'},
            {'name': '李助理', 'role': '法律助理', 'permission': 'user'},
            {'name': '王書記', 'role': '書記員', 'permission': 'readonly'},
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # Simulate AI responses based on keywords
    msg_lower = user_msg.lower()
    
    if '法律' in user_msg or 'law' in msg_lower:
        response = {
            'role': 'assistant',
            'content': '根據香港法例第1條公司法第十四款，公司章程細則一經登記，公司即成為合法法人組織，得以公司名義進行各項法律行為。如需更詳細的法律意見，請聯絡我們的專業團隊。'
        }
    elif '破產' in user_msg or '破產' in user_msg:
        response = {
            'role': 'assistant',
            'content': '根據香港法例第30條破產條例第六款，債權人可向高等法院提交破產呈請，須證明債務人無力償還到期債務。本系統可協助您查閱相關法例及案例。'
        }
    elif '案例' in user_msg or '案件' in user_msg:
        response = {
            'role': 'assistant',
            'content': '以下是相關案例：\n\n【HCA 1234/2023】張三 訴 李四\n案件類型：民事合約糾紛\n裁決：被告人須退還款項港幣五百萬元\n\n【HCMA 567/2024】王某 訴 香港某銀行\n案件類型：銀行服務糾紛\n裁決：上訴被駁回'
        }
    elif '會議' in user_msg or 'meeting' in msg_lower:
        response = {
            'role': 'assistant',
            'content': '請上傳會議錄音或文字記錄，我將為您：\n1. 進行語音轉寫\n2. 萃取重點\n3. 歸納決議\n4. 生成標準會議記錄\n\n支援格式：MP3, M4A, WAV, TXT'
        }
    elif '判詞' in user_msg or '裁決' in user_msg:
        response = {
            'role': 'assistant',
            'content': templates['judgment_template']['sample']
        }
    elif '律師信' in user_msg:
        response = {
            'role': 'assistant',
            'content': templates['lawyer_letter_template']['sample']
        }
    elif '你好' in user_msg or 'hi' in msg_lower:
        response = {
            'role': 'assistant',
            'content': '您好！我是東風 AI 法律助理，很高興為您服務。我可以協助您：\n\n• 查詢香港法例及案例\n• 生成法律文件草稿\n• 分析案件要點\n• 撰寫律師信及判詞\n\n請告訴我您需要什麼幫助？'
        }
    else:
        response = {
            'role': 'assistant',
            'content': f'感謝您的提問。根據您提出的「{user_msg[:20]}...」，我正在分析並從我們的知識庫中搜尋相關資料。\n\n建議您可以嘗試：\n• 查詢特定法例（如：公司法、破產條例）\n• 搜尋相關案例\n• 要求生成法律文件草稿'
        }
    
    if session_id not in sessions:
        sessions[session_id] = {'chat_history': [], 'files': [], 'users': []}
    sessions[session_id]['chat_history'].append({'role': 'user', 'content': user_msg})
    sessions[session_id]['chat_history'].append(response)
    
    return jsonify(response)

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    return jsonify({
        'metrics': {
            'total_queries': 1247,
            'documents_generated': 89,
            'knowledge_base_hits': 3421,
            'cases_processed': 23,
            'active_users': 12
        },
        'weekly_stats': [
            {'day': '週一', 'queries': 45, 'docs': 5},
            {'day': '週二', 'queries': 62, 'docs': 8},
            {'day': '週三', 'queries': 38, 'docs': 4},
            {'day': '週四', 'queries': 71, 'docs': 12},
            {'day': '週五', 'queries': 55, 'docs': 7},
            {'day': '週六', 'queries': 12, 'docs': 2},
            {'day': '週日', 'queries': 5, 'docs': 1}
        ],
        'recent_activity': [
            {'action': '生成判詞草稿', 'user': '陳律師', 'time': '5分鐘前'},
            {'action': '查詢公司法條文', 'user': '李助理', 'time': '12分鐘前'},
            {'action': '上傳會議錄音', 'user': '王書記', 'time': '25分鐘前'},
            {'action': '生成律師信', 'user': '陳律師', 'time': '1小時前'},
        ]
    })

@app.route('/api/files', methods=['GET', 'POST'])
def files():
    session_id = request.args.get('session_id', 'default')
    if session_id not in sessions:
        sessions[session_id] = {'chat_history': [], 'files': [], 'users': []}
    
    if request.method == 'POST':
        # Simulate file upload
        new_file = {
            'name': request.json.get('filename', 'new_file.pdf'),
            'size': request.json.get('size', '1MB'),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'pdf'
        }
        sessions[session_id]['files'].append(new_file)
        return jsonify({'success': True, 'file': new_file})
    
    return jsonify({'files': sessions[session_id]['files']})

@app.route('/api/analyze_meeting', methods=['POST'])
def analyze_meeting():
    return jsonify({
        'transcription': '會議開始。討論案件進度。雙方同意調解。調解日期定於五月十五日。',
        'summary': '本案雙方同意進行調解，調解日期定於二零二四年五月十五日下午二時於高等法院調解室舉行。',
        'action_items': [
            {'item': '準備調解陳述書', 'assignee': '李助理', 'due': '2024-05-10'},
            {'item': '通知客戶調解安排', 'assignee': '陳律師', 'due': '2024-05-08'}
        ]
    })

@app.route('/api/generate_judgment', methods=['POST'])
def generate_judgment():
    case_info = request.json
    return jsonify({
        'content': templates['judgment_template']['sample'],
        'case_no': case_info.get('case_no', 'HCA 0000/2024'),
        'generated_at': datetime.now().isoformat()
    })

@app.route('/api/generate_letter', methods=['POST'])
def generate_letter():
    letter_info = request.json
    return jsonify({
        'content': templates['lawyer_letter_template']['sample'],
        'recipient': letter_info.get('recipient', '對方當事人'),
        'generated_at': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
