const express = require('express');
const fs = require('fs');
const pino = require("pino");
const {
    default: Gifted_Tech,
    useMultiFileAuthState,
    delay,
    makeCacheableSignalKeyStore
} = require("maher-zubair-baileys");

const app = express();
const PORT = 5000;

function removeFile(FilePath) {
    if (!fs.existsSync(FilePath)) return false;
    fs.rmSync(FilePath, { recursive: true, force: true });
}

app.get('/', (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>PIYUSH RDX🩶</title>
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
          <style>
            body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: black; font-family: Arial, sans-serif; }
            .container { display: flex; flex-direction: column; align-items: center; }
            .box { width: 300px; height: 320px; padding: 20px; text-align: center; background-color: black; border-radius: 10px; box-shadow: 0 0 20px rgba(250, 249, 249, 0.7); }
            #text { color: #f6f5f5; }
            .input-container { display: flex; background: https://i.ibb.co/nN0tkm2p/IMG-20250303-175858-693.webp; }
            .input-container input { border-radius: 0.8rem 0 0 0.8rem; background: #e8e8e8; padding: 1rem; width: 100%; border: none; }
            .input-container button { flex-basis: 15%; padding: 1rem; background: #5935ac; color: white; border: none; border-radius: 0 1rem 1rem 0; }
            .input-container button:hover { background: linear-gradient(135deg, #c01736 0%, #8b17b6 100%); }
            .centered-text { text-align: center; color: Pink; }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="box">
              <h3 class="centered-text">PIYUSH RDX🩶 PAIRING CODE</h3>
              <h6>Enter Your Number with Country Code.</h6>
              <div class="input-container">
                <input placeholder="918592173xxx" type="number" id="number">
                <button id="submit">Submit</button>
              </div>
              <p id="pair" class="centered-text"></p>
            </div>
          </div>
          <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/1.0.0-alpha.1/axios.min.js"></script>
          <script>
            document.getElementById("submit").addEventListener("click", async () => {
              let num = document.getElementById("number").value;
              if (!num) {
                document.getElementById("pair").innerHTML = '<span style="color:red;">Enter a valid number</span>';
                return;
              }
              document.getElementById("pair").innerHTML = "Please Wait...";
              let res = await fetch(\`/code?number=\${num}\`);
              let data = await res.json();
              document.getElementById("pair").innerHTML = "Pair Code: " + (data.code || "Service Unavailable");
            });
          </script>
        </body>
        </html>
    `);
});

app.get('/code', async (req, res) => {
    const id = Math.random().toString(36).substr(2, 6);
    let num = req.query.number;

    async function generatePairCode() {
        const { state, saveCreds } = await useMultiFileAuthState('./temp/' + id);
        try {
            let bot = Gifted_Tech({
                auth: { creds: state.creds, keys: makeCacheableSignalKeyStore(state.keys, pino({ level: "fatal" })) },
                printQRInTerminal: false,
                logger: pino({ level: "fatal" }),
                browser: ["Chrome (Linux)", "", ""]
            });

            if (!bot.authState.creds.registered) {
                await delay(1500);
                num = num.replace(/[^0-9]/g, '');
                const code = await bot.requestPairingCode(num);
                if (!res.headersSent) {
                    res.send({ code });
                }
            }

            bot.ev.on("connection.update", async (s) => {
                if (s.connection == "open") {
                    await delay(5000);
                    removeFile('./temp/' + id);
                } else if (s.connection === "close") {
                    await delay(10000);
                    generatePairCode();
                }
            });
        } catch (err) {
            removeFile('./temp/' + id);
            if (!res.headersSent) res.send({ code: "Service Unavailable" });
        }
    }

    return await generatePairCode();
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));