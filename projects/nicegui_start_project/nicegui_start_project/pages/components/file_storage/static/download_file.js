function downloadFile(filename) {
    fetch(`/pages/components/file_storage/api/download?uid=${filename}`)
        .then(response => {
            console.log(response);
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(text);
                });
            }
            return response.blob()
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        })
        .catch(error => {
            console.error('下载失败:', error);
            alert(error.message);
        });
}
