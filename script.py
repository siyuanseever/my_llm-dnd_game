from zhipuai import ZhipuAI
import copy

def chat(query:str, history:list=[]):
    client = ZhipuAI(api_key="5c43d4873ee6d67c69c195fc86b5872f.581qTcuFl6ezdTcj") # 填写您自己的APIKey

    messages = copy.copy(history)
    messages.append({"role": "user", "content": query})
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=messages
    )
    
    answer = response.choices[0].message.content
    messages.append({
        "role": response.choices[0].message.role,
        "content": response.choices[0].message.content,
    })
    return messages, answer

def is_convertible_to_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
