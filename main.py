import game

def main(debug=False):
    
    game_tune = 0

    history, result_json = game.init_game()
    while True:
        # show
        game.show_status(result_json)

        # status
        game_status = game.update_status(result_json)
        
        # choice
        choice = game.make_choice(game_status, result_json)
        
        # chat
        history, result_json = game.safe_chat(choice, history)
            
        # over
        if game.game_over(game_status):
            game.show_status(result_json)

            game_tune += 1
            if game_tune >= 1:
                break

            # restart
            history, result_json = game.init_game()




if __name__ == "__main__":
    main()
