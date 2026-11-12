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

SYSTEM = """You are a kind, encouraging coding teacher grading a kid's python homework. You can use read_assignment to read the assignment document, get_rubric to get the rubric document, and run_code to run the code file
submitted by the student. Be kind and patient, never use discouraging language. Recognize the efforts of students who come up with unique or creative solutions. Provide constructive feedback, praise the students
who come up unique solutions. You are evaluating  more than whether a student's program produces the correct output. You must consider both the functionality of the program and the student's approach to solving the problem. 
Award the logic even if minor mistakes prevent the program from running.Examine the actual source code to understand the student's approach. Evaluate whether the student has understood and applied the relevant programming 
concepts.The output returned by run_code must be treated as the actual result of executing the student's program. The grader must never assume that an execution result is incorrect, even if it appears surprising or unexpected. 
Code is written by beginners(children) expect beginner-level code, don’t demand professional practices. Grade strictly by the rubric.
Give: the score out of 10 with per-row breakdown, what they did well, what to improve, encouragement"""

client = anthropic.Anthropic()
def grade(assignment_name: str, submission_path: str) -> str:
    with open(submission_path, "r") as file:
        submission_code = file.read()

    messages = [{"role": "user", "content":
        f"Grade this submission for assignment {assignment_name}:\n\n{submission_code}"}]

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
                    out = run_code(block.input["code"], block.input.get("stdin", ""))
                elif block.name == "read_assignment":
                    out = read_assignment(block.input["assignment_name"])
                elif block.name == "get_rubric":
                    out = get_rubric(block.input["assignment_name"])
                print(block.name, block.input)
                results.append({"type":"tool_result", "tool_use_id": block.id, "content":out})
        messages.append({"role":"user", "content": results})

    final_text = ""
    for block in message.content:
        if block.type == "text":
            final_text += block.text

    return final_text



if __name__ == "__main__":
    kids = ["empty_input.py", "perfect.py", "no_var.py"]
    print(grade("03_vote", f"assignments/03_vote/submissions/perfect.py"))
    '''for kid in kids:
        print(f"Grading: \n\n{'='*60} {kid} {'='*60}\n")
        print(grade("02_ask_name", f"assignments/02_ask_name/submissions/{kid}"))
    '''


