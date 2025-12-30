import pytest
from veri_abyss_engine import veri_abyss_engine

def test_original_smoke_test():
    """Original minimal smoke test — ensures backward compatibility."""
    record = {
        "verilock_version": "1.0.0",
        "record_id": "TEST",
        "claims": []
    }
    result = veri_abyss_engine(record)
    
    # Original requirement
    assert "seal" in result
    assert result["seal"] == "VERIABYSS_ULTIMATE_SEALED"
    
    # Basic provenance
    assert result["seals"]["veriabyss_seal"]["enabled"] is True
    assert result["seals"]["veriabyss_seal"]["score_avg"] == 1.0
    assert len(result["audit_trail"]) >= 2


def test_good_clinical_claim_with_supporting_evidence():
    """Legitimate high-stakes claim with strong evidence should pass."""
    record = {
        "verilock_version": "1.0.0",
        "record_id": "CLIN-001",
        "claims": [{
            "claim_id": "C001",
            "claim_text": "The primary efficacy endpoint was met with p=0.032 in the phase III trial.",
            "domain": "CLINICAL_TRIAL",
            "confidence": 0.95,
            "evidence": [{
                "extract": "Phase III results: primary endpoint p-value = 0.032 (statistically significant)"
            }]
        }]
    }
    result = veri_abyss_engine(record)
    claim = result["claims"][0]
    
    assert result["seals"]["veriabyss_seal"]["score_avg"] >= 0.95
    assert claim["risk_level"] == "LOW"
    assert claim["truth_state"] == "VERIFIED"
    assert claim["confidence"] >= 0.85  # After penalty, still high


def test_repetitive_hallucinated_claim():
    """Classic SIM-style repetition should be crushed."""
    record = {
        "verilock_version": "1.0.0",
        "record_id": "HAL-001",
        "claims": [{
            "claim_text": "The trial was very very successful successful successful and great great great.",
            "domain": "CLINICAL_TRIAL"
        }]
    }
    result = veri_abyss_engine(record)
    claim = result["claims"][0]
    
    assert claim["risk_level"] == "CRITICAL"
    assert claim["truth_state"] == "DISPROVEN"
    assert result["seals"]["veriabyss_seal"]["score_avg"] == 0.0


def test_unsupported_clinical_claim():
    """Strong intrinsic text but contradicted/no overlap with evidence."""
    record = {
        "verilock_version": "1.0.0",
        "record_id": "UNS-001",
        "claims": [{
            "claim_text": "No serious adverse events were reported.",
            "domain": "CLINICAL_TRIAL",
            "evidence": [{
                "extract": "Serious adverse events occurred in 8 patients including 2 hospitalizations."
            }]
        }]
    }
    result = veri_abyss_engine(record)
    claim = result["claims"][0]
    
    assert claim["risk_level"] == "CRITICAL"
    assert claim["truth_state"] == "DISPROVEN"


def test_general_domain_relaxed():
    """Non-high-stakes domain — no x1000 penalty."""
    record = {
        "verilock_version": "1.0.0",
        "record_id": "GEN-001",
        "claims": [{
            "claim_text": "hello hello hello",  # Repetitive but not critical
            "domain": "GENERAL"
        }]
    }
    result = veri_abyss_engine(record)
    claim = result["claims"][0]
    
    assert claim["risk_level"] in ["HIGH", "MEDIUM"]  # Not CRITICAL
    assert result["seals"]["veriabyss_seal"]["score_avg"] > 0.0


def test_missing_required_field():
    """Validation works."""
    with pytest.raises(ValueError, match="Missing required field"):
        veri_abyss_engine({"verilock_version": "1.0.0"})  # No record_id
