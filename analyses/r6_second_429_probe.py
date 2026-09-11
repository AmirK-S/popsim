"""Ajoute une lecture authentifiée, sans POST, à la réconciliation R6 bornée."""

import datetime
import json
import os
import sys
from urllib.parse import urlencode

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r6_oracle_distant as R6


PATH = "data/traces/reprise/r6-reconciliation-deepseek-fucitzn-second429-20260911.json"


def get(endpoint, generation_id, content=False):
    try:
        payload = R6._lire(R6.BASE + endpoint + "?" + urlencode({"id": generation_id}),
                           R6.cle_api())
        data = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(data, dict):
            return {"outcome": "schema_invalid"}
        if content:
            output = data.get("output") if isinstance(data.get("output"), dict) else {}
            return {"outcome": "200", "completion_present": output.get("completion") is not None,
                    "completion_characters": len(output.get("completion") or "")}
        fields = ("id", "model", "provider_name", "total_cost", "usage", "cancelled",
                  "finish_reason", "created_at")
        return {"outcome": "200", "data": {k: data.get(k) for k in fields if k in data}}
    except Exception as exc:
        return {"outcome": "error", "http_status": getattr(exc, "code", None),
                "error_type": type(exc).__name__}


record = json.load(open(PATH, encoding="utf-8"))
generation_id = record["generation_id"]
probe = {"at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
         "metadata": get("/generation", generation_id),
         "content": get("/generation/content", generation_id, content=True)}
try:
    credits = R6.solde(R6.cle_api())
    probe["credits"] = {"outcome": "200", "available": str(R6.solde_disponible(credits)),
                        "total_usage": str(credits.get("total_usage"))}
except Exception as exc:
    probe["credits"] = {"outcome": "error", "http_status": getattr(exc, "code", None),
                        "error_type": type(exc).__name__}
record.setdefault("probes", []).append(probe)
fd = os.open(PATH, os.O_WRONLY | os.O_TRUNC, 0o600)
with os.fdopen(fd, "w", encoding="utf-8") as fh:
    json.dump(record, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
os.chmod(PATH, 0o600)
print(json.dumps(probe, ensure_ascii=False, sort_keys=True))
