import pyautogui
import os
import logging

# Создаем папку для скриншотов элементов
SCREENSHOT_DIR = 'ui_elements'
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
logger = logging.getLogger("Owen-capture")


def capture_ui_elements():
    """Функция для создания скриншотов элементов UI"""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    print("=== Режим создания шаблонов ===")
    input("1. Подведите курсор к иконке 'Константа' на палитре и нажмите Enter...")
    const_pos = pyautogui.position()
    pyautogui.screenshot(f'{SCREENSHOT_DIR}/constant_icon.png',
                         region=(const_pos.x - 20, const_pos.y - 20, 40, 40))

    input("2. Подведите курсор к выходу Q1 на схеме и нажмите Enter...")
    q1_pos = pyautogui.position()
    pyautogui.screenshot(f'{SCREENSHOT_DIR}/q1_output.png',
                         region=(q1_pos.x - 20, q1_pos.y - 20, 40, 40))

    input("3. Подведите курсор к выходу Q2 на схеме и нажмите Enter...")
    q2_pos = pyautogui.position()
    pyautogui.screenshot(f'{SCREENSHOT_DIR}/q2_output.png',
                         region=(q2_pos.x - 20, q2_pos.y - 20, 40, 40))


    input("5. Подведите курсор к кнопке 'Старт' и нажмите Enter...")
    start_pos = pyautogui.position()
    pyautogui.screenshot(f'{SCREENSHOT_DIR}/start_button.png',
                         region=(start_pos.x - 25, start_pos.y - 25, 50, 50))

    print(f"Шаблоны сохранены в папке {SCREENSHOT_DIR}")

if __name__ == "__main__":
    # Инициализация
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    logger.info("Запуск тестового Owen Logic...")
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    capture_ui_elements()
    logger.info("Я все сделяль")