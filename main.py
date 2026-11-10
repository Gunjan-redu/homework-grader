from dotenv import load_dotenv
import anthropic
from tools import run_code

load_dotenv()

tools =  [
    {
        "name":"run_code",
        "description": "Execute a student's Python submission. Returns exit code, stdout, and any errors. Optionally pass stdin to feed input() calls.",
        "input_schema": {
            "type":"object",
            "properties": {
                "code": {"type": "string", "description": "The Python code to execute"},
                "stdin": {"type": "string", "description": "Inputs needed to execute the code."}
            },
            "required": ["code"]
        }
    }
]

SYSTEM = """You are a kind, encouraging coding teacher grading a kid's Python homework.
Use run_code to actually execute the submission - its output is ground truth; never
assume an execution result is mistaken, even if surprising. Judge intent from the
source code as well as the result. Grade strictly by the rubric. Never discourage;
mistakes are learning opportunities. Give: the score out of 10 with per-row breakdown,
what they did well, what to improve, and encouragement."""

ASSIGNMENT = open("assignments/01_greeting/assignment.md").read()
RUBRIC = open("assignments/01_greeting/rubrics.md").read()
SUBMISSION = 'print(Hello Gunjan)'


messages = [{"role": "user", "content":f"Assignment:\n{ASSIGNMENT}\n\nRubric:\n{RUBRIC}\n\nStudent submission:\n{SUBMISSION}\n\nGrade it."}]


client = anthropic.Anthropic()

while True:
    message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1500,
        system= SYSTEM,
        tools = tools,
        messages= messages
    )

    if message.stop_reason != "tool_use":
        break

    messages.append({"role": "assistant", "content":message.content})

    results = []
    for block in message.content:
        if block.type == "tool_use":
            out = run_code(block.input["code"], block.input.get("stdin", 0))
            results.append({"type":"tool_result", "tool_use_id": block.id, "content":out})
    messages.append({"role":"user", "content": results})




for block in message.content:
    if block.type == "text":
        print(block.text)

