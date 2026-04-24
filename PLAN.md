# Technical Implementation Plan: Stream Achievement Counter

**Feature**: Sistema de Contagem de Conquistas para Streaming  
**Stack**: Python 3.10+ | Flask + WebSocket  
**Created**: 2026-04-23

---

## Phase 1: Core Infrastructure

### 1.1 Project Setup
- [ ] Criar estrutura de diretórios: `src/`, `templates/`, `config/`, `logs/`
- [ ] Criar `requirements.txt` com dependências
- [ ] Setup virtual environment e instalação de deps
- [ ] Criar config.json template

### 1.2 VDF Parser Module
- [ ] Implementar parser VDF (Valve Data Format)
- [ ] Ler arquivo achievements.dat do Steam
- [ ] extrair: achievement name, description, unlock time, unlocked status
- [ ] Tratar formato binário e Unicode

### 1.3 Achievement Data Model
- [ ] Criar classe Achievement com atributos
- [ ] Implementar cache em memória
- [ ] Comparar snapshots para detectar novos unlocks
- [ ] Calcular raridade based on global unlock %

---

## Phase 2: Server & Overlay

### 2.1 HTTP Server
- [ ] Setup Flask app na porta configurável
- [ ] Implementar endpoint `/` - overlay HTML
- [ ] Implementar `/data` - JSON com achievements
- [ ] Implementar `/dock` - control panel

### 2.2 WebSocket Server
- [ ] Setup WebSocket em porta separada
- [ ] Broadcast de novos unlocks para clients
- [ ] Suporte a múltiplas conexões simultâneas

### 2.3 Overlay Templates
- [ ] Criar `overlay.html` - main display
- [ ] Criar `overlay-vertical.html` - 9:16 mode
- [ ] Criar `dock.html` - control panel
- [ ] CSS responsivo para OBS

---

## Phase 3: Session Tracking

### 3.1 Session Manager
- [ ] Implementar timer de sessão
- [ ] Contador de achievements gainhas (+X)
- [ ] Persistence de sessão (JSON)
- [ ] Reset via endpoint ou dock

### 3.2 Game Detection
- [ ] Monitoring do app corrente via Steam client
- [ ] Adaptação de tema based on appid
- [ ] Fallback para profile card

---

## Phase 4: Integrations

### 4.1 Streamer.bot Webhook
- [ ] POST webhook em nuevo unlock
- [ ] Configurable rarity threshold
- [ ] Custom message template

### 4.2 Logging & Metrics
- [ ] Structured logging (JSON)
- [ ] Métricas de performance
- [ ] Error handling robusto

---

## Phase 5: Build & Package

### 5.1 Executable
- [ ] PyInstaller config
- [ ] Build .exe para Windows
- [ ] Teste deportabilidade
- [ ] Doc README

---

## File Structure

```
stream-achievement-counter/
├── src/
│   ├── main.py              # Entry point
│   ├── vdf_parser.py       # VDF parsing
│   ├── achievement.py      # Data models
│   ├── session.py         # Session manager
│   ├── server.py         # HTTP/WS server
│   └── config.py         # Configuration
├── templates/
│   ├── overlay.html
│   ├── overlay-vertical.html
│   └── dock.html
├── config/
│   └── config.json.example
├── requirements.txt
├── SPEC.md
└── README.md
```

---

## Dependencies

```
flask>=3.0.0
websockets>=12.0
pyyaml>=6.0
watchdog>=3.0.0
pyinstaller>=6.0
```

---

## Acceptance Checkpoints

- [ ] Overlay exibe conquistas carregadas em <5s
- [ ] Novos unlocks detectáveis em <5s
- [ ] Contador de sessão incrementa corretamente
- [ ] Browser Sourcerenderiza sem erros no OBS
- [ ] WebSocket conecta e recebe updates
- [ ] .exe executa standalone

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| VDF parsing complex | Alto | Usar biblioteca existente (s稳定) |
| Steam path varies | Médio | Detecção automática + config manual |
| OBS compatibility | Médio | Testar múltiplos browsers |
| Resource usage | Médio | Polling eficiente, caching |

---

## Estimated Timeline: 4-6 horas

**Phase 1**: 1h | **Phase 2**: 1.5h | **Phase 3**: 1h | **Phase 4**: 0.5h | **Phase 5**: 1h