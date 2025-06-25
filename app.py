from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, JournalEntry
from config import Config
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_mistralai import ChatMistralAI

# Load .env variables
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

os.makedirs(app.instance_path, exist_ok=True)


# Initialize Mistral LLM via LangChain
llm = ChatMistralAI(model="mistral-tiny")

# Summarization Chain
summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="""You are a journaling assistant. 
    Given this journal entry:
    "{text}"

    Summarize it in 2-3 lines, then detect the mood in one word.
    Return in the following format:
    Summary: <summary text>
    Mood: <mood word>"""
)
summary_chain = LLMChain(llm=llm, prompt=summary_prompt, output_key="result")

@app.route('/entry', methods=['POST'])
def add_entry():
    data = request.json
    text = data.get('text')

    # Call LangChain chain
    result = summary_chain.run(text=text)

    # Parse summary and mood
    try:
        summary_part, mood_part = result.split("Mood:")
        summary = summary_part.replace("Summary:", "").strip()
        mood = mood_part.strip()
    except ValueError:
        summary = "Could not generate summary."
        mood = "Unknown"

    # Save to DB
    new_entry = JournalEntry(text=text, summary=summary, mood=mood)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Entry saved successfully."}), 201


@app.route('/entries', methods=['GET'])
def get_entries():
    entries = JournalEntry.query.order_by(JournalEntry.created_at.desc()).all()
    result = [
        {
            "id": e.id,
            "text": e.text,
            "summary": e.summary,
            "mood": e.mood,
            "created_at": e.created_at.strftime('%Y-%m-%d %H:%M')
        } for e in entries
    ]
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
