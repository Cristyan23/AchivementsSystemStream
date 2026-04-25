# Stream Achievement Counter

Sistema de contagem de conquistas para streaming integrado com Steam.

## Requisitos

- Python 3.10+
- Steam instalado

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Edite `config/config.json`:

```json
{
  "steam_id": "YOUR_STEAM_ID_64",
  "http_port": 5000,
  "ws_port": 8765,
  "poll_interval": 5,
  "webhook_url": "http://localhost:8080/webhook",
  "theme": {
    "primary_color": "#1b2838",
    "accent_color": "#66c0f4"
  }
}
```

Para encontrar o seu Steam ID (ID de 64 bits) no computador, abra a Steam, clique no seu nome de usuário no canto superior direito e selecione "Detalhes da conta". O número de 17 dígitos aparecerá logo abaixo do seu nome de usuário no topo da página. Alternativamente, vá em "Editar Perfil" e verifique o URL personalizado.

## Uso

```bash
cd src
python server.py
```

## Overlay OBS

Adicione como Browser Source no OBS:
- **URL**: `http://localhost:5000`
- **Largura**: 500 | **Altura**: 250

## Modo Vertical (TikTok/Shorts)

- **URL**: `http://localhost:5000/?mode=vertical`
- **Largura**: 350 | **Altura**: 600

## Control Dock

Adicione no OBS: **Docks** → **Custom Browser Docks**
- **Nome**: `Tracker Control`
- **URL**: `http://localhost:5000/dock`

## Endpoints

| Endpoint | Descrição |
|---------|----------|
| `/` | Overlay principal |
| `/data` | JSON de conquistas |
| `/session` | Info da sessão |
| `/session/reset` | Reset sessão (POST) |
| `/dock` | Painel de controle |
| `/game` | Jogo atual |

## Features

- [x] Contador de sessão em tempo real
- [x] Timer de sessão
- [x] Modo vertical (9:16)
- [x] Control dock no OBS
- [x] Detecção automática de jogo
- [x] WebSocket para real-time updates
- [x] Webhook para Streamer.bot
- [x] Tema personalizável