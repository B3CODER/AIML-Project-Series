# Q&A Bot for College Admission

This project is a Flask-based chatbot designed to assist users with inquiries related to college admissions. The chatbot can handle a variety of queries about the admission process, eligibility criteria, available courses, fees, and more.

## What is a Chatbot?

A chatbot is a software application designed to simulate human conversation. It interacts with users using natural language, allowing them to ask questions and receive relevant responses. Chatbots are widely used for customer service, information retrieval, and automating repetitive tasks.

## Why Do We Need a Chatbot?
### Chatbots provide several benefits, including:

- 24/7 Availability: They can assist users at any time, providing immediate responses to queries.
- Consistency: They offer consistent information, reducing the chances of human error.
- Efficiency: They can handle multiple queries simultaneously, improving user experience and reducing wait times.
- Cost-effective: They help reduce operational costs by automating routine tasks and customer interactions.

## Features

- User Interaction: The chatbot can greet users and respond to common greetings.
- Admission Information: It provides detailed information about the admission process, including application deadlines, eligibility criteria, and required documents.
- Course Information: Users can inquire about the courses offered and the associated tuition fees.
- Scholarship Details: The chatbot provides information on how to apply for scholarships.
- Campus Information: It gives details about the campus location and available accommodations.
- Contact Information: Users can get contact details for the admission office.
- Error Handling: The chatbot handles unknown queries gracefully by prompting the user to rephrase their question.
- Logging: All interactions are logged for future reference and analysis.

## Requirements

To install the required packages for this project, run:

```bash
pip install -r requirements.txt
```
---------------------------------------------------------------------------

# Project Structure

```bash
Project2_Q&A_Bot_for_College_Admission/
│
├── static/
│   └── styles.css
│
├── templates/
│   └── index.html
│
├── interaction_log.json
│
├── chatbot.py
│
├── main.py
│
├── long_responses.py
│
└── requirements.txt

```
---------------------------------------------------------------------------

# Setup Instructions

1) Clone the repository:
   ```bash
   git clone https://github.com/yourusername/admission_chatbot.git 
   cd admission_chatbot
   ```
2) Install dependencies: 
   ```bash
   pip install -r requirements.txt
    ```  
3) Run the chatbot:
   ```bash
   python chatbot.py
   ```
4) Access the chatbot: 
    Open your web browser and go to http://127.0.0.1:5000/.
   
