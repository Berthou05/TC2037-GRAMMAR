import subprocess
import sys
from pathlib import Path


SCRIPTS = {
    "g0": "g0_tree.py",
    "g1": "g1_tree.py",
    "g2": "g2_tree.py",
}

SENTENCE = "SELECT id . id FROM id , id WHERE id . id = num OR id . id = num ;"

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SCRIPTS:
        options = ", ".join(SCRIPTS)
        print(f"Usage: python scripts/run_tree.py <{options}>")
        raise SystemExit(1)

    grammar_key = sys.argv[1]
    script = Path(__file__).with_name(SCRIPTS[grammar_key])

    subprocess.run(
        [sys.executable, str(script), SENTENCE],
        check=True,
    )


if __name__ == "__main__":
    main()
