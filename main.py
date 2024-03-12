import prompt
import game


def main():
    history = [
        {"role": "user", "content": prompt.background+prompt.goal+prompt.instruction},
        {"role": "assistant", "content": prompt.one_shot},
    ]
    result_json = eval(prompt.one_shot)

    while True:
        # show
        game.show_status(result_json)

        # status
        game_status = game.update_status(result_json)
        
        # choice
        choice = game.make_choice(game_status, result_json)
        
        # chat
        history, result_json = game.safe_chat(choice, history)
            
        # finish
        if game.game_over(game_status):
            break


if __name__ == "__main__":
    main()
