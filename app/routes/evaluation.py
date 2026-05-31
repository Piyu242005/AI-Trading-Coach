from typing import Any, Dict, List, Set

from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

from app.database import dataset
from app.services.coaching import detect_signals_for_user_trades
from app.services.dataset_utils import flatten_user_trades, get_ground_truth_map

router = APIRouter()

TARGET_LABELS = [
    "overtrading",
    "revenge_trading",
    "session_tilt",
    "fomo_entries",
    "plan_non_adherence",
    "premature_exit",
    "loss_running",
    "time_of_day_bias",
    "position_sizing_inconsistency",
]
SIGNAL_TO_LABEL = {
    "overtrading": "overtrading",
    "revenge_trading": "revenge_trading",
    "session_tilt": "session_tilt",
    "fomo_entries": "fomo_entries",
    "plan_non_adherence": "plan_non_adherence",
    "premature_exit": "premature_exit",
    "loss_running": "loss_running",
    "time_of_day_bias": "time_of_day_bias",
    "position_sizing_inconsistency": "position_sizing_inconsistency",
}


def _safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def _compute_metrics(tp: int, fp: int, fn: int) -> Dict[str, Any]:
    precision = _safe_divide(tp, tp + fp)
    recall = _safe_divide(tp, tp + fn)
    f1 = _safe_divide(2 * precision * recall, precision + recall)
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def _predict_user_pathologies(user_id: str) -> Dict[str, Any]:
    user_trades = flatten_user_trades(dataset, user_id)
    signals = detect_signals_for_user_trades(user_id, user_trades)
    predicted_labels = sorted(
        {
            SIGNAL_TO_LABEL[signal["signal"]]
            for signal in signals
            if signal["signal"] in SIGNAL_TO_LABEL
        }
    )

    return {
        "predictedPathologies": predicted_labels,
        "signals": signals,
    }


def _build_evaluation_report() -> Dict[str, Any]:
    truth_map = get_ground_truth_map(dataset)
    user_ids = sorted(truth_map.keys())

    per_user: List[Dict[str, Any]] = []
    predicted_map: Dict[str, Set[str]] = {}
    filtered_truth_map: Dict[str, Set[str]] = {}

    for user_id in user_ids:
        prediction = _predict_user_pathologies(user_id)
        predicted_labels = set(prediction["predictedPathologies"])
        truth_labels = {label for label in truth_map[user_id] if label in TARGET_LABELS}

        predicted_map[user_id] = predicted_labels
        filtered_truth_map[user_id] = truth_labels

        per_user.append(
            {
                "userId": user_id,
                "predictedPathologies": sorted(predicted_labels),
                "groundTruthPathologies": sorted(truth_labels),
                "signals": prediction["signals"],
            }
        )

    tp = 0
    fp = 0
    fn = 0

    for user_id in user_ids:
        predicted = predicted_map[user_id]
        truth = filtered_truth_map[user_id]

        tp += len(predicted.intersection(truth))
        fp += len(predicted.difference(truth))
        fn += len(truth.difference(predicted))

    per_label: Dict[str, Dict[str, Any]] = {}
    for label in TARGET_LABELS:
        label_tp = 0
        label_fp = 0
        label_fn = 0
        for user_id in user_ids:
            predicted_has = label in predicted_map[user_id]
            truth_has = label in filtered_truth_map[user_id]
            if predicted_has and truth_has:
                label_tp += 1
            elif predicted_has and not truth_has:
                label_fp += 1
            elif truth_has and not predicted_has:
                label_fn += 1
        per_label[label] = _compute_metrics(label_tp, label_fp, label_fn)

    return {
        "targetLabels": TARGET_LABELS,
        "overall": _compute_metrics(tp, fp, fn),
        "perLabel": per_label,
        "perUser": per_user,
    }


def _render_html(report: Dict[str, Any]) -> str:
    rows = []
    for user in report["perUser"]:
        rows.append(
            "<tr>"
            f"<td>{user['userId']}</td>"
            f"<td>{', '.join(user['predictedPathologies']) or 'none'}</td>"
            f"<td>{', '.join(user['groundTruthPathologies']) or 'none'}</td>"
            "</tr>"
        )

    per_label_rows = []
    for label, metrics in report["perLabel"].items():
        per_label_rows.append(
            "<tr>"
            f"<td>{label}</td>"
            f"<td>{metrics['precision']}</td>"
            f"<td>{metrics['recall']}</td>"
            f"<td>{metrics['f1']}</td>"
            "</tr>"
        )

    overall = report["overall"]
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>NevUp Evaluation Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 24px; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background: #f3f3f3; }}
  </style>
</head>
<body>
  <h1>NevUp Evaluation Report</h1>
  <p><strong>Overall Precision:</strong> {overall["precision"]} | <strong>Recall:</strong> {overall["recall"]} | <strong>F1:</strong> {overall["f1"]}</p>

  <h2>Per-Label Metrics</h2>
  <table>
    <thead>
      <tr><th>Label</th><th>Precision</th><th>Recall</th><th>F1</th></tr>
    </thead>
    <tbody>
      {"".join(per_label_rows)}
    </tbody>
  </table>

  <h2>Per-User Predictions</h2>
  <table>
    <thead>
      <tr><th>User ID</th><th>Predicted</th><th>Ground Truth</th></tr>
    </thead>
    <tbody>
      {"".join(rows)}
    </tbody>
  </table>
</body>
</html>
"""


@router.get("/evaluation/report")
def evaluation_report(format: str = Query("json", pattern="^(json|html)$")):
    report = _build_evaluation_report()
    if format == "html":
        return HTMLResponse(content=_render_html(report))
    return report


@router.get("/evaluation/report.html", response_class=HTMLResponse)
def evaluation_report_html():
    report = _build_evaluation_report()
    return HTMLResponse(content=_render_html(report))
