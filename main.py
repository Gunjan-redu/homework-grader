from dotenv import load_dotenv
import anthropic
from tools import run_code, get_rubric, read_assignment

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
    },
    {
        "name": "read_assignment",
        "description": "Read the assignment from the folder. Returns the read assignment as a string. Call this when you need the assignment",
        "input_schema":{
            "type": "object",
            "properties":{
                "assignment_name": {"type": "string", "description": "The assignment's folder name, e.g. '01_greeting'"}
            },
            "required": ["assignment_name"]
        },

    },
    {
            "name": "get_rubric",
            "description": "Read the rubric from the folder. Returns the read rubric as a string. Call this when you need the rubric",
            "input_schema":{
                "type": "object",
                "properties":{
                    "assignment_name": {"type": "string", "description": "The assignment's folder name, e.g. '01_greeting'"}
                },
                "required": ["assignment_name"]
            },

    }

]

SYSTEM = """You are a kind, encouraging coding teacher grading a kid's Python homework.
Use run_code to actually execute the submission - its output is ground truth; never
assume an execution result is mistaken, even if surprising. Judge intent from the
source code as well as the result. Grade strictly by the rubric. Never discourage;
mistakes are learning opportunities. Give: the score out of 10 with per-row breakdown,
what they did well, what to improve, and encouragement."""

ASSIGNMENT = open("assignments/01_greeting/assignment.md").read()
RUBRIC = open("assignments/01_greeting/rubric.md").read()
SUBMISSION = 'print("Hello Gunjan")'


messages = [{"role": "user", "content":f"Grade this submission for assignment 01_greeting:\n\n{SUBMISSION}"}]


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
            if block.name == "run_code":
                out = run_code(block.input["code"], block.input.get("stdin", 0))
            elif block.name == "read_assignment":
                out = read_assignment(block.input["assignment_name"])
            elif block.name == "get_rubric":
                out = get_rubric(block.input["assignment_name"])
            print(block.name, block.input)
            results.append({"type":"tool_result", "tool_use_id": block.id, "content":out})
    messages.append({"role":"user", "content": results})




for block in message.content:
    if block.type == "text":
        print(block.text)


