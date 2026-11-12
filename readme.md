# Homework Grader

An AI agent that grades kids' Python homework, runs their code, reads the assignment and rubric, gives encouraging feedback and applies my personal beliefs and values. I have been a coding teacher for several years now, I have been teaching kids starting from age 6.

In my journey, I have learned being kind, sympathetic and patient with a learner is the best way to teach them. To teach kids you need not have as much subject matter knowledge as much patience and encouragement is required. I encourage all the kids who try writing the code, because it can be quite intimidating for a beginner to write the code (especially because I remember how much time it took for me to learn it, even though I was much older and in college).

This agent is built around the same philosophy. It encourages students for trying to solve the problem, while also finding the gaps in their knowledge and gently showing them how to correct their mistakes.

## How it works

This Homework grader works with help of the Claude API. I have given it a system prompt that tells it to be an encouraging teacher for kids. I have also created three tools for it: read_assignment, get_rubric and run_code. These tools allow Claude to read the assignment document, the rubric to judge the assignment, and submissions by the students.

Claude has access to all three tools and decides which tools to call and when. A typical sequence I observed was that Claude first asked to use the read_assignment tool. We ran this tool and gave the read assignment to Claude. Next, it asked to use get_rubric to read the rubric, and again we ran the requested tool and gave Claude the read rubric. Then, it asked to use the run_code tool. The run_code tool starts a subprocess that runs the code submitted by the student. We store the output and errors of this subprocess and give them back to Claude.

Claude can decide to use tools again based on the results it receives. At the end, it grades the submission, gives the student some words of encouragement and explains how to fix their mistakes.


```text
student's code --> claude --> read_assignment tool
                         --> get_rubric tool
                         --> run_code tool --> runs the code as a subprocess
                         --> results and errors given back to claude
                         --> claude decides whether it needs more tools
                         --> finally claude gives the response
                                      ^                    |
                                      |____________________|
                                           more tools?
```



## What makes it interesting (the findings)


- 8 fixture submissions across 3 assignments: the agent's grades matched my own rubric arithmetic 8/8 (and held across a full system-prompt change).

- In one of the assignments, students are instructed to write an if/else condition. To check that each submission is producing the correct result of both if and else cases, it voluntarily decided to run the code twice. It intentionally put 2 different values so both cases could be tested.

- Even though I created tools to read the assignment and rubric, initially I didn't set up a way to read the code file submitted by the student. Claude started using its own code to open the submission files. That revealed a security lesson to me, so I had to set up the code to read the student submission.

- I tried to keep my rubric really tight. I wrote down how many points should be awarded for each task a student does correctly. But I also noticed Claude used its own deduction and logic in the scenario where the rubric I provided wouldn't have been helpful. It even flagged the gap and asked for a ruling in the verdict itself: "If your teacher prefers partial credit..." it explained that the score could be higher depending on how I wanted to award the marks.


## Teaching Values

- Acknowledge the effort students put into attempting an assignment.
- Make feedback supportive, patient, and encouraging.
- I have written my values for grading as a system prompt- `You are a kind, encouraging coding teacher grading a kid's python homework`. It means everytime Claude gets a request
to grade a submission it also gets all the values I want to keep in ,ind while grading the assignment.
- I saw it giving constructive feedback to the students:-
  - "Every programmer forgets quotes sometimes."
  - The fill-in-the-blank hint Claude gave for the else condition.