const fs = require('fs');
const path = require('path');
const https = require('https');
const express = require('express');
const { setActive, isActive } = require('./light-api');

const PORT = 8000;

/* Generated with:
openssl req \
  -x509 \
  -nodes \
  -days 365 \
  -newkey rsa:2048 \
  -subj '/CN=localhost/O=FooBar/C=US' \
  -keyout server.key \
  -out server.crt
*/
const options = {
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.crt'),
};

const app = express();
app.use(express.static(path.join(__dirname, '../client/build')));
app.use(express.json());

app.get('/active', async (req, res) => {
  const active = await isActive();
  res.json(active);
});

app.post('/active', async (req, res) => {
  if (!('active' in req.body)) {
    res.sendStatus(400);
    return;
  }

  if (req.body.active === true) {
    await setActive(true);
    res.json(true);
    return;
  }

  if (req.body.active === false) {
    await setActive(false);
    res.json(false);
    return;
  }

  res.sendStatus(400);
});

const server = https.createServer(options, app);
server.listen(PORT, () => console.log(`https://localhost:${PORT}`));
