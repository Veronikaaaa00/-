print("\033[1;32;40m Bright Green  \n")
import random

# Определение значений карт
# Словари
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5,
    '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': (1, 11)  # Кортеж
}

SUITS = ['♠', '♥', '♦', '♣']
DECK = [f"{value}{suit}" for value in CARD_VALUES.keys() for suit in SUITS]  # Списки


def create_deck():
    """Создание колоды карт."""
    deck = DECK.copy()
    random.shuffle(deck)
    return deck


def calculate_hand_value(hand):
    """Подсчет стоимости руки."""
    value = 0
    aces = 0
    for card in hand:
        if card[:-1] == 'A':
            aces += 1
            value += CARD_VALUES[card[:-1]][1]
        else:
            value += CARD_VALUES[card[:-1]]

    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value


def display_hand(hand, hide_first_card=False):
    """Отображение руки игрока."""
    if hide_first_card:
        print("?? ", end="")
        print(" ".join(hand[1:]))
    else:
        print(" ".join(hand))


def play_blackjack():
    """Основная логика игры в блэкджек."""
    deck = create_deck()

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    print("Ваша рука:")
    display_hand(player_hand)

    print("\nРука дилера:")
    display_hand(dealer_hand, hide_first_card=True)

    # Ход игрока
    while True:
        player_value = calculate_hand_value(player_hand)
        if player_value > 21:
            print(f"\nВы превысили 21! Ваш итог: {player_value}. Вы проиграли!")
            return

        action = input("\nХотите взять карту (H) или остановиться (S)? ").strip().upper()

        if action == 'H':
            player_hand.append(deck.pop())
            print("\nВаша рука:")
            display_hand(player_hand)
        elif action == 'S':
            break
        else:
            print("Неверный ввод. Пожалуйста, выберите H или S.")

    # Ход дилера
    print("\nРука дилера:")
    display_hand(dealer_hand)

    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        print("\nДилер берет карту.")
        display_hand(dealer_hand)

    dealer_value = calculate_hand_value(dealer_hand)

    # Определение победителя
    if dealer_value > 21:
        print(f"\nДилер превысил 21! Вы выиграли с итогом {player_value}.")
    elif player_value > dealer_value:
        print(f"\nВы выиграли с итогом {player_value} против {dealer_value}.")
    elif player_value < dealer_value:
        print(f"\nВы проиграли с итогом {player_value} против {dealer_value}.")
    else:
        print(f"\nНичья! Оба игрока имеют {player_value}.")


def main():
    """Главная функция для запуска игры."""
    print("Добро пожаловать в игру Блэкджек!")

    while True:
        play_blackjack()

        play_again = input("\nХотите сыграть еще раз? (да/нет): ").strip().lower()
        if play_again != 'да':
            break

    print("Спасибо за игру! До свидания!")


if __name__ == "__main__":
    main()