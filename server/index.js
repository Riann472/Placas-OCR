const fs = require('fs')
const express = require('express')
const cors = require('cors')
const multer = require('multer')
const sharp = require('sharp')
const OCR = require('tesseract.js')
require('dotenv').config()

const storage = require('./storage')

const app = express()
app.use(cors())
app.use(express.json())

fs.mkdirSync('./processamento', { recursive: true })
fs.mkdirSync('./uploads', { recursive: true })

const upload = multer({ storage })

app.post('/upload', upload.single('file'), async (req, res) => {
    const buffer = await sharp(req.file.path)
        .resize({ width: 600 })
        .grayscale()
        .linear(1.2, -10)
        .threshold(140)
        .sharpen()
        .toBuffer();

    sharp(buffer).toFile('./processamento/atual.png', (err, info) => {
        if (err) {
            console.error('Erro ao salvar a imagem:', err);
            return res.status(500).json({ error: 'Erro ao salvar a imagem' });
        }
    })

    const worker = await OCR.createWorker('placanovo')
    await worker.setParameters({
        tessedit_char_whitelist: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        tessedit_pageseg_mode: '6',
        user_defined_dpi: '300'
    }); 

    const result = await worker.recognize(buffer)
    await worker.terminate()

    const textoBruto = result.data.text.replace(/[^A-Z0-9]/gi, '')
    const plateRegex = /\b([A-Z]{3}-?\d{4}|[A-Z]{3}\d[A-Z0-9]\d{2})\b/;
    const match = textoBruto.match(plateRegex);
    // console.log(match)
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

app.listen(process.env.PORT, () => {
    console.log(`Rodando na porta ${process.env.PORT}`)
})