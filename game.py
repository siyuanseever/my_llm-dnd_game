import os

import prompt
import script
import llm
import config

debug = os.environ.get("DEBUG")

GAME_STATUS = {
    "inprogress": 0,
    "win": 1,
    "lose": 2,
}

def init_game():
    history = [
        {"role": "user", "content": 
            prompt.background + prompt.goal + prompt.instruction
        },
        {"role": "assistant", "content": prompt.one_shot},
    ]
    result_json = eval(prompt.one_shot)

    return history, result_json


def show_status(result_json, game_step, show_options=True):
    text = ''
    for key in prompt.chat_show_keys:
        text += f'{key}: {result_json[key]}\n'

    goal_completion_percentage = round(result_json['goal_percentage'] * 100)
    text += f'goal completion: {goal_completion_percentage}%\n'

    text += f'total steps: {game_step}/{config.GAME_MAX_STEPS}\n'

    if show_options:
        text += 'options: \n'
        for i, o in enumerate(result_json['options']):
            text += f'\t{i}: {o}\n'
        text += f'\t{prompt.other_choices}'

    print(text)


def update_status(result_json, game_step, goal_score: float = 1.0):
    game_status = GAME_STATUS["inprogress"]

    if result_json['goal_percentage'] >= goal_score:
        print("GG~")
        print("🎮🎉🎮 (＾▽＾) (＾▽＾) 🎉🎮🎉")
        print("To be continued~")
        game_status = GAME_STATUS["win"]
    elif result_json['goal_percentage'] < 0.0 or game_step >= config.GAME_MAX_STEPS:
        print("You Lose.")
        game_status = GAME_STATUS["lose"]

    return game_status


def reform_choice(choice, result_json):
    if len(choice) == 0:
        choice = '0'
    if script.is_convertible_to_int(choice) and 0 <= int(choice) < len(result_json['options']):
        choice = result_json['options'][int(choice)]
    return choice


def make_choice(game_status, result_json):
    if game_status == GAME_STATUS["win"]:
        choice = prompt.game_win_show
    elif game_status == GAME_STATUS["lose"]:
        choice = prompt.game_lose_show
    else:
        if debug:
            # choice = str(random.randint(0, len(result_json['options'])-1))
            choice = ''
        else:
            choice = input('input number or other text: ')

        choice = reform_choice(choice, result_json)
        print('=' * 100 + '\n' +  '...***' + choice + '***...')
    return choice


def safe_chat(choice, history, max_retry=3):
    retry_num = 0
    while retry_num <= max_retry:
        try:
            history_tmp, answer = llm.chat(
                choice + prompt.every_chat_prompt, 
                history
            )
            result_json = eval(answer)
            break
        except Exception as e:
            if debug:
                print('[warning]', e)
            retry_num += 1
    if retry_num > max_retry:
        print('[error]', history_tmp)
        print('[error]', answer)
        print('[error]')
        assert False
    else:
        history = history_tmp

    return history, result_json

def game_over(game_status):
    if game_status in [
        GAME_STATUS["win"],
        GAME_STATUS["lose"],
    ]:
        return True
    return False
