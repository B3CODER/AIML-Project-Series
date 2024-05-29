import os
import json
from datetime import datetime
import long_responses as long  # Assuming you have a module for long responses

# Function to log interactions
def log_interaction(user_message, bot_response):
    interaction = {
        "timestamp": datetime.now().isoformat(),
        "user_message": user_message,
        "bot_response": bot_response
    }
    log_file = "interaction_log.json"  # Change the file name if needed
    mode = 'a' if os.path.exists(log_file) else 'w'
    with open(log_file, mode) as f:
        if mode == 'a':
            f.write(',\n')
        json.dump(interaction, f, indent=4)
    return interaction

# Maintain a memory dictionary to store context
memory = {}

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Example responses (you can add more)
    response('Hello! I am your Chat bot', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace', 'nice', 'meet'], required_words=['code', 'palace'])
    response('I am glad I met you!', ['nice', 'meet'], required_words=['meet'])
    response('Bye Good Night', ['good', 'night'], required_words=['night'])
    response('Good to hear that', ['good', 'fine', 'great'])
    response('Yes my dear', ['really'])
    response('Our admission process includes filling out an online application, submitting required documents, and attending an interview.', 
             ['admission', 'process'], required_words=['admission', 'process'])
    response('The application deadline is June 30th.', 
             ['application', 'deadline'], required_words=['application', 'deadline'])
    response('We offer undergraduate, postgraduate, and doctoral programs in various fields such as engineering, science, and management.', 
             ['courses', 'offered'], required_words=['courses', 'offered'])
    response('The tuition fee for undergraduate programs is $10,000 per year.', 
             ['tuition', 'fee'], required_words=['tuition', 'fee'])
    response('You can apply for a scholarship by submitting a scholarship application along with your admission form.', 
             ['scholarship', 'apply'], required_words=['scholarship', 'apply'])
    response('Our campus is located in the heart of the city, easily accessible by public transport.', 
             ['campus', 'location'], required_words=['campus', 'location'])
    response('The eligibility criteria include a minimum of 75% in high school for undergraduate programs.', 
             ['eligibility', 'criteria'], required_words=['eligibility', 'criteria'])
    response('The entrance exam is scheduled for July 15th.', 
             ['entrance', 'exam', 'date'], required_words=['entrance', 'exam', 'date'])
    response('You can contact the admission office at admission@example.com or call us at (123) 456-7890.', 
             ['contact', 'admission', 'office'], required_words=['contact', 'admission', 'office'])
    response('Yes, we provide on-campus accommodation for all students.', 
             ['accommodation', 'available'], required_words=['accommodation', 'available'])

    # Check if there is context to provide a more personalized response
    if 'context' in memory:
        for key in memory['context']:
            if key in highest_prob_list:
                highest_prob_list[key] += memory['context'][key]

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    # Update memory with current interaction
    memory['context'] = { best_match: memory.get('context', {}).get(best_match, 0) + 1 }

    if highest_prob_list[best_match] < 1:
        bot_response = long.unknown()  # If no suitable response found, use a fallback response
        log_interaction(' '.join(message), bot_response)  # Log the interaction
        return bot_response
    else:
        bot_response = best_match
        log_interaction(' '.join(message), bot_response)  # Log the interaction
        return bot_response

def update_memory(user_message, bot_response):
    # Update memory based on user's message and bot's response
    if 'context' not in memory:
        memory['context'] = {}

    # Store the interaction in memory
    if bot_response in memory['context']:
        memory['context'][bot_response] += 1
    else:
        memory['context'][bot_response] = 1

    with open('memory.json', 'w') as f:
        json.dump(memory, f, indent=4)



