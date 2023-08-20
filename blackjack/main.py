from blackjack.core import Game

def main():
    print("Let's play BlackJack!\n")
    num_players = ask_number_of_players()
    
    game = Game(num_players=num_players)
    game.start()
    

def ask_number_of_players():
    while True:
        try:
            num = int(input('How many players will play (1-6): '))
            if num < 1 or num > 6:
                print("Value should be value between 1 and 6!")
            else:
                return num
        except ValueError:
            print("Value must be an integer!")


if __name__ == "__main__":
    main()