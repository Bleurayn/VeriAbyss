import json
import sys
from veri_abyss_engine import veri_abyss_engine

def main():
    if len(sys.argv) < 2:
        print("Usage: veriabyss-seal input.json [output.json]")
        return
    with open(sys.argv[1]) as f:
        record = json.load(f)
    sealed = veri_abyss_engine(record)
    out = sys.argv[2] if len(sys.argv) > 2 else "sealed_output.json"
    with open(out, "w") as f:
        json.dump(sealed, f, indent=2)
    print(f"Sealed record written to {out} (avg_score: {sealed['seals']['veriabyss_seal']['score_avg']})")

if __name__ == "__main__":
    main()
