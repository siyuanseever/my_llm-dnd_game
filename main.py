from prompt import prompt, instruction, one_shot, chat_show_keys
from script import chat, is_convertible_to_int

history = [
    {"role": "user", "content": prompt+instruction},
    {"role": "assistant", "content": one_shot},
]
result_json = eval(one_shot)
max_retry = 3


while True:
    # show
    text = ''
    for key in chat_show_keys:
        text += f'{key}: {result_json[key]}\n'
    text += 'options: \n'
    for i, o in enumerate(result_json['options']):
        text += f'\t{i}: {o}\n'
    text += '\tor: 其它任意决策'
    print(text)

    # finish
    if result_json['goal_percentage'] >= 1.0:
        print("GG~")
        print("🎮🎉🎮 (＾▽＾) (＾▽＾) 🎉🎮🎉")
        break
    
    # choice
    choice = input('input number or other text: ')
    if is_convertible_to_int(choice) and 0 <= int(choice) < len(result_json['options']):
        choice = result_json['options'][int(choice)]
    print('=' * 100 + '\n' +  '...***' + choice + '***...')
    
    # chat
    retry_num = 0
    while retry_num <= max_retry:
        try:
            history_tmp, answer = chat(choice, history)
            result_json = eval(answer)
            break
        except:
            retry_num += 1
    if retry_num > max_retry:
        print('[error]', history)
        print('[error]', answer)
        print('[error]')
        break
    else:
        history = history_tmp
