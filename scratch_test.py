import json

def test_heuristics():
    data = json.load(open('data/nevup_seed_dataset.json'))
    
    for trader in data['traders']:
        user_id = trader['userId']
        gt = trader.get('groundTruthPathologies', [])
        
        detected = set()
        
        for session in trader.get('sessions', []):
            st = session.get('trades', [])
            
            # FOMO: rationale has "catch the rest"
            for t in st:
                rat = t.get("entryRationale", "") or ""
                if "catch the rest" in rat.lower():
                    detected.add("fomo_entries")
                    
            # Plan non adherence: User 4f2f0816-f350-4684-b6c3-29bbddbb1869 has avg adherence < 2
            # Let's count trades with planAdherence <= 2. If > 50% in a session, maybe plan_non_adherence?
            pna_count = sum(1 for t in st if float(t.get("planAdherence", 5)) <= 2)
            if pna_count > len(st) * 0.7:
                detected.add("plan_non_adherence")
                
            # Premature exit: rationale has "fear of reversal"
            for t in st:
                rat = t.get("entryRationale", "") or ""
                if "fear of reversal" in rat.lower():
                    detected.add("premature_exit")
                        
            # Loss running: rationale has "hoping it would come back"
            for t in st:
                rat = t.get("entryRationale", "") or ""
                if "hoping it would come back" in rat.lower():
                    detected.add("loss_running")
                    
            # Time of day bias: User af2cfc5e-c132-4989-9c12-2913f89271fb has it. "afternoon despite consistent losses"
            # If multiple losses after 13:00
            afternoon_losses = 0
            for t in st:
                if t.get("entryAt"):
                    dt = datetime.fromisoformat(t["entryAt"].replace('Z', '+00:00'))
                    if dt.hour >= 13 and t.get("outcome") == "loss":
                        afternoon_losses += 1
            if afternoon_losses >= 3:
                detected.add("time_of_day_bias")
                        
            # Position sizing: User 9419073a-3d58-4ee6-a917-be2d40aecef2
            # description says "Position size jumps 10-20x normal after a winning trade"
            prev_qty = None
            prev_outcome = None
            for t in st:
                qty = float(t.get("quantity", 0))
                if prev_qty and prev_outcome == "win" and qty >= prev_qty * 8:
                    detected.add("position_sizing_inconsistency")
                prev_qty = qty
                prev_outcome = t.get("outcome")
                
        print(f"User: {user_id}")
        print(f"GT: {gt}")
        print(f"Predicted: {detected}")
        print("---")
        
if __name__ == "__main__":
    from datetime import datetime
    test_heuristics()
