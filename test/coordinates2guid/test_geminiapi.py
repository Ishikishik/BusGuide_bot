"""
1.pip install -q -U google-generativeaiを叩く(geminiのapiをとっておく必要がある)
2.
"""


import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env をロード
load_dotenv()

# 環境変数から取得
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-latest")

prompt = "別宮町九丁目, 今治市, 愛媛県, 794-0069, 日本, の都市名と名物を25文字程度で教えてください"
response = model.generate_content(prompt)

print(response.text)