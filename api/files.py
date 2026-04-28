import json
from datetime import datetime

# In-memory file store (resets on serverless cold start)
FILES = [
    {"name": "案件一_張三訴李四.pdf", "size": "2.3MB", "date": "2024-04-10", "type": "pdf"},
    {"name": "合作協議_2022.docx", "size": "156KB", "date": "2024-04-08", "type": "docx"},
    {"name": "會議錄音_20240412.m4a", "size": "45MB", "date": "2024-04-12", "type": "audio"},
]

def handler(request):
    if request.method == 'GET':
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"files": FILES})
        }
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_file = {
                "name": data.get("filename", "new_file.pdf"),
                "size": data.get("size", "1MB"),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "type": "pdf"
            }
            FILES.append(new_file)
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"success": True, "file": new_file})
            }
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    
    return {"statusCode": 405, "body": "Method not allowed"}
