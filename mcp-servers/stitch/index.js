const https = require('https');

const STITCH_URL = 'https://stitch.googleapis.com/mcp';
const API_KEY = process.env.GOOGLE_API_KEY || '{{YOUR_GOOGLE_API_KEY}}';

function sendToStitch(body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const url = new URL(STITCH_URL);
    const options = {
      hostname: url.hostname,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY
      }
    };
    const req = https.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => responseData += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(responseData));
        } catch (e) {
          reject(new Error('No se pudo parsear respuesta: ' + responseData));
        }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

let initialized = false;

process.stdin.setEncoding('utf-8');
let buffer = '';

process.stdin.on('data', async (chunk) => {
  buffer += chunk;
  const lines = buffer.split('\n');
  buffer = lines.pop();
  for (const line of lines) {
    if (!line.trim()) continue;
    try {
      const msg = JSON.parse(line);
      const { id, method, params } = msg;
      if (method === 'initialize' && !initialized) {
        initialized = true;
        process.stdout.write(JSON.stringify({
          jsonrpc: '2.0',
          id,
          result: {
            protocolVersion: '2024-11-05',
            capabilities: { tools: { listChanged: false } },
            serverInfo: { name: 'StitchBridge', version: '1.0' }
          }
        }) + '\n');
      } else if (method === 'notifications/initialized') {
        // ignore
      } else if (method === 'tools/list') {
        const result = await sendToStitch(msg.method === 'initialize' ? msg : { jsonrpc: '2.0', id, method, params });
        process.stdout.write(JSON.stringify(result) + '\n');
      } else if (method === 'tools/call') {
        const result = await sendToStitch(msg);
        process.stdout.write(JSON.stringify(result) + '\n');
      } else {
        const result = await sendToStitch(msg);
        process.stdout.write(JSON.stringify(result) + '\n');
      }
    } catch (e) {
      process.stderr.write('Error: ' + e.message + '\n');
    }
  }
});
