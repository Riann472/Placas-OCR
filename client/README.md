# Frontend – Leitor de Placas Veiculares

Este é o frontend do sistema de identificação de placas de veículos (carros e motos), desenvolvido em **React**. Ele permite fazer o upload de imagens e enviá-las para o backend para leitura via OCR.

## 🔧 Tecnologias Utilizadas

- React
- React Image Crop
- Axios (requisições HTTP)

---

## 🚀 Como rodar localmente

## ✅ Pré-requisitos

Antes de começar, certifique-se de que você tem o **Node.js (versão 22 ou superior)** instalado em sua máquina.  
Você pode baixar o Node.js em: [https://nodejs.org](https://nodejs.org)

Para verificar se o Node.js está instalado, execute no terminal:

```bash
node -v
npm -v
```

### 1. Clone este repositório
```bash
git clone https://github.com/Riann472/Placas-OCR-Client.git
cd Placas-OCR-Client
```

### 2. Instale as dependências

```bash
npm install
```

### 3. Configure as variaveis de ambiente .env
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
VITE_API_URL=http://localhost:3001
```
(Caso tenha configurado sua api em outra porta, ou em nuvem, colocar a url correta da api)

### 4. Inicie a aplicação

```bash
npm run dev
```

> O frontend estará disponível em [http://localhost:5173](http://localhost:5173)

## ⚙️ Configuração

Certifique-se de que o backend está rodando em [http://localhost:3001](http://localhost:3001),  
ou atualize a URL das requisições no código (por exemplo, nas chamadas do Axios).

## 📸 Funcionalidades

- Captura de imagem  
- Envio da imagem para o backend  
- Exibição da placa identificada na resposta
