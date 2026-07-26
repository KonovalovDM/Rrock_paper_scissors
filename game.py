#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Игра "Камень, ножницы, бумага"
"""

import random
import sys


def get_computer_choice():
    """
    Функция выбора хода компьютера
    Возвращает: 'камень', 'ножницы' или 'бумага'
    """
    choices = ['камень', 'ножницы', 'бумага']
    return random.choice(choices)


def get_user_choice():
    """
    Функция получения выбора пользователя
    Возвращает: 'камень', 'ножницы', 'бумага' или None (при выходе)
    """
    while True:
        user_input = input("\nВаш выбор (камень/ножницы/бумага/exit): ").lower().strip()
        
        if user_input in ['камень', 'ножницы', 'бумага']:
            return user_input
        elif user_input in ['exit', 'выход', 'q']:
            print("Игра завершена. Спасибо за игру!")
            return None
        else:
            print("Ошибка! Введите: камень, ножницы, бумага или exit")


def determine_winner(user_choice, computer_choice):
    """
    Функция определения победителя
    Возвращает: 'user', 'computer' или 'draw'
    """
    if user_choice == computer_choice:
        return 'draw'
    
    # Правила игры
    win_conditions = {
        'камень': 'ножницы',
        'ножницы': 'бумага',
        'бумага': 'камень'
    }
    
    if win_conditions[user_choice] == computer_choice:
        return 'user'
    else:
        return 'computer'


def display_result(user_choice, computer_choice, winner):
    """
    Вывод результата раунда
    """
    print(f"\nВы выбрали: {user_choice}")
    print(f"Компьютер выбрал: {computer_choice}")
    
    if winner == 'draw':
        print("Ничья! 😐")
    elif winner == 'user':
        print("Вы победили! 🎉")
    else:
        print("Компьютер победил! 🤖")


def play_game():
    """
    Основной игровой цикл
    """
    # Счёт
    user_score = 0
    computer_score = 0
    draws = 0
    round_number = 1
    
    print("=" * 50)
    print("Добро пожаловать в игру 'Камень, ножницы, бумага'!")
    print("=" * 50)
    print("Правила:")
    print("  • Камень побеждает ножницы")
    print("  • Ножницы побеждают бумагу")
    print("  • Бумага побеждает камень")
    print("  • Для выхода введите 'exit'")
    print("=" * 50)
    
    while True:
        print(f"\n--- РАУНД {round_number} ---")
        print(f"Счёт: Вы {user_score} : {computer_score} Компьютер (Ничьих: {draws})")
        
        # Получаем выбор пользователя
        user_choice = get_user_choice()
        if user_choice is None:  # Выход из игры
            break
        
        # Получаем выбор компьютера
        computer_choice = get_computer_choice()
        
        # Определяем победителя
        winner = determine_winner(user_choice, computer_choice)
        
        # Отображаем результат
        display_result(user_choice, computer_choice, winner)
        
        # Обновляем счёт
        if winner == 'user':
            user_score += 1
        elif winner == 'computer':
            computer_score += 1
        else:
            draws += 1
        
        round_number += 1
        
        # Спрашиваем, хочет ли игрок продолжить
        if round_number > 1:
            play_again = input("\nЕщё раунд? (y/n/enter - по умолчанию y): ").lower().strip()
            if play_again in ['n', 'no', 'нет']:
                break
    
    # Вывод итоговой статистики
    print("\n" + "=" * 50)
    print("ИГРА ЗАВЕРШЕНА")
    print("=" * 50)
    print(f"Всего сыграно раундов: {round_number - 1}")
    print(f"Ваши победы: {user_score}")
    print(f"Победы компьютера: {computer_score}")
    print(f"Ничьих: {draws}")
    
    if user_score > computer_score:
        print("\n🏆 Вы ПОБЕДИТЕЛЬ по итогам всех раундов! 🏆")
    elif computer_score > user_score:
        print("\n🤖 Компьютер ПОБЕДИЛ по итогам всех раундов! 🤖")
    else:
        print("\n😐 БОЕВАЯ НИЧЬЯ по итогам всех раундов! 😐")


def main():
    """Основная функция игры"""
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nИгра прервана. До свидания!")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()