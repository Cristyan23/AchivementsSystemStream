# Feature Specification: Sistema de Contagem de Conquistas para Streaming

**Feature Branch**: `stream-achievement-counter`  
**Created**: 2026-04-23  
**Status**: Draft  
**Input**: Sistema de contagem de conquistas para streaming que é ligado com o sistema de conquistas da steam

## User Scenarios & Testing

### User Story 1 - Visualização de Conquistas Steam no Overlay (Priority: P1)

Como streamer, desejo que o sistema exiba minhas conquistas da Steam em tempo real no overlay do OBS para que meus viewers vejam meu progresso.

**Why this priority**: Funcionalidade core - sem ela o sistema não tem propósito

**Independent Test**: Testar conectando com API da Steam e verificando exibição no browser source do OBS

**Acceptance Scenarios**:

1. **Given** usuário configurou API key da Steam, **When** inicia o servidor, **Then** overlay exibe lista de conquistas
2. **Given** conquista é desbloqueada no Steam, **When** sistema polling detecta, **Then** overlay atualiza em tempo real

---

### User Story 2 - Contador de Sessão (Priority: P1)

Como streamer, desejo ver quantas conquistas desbloqueei durante a transmissão atual para acompanhar meu progresso.

**Why this priority**: Métrica essencial para streaming - viewers querem ver progresso da sessão

**Independent Test**: Desbloquear conquistas durante sessão e verificar contador "+X"

**Acceptance Scenarios**:

1. **Given** sessão iniciada com timer, **When** conquista é desbloqueada, **Then** contador incrementa
2. **Given** sessão resetada, **When** streamer solicita reset, **Then** contador volta a zero

---

### User Story 3 - Integração com OBS (Priority: P1)

Como streamer, desejo adicionar o overlay como browser source no OBS para exibir durante a transmissão.

**Why this priority**: Integração nativa com OBS é obrigatória para streamers

**Independent Test**: Adicionar como browser source e verificar renderização

**Acceptance Scenarios**:

1. **Given** servidor executando, **When** adiciona Browser Source com URL localhost:5000, **Then** overlay renderediza corretamente
2. **Given** modo vertical ativado, **When** URL com mode=vertical, **Then** layout alternate é exibido

---

### User Story 4 - Detecção Automática de Jogo (Priority: P2)

Como streamer, desejo que o overlay detecte automaticamente o jogo atual via Steam e adapte o tema visual.

**Why this priority**: Experiência seamless - não requer configuração manual por jogo

**Independent Test**: Trocar jogo no Steam e verificar mudança de tema

**Acceptance Scenarios**:

1. **Given** jogo ativo detectado, **When** sistema identifica appid, **Then** cores do overlay adaptam ao jogo
2. **Given** nenhum jogo ativo, **When** sistema em standby, **Then** exibe cartão de perfil

---

### User Story 5 - Integração Streamer.bot (Priority: P3)

Como streamer, desejo que conquistas sejam announcements automaticamente no chat via Streamer.bot.

**Why this priority**: Automação de chat aumenta engajamento

**Independent Test**: Configurar webhook e verificar mensagem no chat

**Acceptance Scenarios**:

1. **Given** conquista desbloqueada, **When** rarity é rara/lendária, **Then** mensagem enviada para chat via webhook

---

### User Story 6 - Modo Hunter (Priority: P3)

Como streamer, desejo fixar uma conquista específica no overlay para mostrar ao chat qual estou tentando conseguir.

**Why this priority**: Recurso popular para grind específico

**Independent Test**: Selecionar conquista e verificar pinning no overlay

**Acceptance Scenarios**:

1. **Given** conquista selecionada via control dock, **When** hunter mode ativado, **Then** detalhes exibidos no overlay

---

## Requirements

### Functional Requirements

- **FR-001**: Sistema DEVE monitorar arquivo achievements.dat local do Steam para detectar novos desbloqueios (sem API key necessária)
- **FR-002**: Sistema DEVE servir overlay via HTTP em porta configurável (default 5000)
- **FR-003**: Sistema DEVE servir WebSocket em porta separada para real-time updates
- **FR-004**: Sistema DEVE manter contador de sessão separado do total global
- **FR-005**: Usuários DEVEM poder resetar contador de sessão via control dock
- **FR-006**: Sistema DEVE suportar modo vertical (9:16) para TikTok/YouTube Shorts
- **FR-007**: Sistema DEVE detectar jogo ativo via polling de ISteamUserStats/GetPlayerAchievements
- **FR-008**: Sistema DEVE servir WebSocket em porta separada para real-time updates
- **FR-009**: Sistema DEVE integrar com Streamer.bot via webhook para announcements
- **FR-010**: Sistema DEVE suportar configuração via arquivo config.json

### Technology Stack

- **Language**: Python 3.10+
- **Dependencies**: requests, websocket-server, Flask/FastAPI

---

## Clarifications

### Session 2026-04-23

- Q: Linguagem e plataforma → A: Python
- Q: Método de detecção de conquistas → A: Arquivo local Steam (achievements.dat)
- Q: Interval de polling → A: 5 segundos
- Q: Configurações extras → A: Todas (cache, polling, webhook)
- Q: Formato do arquivo → A: VDF (Valve Data Format)

### Key Entities

- **Achievement**: Entidade representando conquista unlockable com nome, descrição, ícone, raridade, unlocked status
- **Session**: Sessão de streaming com timer e contador de conquistas gainhas
- **GameProfile**: Perfil de jogo com appid, nome, tema cromático
- **UserConfig**: Configurações do usuário incluindo Steam API Key, Steam ID,portas

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Overlay exibe lista de conquistas carregadas em até 5 segundos após inicialização
- **SC-002**: Novas conquistas são detectadas e exibidas em tempo real via WebSocket
- **SC-003**: Contador de sessão incrementa imediatamente após unlock detectado
- **SC-004**: Overlay funciona como Browser Source no OBS sem lag visível
- **SC-005**: Sistema usa menos de 100MB de memória em operação normal

---

## Assumptions

- Usuário possui API Key da Steam (obtida em https://steamcommunity.com/dev/apikey)
- Usuário sabe adicionar Browser Source no OBS
- Servidor executa localmente na mesma máquina do OBS
- Jogos suportados são aqueles com achievements no Steam
- Não requer autenticação OAuth - usa API key diretamente