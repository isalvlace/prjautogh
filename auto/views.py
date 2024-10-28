import os
import logging
import time
from django.http import JsonResponse
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def handle_error(message, exception):
    print(f"{message} - {exception}")
    return JsonResponse({"status": "error", "message": message})

def execute_webdriver(chromedriver_path):
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service)
        return driver
    except WebDriverException as e:
        return handle_error("Erro ao iniciar o WebDriver.", e)

def wait_for_buttons(driver):
    try:
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'seraclicado'))
        )
        return buttons
    except Exception as e:
        print(f"Erro ao esperar pelos botões: {e}")
        return None

def click_button(driver, button):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
        button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Erro inesperado ao clicar no botão: {e}")
        return False
    return True

def perform_automation(driver):
    try:
        driver.get("http://127.0.0.1:8080/mainapp/get_bills/")
        driver.maximize_window()

        buttons = wait_for_buttons(driver)
        if not buttons:
            return JsonResponse({"status": "error", "message": "Botões não encontrados."})

        time.sleep(2)  

        for button in buttons:
            success = click_button(driver, button)
            if not success:
                print("Tentativa de clicar no botão falhou.")
                return JsonResponse({"status": "error", "message": "Erro ao clicar no botão."})

    except Exception as e:
        return handle_error("Erro inesperado durante a automação.", e)

    finally:
        if driver:
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

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_whatsapp_message(account_sid, auth_token, from_whatsapp_number, to_whatsapp_number, message_body, media_url):
    client = Client(account_sid, auth_token)
    
    try:
        message = client.messages.create(
            from_=f'whatsapp:{from_whatsapp_number}',
            body=message_body,
            to=f'whatsapp:{to_whatsapp_number}',
            media_url=[media_url]  
        )
        return message.sid
    except TwilioRestException as e:
        print(f'Erro ao enviar mensagem: {e}')
        print(f'Código de erro: {e.code}')
        print(f'Mensagem de erro: {e.msg}')
        print(f'Detalhes: {e.extra}')

if __name__ == "__main__":
    account_sid = '' # seu account_sid
    auth_token = '' # seu token
    from_whatsapp_number = '+14155238886'
    to_whatsapp_number = '+556281055985'
    message_body = 'Boleto'  
    media_url = 'https://drive.google.com/uc?export=download&id=1CsDvjUk3TThj8tynyue3F4Agv7-yLhAg' # URL do PDF

    message_sid = send_whatsapp_message(account_sid, auth_token, from_whatsapp_number, to_whatsapp_number, message_body, media_url)
    if message_sid:
        print(f'Mensagem enviada com SID: {message_sid}')

