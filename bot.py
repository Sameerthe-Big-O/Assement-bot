from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))  

@app.route("/bot/general", methods=["POST"])
def general_bot():
    user_message = request.json["message"]
    
    try:
        completion = openai.ChatCompletion.create(
            messages=[
                {"role": "system", "content": "You are a interview assistant."},
                {"role": "user", "content": user_message},
            ],
            model="gpt-3.5-turbo"
        )
        
        bot_message = completion.choices[0].message.content
        return jsonify({"message": bot_message}), 200
    except Exception as e:
        print("Error communicating with OpenAI:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/bot/generate-questions", methods=["POST"])
def generate_questions():
    data = request.json
    role = data["role"]
    level = data["level"]
    description = data["description"]
    
    try:
        completion = openai.ChatCompletion.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Generate interview questions for a {level} {role} specializing in {description}.",
                },
            ],
            model="gpt-3.5-turbo"
        )
        
        bot_message = completion.choices[0].message.content
        return jsonify({"message": bot_message}), 200
    except Exception as e:
        print("Error communicating with OpenAI:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/bot/evaluate-answers", methods=["POST"])
def evaluate_answers():
    data = request.json
    candidate_answers = data["candidateAnswers"]
    role_requirements = data["roleRequirements"]
    
    try:
        completion = openai.ChatCompletion.create(
            messages=[
                {"role": "system", "content": "You are an assesment bot of canidate."},
                {
                    "role": "user",
                    "content": "Evaluate the following candidate answers based on the role requirements.",
                },
                {
                    "role": "user",
                    "content": f"Candidate Answers: {candidate_answers}",
                },
                {
                    "role": "user",
                    "content": f"Role Requirements: {role_requirements}",
                },
            ],
            model="gpt-3.5-turbo"
        )
        
        bot_message = completion.choices[0].message.content
        return jsonify({"message": bot_message}), 200
    except Exception as e:
        print("Error communicating with OpenAI:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
