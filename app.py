from flask import Flask, render_template_string, request, jsonify
import re

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Study Assistant Agent</title>
<style>
:root{--bg:#081426;--panel:#10223b;--line:#244362;--text:#eef6ff;--muted:#a8bdd4;--lime:#c7ff32;--cyan:#37d7ff}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at top right,#12385b,transparent 40%),var(--bg);font-family:Arial,sans-serif;color:var(--text)}
main{max-width:1000px;margin:auto;padding:28px 18px 50px}.tag{color:var(--cyan);font-weight:bold;letter-spacing:2px;font-size:12px}
h1{font-size:clamp(30px,5vw,48px);margin:10px 0}h1 span{color:var(--lime)}p{color:var(--muted);line-height:1.6}
.grid{display:grid;grid-template-columns:1.1fr .9fr;gap:18px;margin-top:24px}
.card{background:rgba(16,34,59,.92);border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 10px 30px #0002}
label{display:block;margin:14px 0 7px;color:#d8e8fa;font-weight:bold}textarea,select,input{width:100%;padding:12px;border-radius:10px;border:1px solid #345576;background:#09182b;color:var(--text);font:inherit}
textarea{min-height:125px;resize:vertical}button{border:0;border-radius:10px;background:var(--lime);color:#102033;padding:12px 16px;font-weight:bold;cursor:pointer;margin:8px 6px 0 0}button.secondary{background:#173b5d;color:var(--text);border:1px solid #3a6a8f}
#result{white-space:pre-wrap;line-height:1.7;color:#e8f3ff;min-height:180px}.small{font-size:12px;color:var(--muted)}.pill{display:inline-block;border:1px solid #376184;border-radius:30px;padding:6px 10px;color:var(--cyan);font-size:12px;margin:3px}
ul{color:var(--muted);line-height:1.8;padding-left:20px}
@media(max-width:720px){.grid{grid-template-columns:1fr}}
</style></head>
<body><main>
<div class="tag">MINI PROJECT • AI AGENTS (101)</div>
<h1>AI Study <span>Assistant Agent</span></h1>
<p>A student productivity prototype that turns a topic into revision notes, practice questions, and a study plan. This demo uses transparent, rule-based generation and does not require an API key.</p>
<div><span class="pill">Python</span><span class="pill">Flask</span><span class="pill">Agent workflow</span><span class="pill">Education</span></div>
<div class="grid">
<section class="card">
<h2>Build your study output</h2>
<label for="topic">Topic or subject</label><input id="topic" placeholder="e.g. Solar PV system" value="Solar PV system">
<label for="mode">Choose task</label><select id="mode">
<option value="notes">Generate revision notes</option><option value="quiz">Create practice quiz</option><option value="plan">Create a study plan</option><option value="explain">Explain a topic simply</option>
</select>
<label for="level">Study level</label><select id="level"><option>Beginner</option><option>Diploma</option><option selected>Engineering</option></select>
<label for="context">Extra instructions (optional)</label><textarea id="context" placeholder="e.g. Keep it simple and focus on exam points."></textarea>
<button onclick="runAgent()">Run Study Agent</button><button class="secondary" onclick="copyResult()">Copy output</button>
<p class="small">Prototype note: output is generated locally using templates, not a connected large language model.</p>
</section>
<section class="card">
<h2>Agent output</h2><p class="small" id="status">Ready • Waiting for your task</p>
<div id="result">Your generated notes, quiz, or plan will appear here.</div>
</section>
</div>
<div class="grid">
<section class="card"><h2>How the agent works</h2><ul><li><b>1. Input:</b> receives topic, task, and level.</li><li><b>2. Planning:</b> selects a workflow for notes, quiz, explanation, or schedule.</li><li><b>3. Action:</b> generates a structured result.</li><li><b>4. Review:</b> user checks and copies the output.</li></ul></section>
<section class="card"><h2>Future enhancements</h2><ul><li>Connect a verified LLM API.</li><li>Upload PDFs and summarize course material.</li><li>Save study plans and quiz scores.</li><li>Add citations and fact-checking for generated answers.</li></ul></section>
</div>
<footer class="small" style="margin-top:22px">Student mini-project prototype • Verify generated study material before using it in exams.</footer>
</main>
<script>
async function runAgent(){
 const topic=document.getElementById('topic').value.trim();
 if(!topic){document.getElementById('status').textContent='Please enter a topic.';return}
 document.getElementById('status').textContent='Agent is processing…';
 const payload={topic,mode:document.getElementById('mode').value,level:document.getElementById('level').value,context:document.getElementById('context').value};
 try{
 const res=await fetch('/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
 const data=await res.json();document.getElementById('result').textContent=data.output;document.getElementById('status').textContent='Completed • Review before use';
 }catch(e){document.getElementById('status').textContent='Could not run. Start the Flask server and try again.'}
}
function copyResult(){navigator.clipboard.writeText(document.getElementById('result').textContent).then(()=>document.getElementById('status').textContent='Copied to clipboard').catch(()=>document.getElementById('status').textContent='Select and copy the output manually')}
</script></body></html>
"""

def make_output(topic, mode, level, context):
    t = topic.strip()
    extra = f"\n\nExtra instructions: {context.strip()}" if context.strip() else ""
    if mode == "notes":
        return (f"REVISION NOTES: {t}\nStudy level: {level}\n\n"
                f"1. Meaning\nWrite a clear definition of {t} in 2–3 sentences.\n\n"
                f"2. Key concepts\n• Main principle and how it works\n• Important components or terms\n• Common applications\n• Advantages and limitations\n\n"
                f"3. Exam revision\n• Learn the definition and working principle.\n• Prepare a labelled diagram if the topic is technical.\n"
                f"• Add one real-world example and key formulae, where applicable.\n\n"
                f"4. Self-check\nCan you explain {t} in your own words without looking at the notes?\n"
                f"{extra}\n\nNote: This starter prototype uses a template. Verify topic-specific facts from your course material.")
    if mode == "quiz":
        return (f"PRACTICE QUIZ: {t}\nStudy level: {level}\n\n"
                f"1. Define {t}.\n2. Explain the working principle of {t}.\n"
                f"3. List two applications of {t}.\n4. State two advantages and one limitation.\n"
                f"5. Draw or describe a relevant diagram, flowchart, or example.\n\n"
                f"Suggested method: answer without notes, then verify each response using your textbook.\n{extra}")
    if mode == "plan":
        return (f"3-DAY STUDY PLAN: {t}\nStudy level: {level}\n\n"
                f"DAY 1 — Understand\n• Read the basic definition and concepts (25 min).\n• Make a one-page summary (20 min).\n• Explain the topic aloud (10 min).\n\n"
                f"DAY 2 — Practise\n• Revise yesterday's summary (10 min).\n• Solve 5 questions or problems (30 min).\n• Mark doubts for review (10 min).\n\n"
                f"DAY 3 — Test and revise\n• Take a 20-minute closed-book test.\n• Correct mistakes using trusted notes.\n• Review key terms and formulas (15 min).\n{extra}")
    return (f"SIMPLE EXPLANATION: {t}\nStudy level: {level}\n\n"
            f"Start by answering three questions:\n1. What is {t}?\n2. Why is it needed?\n3. How does it work in a real example?\n\n"
            f"Try this structure: definition → principle → steps/components → example → advantages and limitations.\n"
            f"Write down any term you cannot explain and check it in your course material.\n{extra}\n\nNote: This prototype provides a learning scaffold, not an AI-generated factual explanation.")

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.post("/generate")
def generate():
    data = request.get_json(silent=True) or {}
    topic = str(data.get("topic", ""))[:160]
    mode = str(data.get("mode", "notes"))
    level = str(data.get("level", "Engineering"))
    context = str(data.get("context", ""))[:500]
    if not topic.strip():
        return jsonify({"output": "Please enter a topic."}), 400
    if mode not in {"notes", "quiz", "plan", "explain"}:
        mode = "notes"
    return jsonify({"output": make_output(topic, mode, level, context)})

if __name__ == "__main__":
    app.run(debug=True)
