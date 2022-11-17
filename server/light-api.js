/*
Interacts with the Python process that controls the array
 */

const zmq = require('zeromq');

async function request(body) {
  const sock = new zmq.Request();
  sock.connect('tcp://127.0.0.1:5555');

  await sock.send(JSON.stringify(body));
  const [result] = await sock.receive();

  return JSON.parse(result.toString());
}

function command(name, args) {
  return request({
    command: name,
    ...args,
  });
}

function setBabelMode() {
  return command('setMode', { mode: 'babel' });
}

function setDirectMode() {
  return command('setMode', { mode: 'direct' });
}

function getConnectedLights() {
  return command('getConnectedLights');
}

function blit(brightness, volume) {
  return command('blit', { brightness, volume });
}

function setActive(active) {
  if (active) {
    return command('on');
  }

  return command('off');
}

function isActive() {
  return command('is_on');
}

module.exports = {
  setBabelMode,
  setDirectMode,
  getConnectedLights,
  blit,
  setActive,
  isActive,
};
