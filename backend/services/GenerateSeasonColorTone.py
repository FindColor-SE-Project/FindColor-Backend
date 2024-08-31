from openai import OpenAI
client = OpenAI()
def getSeason(rgb):
    rgb_str = str(rgb)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You know personal color and you only answer in a word."},
            {
                "role": "user",
                "content": f"What is the season of the RGB color {rgb_str}?"
            }
        ]
    )
    return completion.choices[0].message


print(getSeason((100,50,31)))