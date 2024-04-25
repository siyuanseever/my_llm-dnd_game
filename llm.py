import copy
import os

class BaseChat(object):
    def __init__(self):
        pass

    def generate(self, messages):
        pass

    def chat(self, query:str, history:list=[]):
        messages = copy.copy(history)
        messages.append({"role": "user", "content": query})

        message = self.generate(messages)
        
        answer = message["content"]
        messages.append(message)
        return messages, answer


class KimiChat(BaseChat):
    def __init__(self):
        super().__init__()
        from openai import OpenAI

        MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
        self.client = OpenAI(
            api_key=MOONSHOT_API_KEY,
            base_url="https://api.moonshot.cn/v1",
        )

    def generate(self, messages):
        response = self.client.chat.completions.create(
          model="moonshot-v1-8k",
          messages=messages,
          temperature=0.3,
        )
        message = {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content,
        }
        return message


class GLMChat(BaseChat):
    def __init__(self):
        super().__init__()
        from zhipuai import ZhipuAI
        self.client = ZhipuAI(api_key="5c43d4873ee6d67c69c195fc86b5872f.581qTcuFl6ezdTcj") # 填写您自己的APIKey

    def generate(self, messages):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=messages
        )
        message = {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content,
        }
        return message


class GeminiChat(BaseChat):
    def __init__(self):
        super().__init__()
        import google.generativeai as genai
        GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def generate(self, messages):
        role_dict = {
            "user": "user",
            "system": "user",
            "assistant": "model",
        }
        messages_reform = []
        for message in messages:
            messages_reform.append({
                "role": role_dict[message["role"]],
                "parts": [message["content"]],
            })

        response = self.model.generate_content(messages_reform)
        message = {"role": "assistant", "content": response.text}
        return message

chat = GLMChat().chat
# chat = GeminiChat().chat

if __name__ == "__main__":
    response = chat("你好")
    print(f"response:{response}")
