from flask import Flask, jsonify, request
import random

app = Flask(__name__)

def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

@app.route("/")
def play_game():
    # Get user choice from query parameter (default to 'rock' if not provided)
    user_choice = request.args.get("user_choice", "rock")
    if user_choice not in ["rock", "paper", "scissors"]:
        return jsonify({"error": "Invalid choice. Please choose 'rock', 'paper', or 'scissors'."}), 400
    
    computer_choice = get_computer_choice()
    
    return jsonify({
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "result": determine_winner(user_choice, computer_choice)
    })

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "scissors" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock"):
        return "You win!"
    else:
        return "You lose!"

if __name__ == "__main__":
    # Start Flask app without Prometheus server
    app.run(host="0.0.0.0", port=8080)
