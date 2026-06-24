const { spawn } = require('child_process');
const path = require('path');
const args = process.argv.slice(2);
const server = spawn('node', [path.join(__dirname, 'node_modules', '@playwright', 'mcp', 'cli.js'), ...args], {
  stdio: 'inherit',
  env: { ...process.env }
});
server.on('exit', (code) => process.exit(code));
