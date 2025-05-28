# 🔍 Leitor de Placas Veiculares

Este projeto é um sistema completo para leitura de placas veiculares a partir de imagens. Ele é composto por três aplicações:

- `client/`: Interface web em React para upload de imagens.
- `server/`: Backend em Node.js que realiza o processamento com OCR com TesseractJS.
- `server-flask/`: Backend em Flask que orquestra a comunicação e roda modelos YOLO para detecção.

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
└── README.md           # Este arquivo
```

## ✅ Pré-requisitos
- Node.js v18 ou superior
- Python 3.8+
- Pip
- Git

## 📦 Instalação
### 1. Clone o projeto
```bash
git clone https://github.com/SEU_USUARIO/leitor-placas-veiculares.git
cd leitor-placas-veiculares
``` 
### 2. Instale o Frontend (React)
```bash
cd client
npm install
``` 
### 3. Instale o Backend Node.js
```bash
cd ../server
npm install
``` 
### 4. Crie o ambiente virtual e instale as libs do Flask
```bash
cd ../server-flask
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
``` 

## ⚙️ Configuração
### 🔒 Variáveis de Ambiente
**📁React (`client/.env`)**

**1.** Navegue até a pasta client/.

**2.** Crie um arquivo chamado .env (se ainda não existir).

**3.** Adicione a seguinte variável:
> Essa URL define onde está rodando o servidor Flask, que será acessado pelo frontend React.

```env
VITE_API_URL=http://localhost:5000
```
#
**📁Node (`server/.env`)**

**1.** Navegue até a pasta server/.

**2.** Crie um arquivo chamado .env (se ainda não existir).

**3.** Adicione a seguinte variável:
```env
PORT=3001
```
> O backend Node.js irá escutar nessa porta pelas requisições vindas do Flask.
#
**📁Flask**

No main.py ou .env, configure no arquivo main.py:
```env
NODE_API_URL = "http://localhost:3001/upload"
```

## 🚀 Como Rodar
Para facilitar o processo, há um arquivo chamado start-all.bat na raiz do projeto que abre os três servidores (client, Flask e Node) automaticamente em terminais separados.

### ▶️ Como usar
- Dê dois cliques no arquivo start-all.bat
ou

- Execute pelo terminal (cmd ou PowerShell):
```bash
start-all.bat
```
> 💡 Certifique-se de que você já instalou as dependências dos três serviços (client, server e server-flask) antes de executar.
#
## ⚠️ Observação
- O script funciona apenas no Windows, pois usa comandos .bat.

- Ele espera que os diretórios client/, server/ e server-flask/ estejam todos corretamente configurados e no mesmo nível da raiz do projeto.

- O ambiente virtual do Flask (venv) precisa estar criado antes de rodar o script.
