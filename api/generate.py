import json
import os
from datetime import datetime

def load_json(filename):
    path = os.path.join(os.getcwd(), 'mock_data', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

templates = load_json('templates.json')

def handler(request):
    if request.method == 'POST':
        try:
            data = request.get_json()
            action = data.get('action', '')
            
            if action == 'judgment':
                content = templates['judgment_template']['sample']
                case_no = data.get('case_no', 'HCA 0000/2024')
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({
                        "content": content,
                        "case_no": case_no,
                        "generated_at": datetime.now().isoformat()
                    })
                }
            elif action == 'letter':
                content = templates['lawyer_letter_template']['sample']
                recipient = data.get('recipient', '對方當事人')
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({
                        "content": content,
                        "recipient": recipient,
                        "generated_at": datetime.now().isoformat()
                    })
                }
            elif action == 'meeting':
                return {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({
                        "transcription": "會議開始。討論案件進度。雙方同意調解。調解日期定於五月十五日。",
                        "summary": "本案雙方同意進行調解，調解日期定於二零二四年五月十五日下午二時於高等法院調解室舉行。",
                        "action_items": [
                            {"item": "準備調解陳述書", "assignee": "李助理", "due": "2024-05-10"},
                            {"item": "通知客戶調解安排", "assignee": "陳律師", "due": "2024-05-08"}
                        ]
                    })
                }
            else:
                return {"statusCode": 400, "body": json.dumps({"error": "Unknown action"})}
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    
    return {"statusCode": 405, "body": "Method not allowed"}
