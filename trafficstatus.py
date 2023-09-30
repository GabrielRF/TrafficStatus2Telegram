import json
import os
import random
import requests
import sys
import telebot
import urllib.parse

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
MESSAGE_DESTINATION = os.environ.get('MESSAGE_DESTINATION')
ORIGEM = os.environ.get('ORIGEM')
DESTINO = os.environ.get('DESTINO')

def mappoint(local):
    locais = {
        'Rodoviária': 'Rodoviária Plano Piloto, Setor de Diversões Norte - Brasília, DF',
        'Balão do Aeroporto': 'Balão do Aeroporto Internacional de Brasília - Candangolândia, Brasília - DF, 70297-400',
        'Ponte do Bragueto (Lago Norte)': 'Ponte do Bragueto, Lago Paranoá, Brasília - DF',
        'Praça dos Três Poderes': 'Praça dos Três Poderes - Brasília, DF',
        'Ponte JK': 'Ponte Juscelino Kubitschek, Brasília - DF',
        'Balão dos Condomínios': '-15.849110782931751, -47.81518943634656',
        'Águas Claras': 'Águas Claras, Brasília - DF',
        'Taguatinga': 'Taguatinga, Brasília - DF',
        'Gama': 'Gama, Brasília - DF',
        'Planaltina': 'Planaltina, Brasília - DF',
        'Ceilândia': 'Ceilândia, Brasília - DF',
        'Clube do Congresso': 'Clube do Congresso, SHIN QI, 16, Área Especial - Lago Norte - LAGO NORTE, Brasília - DF, 71530-200',
        'Octogonal': 'Octogonal - Brasília, DF',
    }
    return locais.get(local)

def distancematrix(origem, destino):
    response = requests.get(
        f'https://maps.googleapis.com/maps/api/distancematrix/json?' +
        f'destinations={urllib.parse.quote(mappoint(destino))}&' +
        f'origins={urllib.parse.quote(mappoint(origem))}&'+
        f'key={GOOGLE_API_KEY}&' +
        f'units=metric',
        headers = {'User-agent': 'Mozilla/5.1'}
    )
    return response.json()

def averagespeed(response):
    distancia_m = response['rows'][0]['elements'][0]['distance']['value']
    tempo_s = response['rows'][0]['elements'][0]['duration']['value']
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
        relogios = [
            '🕐','🕑','🕒','🕓','🕔','🕕','🕖','🕗',
            '🕘','🕙','🕚','🕛','🕜','🕝','🕞','🕟',
            '🕠','🕡','🕢','🕣','🕤','🕥','🕦','🕧'
        ]
        return random.choice(relogios)
    elif tipo == 'velocidade':
        if valor > 50:
            return '🏎'
        elif 50 >= valor > 40:
            return '🟩'
        elif 40 >= valor > 30:
            return '🟨'
        elif 30 >= valor:
            return '🟥'

def format_info(origem, destino, distancia, tempo, velocidade_media, link):
    line = (
        f'<b>{origem}</b> → <b>{destino}</b>\n\n' +
        f'{get_emoji("carro")} <i>Distância</i>: {distancia}\n' +
        f'{get_emoji("relogio")} <i>Tempo</i>: {tempo}\n' +
        f'{get_emoji("velocidade", int(velocidade_media))} <i>Velocidade Média</i>: {velocidade_media} km/h\n\n' +
        f'🗺 <a href="{link}">Ver no mapa</a>'
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
        resposta['rows'][0]['elements'][0]['duration']['text'],
        velocidade_media,
        link
    )
    return send_message(line)

def generate_link(origem, destino):
    link = (
        f'https://www.google.com/maps/dir/?api=1&' +
        f'origin={urllib.parse.quote(mappoint(origem))}&' +
        f'destination={urllib.parse.quote(mappoint(destino))}'
    )
    return link

def send_message(message):
    bot = telebot.TeleBot(BOT_TOKEN)
    return bot.send_message(MESSAGE_DESTINATION,
        message,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

if __name__ == "__main__":
    get_data(ORIGEM, DESTINO)
