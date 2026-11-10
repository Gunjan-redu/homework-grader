import subprocess
import sys


def run_code(code: str, stdin: str = "") -> str:
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            input=stdin,
            capture_output=True,
            text= True,
            timeout=5)

    except subprocess.TimeoutExpired:
        return "TIMEOUT: code did not finish within 5 seconds (possible infinite loop)"


    output = f"[exit code: {result.returncode}]\n{result.stdout}"
    if result.stderr:
        output += "\nERRORS:\n" + result.stderr
    return output

def read_assignment(assignment_name: str) -> str:
    try:
        assignment = open(f"assignments/{assignment_name}/assignment.md").read()
    except FileNotFoundError:
        return f"ERROR: no assignment named '{assignment_name}' found"
    return assignment

def get_rubric(assignment_name: str) -> str:
    try:
        rubric = open(f"assignments/{assignment_name}/rubric.md").read()
    except FileNotFoundError:
        return f"ERROR: no rubric named '{assignment_name}' found"
    return rubric



if __name__ == "__main__":
    tests = {
        "perfect": 'print("Hello Gunjan")',
        "no_quotes": 'print(Hello Gunjan)',
        "loop": 'while True:\n    pass',
        "asks_name": 'name = input()\nprint("Hello", name)',
    }
    for label, code in tests.items():
        print(f"--- {label}")
        print(run_code(code, stdin="Gunjan"))