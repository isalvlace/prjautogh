import email
from django.shortcuts import render
from mainapp.models import XYZKCLIENT, XYZKNFSAID, XYZKPREST
from django.http import HttpResponse
from django.db import transaction, IntegrityError
from django.core.mail import send_mail
from django.http import JsonResponse
import smtplib
from django.db.models import Prefetch
from auto.views import start_automation
from django.core.cache import cache
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

def home(request):
    return render(request, 'mainapp/home.html')

def populate_data(request):
    try:
        with transaction.atomic():
            # Criar um cliente
            xyzkclient_obj = XYZKCLIENT.objects.create(
                XYZKCLIENTE='Cliente Teste',
                XYZKTELCOB='(11) 1234-5678',
                XYZKTELENT='(11) 9876-5432',
                XYZKEMAIL='cliente@teste.com',
                XYZKCODBARRA='1234567890'
            )

            # Criar uma venda (XYZKNFSAID) relacionada ao cliente criado
            xyzknfsaid_obj = XYZKNFSAID.objects.create(
                XYZKCODCLI=xyzkclient_obj,
                XYZKDTFECHA='2024-06-23',
                XYZKESPECIE='Nota Fiscal',
                XYZKNUMNOTA='123',
                XYZKVLTOTAL=1000.00,
                XYZKDTENTREGA='2024-06-25',
                XYZKNUMPED=456,
                XYZKCLIENTE='Cliente Teste',
                XYZKDTFAT='2024-06-30'
            )

            # Criar uma transação (XYZKPREST) relacionada ao cliente criado
            xyzkprest_obj = XYZKPREST.objects.create(
                XYZKCODCLI=xyzkclient_obj,
                XYZKDUPLIC=789,
                XYZKVALOR=500.00,
                XYZKDTVENC='2024-07-10',
                XYZKDTPAG=None,
                XYZKDTFECHA='2024-06-23',
                XYZKCODBARRA='1234567890',
                XYZKNUMPED=789
            )

        return HttpResponse("Dados populados com sucesso!")
    
    except IntegrityError as e:
        return HttpResponse(f"Erro de integridade ao inserir dados: {str(e)}")

def send_email_message(request):

    try:
        '''corpo_email = """
            <p>Parágrafo1</p>
            <p>Parágrafo2</p>
        """

        msg = email.message.Message()
        msg['Subject'] = "Assunto"
        msg['From'] = ''
        msg['To'] = ''
        password = '' 
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()

        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')'''

        return HttpResponse("<h1>Deu certo!</h1>")

    except Exception as e:
        return HttpResponse(f'Ocorreu um erro inesperado ao enviar o email: {str(e)}')
 
def get_bills(request):
    cache.clear()
    
    clients_with_bills = XYZKCLIENT.objects.prefetch_related(
        Prefetch('xyzknfsaid_set', queryset=XYZKNFSAID.objects.all()),
        Prefetch('xyzkprest_set', queryset=XYZKPREST.objects.all())
    )
  
    context = {
        'clients_with_bills': clients_with_bills
    }

    return render(request, 'mainapp/bills.html', context)