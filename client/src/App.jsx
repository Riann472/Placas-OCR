import { useState } from "react"
import axios from 'axios'

function App() {
  const [preview, setPreview] = useState();
  const [file, setFile] = useState()
  const [placa, setPlaca] = useState()

  async function submit(e) {
    e.preventDefault();
    const form = new FormData();
    form.append('file', file, 'crop.jpg');

    try {
      const result = await axios.post(`${import.meta.env.VITE_API_URL}/upload`, form);
      if (result.data.error) {
        alert(result.data.error)
      } else {
        setPlaca(result.data.message);
      }
    } catch (err) {
      console.log(err)
      alert("Erro na comunicação com o servidor.");
    }
  }

  return (
    <>
      <header>
        <h1>Leitor de Placas</h1>
      </header>
      <main>
        <h1>Envie a sua imagem</h1>
        <form onSubmit={submit}>
          <label htmlFor="file" onClick={() => setPlaca(null)}>
            📁 Escolher imagem
          </label>
          <input type="file" id="file" onChange={e => {
            if (e.target.files.length == 0) setFile(null)
            setFile(e.target.files[0])
            setPreview(URL.createObjectURL(e.target.files[0]))
          }} />

          <img src={preview} alt="" />
          {placa && (<h2>Resultado: {placa}</h2>)}
          <button>Enviar</button>
        </form>
      </main>
    </>
  )
}

export default App
