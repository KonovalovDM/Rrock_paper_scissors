#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Игра "Камень, ножницы, бумага"
"""

import random
import sys
import json
import os
from datetime import datetime


class ScoreBoard:
    """Класс для управления счётом и сохранения результатов"""
    
    def __init__(self, filename="scores.json"):
        """
        Инициализация доски счёта
        :param filename: имя файла для сохранения результатов
        """
        self.filename = filename
        self.user_score = 0
        self.computer_score = 0
        self.draws = 0
        self.rounds_played = 0
        self.history = []
        self.load_results()
    
    def update(self, winner):
        """
        Обновление счёта после раунда
        :param winner: 'user', 'computer' или 'draw'
        """
        self.rounds_played += 1
        
        if winner == 'user':
            self.user_score += 1
        elif winner == 'computer':
            self.computer_score += 1
        else:
            self.draws += 1
        
        # Добавляем запись в историю
        self.history.append({
            'round': self.rounds_played,
            'winner': winner,
            'timestamp': datetime.now().isoformat()
        })
    
    def display(self):
        """
        Отображение текущего счёта
        """
        print("\n" + "=" * 40)
        print("📊 ТЕКУЩИЙ СЧЁТ")
        print("=" * 40)
        print(f"👤 Вы: {self.user_score}")
        print(f"🤖 Компьютер: {self.computer_score}")
        print(f"🤝 Ничьи: {self.draws}")
        print(f"🔄 Всего раундов: {self.rounds_played}")
        print("=" * 40)
    
    def save_results(self):
        """
        Сохранение результатов в файл
        """
        try:
            data = {
                'user_score': self.user_score,
                'computer_score': self.computer_score,
                'draws': self.draws,
                'rounds_played': self.rounds_played,
                'history': self.history,
                'last_updated': datetime.now().isoformat()
            }
            
            # Загружаем существующие результаты, если файл есть
            existing_data = self._load_from_file()
            if existing_data:
                data['previous_games'] = existing_data
            else:
                data['previous_games'] = []
            
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Результаты сохранены в файл: {self.filename}")
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            return False
    
    def load_results(self):
        """
        Загрузка результатов из файла
        """
        data = self._load_from_file()
        if data:
            self.user_score = data.get('user_score', 0)
            self.computer_score = data.get('computer_score', 0)
            self.draws = data.get('draws', 0)
            self.rounds_played = data.get('rounds_played', 0)
            self.history = data.get('history', [])
            print(f"📂 Загружены результаты из {self.filename}")
            return True
        return False
    
    def _load_from_file(self):
        """
        Внутренний метод загрузки из файла
        """
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Ошибка загрузки: {e}")
        return None
    
    def show_history(self, limit=5):
        """
        Показать последние игры
        """
        if not self.history:
            print("📭 История игр пуста")
            return
        
        print("\n" + "=" * 40)
        print("📜 ПОСЛЕДНИЕ РАУНДЫ")
        print("=" * 40)
        
        # Показываем последние N записей
        for record in self.history[-limit:]:
            winner_emoji = {
                'user': '👤',
                'computer': '🤖',
                'draw': '🤝'
            }
            winner_name = {
                'user': 'Вы',
                'computer': 'Компьютер',
                'draw': 'Ничья'
            }
            print(f"Раунд {record['round']}: {winner_emoji[record['winner']]} {winner_name[record['winner']]}")


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
    # Создаём доску счёта
    scoreboard = ScoreBoard()
    
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
        # Показываем счёт
        scoreboard.display()
        
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
        scoreboard.update(winner)
        
        # Спрашиваем, хочет ли игрок продолжить
        play_again = input("\nЕщё раунд? (y/n/enter - по умолчанию y): ").lower().strip()
        if play_again in ['n', 'no', 'нет']:
            break
    
    # Сохраняем результаты
    scoreboard.save_results()
    
    # Показываем итоговую статистику
    print("\n" + "=" * 50)
    print("ИГРА ЗАВЕРШЕНА")
    print("=" * 50)
    
    scoreboard.display()
    scoreboard.show_history(5)
    
    if scoreboard.user_score > scoreboard.computer_score:
        print("\n🏆 Вы ПОБЕДИТЕЛЬ по итогам всех раундов! 🏆")
    elif scoreboard.computer_score > scoreboard.user_score:
        print("\n🤖 Компьютер ПОБЕДИЛ по итогам всех раундов! 🤖")
    else:
        print("\n😐 БОЕВАЯ НИЧЬЯ по итогам всех раундов! 😐")


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