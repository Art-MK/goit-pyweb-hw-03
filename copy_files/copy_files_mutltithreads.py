import shutil
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from pathlib import Path

# Декоратор для обробки помилок
def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
    return wrapper

# Головна функція, яка копіює файли з origin директорії до цільової
@error_handler
def copy_files(source_dir, target_dir='dist'):
    # Перетворюємо шляхи в об'єкти Path
    source_path = Path(source_dir)
    target_path = Path(target_dir)

    # Переверяємо наявнiсть origin директоріі
    if not source_path.exists():
        print("source_directory not exists")
        sys.exit(1)

    # Створюємо цільову директорію, якщо вона не існує
    if not target_path.exists():
        target_path.mkdir(parents=True)

    # Створюємо словник для зберігання списку файлів за розширеннями
    file_dict = defaultdict(list)

    # Використовуємо багатопотоковість для обробки файлів паралельно
    with ThreadPoolExecutor() as executor:
        # Паралельно обходимо всі піддиректорії та файли в origin директорії
        for file_path in source_path.rglob('*'):
            if file_path.is_file():
                # Визначаємо розширення файлу
                extension = file_path.suffix[1:]
                # Визначаємо цільову директорію для копіювання файлу
                target_subdir = target_path / extension
                # Додаємо файл до списку для копіювання
                file_dict[target_subdir].append(file_path)

    # Запускаємо копіювання файлів у цільові директорії паралельно
    with ThreadPoolExecutor() as executor:
        for target_subdir, files in file_dict.items():
            if files:
                executor.submit(copy_files_to_target, files, target_subdir)

# Функція для копіювання файлів у цільову директорію
@error_handler
def copy_files_to_target(files, target_dir):
    # Створюємо цільову директорію, якщо вона не існує
    if not target_dir.exists():
        target_dir.mkdir(parents=True)

    # Копіюємо файли у цільову директорію
    for file in files:
        shutil.copy(file, target_dir)

if __name__ == "__main__":
    import sys

    # Перевірка наявності аргументів командного рядка
    if not 2 <= len(sys.argv) <= 3:
        print("Usage: python script.py source_directory [target_directory]")
        sys.exit(1)

    # Отримання шляхів origin та цільової директорій
    source_dir = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else 'dist'

    # Виклик головної функції для копіювання файлів
    copy_files(source_dir, target_dir)
    print("Files copied successfully.")