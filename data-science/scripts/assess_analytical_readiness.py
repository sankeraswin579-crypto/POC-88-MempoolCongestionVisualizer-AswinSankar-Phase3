import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUT = ROOT / "data-science" / "outputs"

df = pd.read_csv(CSV)

quality = json.load(open(OUT / "quality_assessment.json", encoding="utf-8"))
rep = json.load(open(OUT / "representativeness_assessment.json", encoding="utf-8"))

quality_pass = quality["overall_status"] == "PASS"

readiness = {
    "dataset_archetype": "time-stamped operational measurement dataset",
    "primary_analytical_question": (
        "How do observed Bitcoin mempool, transaction, block, and fee measurements "
        "vary across the captured observation timestamps?"
    ),
    "tracks": {
        "descriptive": "READY",
        "diagnostic": "READY",
        "temporal": "READY_WITH_LIMITATIONS",
        "predictive": "NOT_ESTABLISHED_FROM_CURRENT_SNAPSHOT_ALONE"
    },
    "data_quality_gate": quality["overall_status"],
    "representativeness": {
        "unique_timestamps": rep["unique_observation_timestamps"],
        "categories": rep["category_distribution"],
        "sources": rep["source_distribution"]
    },
    "limitations": rep["assessment"]["limitations"],
    "readiness_decision": (
        "DATA READY FOR ANALYTICAL TRACK DEVELOPMENT"
        if quality_pass
        else "CANONICAL DATA CHANGES REQUIRED"
    ),
}

with open(OUT / "analytical_readiness.json", "w", encoding="utf-8") as f:
    json.dump(readiness, f, indent=2, default=str)

print("analytical_readiness.json generated")
print("Decision:", readiness["readiness_decision"])
