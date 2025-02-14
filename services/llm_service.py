import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()


def extract_credit_card_number():
    BASE_URL = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('AIPROXY_TOKEN')}"
    }
    image_path = "./data/credit_card.png"
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        raise Exception("Credit card image not found at the specified path.")

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that provides detailed and accurate descriptions of images. "
                    "Focus on describing the objects, colors, textures, the overall scene, and most importantly, "
                    "the text and numbers in the image. Be concise but thorough."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are given an image containing a credit card number. Extract the credit card number from the image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        cno = result["choices"][0]["message"]["content"].strip()
        output_path = "./data/credit-card.txt"
        with open(output_path, "w") as f:
            f.write(cno)
        return cno
    else:
        raise Exception(
            f"LLM API error: {response.status_code} {response.text}")
