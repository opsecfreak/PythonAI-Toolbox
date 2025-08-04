import os
import asyncio
from flask import Flask, request, render_template_string
from agents import get_agents
from utils.database import log_interaction
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HTML_TEMPLATE = """
<!doctype html>
<title>AI Agent</title>
<h1>Ask the Code Agent</h1>
<form method="POST">
  <textarea name="prompt" rows="5" cols="60" placeholder="Enter your prompt here...">{{prompt}}</textarea><br>
  <input type="submit" value="Submit">
</form>
{% if response %}
<hr>
<h2>Response</h2>
<div style="white-space: pre-wrap;">{{response}}</div>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    response = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        agents = get_agents()
        config = agents.get("code")
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": config["instructions"]},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        response = completion.choices[0].message.content
        
        # log interaction asynchronously
        asyncio.run(log_interaction("code", prompt, response))

    return render_template_string(HTML_TEMPLATE, prompt=prompt, response=response)

if __name__ == "__main__":
    app.run(debug=True)
