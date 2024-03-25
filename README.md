# encodeai
# Chef Assistant Chatbot

## Description
This Python script implements a chatbot using OpenAI's GPT-3.5 model. The chatbot assists users in various culinary tasks, such as suggesting dishes based on ingredients provided, providing recipes for specified dishes, and critiquing recipes provided by users.

## Usage
1. Upon execution, the script prompts the user to input the name of a dish they want a recipe for.
2. The user then inputs the dish name.
3. The chatbot then requests the user for a detailed recipe and preparation steps for the specified dish.
4. The GPT-3.5 model processes the input messages and provides a response, either suggesting a recipe, critiquing the provided recipe, or requesting clarification if the input does not match one of the predefined scenarios.
5. The conversation continues iteratively, with the user and the chatbot exchanging messages until terminated by the user.

## Input Scenarios
- **Suggesting Dishes:** If the user inputs one or more ingredients, the chatbot suggests a dish name that can be made with those ingredients.
- **Requesting a Recipe:** If the user inputs the name of a dish, the chatbot provides a recipe for that dish.
- **Providing a Recipe for Critique:** If the user provides a recipe for a dish, the chatbot critiques the recipe and suggests changes.

## Dependencies
- `openai`: The script relies on the OpenAI API to interact with the GPT-3.5 model.

## Usage Example
```python
# Initialize OpenAI client and retrieve user input
from openai import OpenAI

client = OpenAI()

# Define initial system prompt
system_prompt = """
    You are an experienced chef that likes suggesting dishes based on ingredients, giving recipes to dishes, or criticizing the recipes given any your user input.  

    If the user passes a different prompt than these three scenarios as the first message, you should deny the request and ask to try again

    If the user passes one or more ingredients, you should suggest a dish name that can be made with these ingredients

    Try to make you suggest the dish name only, and not the recipe at this stage

    If the user passes a dish name, you should give a recipe for that dish

    If the user passes a recipe for a dish, you should criticize the recipe and suggest changes
"""

# Define initial message
messages = [
    {
        "role": "system",
        "content": system_prompt,
    }
]

# Get dish name from user input
dish = input("Type the name of the dish you want a recipe for:\n")
messages.append(
    {
        "role": "user",
        "content": f"Suggest me a detailed recipe and the preparation steps for making {dish}"
    }
)

# Define GPT-3.5 model
model = "gpt-3.5-turbo"

# Initialize chat stream
stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)

# Collect and print responses
collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

# Add collected responses to message history
messages.append(
    {
        "role": "system",
        "content": "".join(collected_messages)
    }
)

# Continuously interact with user
while True:
    print("\n")
    user_input = input()
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)
    
    messages.append(
        {
            "role": "system",
            "content": "".join(collected_messages)
        }
    )
