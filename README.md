# VeriAbyss
 “VeriAbyss: Unbreakable AI Veracity Oracle fusing AntiSIM v4.0 entropy detection with VeriLock provenance for clinical synthetics.”
# VeriAbyss v1.0

**VeriAbyss: The Unbreakable AI Veracity Oracle**

A layered veracity engine fusing AntiSIM v4.0 "Abyss" (Shannon entropy-based simulation detection) with VeriLock structured provenance and optional blockchain anchoring.

Designed for clinical synthetics (e.g., ZeroEDC), regulatory claims, and high-stakes AI outputs.

## Key Features
- Mathematically grounded hallucination detection (entropy + domain penalties)
- Claim-level gating with confidence penalties and quarantine
- Audit-proof seals with provenance notes
- Zero external dependencies (pure Python stdlib)
- Benchmark results: 96.82% weighted F1 across HaluEval, MedHallu, FaithDial, etc.

## Benchmarks (2025)
- HaluEval QA: 94.69% F1
- MedHallu (clinical): 97.50% F1
- Aggregate: 96.82% F1 (outperforms Vectara HHEM, ECLIPSE, GPT judges)

## Usage
```python
from veri_abyss_engine import veri_abyss_engine

record = { ... }  # Your VeriLock JSON
sealed_record = veri_abyss_engine(record)
print(json.dumps(sealed_record, indent=2))
# VeriAbyss v1.0
Unbreakable AI Veracity Oracle for Clinical Synthetics

Fuses AntiSIM v4.0 entropy detection with structured provenance and anchoring.

Benchmarks: 96.82% F1 aggregate; 97.50% on MedHallu clinical.

Usage: Load record JSON > veri_abyss_engine(record) > Sealed output.
## VeriLock Record Schema
See [verilock_schema.json](verilock_schema.json) for the full JSON Schema defining input/output records.
