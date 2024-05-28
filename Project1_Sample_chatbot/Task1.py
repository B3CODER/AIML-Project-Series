import tkinter as tk
from tkinter import scrolledtext
import datetime
import re
import requests
from googletrans import Translator
import random
class SimpleChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Chatbot")

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=60, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # User input field
        self.user_input = tk.Entry(root, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.process_user_input)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Chatbot memory for previous interactions and questions
        self.memory = {'questions': [
            "What's your name?",
            "What do you like to do for fun?",
            "Do you have any favorite books or movies?"
        ], 'question_index': 0, 'user_info': {}}

        # Greeting message
        self.display_message("Chatbot", "Hello! How can I assist you today?")

    def display_message(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def process_user_input(self):
        user_message = self.user_input.get().strip()
        if user_message:
            self.display_message("You", user_message)
            self.user_input.delete(0, tk.END)
            self.respond_to_user(user_message)

    def respond_to_user(self, message):
        if self.memory['question_index'] < len(self.memory['questions']):
            if self.memory['question_index'] == 0:
                self.memory['user_info']['name'] = message
                response = f"Nice to meet you, {message}! " 
            elif self.memory['question_index'] == 1:
                self.memory['user_info']['hobby'] = message
                response = f"{message} sounds fun! " 
            elif self.memory['question_index'] == 2:
                self.memory['user_info']['favorites'] = message
                response = f"I like those too! " 
        else:
            response = self.generate_response(message)
        
        self.display_message("Chatbot", response)
        if self.memory['question_index'] < len(self.memory['questions']):
            next_question = self.memory['questions'][self.memory['question_index']]
            self.memory['question_index'] += 1
            self.display_message("Chatbot", next_question)

    def generate_response(self, message):
        message = message.lower()
        responses = {
            "hi": "Hello! How can I help you?",
            "how are you": "I'm a bot, so I'm always good. How about you?",
            "what is your name": "I am a simple chatbot created to assist you.",
            "what can you do": "I can chat with you, tell you today's date, provide weather information, tell a joke, provide news headlines, provide famous quotes, and perform basic math operations.",
            "bye": "Goodbye! Have a nice day!"
        }

        if message in responses:
            return responses[message]
        elif "date" in message:
            return f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}."
        elif "weather" in message:
            return self.get_weather()
        elif "joke" in message:
            return self.get_jokes(message)
        elif "news" in message:
            return self.get_news()
        elif "quote" in message:
            return self.get_quote()
        elif "translate" in message:
            return self.translate_message(message)
        elif "wiki" in message:
            return self.search_wikipedia(message)
        elif re.search(r'\b(add|plus|subtract|minus|multiply|times|divide|over)\b', message):
            return self.handle_math_operations(message)
        else:
            return "I understand and okay what next, what question you want to ask."

    def get_weather(self):
        weather_data = {
            "description": "Sunny",
            "temperature": "25°C",
            "location": "Your location"
        }
        return f"Today's weather in {weather_data['location']}: {weather_data['description']}, {weather_data['temperature']}."

    def get_jokes(self, message):
        num_jokes = self.extract_number(message)
        if num_jokes:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Parallel lines have so much in common. It's a shame they'll never meet.",
                "I told my wife she should embrace her mistakes. She gave me a hug."
            ]
            if num_jokes > len(jokes):
                num_jokes = len(jokes)
            return "\n\n".join(jokes[:num_jokes])
        else:
            return "Here's a joke: Why don't scientists trust atoms? Because they make up everything!"

    def get_news(self):
        api_key = '8f8b9f5b94a343779d917e71f586d64d'
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                news_data = response.json()
                articles = news_data.get('articles', [])

                if articles:
                    headlines = [f"{article['title']} - {article['description']}" for article in articles[:3]]
                    return "\n".join(headlines)
                else:
                    return "No news articles found."
            else:
                return "Failed to fetch news."
        except Exception as e:
            print(f"Error fetching news: {e}")
            return "Error fetching news. Please try again later."

    def get_quote(self):
        quotes = [
            "The only way to do great work is to love what you do. – Steve Jobs",
            "Start where you are. Use what you have. Do what you can. – Arthur Ashe",
            "In the end, it's not the years in your life that count. It's the life in your years. – Abraham Lincoln"
        ]
        return f"Here's a famous quote: {random.choice(quotes)}"

    def handle_math_operations(self, message):
        # Extract numbers from message
        numbers = re.findall(r'\d+', message)
        if len(numbers) >= 2:
            num1 = int(numbers[0])
            num2 = int(numbers[1])

            if "add" in message or "plus" in message:
                result = num1 + num2
                return f"The sum of {num1} and {num2} is {result}."
            elif "subtract" in message or "minus" in message:
                result = num1 - num2
                return f"The difference between {num1} and {num2} is {result}."
            elif "multiply" in message or "times" in message:
                result = num1 * num2
                return f"The product of {num1} and {num2} is {result}."
            elif "divide" in message or "over" in message:
                if num2 == 0:
                    return "Cannot divide by zero."
                result = num1 / num2
                return f"{num1} divided by {num2} is {result}."
        return "Invalid operation. Please provide two numbers and specify the operation (add, subtract, multiply, divide)."

    def translate_message(self, message):
    # Extract source and target languages from user input
        match = re.search(r'translate (.*) to (.*)', message.lower())
        if match:
            source_text = match.group(1).strip()
            target_lang = match.group(2).strip()
        
            translator = Translator()
            try:
                translation = translator.translate(source_text, dest=target_lang)
                return f"Translation from {translation.src} to {translation.dest}: {translation.text}"
            except Exception as e:
                print(f"Translation error: {e}")
                return "Translation error. Please try again later."
        else:
            return "Invalid translation format. Please provide a message to translate and the target language."


    def search_wikipedia(self, message):
        search_query = message.replace("wiki ", "")
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&redirects=1&titles={search_query}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                pages = data['query']['pages']
                for page_id in pages:
                    return pages[page_id]['extract']
            else:
                return "No Wikipedia article found."
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return "Wikipedia search error. Please try again later."

    def extract_number(self, message):
        # Extracts number of jokes requested
        numbers = re.findall(r'\d+', message)
        if numbers:
            return int(numbers[0])
        return None

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = SimpleChatbot(root)
    root.mainloop()
