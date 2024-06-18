from flask import Flask, render_template, request, jsonify
import re
from main import check_all_messages, update_memory

app = Flask(__name__)

# Define routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    split_message = re.split(r'\s+|[,;?!.-]\s*', userText.lower())
    response = check_all_messages(split_message)
    update_memory(userText, response)  # Update memory based on user input and bot response
    return jsonify(response)

# Error handling for 404 - Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return "Sorry, the page you are looking for does not exist.", 404

# Error handling for 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return "Oops! Something went wrong on our end.", 500

if __name__ == "__main__":
    app.run(debug=True)
