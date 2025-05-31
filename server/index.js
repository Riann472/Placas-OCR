// Imports
const fs = require('fs')
const express = require('express')
const cors = require('cors')
const multer = require('multer')
const sharp = require('sharp')
const OCR = require('tesseract.js')
require('dotenv').config()

// Storage do multer
const storage = require('./storage')

// Inicialização e middlewares
const app = express()
app.use(cors())
app.use(express.json())

// Criação das pastas
fs.mkdirSync('./processamento', { recursive: true })
fs.mkdirSync('./uploads', { recursive: true })

const upload = multer({ storage })

// endpoint upload
app.post('/upload', upload.single('file'), async (req, res) => {
    // processa a imagem e armazena numa variavel
    const buffer = await sharp(req.file.path)
        .resize({ width: 600 })
        .grayscale()
        .linear(1.2, -10)
        .threshold(140)
        .sharpen()
        .toBuffer();

    // apenas para analise da foto processada, comentar se não for analisar
    sharp(buffer).toFile('./processamento/atual.png', (err, info) => {
        if (err) {
            console.error('Erro ao salvar a imagem:', err);
            return res.status(500).json({ error: 'Erro ao salvar a imagem' });
        }
    })

    // cria o worker e seta os paramentros
    const worker = await OCR.createWorker('placa')
    await worker.setParameters({
        tessedit_char_whitelist: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        tessedit_pageseg_mode: '6',
        user_defined_dpi: '300'
    });

    // pega os resultados e finaliza o worker
    const result = await worker.recognize(buffer)
    await worker.terminate()

    // regex para pegar apenas texto de placa
    const textoBruto = result.data.text.replace(/[^A-Z0-9]/gi, '')
    const plateRegex = /\b([A-Z]{3}-?\d{4}|[A-Z]{3}\d[A-Z0-9]\d{2})\b/;
    const match = textoBruto.match(plateRegex);

    // caso bata com o regex, retorna placa, senao, retorna placa nao reconhecida
    if (match) {
        const placa = match[0];
        console.log("Placa identificada:", placa);
        return res.json(placa);
    } else {
        console.log("Nenhuma placa encontrada.");
        console.log("Texto bruto: " + result.data.text)
        return res.json("Placa não reconhecida");
    }
})

// subindo o server
app.listen(process.env.PORT, () => {
    console.log(`Rodando na porta ${process.env.PORT}`)
})