import json
import os

def load_data(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def predict_pathologies(trader):
    predictions = set()
    
    # overtrading: if any session has > 10 trades
    for session in trader.get('sessions', []):
        if session.get('tradeCount', 0) > 10:
            predictions.add('overtrading')
            break
            
    # revenge_trading: if any trade has revengeFlag == True
    for session in trader.get('sessions', []):
        for trade in session.get('trades', []):
            if trade.get('revengeFlag') is True:
                predictions.add('revenge_trading')
                break
                
    # fomo_entries: if emotionalState is greedy
    for session in trader.get('sessions', []):
        for trade in session.get('trades', []):
            rationale = trade.get('entryRationale') or ''
            if 'catch the rest of the move' in rationale.lower():
                predictions.add('fomo_entries')
                break
                
    return list(predictions)

def calc_metrics(y_true, y_pred):
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1

def evaluate(filepath):
    data = load_data(filepath)
    
    ground_truths = {}
    for gt in data.get('groundTruthLabels', []):
        ground_truths[gt['userId']] = set(gt['pathologies'])
        
    all_pathologies = set()
    for paths in ground_truths.values():
        all_pathologies.update(paths)
    all_pathologies = list(all_pathologies)
    
    y_true_dict = {p: [] for p in all_pathologies}
    y_pred_dict = {p: [] for p in all_pathologies}
    
    for trader in data.get('traders', []):
        user_id = trader['userId']
        true_paths = ground_truths.get(user_id, set())
        pred_paths = set(predict_pathologies(trader))
        
        for p in all_pathologies:
            y_true_dict[p].append(1 if p in true_paths else 0)
            y_pred_dict[p].append(1 if p in pred_paths else 0)
            
    report = {}
    for p in ['overtrading', 'fomo_entries', 'revenge_trading']:
        if p in all_pathologies:
            precision, recall, f1 = calc_metrics(y_true_dict[p], y_pred_dict[p])
            report[p] = {
                "precision": round(precision, 2),
                "recall": round(recall, 2),
                "f1": round(f1, 2)
            }
            
    os.makedirs('reports', exist_ok=True)
    with open('reports/classification_report.json', 'w') as f:
        json.dump(report, f, indent=2)
        
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    evaluate('data/nevup_seed_dataset.json')
