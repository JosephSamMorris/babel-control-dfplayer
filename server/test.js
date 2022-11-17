const { blit } = require('./light-api');

const unitCount = 180;
let t = 0;

setInterval(async () => {
  const brightness = Array.from(Array(unitCount)).map((_, i) => i / 180);
  const volume = Array.from(Array(unitCount)).map(() => t % 2 === 0 ? 0 : 1);

  await blit(brightness, volume);
  console.log('blit', brightness, volume);

  t += 1;
}, 1000 / 3);
