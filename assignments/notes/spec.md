# Homework Grader – Project Specification

## 1. Project Overview

The Homework Grader is an AI-powered application designed to evaluate Python homework submissions from children.

Its purpose is not just to assign grades but also to help students understand their mistakes, recognize their strengths, and feel encouraged to continue learning programming.

## 2. Student Submission

- The student will submit a single Python file (`.py`).
- The grader will evaluate the submitted Python code against the given assignment and its grading rubric.
### 2.1 Project Folder Structure

Each assignment will have its own directory containing the assignment instructions, grading rubric, and student submissions.

Example:
```text
homework-grader/
├── README.md
├── notes/
│   └── spec.md
├── assignments/
│   ├── 01_greeting/
│   │   ├── assignment.md
│   │   ├── rubric.md
│   │   └── submissions/
│   ├── 02_variables/
│   │   ├── assignment.md
│   │   ├── rubric.md
│   │   └── submissions/
│   └── 03_loops/
│       ├── assignment.md
│       ├── rubric.md
│       └── submissions/
```

## 3. Required AI Tools

The AI grader will have access to the following tools:

### 3.1 `run_code`
- Executes the student's Python code.
- Allows the grader to check whether the code runs successfully.
- Helps identify runtime errors and issues with the implementation.
- Executes submissions as a separate subprocess with a maximum timeout of 5 seconds.
- Captures stdout and stderr and returns them as text instead of displaying live execution in the grader's own process.
- Accepts an optional stdin string, which is passed to the process so submissions using input() can run.
- Version 1 will run locally on the teacher's machine for known students' submissions. It is not intended to be a publicly accessible service.

### 3.2 `read_assignment`
- Reads the assignment instructions.
- Helps the grader understand what the student was asked to build.
- Allows the grader to compare the submitted solution against the actual requirements.

### 3.3 `get_rubric`
- Retrieves the grading rubric.
- Helps the grader evaluate submissions consistently.
- Ensures that grades are based on predefined evaluation criteria.

**Not required:** `ask_the_teacher`. The initial version of the grader will not include a tool for asking the teacher questions.

## 4. Grading Output

Every student submission should receive:

### 4.1 Numerical Grade
- A numerical score representing the quality of the submission.
- The score should be based on the grading rubric.

### 4.2 Written Feedback

The feedback should include:

- **What the student did well:** Highlight correct implementations, good ideas, and things the student understood.
- **What needs improvement:** Explain mistakes or missing requirements in a constructive and understandable way.
- **Encouragement:** Motivate the student to keep practicing and improving.

## 5. Teaching Values and Restrictions

The grader must follow these principles when evaluating student submissions.

### 5.1 Never Discourage Beginners
- Never use discouraging, insulting, or harsh language.
- Never make a student feel bad about making mistakes.
- Recognize that attempting to write code is itself an important step in learning programming.
- Make feedback supportive, patient, and encouraging.

### 5.2 Always Encourage Effort
- Acknowledge the effort students put into attempting an assignment.
- Encourage students to keep experimenting and practicing, even when their code does not work as expected.
- Help students see mistakes as opportunities to learn.

### 5.3 Appreciate Creativity and Out-of-the-Box Thinking
- Recognize and praise students who attempt unusual or creative solutions.
- Appreciate approaches that demonstrate independent thinking.
- Do not penalize a student simply because their solution differs from the usual approach, provided it meets the assignment requirements.
- Give constructive suggestions while acknowledging creative thinking.

### 5.4 Provide Constructive Feedback
- Explain mistakes clearly and patiently.
- Focus on helping students understand how they can improve.
- Avoid unnecessarily complicated technical language.
- Balance suggestions for improvement with recognition of what the student did well.

## 6. Grading Philosophy and Evaluation Criteria

The grader must evaluate more than whether a student's program produces the correct output.

It must consider both the functionality of the program and the student's approach to solving the problem.

### 6.1 Functionality
- Check whether the program executes successfully.
- Compare the actual output against the expected output.
- Identify runtime errors and incorrect results.

### 6.2 Logic and Approach
- Examine the actual source code to understand the student's approach.
- Evaluate whether the student has understood and applied the relevant programming concepts.
- Recognize reasonable alternative solutions.
- Do not judge a student's understanding solely by whether their program executes successfully.

### 6.3 Partial Credit
- Award credit for correct logic and concepts even when minor mistakes prevent the program from running.
- Distinguish between conceptual mistakes and small implementation errors, such as spelling mistakes in variable names.
- Do not treat every runtime error as evidence that the student does not understand the concept.

### 6.4 Age and Learning-Level Awareness
- Evaluate code according to the concepts and techniques expected at the student's learning level.
- Do not expect advanced programming practices from beginners.
- Prioritize understanding of the concepts taught in the assignment over unnecessarily sophisticated code.

### 6.5 Overall Evaluation
The final grade should reflect the student's demonstrated understanding, functionality, adherence to assignment requirements, and code quality.

The feedback must explain both what worked and what needs improvement, while remaining encouraging and constructive.

### 6.6 Execution Results as Ground Truth

- The output returned by run_code must be treated as the actual result of executing the student's program.
- The grader must never assume that an execution result is incorrect, even if it appears surprising or unexpected.
- Grade the student's work based on what actually happened during execution, rather than what seems plausible.
- Claude may interpret whether the actual output satisfies the assignment requirements, but must never invent, modify, or disregard execution results.