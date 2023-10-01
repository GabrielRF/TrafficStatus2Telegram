import datetime
import json
import os
import random
import requests
import sys
import telebot
import urllib.parse
from telebot import types

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
MESSAGE_DESTINATION = os.environ.get('MESSAGE_DESTINATION')
ORIGEM = os.environ.get('ORIGEM')
DESTINO = os.environ.get('DESTINO')
TITULO = os.environ.get('TITULO', f'{ORIGEM} → {DESTINO}')

def distancematrix(origem, destino):
    response = requests.get(
        f'https://maps.googleapis.com/maps/api/distancematrix/json?' +
        f'destinations={urllib.parse.quote(destino)}&' +
        f'origins={urllib.parse.quote(origem)}&' +
        f'key={GOOGLE_API_KEY}&' +
        f'units=metric&language=pt-BR&mode=driving&' +
        f'departure_time=now',
        headers = {'User-agent': 'Mozilla/5.1'}
    )
    return response.json()

def averagespeed(response):
    distancia_m = response['rows'][0]['elements'][0]['distance']['value']
    tempo_s = response['rows'][0]['elements'][0]['duration_in_traffic']['value']
    distancia_km = distancia_m/1000
    tempo_h = tempo_s * 0.000277778
    return round(distancia_km/tempo_h, 2)

def get_emoji(tipo, valor=None):
    if tipo == 'carro':
        carros = [
            '🚗', '🚕', '🚙', '🚌',
            '🚐', '🛻', '🚚', '🚛'
        ]
        return random.choice(carros)
    elif tipo == 'relogio':
        valor = int(valor/60)
        while valor > 60: valor = valor - 60
        relogios = {
            range(0, 5): '🕐',
            range(5, 10): '🕑',
            range(10, 15): '🕒',
            range(15, 20): '🕓',
            range(20, 25): '🕔',
            range(25, 30): '🕕',
            range(30, 35): '🕖',
            range(35, 40): '🕗',
            range(40, 45): '🕘',
            range(45, 50): '🕙',
            range(50, 55): '🕚',
            range(55, 60): '🕛',
        }
        relogios = {num: valor for rng, valor in relogios.items() for num in rng}
        return relogios.get(valor)
    elif tipo == 'velocidade':
        if valor < 1.25:
            return '🟩'
        elif 1.25 <= valor < 1.5:
            return '🟨'
        elif 1.5 <= valor < 1.75:
            return '🟧'
        elif valor >= 1.75:
            return '🟥'

def format_info(origem, destino, distancia, tempo, tempo_s, tempo_s_padrao, velocidade_media):
    line = (
        f'{get_emoji("carro")} <b>{TITULO.replace("->", "→")}</b>\n\n' +
        f'🛣 <i>Distância</i>: {distancia}\n' +
        f'{get_emoji("relogio", int(tempo_s))} <i>Tempo</i>: {tempo}\n' +
        f'{get_emoji("velocidade", float(tempo_s/tempo_s_padrao))} <i>Velocidade Média</i>: {velocidade_media} km/h\n\n'
    )
    return line

def get_data(origem, destino):
    resposta = distancematrix(origem, destino)
    link = generate_link(origem, destino)
    velocidade_media = averagespeed(resposta)
    line = format_info(
        origem,
        destino,
        resposta['rows'][0]['elements'][0]['distance']['text'],
        resposta['rows'][0]['elements'][0]['duration_in_traffic']['text'],
        resposta['rows'][0]['elements'][0]['duration_in_traffic']['value'],
        resposta['rows'][0]['elements'][0]['duration']['value'],
        velocidade_media
    )
    return send_message(line, link)

def generate_link(origem, destino):
    link = (
        f'https://www.google.com/maps/dir/?api=1&' +
        f'origin={urllib.parse.quote(origem)}&' +
        f'destination={urllib.parse.quote(destino)}'
    )
    return link

def send_message(message, link):
    bot = telebot.TeleBot(BOT_TOKEN)
    btn_link = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(f'🗺 Ver no Mapa', url=link)
    btn_link.row(btn)
    return bot.send_message(MESSAGE_DESTINATION,
        message,
        parse_mode='HTML',
        disable_web_page_preview=True,
        reply_markup=btn_link,
        disable_notification=True
    )

if __name__ == "__main__":
    print(TITULO)
    get_data(ORIGEM, DESTINO)
