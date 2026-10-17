# AI Study Assistant Agent

**Mini project for EWB Courses — AI/ML vs Future AI Agents (101)**

## Overview
AI Study Assistant Agent is a small educational productivity prototype. A user enters a subject or topic, selects a task, and receives a structured revision template, practice quiz, or study plan.

## Features
- Topic input and study-level selection
- Revision-notes template
- Practice-question generator
- Three-day study-plan generator
- Simple web interface
- Copy output button
- No API key required

## Technology stack
- Python 3.10+
- Flask
- HTML, CSS, JavaScript

## How to run
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

## Workflow
1. Collect topic, task type, level, and optional instructions.
2. Validate the topic and selected task.
3. Route the request to the appropriate task template.
4. Display the output for the learner to review and copy.

## Important limitation
This submission is a **rule-based prototype**, not a connected large language model. It demonstrates a basic agent-style workflow but does not claim to reason autonomously or verify facts. For an actual LLM-powered version, integrate an approved model API, add error handling, and disclose data/privacy practices.

## Suggested test cases
- Topic: `Solar PV system`, task: notes
- Topic: `Ohm's law`, task: quiz
- Topic: `Network security`, task: study plan
- Empty topic: app should request a topic

## Future scope
- PDF upload and summarization
- LLM API integration
- Quiz scoring and saved progress
- Source citations and fact-checking
- Login and personalized study plans

## Submission checklist
- [ ] Run locally and test all four task modes
- [ ] Add screenshots of the running app to this repository
- [ ] Replace this README's author details with your real details if desired
- [ ] Upload the project to your own GitHub repository
- [ ] Paste the repository URL into the EWB project form
- [ ] Upload your resume PDF separately in the form

## Author
Name: Sagar Chhanwal
College: Maharashtra Institute of Technology, Chhatrapati Sambhajinagar
Course: B.Tech in Electrical Engineering
Project: AI Study Assistant Agent 
Project Type:Mini-Project
