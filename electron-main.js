const { app, BrowserWindow } = require('electron');
const { exec } = require('child_process');

let mainWindow;

app.on('ready', () => {
  // Start the Flask app
  exec('python run.py', (err, stdout, stderr) => {
    if (err) {
      console.error("Flask failed to start", stderr);
      return;
    }
    console.log(stdout);
  });

  // Create the Electron window
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false
    }
  });

  // Load the Flask app
  mainWindow.loadURL('http://127.0.0.1:5000');
});
