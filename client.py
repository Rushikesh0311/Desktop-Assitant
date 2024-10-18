import openai

# Replace with your actual API key
openai.api_key = "YOUR_NEW_API_KEY_HERE"

response = openai.ChatCompletion.create(
    model="gpt-4",  # Correct model name, verify if needed
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(response.choices[0].message['content'])
