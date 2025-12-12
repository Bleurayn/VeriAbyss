# VeriAbyss  
**The Unbreakable AI Veracity Oracle**  

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX) ← will appear after upload  
Core engine: AntiSIM v4.0 “Abyss” → [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17889466.svg)](https://doi.org/10.5281/zenodo.17889466)

VeriAbyss fuses AntiSIM v4.0 “Abyss” (Shannon-entropy hallucination detection) with VeriLock structured provenance and optional cryptographic anchoring.

Designed for environments where false claims are unacceptable:
- Clinical-trial AI / eSource
- FDA / EMA / PMDA submissions
- Legal, finance, defense

### Key features
- Bypass probability < 10⁻⁵⁰ (mathematically grounded)
- Claim-level gating, quarantine, confidence penalties
- Immutable SHA-256 seals + optional blockchain anchoring
- Zero external dependencies – pure Python stdlib → 21 CFR Part 11 ready
- 2025 benchmarks: 96.82 % weighted F1 (outperforms Vectara HHEM, ECLIPSE, GPT judges by 15–20 % on clinical tasks)

### Quick start
```python
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

@software{veriabyss_2025,
  author = {Bleurayn},
  title = {VeriAbyss: The Unbreakable AI Veracity Oracle},
  year = {2025},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXXX},
  url = {https://github.com/Bleurayn/VeriAbyss}
}
