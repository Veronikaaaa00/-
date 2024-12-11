import json

# Данные о пользователях и блюдах
users = []
dishes = []


def load_data():
    global users, dishes
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []
    except json.JSONDecodeError:
        users = []  # Если файл пуст или невалидный

    try:
        with open("dishes.json", "r") as f:
            dishes = json.load(f)
    except FileNotFoundError:
        dishes = []
    except json.JSONDecodeError:
        dishes = []  # Если файл пуст или невалидный


def save_data():
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)
    with open("dishes.json", "w") as f:
        json.dump(dishes, f, indent=4)


def find_user(username):
    return next((user for user in users if user['username'] == username), None)


def sign_in():
    username = input("Логин: ")
    password = input("Пароль: ")
    user = find_user(username)

    if user and user['password'] == password:
        print(f"Добро пожаловать, {username}!")
        return user
    else:
        print("Неверный логин или пароль.")
        return None


def user_menu(user):
    while True:
        print("\n--- Меню пользователя ---")
        print("1. Просмотреть доступные блюда")
        print("2. Заказать блюдо")
        print("3. Просмотреть историю заказов")
        print("4. Фильтровать и сортировать блюда")
        print("5. Обновить профиль")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            view_dishes()
        elif choice == "2":
            order_dish(user)
        elif choice == "3":
            view_order_history(user)
        elif choice == "4":
            sort_and_filter_dishes()
        elif choice == "5":
            update_profile(user)
        elif choice == "6":
            print("Выход из системы...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


def admin_menu():
    while True:
        print("\n--- Меню администратора ---")
        print("1. Добавить блюдо")
        print("2. Удалить блюдо")
        print("3. Редактировать блюдо")
        print("4. Управление братишками")
        print("5. Просмотреть статистику")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            add_dish()
        elif choice == "2":
            remove_dish()
        elif choice == "3":
            edit_dish()
        elif choice == "4":
            manage_users()
        elif choice == "5":
            view_statistics()
        elif choice == "6":
            print("Выход из системы...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


def manage_users():
    """Управление пользователями для администратора."""
    while True:
        print("\n--- Управление пользователями ---")
        print("1. Создать мини-бро")
        print("2. Удалить мини-бро")
        print("3. Показать всех братишек")
        print("4. Вернуться в главное меню")

        choice = input("Введите номер действия: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            delete_user()
        elif choice == "3":
            show_all_users()
        elif choice == "4":
            break  # Возврат в меню администратора
        else:
            print("Неверный выбор, попробуйте снова.")


def view_dishes():
    if not dishes:
        print("Нет доступных блюд.")
        return

    print("\nСписок доступных блюд:")
    print(f"{'Название':<50} {'Цена (₽)':<15} {'Рейтинг':<10}")  # Заголовки столбцов
    for dish in dishes:
        print(f"{dish['name']:<50} {dish['price']:>10,.2f} {dish['rating']:>10,.1f}")


def order_dish(user):
    view_dishes()

    cart = {}
    total_price = 0.0

    while True:
        name = input("Введите название блюда для заказа (или 'стоп' для завершения): ")

        if name.lower() == 'стоп':
            break

        dish = next((d for d in dishes if d['name'].lower() == name.lower()), None)

        if dish:
            try:
                quantity = int(input(f"Введите количество блюда '{dish['name']}': "))
                if quantity <= 0:
                    print("Количество должно быть положительным.")
                    continue
            except ValueError:
                print("Введите корректное число.")
                continue

            cart[dish['name']] = {
                'price': dish['price'],
                'quantity': quantity
            }
        else:
            print("Блюдо не найдено.")

    if cart:
        print("\n--- Чек ---")
        print(f"{'Название':<36} {'Количество':<17} {'Цена (₽)':<13} {'Сумма (₽)':<6}")
        for item, details in cart.items():
            item_total = details['price'] * details['quantity']
            total_price += item_total
            print(f"{item:<40} {details['quantity']:<10} {details['price']:>5,.2f} {item_total:>16,.2f}")

        print(f"\nИтоговая сумма: {total_price:,.2f}₽")
        user.setdefault('history', []).append(cart)  # Сохраним детали заказа в истории
        save_data()
        print("Заказ завершен!")
    else:
        print("Вы ничего не заказали.")


def view_order_history(user):
    print("\nВаша история заказов:")
    history = user.get('history', [])

    if history:
        for index, order in enumerate(history):
            print(f"\nЗаказ #{index + 1}:")
            for item, details in order.items():
                if isinstance(details, dict):
                    print(f"Блюдо: {item}, Количество: {details['quantity']}, Цена: {details['price']:.2f}")
            print("-----------")  # Разделитель для разных заказов
    else:
        print("У вас нет истории заказов.")


def sort_and_filter_dishes():
    if not dishes:
        print("Нет доступных блюд для сортировки или фильтрации.")
        return

    print("\nФильтрация блюд по критериям.")
    criteria = [
        {"key": "price", "label": "Цена"},
        {"key": "rating", "label": "Рейтинг"},
    ]

    print("Сортировка по:")
    for i, c in enumerate(criteria, start=1):
        print(f"{i}. {c['label']}")

    choice = input("Введите номер критерия для сортировки: ")
    reverse = input("Убывающая (y/n)? ").lower() == 'y'

    try:
        key = criteria[int(choice) - 1]["key"]
        sorted_dishes = sorted(dishes, key=lambda x: x[key], reverse=reverse)
        print(f"\nБлюда, отсортированные по {criteria[int(choice) - 1]['label']}:")
        for dish in sorted_dishes:
            print(f"{dish['name']: <50} {dish['price']:>10,.2f} {dish['rating']:>10,.1f}")  # Форматированный вывод
    except (IndexError, ValueError):
        print("Неверный ввод.")


def add_dish():
    name = input("Введите название блюда: ")
    try:
        price = float(input("Введите цену блюда: "))
        rating = float(input("Введите рейтинг блюда (0-10): "))
    except ValueError:
        print("Цена и рейтинг должны быть числами.")
        return

    dish = {
        'name': name,
        'price': price,
        'rating': rating
    }
    dishes.append(dish)
    save_data()
    print("Блюдо добавлено.")


def remove_dish():
    name = input("Введите название блюда для удаления: ")
    global dishes
    dishes = [dish for dish in dishes if dish['name'] != name]
    save_data()
    print(f"Блюдо '{name}' удалено.")


def edit_dish():
    name = input("Введите название блюда для редактирования: ")
    dish = next((d for d in dishes if d['name'] == name), None)

    if dish:
        try:
            new_price = float(
                input("Введите новую цену блюда (или оставьте пустым, чтобы не менять): ") or dish['price'])
            new_rating = float(
                input("Введите новый рейтинг блюда (или оставьте пустым, чтобы не менять): ") or dish['rating'])
            dish['price'] = new_price
            dish['rating'] = new_rating
            save_data()
            print("Блюдо успешно отредактировано.")
        except ValueError:
            print("Цена и рейтинг должны быть числами.")
    else:
        print("Блюдо не найдено.")


def update_profile(user):
    new_password = input("Введите новый пароль: ")
    user['password'] = new_password
    save_data()
    print("Профиль обновлен.")


def create_user():
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    if find_user(username):
        print("Пользователь с таким именем уже существует.")
        return

    user = {
        'username': username,
        'password': password,
        'role': 'user',
        'history': []
    }
    users.append(user)
    save_data()
    print("Пользователь создан.")


def delete_user():
    username = input("Введите имя пользователя для удаления: ")
    user = find_user(username)
    if user:
        users.remove(user)
        save_data()
        print("Пользователь удалён.")
    else:
        print("Пользователь не найден.")


def show_all_users():
    """Показать всех пользователей."""
    if not users:
        print("Нет зарегистрированных пользователей.")
        return
    print(f"\n{'Имя пользователя':<20} {'Роль':<10}")
    for user in users:
        print(f"{user['username']:<20} {user.get('role', 'user'):<10}")


def view_statistics():
    total_dishes = len(dishes)
    total_users = len(users)
    print(f"Всего блюд: {total_dishes}")
    print(f"Всего пользователей: {total_users}")


def main():
    load_data()

    while True:
        print("\nДорогой пользователь, добро пожаловать в ресторан ХОЧУ 5!")
        print("1. Войти как пользователь")
        print("2. Войти как администратор")
        print("3. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            user = sign_in()
            if user:
                user_menu(user)
        elif choice == "2":
            username = input("Логин администратора: ")
            password = input("Пароль администратора: ")
            if username == 'Админ' and password == '228':
                admin_menu()
            else:
                print("Неверный логин или пароль администратора.")
        elif choice == "3":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()