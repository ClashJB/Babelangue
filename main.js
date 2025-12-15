const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let flaskProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
    icon: path.join(__dirname, 'static/babelangue_logo.png')
  });

  // Start Flask server
  startFlaskServer();

  // Wait a bit for Flask to start, then load the page
  setTimeout(() => {
    mainWindow.loadURL('http://127.0.0.1:5000');
  }, 2000);

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

function startFlaskServer() {
  // Determine Python command (python3 on Unix, python on Windows)
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

  // Start Flask app
  flaskProcess = spawn(pythonCmd, ['flasktest.py'], {
    cwd: __dirname
  });

  flaskProcess.stdout.on('data', (data) => {
    console.log(`Flask: ${data}`);
  });

  flaskProcess.stderr.on('data', (data) => {
    console.error(`Flask Error: ${data}`);
  });

  flaskProcess.on('close', (code) => {
    console.log(`Flask process exited with code ${code}`);
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', function () {
  // Kill Flask process when app closes
  if (flaskProcess) {
    flaskProcess.kill();
  }

  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow();
  }
});

// Clean up Flask process on app quit
app.on('will-quit', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
});