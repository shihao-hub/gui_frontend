from nicegui import ui

# 创建一个共享的输入框
input_value = ui.input(placeholder='Type Here...')


@ui.page("/home")
def home_page():
    ui.label('Home Page')
    ui.label('Current Input: ')
    ui.label(input_value.value)  # 显示输入框的当前值
    ui.button('Go to About Page', on_click=lambda: ui.navigate.to('about'))


@ui.page("/about")
def about_page():
    ui.label('About Page')
    ui.label('Input from Home Page: ')
    ui.label(input_value.value)  # 显示输入框的当前值
    ui.button('Back to Home', on_click=lambda: ui.navigate.to('home'))


ui.run()
