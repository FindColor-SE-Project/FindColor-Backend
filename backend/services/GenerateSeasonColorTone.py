import openai
import os

# ดึง API Key จาก environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# ตั้งค่า API Key
openai.api_key = OPENAI_API_KEY

# เรียกใช้งาน ChatCompletion API
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "#ff5359 #e77076 #ea8b27 #e884c8 #fc5aa6 these colors are in which personal color (Summer, Spring, Autumn, and Winter)"}
    ]
)

# def getSeason(rgb):
#     return rgb

# พิมพ์ข้อความที่ได้จากการตอบกลับของ AI
print(completion.choices[0].message['content'])
