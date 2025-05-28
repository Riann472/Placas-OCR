# 🔍 Leitor de Placas Veiculares – Full Stack

Este projeto é um sistema completo para leitura de placas veiculares a partir de imagens. Ele é composto por três aplicações:

- `client/`: Interface web em React para upload de imagens.
- `server/`: Backend em Node.js que realiza o processamento com OCR.
- `server-flask/`: Backend em Flask que orquestra a comunicação e pode rodar modelos YOLO para detecção.

---

## 🗂 Estrutura de Pastas

```bash
leitor-placas-veiculares/
│
├── client/             # Frontend (React)
│
├── server/             # Backend (Node.js)
│   ├── processamento/  # Última imagem processada (para análise)
│   └── uploads/        # Todas as imagens enviadas
│
├── server-flask/       # Backend (Flask)
│   ├── venv/           # Ambiente virtual Python
│   └── yoloModels/     # Modelos treinados do YOLO
│
