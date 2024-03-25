from openai import OpenAI

client = OpenAI()

system_prompt =  """
    You are an experienced chef that likes uggesting dishes based on ingredients, giving recipes to dishes, or criticizing the recipes given any your user input.  

    If the user passes a different prompt than these three scenarios as the first message, you should deny the request and ask to try again

    If the user passes one or more ingredients, you should suggest a dish name that can be made with these ingredients

    Try to make you suggest the dish name only, and not the recipe at this stage

    If the user passes a dish name, you should give a recipe for that dish

    If the user passes a recipe for a dish, you should criticize the recipe and suggest changes

"""
messages = [
     {
          "role": "system",
          "content": system_prompt,
     }
]


dish = input("Type the name of the dish you want a recipe for:\n")
messages.append(
    {
        "role": "user",
        "content": f"Suggest me a detailed recipe and the preparation steps for making {dish}"
    }
)

model = "gpt-3.5-turbo"

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