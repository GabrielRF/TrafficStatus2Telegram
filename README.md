# Traffic Status to Telegram

Envio automático do tempo de viagem de carro entre dois pontos usando Google Maps.

## Sugestões

**Envie novas rotas**! Faça um *Pull Request* considerando as instruções em [GitHub Action](#github-action) e novas mensagens serão enviadas no canal [@BsbDF](https://t.me/BsbDF).

## trafficstatus.py

### Variáveis de ambiente

* `BOT_TOKEN`: Token do bot que faz o envio;
* `GOOGLE_API_KEY`: Chave de acesso à *Distance Matrix API* do Google [(Mais informações)](https://developers.google.com/maps/documentation/distance-matrix/overview?hl=pt-br);
* `MESSAGE_DESTINATION`: Destino da mensagem;
* `ORIGEM`: Ponto de início da viagem;
* `DESTINO`: Ponto de término da viagem;
* `TITULO`: Título da mensagem.

### Indicativo do tempo de viagem

A API do Google retorna dois indicativos de tempo, o de viagem baseado na velocidade das vias e o de viagem baseado no trânsito atual. É feita a divisão do dos dois valores de tempo, obtendo-se o estado atual das vias.

* 🟩 Para viagens em que o tempo é de até 25% acima do tempo sem trânsito;
* 🟨 Caso seja entre 25% e 50%;
* 🟧 Entre 50% e 75%;
* 🟥 Acima de 75%.

## GitHub Action

> Localizadas em *.github/workflows*

Adicione um novo arquivo usando qualquer outro da mesma pasta como modelo e ajuste as variáveis abaixo:

* `name` (linha 1): Nome da ação. Este valor será o título da mensagem;
* `cron` (linha ~5): Ajuste do cronjob ([guia](https://crontab.guru/)). Horário em UTC;
* `ORIGEM` (linha ~27): Origem da viagem. Este valor deve funcionar perfeitamente na busca do Google Maps;
* `DESTINO` (linha ~28): Destino da viagem. Este valor também deve funcionar na busca.
