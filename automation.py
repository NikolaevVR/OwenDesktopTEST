import time
import pyautogui
import subprocess
import os
import logging
from pywinauto import Application


SCREENSHOT_DIR = "results"
UI_DIR = "ui_elements"
logger = logging.getLogger("Owen-testing")
file_handler = logging.FileHandler('logs.txt', mode='a', encoding='utf-8')
logger.addHandler(file_handler)
logger.setLevel('INFO')
CONFIDENCE = 0.8  # Точность распознавания
TIMEOUT = 15  # Макс. время поиска элемента
controller = "ПР200-24.2(4).Х"


def find_element(image_path, timeout=TIMEOUT, confidence=CONFIDENCE):
    """Поиск элемента на экране по изображению"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            position = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if position:
                return position
        except:
            pass
        time.sleep(0.5)
    raise Exception(f"Элемент {image_path} не найден за {timeout} секунд")


def drag_and_drop(start_x, start_y, end_x, end_y, duration=0.5):
    """Функция для перетаскивания элементов"""
    pyautogui.moveTo(start_x, start_y)
    pyautogui.click()
    time.sleep(0.2)
    pyautogui.moveTo(end_x, end_y, duration=duration)
    pyautogui.click()
    time.sleep(0.5)


def main():
    try:
        logger.info("Запуск Owen Logic...")
        #subprocess.Popen([r"C:\Program Files\Owen\Owen Logic\ProgramRelayFBD.exe"], shell=True)
        app = Application(backend="uia").start(r"C:\Program Files\Owen\Owen Logic\ProgramRelayFBD.exe")
        time.sleep(5)
    except Exception as e:
        logger.info(f"Ошибка запуска: {e}")
        return

    # 2. Создание нового проекта
    try:
        logger.info("Создание проекта...")
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(2)
        search = find_element(f'{UI_DIR}/search_input.png')
        pyautogui.click(search.x, search.y)
        pyautogui.write(controller)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.screenshot(f'{SCREENSHOT_DIR}/new_proj.png')
        logger.info(f"Создал проект {controller}")
    except Exception as e:
        logger.info(f"Ошибка создания проекта: {e}")

    # 3. Добавление двух констант
    try:
        logger.info("Добавление констант...")
        # Поиск иконки константы на палитре
        const_icon_pos = find_element(f'{UI_DIR}/constant_icon.png')

        # Перетаскивание первой константы

        drag_and_drop(
            const_icon_pos.x, const_icon_pos.y,
            const_icon_pos.x + 300, const_icon_pos.y + 100
        )

        # Перетаскивание второй константы
        drag_and_drop(
            const_icon_pos.x, const_icon_pos.y,
            const_icon_pos.x + 300, const_icon_pos.y + 200
        )

        pyautogui.screenshot(f'{SCREENSHOT_DIR}/new_constants.png')
    except Exception as e:
        logger.info(f"Ошибка добавления констант: {e}")

    # 4. Установка значения константы
    try:
        logger.info("Установка значения константы...")
        # Координаты первой константы (рассчитаны относительно иконки)
        const1_x = const_icon_pos.x + 300
        const1_y = const_icon_pos.y + 100

        pyautogui.doubleClick(const1_x, const1_y)
        time.sleep(1)
        pyautogui.write('1')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.screenshot(f'{SCREENSHOT_DIR}/new_const_value.png')
        dlg_spec = app.window()
        controll = app.dlg.control
        logger.info(f"Спецификация:")
        try:
            for a in dlg_spec:
                logger.info(a.wrapper_object())
        except Exception as e:
            logger.info(f"Ошибка выдачи спецификации: {e}\n{dlg_spec}\n{controll}")
    except Exception as e:
        logger.info(f"Ошибка установки значения: {e}")

    # 5. Соединение с выходами Q1 и Q2
    try:
        logger.info("Соединение элементов...")
        # Поиск выходов на схеме
        q1_pos = find_element(f'{UI_DIR}/q1_output.png')
        q2_pos = find_element(f'{UI_DIR}/q2_output.png')


        # Соединение первой константы с Q1
        drag_and_drop(
            const1_x+30, const1_y,  # Правее центра константы
            q1_pos.x - 20, q1_pos.y  # Левее центра Q1
        )

        # Соединение второй константы с Q2
        drag_and_drop(
            const1_x + 30, const1_y + 100,
            q2_pos.x - 20, q2_pos.y
        )
        pyautogui.screenshot(f'{SCREENSHOT_DIR}/new_elem_connection.png')
    except Exception as e:
        logger.info(f"Ошибка соединения элементов: {e}")

    # 6. Запуск симуляции
    try:
        logger.info("Запуск...")
        start_btn = find_element(f'{UI_DIR}/start_button.png')
        pyautogui.click(start_btn)
        pyautogui.hotkey('F6')
        time.sleep(3)

        # Скриншот результата
        pyautogui.screenshot(f'{SCREENSHOT_DIR}/simulation_result.png')
        logger.info("Скриншот сохранен как simulation_result.png")
    except Exception as e:
        logger.info(f"Ошибка запуска: {e}")


if __name__ == "__main__":
    # Инициализация
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    logger.info("Запуск тестового Owen Logic...")
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    main()
    logger.info("Я все сделяль")