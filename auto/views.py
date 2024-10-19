import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import os
from django.views.decorators.csrf import csrf_exempt
from selenium.common.exceptions import WebDriverException

logger = logging.getLogger(__name__)

def handle_error(message, exception):
    logger.error(f"{message}: {str(exception)}")
    return JsonResponse({"status": "error", "message": message})

def execute_webdriver(chromedriver_path):
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service)
        return driver
    except Exception as e:
        return handle_error("Erro ao iniciar o WebDriver.", e)

def perform_automation(driver):
    try:
        driver.get("http://127.0.0.1:8080/mainapp/get_bills/")  
        driver.maximize_window()

        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "seraclicado"))
        )

        if not buttons:
            return JsonResponse({"status": "error", "message": "Botões não encontrados."})

        for button in buttons:
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))

                if button.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    button.click()
                    logger.info(f"Clicou no botão: {button.text}")

                    time.sleep(2)

                    driver.execute_script("arguments[0].style.display = 'none';", button)

                    WebDriverWait(driver, 5).until(EC.invisibility_of_element(button))

                    if driver.find_elements(By.CLASS_NAME, "seraclicado"):
                        logger.warning(f"Botão ainda presente após o clique: {button.text}")
                else:
                    logger.warning(f"Botão não visível: {button.text}")
            except (TimeoutException, NoSuchElementException) as e:
                logger.error(f"Erro ao clicar no botão {button.text}: {str(e)}")
                continue  

    except Exception as e:
        return handle_error("Erro inesperado durante a automação.", e)
    finally:
        driver.quit()

    return JsonResponse({"status": "success", "message": "Automação concluída com sucesso."})


def start_automation(request):
    if request.method == "POST":
        chromedriver_path = os.path.join(os.path.dirname(__file__), os.pardir, 'chromedriver')


        driver = execute_webdriver(chromedriver_path)
        if isinstance(driver, JsonResponse):
            return driver  

        return perform_automation(driver)

    return JsonResponse({"status": "error", "message": "Método não permitido."})