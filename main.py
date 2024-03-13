import game

def main(debug=False):
    
    history, result_json = game.init_game()
    game_step = 0

    while True:
        game_step += 1

        # show
        game.show_status(result_json, game_step)

        # status
        game_status = game.update_status(result_json, game_step)
        
        # choice
        choice = game.make_choice(game_status, result_json)
        
        # chat
        history, result_json = game.safe_chat(choice, history)
            
        # over
        if game.game_over(game_status):
            game.show_status(result_json, game_step)
            break




if __name__ == "__main__":
    main()
