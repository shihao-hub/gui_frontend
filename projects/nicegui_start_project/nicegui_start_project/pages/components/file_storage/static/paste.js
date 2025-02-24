document.addEventListener('paste', async (e) => {{
            const pasteArea = document.getElementById('{paste_area_id}');
            if (!pasteArea) return;

            const rect = pasteArea.getBoundingClientRect();
            const inBounds =
                e.clientX >= rect.left &&
                e.clientX <= rect.right &&
                e.clientY >= rect.top &&
                e.clientY <= rect.bottom;
                
            if (inBounds) {{
                const items = e.clipboardData.items;
                for (const item of items) {{
                    if (item.kind === 'file') {{
                        const file = item.getAsFile();

                        // 通过隐藏的input触发上传
                        const input = document.getElementById('{paste_upload_id}').querySelector('input');
                        const dataTransfer = new DataTransfer();
                        dataTransfer.items.add(file);
                        input.files = dataTransfer.files;

                        // 触发NiceGUI上传事件
                        input.dispatchEvent(new Event('change'));
                    }}
                }}
            }}
        }});