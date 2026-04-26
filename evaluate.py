import json
import os
from app.routes.evaluation import _build_evaluation_report

def evaluate():
    report = _build_evaluation_report()
    
    # Extract just the perLabel section for the classification report JSON to maintain the format
    output = report.get("perLabel", {})
            
    os.makedirs('reports', exist_ok=True)
    with open('reports/classification_report.json', 'w') as f:
        json.dump(output, f, indent=2)
        
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    evaluate()
