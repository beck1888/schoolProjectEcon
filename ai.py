import openai

def debate_me(name: str, supports_prop_32: bool, reasons: list, justification: str, user_profile: list, openai_api_key: str) -> str:
    client = openai.Client(api_key=openai_api_key)

    # Create the prompt
    if supports_prop_32:
        support = "supports"
    else:
        support = "does not support"

    with open("static_assets/prop_32_description.md") as f:
        content = ""
        for line in f:
            content += line

    with open("static_assets/prop32_extra_info.txt") as f:
        extra_info = ""
        for line in f:
            extra_info += line


    prompt = f"Proposition 32 is the following: {content}\n\n{name} {support} Proposition 32. Using these facts, write a short, persuasive argument against their view point."

    # Generate the response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Proposition 32 is a CA ballot measure to do the following: {content} and {extra_info}"},
            {"role": "system", "content": f"{name} {support} Proposition 32. Your task is to write a short, persuasive letter to {name} trying to get them to change their view point (try to spin their logic against them, be argumentative, appeal to the reasons they give). The letter should be from Jane Doe, a concerned friend. The letter should be short and to the point."},
            {"role": "system", "content": f"Here's some extra info about {name} to inform your response: {str(user_profile)}. Make sure to use all of this info. Do not include ay information placeholders in your response."},
            {"role": "system", "content": f"Here is why the user {support} Proposition 32: {reasons} and here is why they {support} it: {justification}"},
        ]
    )

    return response.choices[0].message.content