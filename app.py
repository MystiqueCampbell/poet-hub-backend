from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from config import VALID_TOKENS, OPENAI_MODEL

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def call_openai(prompt, max_tokens=1500):
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.choices[0].message.content

@app.route('/api/verify-token', methods=['POST'])
def verify_token():
    data = request.json
    token = data.get('token', '')
    if token in VALID_TOKENS:
        return jsonify({"valid": True})
    return jsonify({"valid": False})

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    poem = data.get('poem', '')
    prompt = f"""Analyze this poem comprehensively:

{poem}

Provide:
1. Overall tone and mood
2. Main themes
3. Strengths (what works well)
4. Weaknesses (areas for improvement)
5. Emotional impact rating (1-10)
6. Technical execution rating (1-10)

Be specific and actionable."""
    result = call_openai(prompt)
    return jsonify({"result": result})

@app.route('/api/rewrite', methods=['POST'])
def rewrite():
    data = request.json
    poem = data.get('poem', '')
    prompt = f"""Rewrite this poem in 3 different styles:

Original:
{poem}

Provide:
1. SOFTER VERSION (gentler, more vulnerable tone)
2. PUNCHIER VERSION (sharp, impactful, concise)
3. CINEMATIC VERSION (visual, expansive, story-driven)

Label each version clearly."""
    result = call_openai(prompt, max_tokens=2000)
    return jsonify({"result": result})

@app.route('/api/style-match', methods=['POST'])
def style_match():
    data = request.json
    poem = data.get('poem', '')
    poet = data.get('poet', '')
    prompt = f"""Rewrite this poem in the style of {poet}:

Original poem:
{poem}

Capture {poet}'s:
- Signature techniques
- Tone and voice
- Structural patterns
- Imagery choices
- Emotional approach

Provide the rewritten version."""
    result = call_openai(prompt, max_tokens=2000)
    return jsonify({"result": result})

@app.route('/api/title-gen', methods=['POST'])
def title_gen():
    data = request.json
    poem = data.get('poem', '')
    prompt = f"""Generate 10 compelling titles for this poem:

{poem}

Make titles:
- Emotionally engaging
- Instagram-friendly
- Mysterious or intriguing
- Memorable
- Varied in style (some poetic, some direct, some metaphorical)

List them numbered 1-10."""
    result = call_openai(prompt)
    return jsonify({"result": result})

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.json
    poem = data.get('poem', '')
    prompt = f"""Provide line-by-line feedback for this poem:

{poem}

For each line or section:
- What works
- What could be stronger
- Specific suggestions
- Alternative phrasings where helpful

Be encouraging but honest."""
    result = call_openai(prompt, max_tokens=2000)
    return jsonify({"result": result})

@app.route('/api/meter-rhythm', methods=['POST'])
def meter_rhythm():
    data = request.json
    poem = data.get('poem', '')
    prompt = f"""Analyze the meter and rhythm of this poem:

{poem}

Provide:
1. Rhythmic pattern analysis
2. Flow assessment (smooth vs. jarring)
3. Pacing evaluation
4. Line length variation impact
5. Suggestions for improving rhythm
6. Overall rhythm score (1-10)"""
    result = call_openai(prompt)
    return jsonify({"result": result})

@app.route('/api/imagery-score', methods=['POST'])
def imagery_score():
    data = request.json
    poem = data.get('poem', '')
    prompt = f"""Evaluate the imagery in this poem:

{poem}

Provide:
1. Imagery strength rating (1-10)
2. Most powerful images
3. Weak or cliché imagery
4. Sensory details assessment (visual, tactile, auditory, etc.)
5. Specific suggestions for stronger imagery
6. Examples of how to enhance 2-3 lines"""
    result = call_openai(prompt)
    return jsonify({"result": result})

@app.route('/api/voice-detection', methods=['POST'])
def voice_detection():
    data = request.json
    poem = data.get('poem', '')
    prompt = f"""Identify the unique voice and writing identity in this poem:

{poem}

Analyze:
1. Voice characteristics (formal, conversational, raw, etc.)
2. Recurring stylistic choices
3. Emotional signature
4. Unique strengths in this writer's voice
5. How to amplify their authentic voice
6. Comparison to similar poets (if applicable)"""
    result = call_openai(prompt)
    return jsonify({"result": result})

@app.route('/api/prompt-expander', methods=['POST'])
def prompt_expander():
    data = request.json
    idea = data.get('idea', '')
    prompt = f"""Expand this poetry idea into a full draft poem:

Idea: {idea}

Create a complete poem (12-20 lines) that:
- Develops the core concept
- Uses vivid imagery
- Has emotional depth
- Maintains consistent tone
- Includes specific details
- Feels authentic and raw"""
    result = call_openai(prompt, max_tokens=1500)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
