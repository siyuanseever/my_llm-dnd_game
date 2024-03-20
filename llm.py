import copy
import os

from zhipuai import ZhipuAI
from openai import OpenAI

MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")

CHAT_FUNC = "chat_glm"

def chat_kimi(messages) -> str:
    client = OpenAI(
        api_key=MOONSHOT_API_KEY,
        base_url="https://api.moonshot.cn/v1",
    )

    completion = client.chat.completions.create(
      model="moonshot-v1-8k",
      messages=messages,
      temperature=0.3,
    )
    return completion


def chat_glm(messages):
    client = ZhipuAI(api_key="5c43d4873ee6d67c69c195fc86b5872f.581qTcuFl6ezdTcj") # 填写您自己的APIKey

    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages
    )

    return response
    

def chat(query:str, history:list=[]):
    messages = copy.copy(history)
    messages.append({"role": "user", "content": query})

    chat_func = eval(CHAT_FUNC)
    response = chat_func(messages)
    
    answer = response.choices[0].message.content
    messages.append({
        "role": response.choices[0].message.role,
        "content": response.choices[0].message.content,
    })
    return messages, answer

if __name__ == "__main__":
    response = chat("你好")
    print(f"response:{response}")
