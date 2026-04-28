import json

def handler(request):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "metrics": {
                "total_queries": 1247,
                "documents_generated": 89,
                "knowledge_base_hits": 3421,
                "cases_processed": 23,
                "active_users": 12
            },
            "weekly_stats": [
                {"day": "週一", "queries": 45, "docs": 5},
                {"day": "週二", "queries": 62, "docs": 8},
                {"day": "週三", "queries": 38, "docs": 4},
                {"day": "週四", "queries": 71, "docs": 12},
                {"day": "週五", "queries": 55, "docs": 7},
                {"day": "週六", "queries": 12, "docs": 2},
                {"day": "週日", "queries": 5, "docs": 1}
            ],
            "recent_activity": [
                {"action": "生成判詞草稿", "user": "陳律師", "time": "5分鐘前"},
                {"action": "查詢公司法條文", "user": "李助理", "time": "12分鐘前"},
                {"action": "上傳會議錄音", "user": "王書記", "time": "25分鐘前"},
                {"action": "生成律師信", "user": "陳律師", "time": "1小時前"},
            ]
        })
    }
