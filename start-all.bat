@echo off
echo Iniciando os servidores...

:: Iniciar o React (client)
start cmd /k "cd client && npm run dev"

:: Iniciar o Node.js (server)
start cmd /k "cd server && npm run start"

:: Iniciar o Flask (server-flask com venv)
start cmd /k "cd server-flask && call venv\Scripts\activate && python -m flask --app main run"

echo Todos os serviços foram iniciados em janelas separadas.