import random


def setup_game():
    doors = ['A', 'B', 'C']
    prize_door = random.choice(doors)
    return prize_door, doors


def player_choice(doors):
    choice = input(f"Выберите дверь ({', '.join(doors)}): ").strip().upper()
    while choice not in doors:
        choice = input(f"Неверный выбор. Выберите дверь ({', '.join(doors)}): ").strip().upper()
    return choice


def reveal_door(doors, player_choice, prize_door):
    remaining_doors = set(doors) - {player_choice, prize_door}
    revealed_door = random.choice(list(remaining_doors))
    return revealed_door


def switch_choice(doors, player_choice, revealed_door):
    remaining_doors = set(doors) - {player_choice, revealed_door}
    new_choice = remaining_doors.pop()
    return new_choice


def play_game():
    prize_door, doors = setup_game()

    print("Добро пожаловать в игру 'Задача Монти Холла'!")

    player_first_choice = player_choice(doors)

    revealed_door = reveal_door(doors, player_first_choice, prize_door)

    print(f"Монти открыл дверь {revealed_door}, за которой нет приза.")

    switch = input("Хотите поменять свой выбор? (да/нет): ").strip().lower()

    if switch == 'да':
        player_final_choice = switch_choice(doors, player_first_choice, revealed_door)
        print(f"Вы поменяли свой выбор на дверь {player_final_choice}.")
    else:
        player_final_choice = player_first_choice
        print(f"Вы остались при своем выборе: дверь {player_final_choice}.")

    if player_final_choice == prize_door:
        print("Поздравляем! Вы выиграли приз!")
    else:
        print("К сожалению, вы не выиграли. Приз был за дверью", prize_door)


if __name__ == "__main__":
    while True:
        play_game()
        play_again = input("Хотите сыграть еще раз? (да/нет): ").strip().lower()
        if play_again != 'да':
            break
