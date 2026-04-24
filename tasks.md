# Tasks: Stream Achievement Counter

**Feature**: Sistema de Contagem de Conquistas para Streaming  
**Stack**: Python 3.10+ | Flask + WebSocket  
**Created**: 2026-04-23

---

## Phase 1: Setup

- [ ] T001 Criar estrutura de diretórios: `src/`, `templates/`, `config/`, `logs/`
- [ ] T002 Criar `requirements.txt` com dependências: flask, websockets, pyyaml, watchdog
- [ ] T003 Criar `config/config.json.example` com template de configuração

---

## Phase 2: Foundational

- [ ] T004 [P] Implementar parser VDF em `src/vdf_parser.py`
- [ ] T005 [P] Criar classe Achievement em `src/achievement.py`
- [ ] T006 Implementar config loader em `src/config.py`
- [ ] T007 Setup Flask server base em `src/server.py`

---

## Phase 3: User Story 1 - Overlay de Conquistas

**Goal**: Exibir conquistasSteam no overlay OBS

**Independent Test**: Adicionar Browser Source no OBS e verificar exibição

- [ ] T008 [US1] Implementar endpoint `/data` em `src/server.py` retornando JSON de conquistas
- [ ] T009 [US1] Criar template `templates/overlay.html` com CSS responsivo para OBS
- [ ] T010 [US1] Implementar polling do arquivo achievements.dat (5s interval)
- [ ] T011 [US1] Integrar VDF parser com server para alimentar endpoint /data

---

## Phase 4: User Story 2 - Contador de Sessão

**Goal**: Mostrar conquistas gainhas durante sessão atual

**Independent Test**: Desbloquear conquista e verificar incremento do contador

- [ ] T012 [US2] Implementar Session Manager em `src/session.py`
- [ ] T013 [US2] Adicionar timer e contador (+X) ao overlay HTML
- [ ] T014 [US2] Implementar endpoint reset de sessão via POST `/session/reset`
- [ ] T015 [US2] Persistir sessão em JSON para survive restart

---

## Phase 5: User Story 3 - Integração OBS

**Goal**: Overlay funciona como Browser Source no OBS

**Independent Test**: Adicionar como Browser Source e verificar renderização

- [ ] T016 [US3] Implementar `/dock` endpoint para control panel
- [ ] T017 [US3] Criar `templates/dock.html` com controles de sessão
- [ ] T018 [US3] Implementar modo vertical: `templates/overlay-vertical.html`
- [ ] T019 [US3] Suporte a query param `?mode=vertical` para alternar layouts

---

## Phase 6: User Story 4 - Detecção de Jogo

**Goal**: Detectar jogo atual e adaptar tema visual

**Independent Test**: Trocar jogo no Steam e verificar mudança de tema

- [ ] T020 [US4] Implementar game detection via active process ou API local
- [ ] T021 [US4] Extrair cores do jogo via Steam API (schema)
- [ ] T022 [US4] Aplicar tema dinâmico no overlay via CSS variables

---

## Phase 7: User Story 5 - WebSocket

**Goal**: Real-time updates via WebSocket

**Independent Test**: Conectar via WebSocket client e receber updates

- [ ] T023 [P] Setup WebSocket server em porta separada
- [ ] T024 [P] Broadcast de novos unlocks para todos os clients conectados
- [ ] T025 Integrar WebSocket com session manager paranotificação imediata

---

## Phase 8: User Story 6 - Streamer.bot

**Goal**:Announcements automáticos no chat

**Independent Test**: Configurar webhook e verificar mensagem

- [ ] T026 [US6] Implementar webhook client em `src/webhook.py`
- [ ] T027 [US6] Configurar rarity threshold (rara/lendária)
- [ ] T028 [US6] Enviar POST para Streamer.botem novo unlock

---

## Phase 9: Polish & Build

- [ ] T029 [P] Adicionar logging estruturado (JSON format)
- [ ] T030 [P] Tratar erros e edge cases (arquivo não encontrado,Parsing error)
- [ ] T031 Criar `PyInstaller` config para gerar .exe
- [ ] T032 Build e teste do executável
- [ ] T033 Criar README.md com instruções de uso

---

## Dependencies

| From | To | Reason |
|------|-----|--------|
| T001 | T002 | Setup básico |
| T002 | T003 | Dependências disponíveis |
| T003 | T004 | Config disponível |
| T004 | T005 | Parser alimenta models |
| T005 | T006 | Models configurados |
| T006 | T007 | Server usa config |
| T007 | T008 | Server pronto |
| T004+T005 | T008 | Parser + models para endpoint |
| T008 | T009 | Dados para overlay |
| T009 | T010 | Template precisa dados |
| T008+T010 | T011 | Integração completa |
| T011 | T012 | Dados prontos para sessão |
| T012 | T013 | Session para UI |
| T007 | T016 | Server para dock |
| T013 | T017 | Session para dock controls |
| T016+T009 | T018 | Templates prontos para vertical |
| T010 | T023 | Polling triggers WebSocket |
| T023 | T025 | WS conecta com session |
| T012 | T026 | Session para webhook |

---

## Parallel Opportunities

- **T004 + T005**: VDF parser e Achievement model são independentes (parallelizáveis)
- **T023 + T024**: WebSocket server pode ser implementado em paralelo com session manager
- **T029 + T030**: Logging e error handling podem ser feitos em paralelo

---

## Implementation Strategy: MVP First

**MVP Scope**: Fase 1 + Fase 2 + Fase 3 (US1)
- Serve funcionalidadecore: overlay com conquistas
- Independentemente testável
- Tempo estimado: 2 horas

**Incremental Delivery**:
1. MVP (2h) → Overlay básico
2. + Session (1h) → Contador funciona
3. + OBS (1h) → Dock e vertical
4. + Game detection (1h) → Temas automáticos
5. + WebSocket (0.5h) → Real-time
6. + Streamer.bot (0.5h) → Announcements
7. + Polish (1h) → Build final

---

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 33 |
| User Stories | 6 |
| Parallelizable Tasks | 6 |
| Estimated Time | 5.5h |

| Story | Tasks | Focus |
|-------|-------|-------|
| US1 | 4 | Overlay core |
| US2 | 4 | Session tracking |
| US3 | 4 | OBS integration |
| US4 | 3 | Game detection |
| US5 | 3 | WebSocket |
| US6 | 3 | Streamer.bot |

**Recommended MVP**: Fases 1-3 (US1) → Overlay funcional com conquistas