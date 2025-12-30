# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Bleurayn

import datetime
import hashlib
import math
from collections import Counter
import unicodedata

def normalize_text(text: str) -> str:
    return unicodedata.normalize('NFC', str(text).strip().lower())

def calculate_char_entropy(text: str) -> float:
    if not text:
        return 0.0
    freq = Counter(text)
    length = len(text)
    return round(-sum((count / length) * math.log2(count / length) for count in freq.values()), 4)

def calculate_word_entropy(text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    freq = Counter(words)
    length = len(words)
    return round(-sum((count / length) * math.log2(count / length) for count in freq.values()), 4)

def detect_repetition(text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    return len(set(words)) / len(words)

def evidence_overlap_score(claim_text: str, evidence_extracts: list[str]) -> float:
    claim_ngrams = set(claim_text[i:i+3] for i in range(max(len(claim_text)-2, 0)))
    if not claim_ngrams:
        return 0.0
    ev_ngrams = set()
    for ext in evidence_extracts:
        ev_ngrams.update(ext[i:i+3] for i in range(max(len(ext)-2, 0)))
    if not ev_ngrams:
        return 0.0
    return len(claim_ngrams & ev_ngrams) / len(claim_ngrams | ev_ngrams)

def veri_abyss_engine(record: dict, strict_threshold: float = 0.95) -> dict:
    required = ["verilock_version", "record_id"]
    for key in required:
        if key not in record:
            raise ValueError(f"Missing required field: {key}")
    
    claims_input = record.get("claims", [])
    now = datetime.datetime.utcnow().isoformat() + "Z"
    
    sealed_record = {
        "verilock_version": record["verilock_version"],
        "record_id": record["record_id"],
        "status": "DRAFT",
        "created_at": now,
        "updated_at": None,
        "created_by": {"actor_id": "auto-sealer", "actor_role": "system"},
        "division_scope": record.get("division_scope", ["general"]),
        "classification": record.get("classification", {
            "data_sensitivity": "INTERNAL",
            "ip_tier": "TIER_1",
            "distribution": "NEED_TO_KNOW"
        }),
        "claims": [],
        "audit_trail": [
            {"event_id": "EVT-AUTO-001", "timestamp": now, "actor": {"actor_id": "auto-sealer", "actor_role": "system"}, "action": "CREATE", "details": {"note": "Initial creation"}},
            {"event_id": "EVT-SEAL-001", "timestamp": now, "actor": {"actor_id": "auto-sealer", "actor_role": "system"}, "action": "SEAL", "details": {"engine": "VeriAbyss v1.0.0 Ultimate"}}
        ],
        "seals": {
            "veriabyss_seal": {
                "enabled": True,
                "product_version": "1.0.0",
                "antisim_version": "4.0 Abyss x1000",
                "sealed_at": now,
                "math_proof": "Multi-layer Shannon entropy + repetition ratio + char-3gram evidence overlap + x1000 domain penalty on weakness"
            }
        },
        "seal": "VERIABYSS_ULTIMATE_SEALED"
    }
    
    scores = []
    high_stakes_domains = {"CLINICAL_TRIAL", "GENOMICS", "LEGAL", "REGULATORY", "FINANCIAL"}
    
    for idx, raw_claim in enumerate(claims_input):
        claim_text_norm = normalize_text(raw_claim.get("claim_text", ""))
        domain = str(raw_claim.get("domain", "GENERAL")).upper()
        
        char_ent = calculate_char_entropy(claim_text_norm)
        word_ent = calculate_word_entropy(claim_text_norm)
        rep_ratio = detect_repetition(claim_text_norm)
        base_score = (char_ent / 5.0 + word_ent / 10.0) / 2 * rep_ratio
        
        evidence_extracts = [normalize_text(ev.get("extract", "")) for ev in raw_claim.get("evidence", [])]
        overlap = evidence_overlap_score(claim_text_norm, evidence_extracts)
        
        final_base = (base_score + overlap) / 2  # Balanced intrinsic + external
        
        penalty = 0.0
        if domain in high_stakes_domains and final_base < strict_threshold:
            penalty = (1.0 - final_base) * 1000
        
        final_score = max(final_base - penalty, 0.0)
        scores.append(final_score)
        
        if final_score >= 0.98:
            risk, truth = "LOW", "VERIFIED"
        elif final_score >= 0.9:
            risk, truth = "MEDIUM", "PARTIALLY_VERIFIED"
        elif final_score > 0.0:
            risk, truth = "HIGH", "UNVERIFIED"
        else:
            risk, truth = "CRITICAL", "DISPROVEN"
        
        orig_conf = float(raw_claim.get("confidence", 1.0))
        adjusted_conf = round(min(orig_conf * (final_score ** 3), 1.0), 4)
        
        processed_claim = {
            "claim_id": raw_claim.get("claim_id", f"C{idx+1:04d}"),
            "claim_text": claim_text_norm,
            "claim_type": raw_claim.get("claim_type", "FACT"),
            "domain": domain,
            "risk_level": risk,
            "truth_state": truth,
            "confidence": adjusted_conf,
            "evidence": []
        }
        
        for ev_idx, raw_ev in enumerate(raw_claim.get("evidence", [])):
            extract = normalize_text(raw_ev.get("extract", ""))
            ev_hash = hashlib.sha256(extract.encode()).hexdigest() if extract else ""
            processed_ev = {
                "evidence_id": f"EV{idx+1:04d}-{ev_idx+1}",
                "evidence_type": raw_ev.get("evidence_type", "DOCUMENT"),
                "source": {
                    "location": raw_ev.get("source", "internal"),
                    "hash_sha256": ev_hash,
                    "retrieved_at": now
                },
                "relevance": raw_ev.get("relevance", "direct"),
                "extract": extract
            }
            processed_claim["evidence"].append(processed_ev)
        
        sealed_record["claims"].append(processed_claim)
    
    avg_score = round(sum(scores) / len(scores), 4) if scores else 1.0
    sealed_record["seals"]["veriabyss_seal"]["score_avg"] = avg_score
    
    return sealed_record
