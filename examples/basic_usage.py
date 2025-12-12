from veri_abyss_engine import veri_abyss_engine
import json

record = {
    "verilock_version": "1.0.0",
    "record_id": "VL-REC-001",
    "claims": [{
        "claim_id": "C001",
        "claim_text": "Efficacy endpoint met with p<0.05",
        "domain": "CLINICAL_TRIAL",
        "confidence": 0.95,
        "evidence": [{"extract": "p=0.04 from CRF log"}]
    }]
}

sealed = veri_abyss_engine(record)
print(json.dumps(sealed, indent=2))
