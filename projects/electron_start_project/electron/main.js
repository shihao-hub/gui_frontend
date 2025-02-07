// electron main.js

const {app, BrowserWindow} = require('electron');

function createWindow() {
    // 创建窗口
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true // 启用 Node 集成（注意安全）
        }
    });

    // 加载 URL 或本地 HTML 文件
    let url = 'http://localhost:8888/api/docs';
    win.loadURL(url)
        .then(r => {
            console.log(`loading url: ${url} success!`);
        })
        .catch(e => {
            console.log(e);
        });

    // 或者你可以加载本地文件
    // win.loadFile('index.html');
}

// 当 Electron 完成初始化时
app.whenReady().then(createWindow);

// 退出应用时的处理
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});