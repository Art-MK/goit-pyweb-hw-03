import time
from multiprocessing import Pool, cpu_count, freeze_support

def factorial(number):
    """
    Функція, що знаходить всі множники (фактори) числа.
    """
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize(*args)-> dict:
    """
    Функція, яка факторизує список чисел, використовуючи паралельні процеси.

    Args:
        *args: Змінна кількість аргументів - числа для факторизації.

    Returns:
        dict: Словник, де ключами є вихідні числа, а значеннями - їх фактори.
    """
    numbers = args  # Упаковуємо args у кортеж
    num_cores = cpu_count()
    start_time = time.time()
    with Pool(num_cores) as p:
        results = p.map(factorial, numbers)
    end_time = time.time()

    # Створюємо словник, де ключами є вихідні числа, а значеннями - їх фактори
    result_dict = {number: factors for number, factors in zip(numbers, results)}

    print("Час виконання:", end_time - start_time, "секунд")
    return result_dict

if __name__ == '__main__':
    freeze_support()  # пiдтримка платформи Windows
    print(factorize(128, 255, 99999, 10651060))  # Передаємо числа як аргументи
