from flask import Flask, jsonify, render_template, request
import openai
import pandas as pd
import os
app = Flask(__name__)

openai.api_key = 'sk-proj-5mlkKHx2VA3k0Iq9hQ6iT3BlbkFJGvwcapJswEEDv5pONobS'


data = pd.read_csv('Vivriti_Details.csv')

def ask_question(question):

    prompt = "You have the following project details:\n\n"
    for _, row in data.iterrows():
        prompt += (f"Members: {row['Members']}\n"
                   f"Class: {row['Class']}\n"
                   f"Name of Project: {row['Name of Project']}\n"
                   f"Project Description: {row['Project Description ']}\n"
                   f"Subject: {row['Subject']}\n"
                   f"Venue: {row['Venue']}\n\n")
                 
    prompt += f"\nThe user asked the question: {question}\n\nProvide a detailed answer based on the project details above. The project details are for an event named VIVRITI, NPSHSR's science fest.Principal Mrs. Shefali Tyagi."

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful precise accurate assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message['content'].strip()
    return answer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    answer = ask_question(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=80)
