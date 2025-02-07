// 2025-01-29：打包这么多细节？暂且搁置。参考资料的链接已由 OneTab 插件保存。

const createWindowsInstaller = require('electron-winstaller').createWindowsInstaller;
const path = require('path');

getInstallerConfig()
    .then(createWindowsInstaller)
    .catch((error) => {
        console.error(error.message || error);
        process.exit(1);
    });

function getInstallerConfig() {
    console.log('creating windows installer');
    const rootPath = path.join('./');
    const outPath = path.join(rootPath, 'release-builds');

    return Promise.resolve({
        appDirectory: path.join(outPath, 'api-docs-win32-ia32/'),
        authors: 'zsh',
        noMsi: true,
        outputDirectory: path.join(outPath, 'windows-installer'),
        exe: 'api_docs.exe',
        setupExe: 'ApiDocsInstaller.exe',
        setupIcon: path.join(rootPath, 'assets', 'icons', 'win', 'icon.ico')
    });
}
