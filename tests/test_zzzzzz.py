import markdown
from nicegui import ui

md_text = '''
# 这是标题

这是一个段落，**带有加粗文本** 和 *斜体文本*。

- 列表项 1
- 列表项 2
- 列表项 3

```python
def hello():
    pass
```
'''

# 使用 markdown 库将 Markdown 转换为 HTML
# html_content = markdown.markdown(md_text)
html_content = md_text

ui.markdown(html_content)
ui.run()