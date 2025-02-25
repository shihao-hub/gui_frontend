from datetime import datetime, timedelta

from nicegui import ui

TITLE = "倒计时"
ICON = "schedule"


class Widget:
    def __init__(self, parent):
        self.parent = parent

        self.remaining = 0
        self.timer = None

    def init_widget(self):
        def _update_display():
            self.remaining -= 1
            if self.remaining <= 0:
                self.timer.deactivate()
                time_display.set_text('时间到！')
                start_btn.enable()
                for _input in [hours, minutes, seconds]:
                    _input.enable()
                ui.notify('倒计时结束！', type='positive')
                return

            time_display.set_text(str(timedelta(seconds=self.remaining)))

        def start_btn_on_click():
            total = hours.value * 3600 + minutes.value * 60 + seconds.value

            if total < 1:
                ui.notify('时间必须至少1秒！', type='negative')
                return

            self.remaining = total
            time_display.set_text(str(timedelta(seconds=self.remaining)))

            # 禁用控件
            start_btn.disable()
            for _input in [hours, minutes, seconds]:
                _input.disable()

            # 启动计时器
            self.timer = ui.timer(1.0, _update_display)

        def cancel_btn_on_click():
            if self.timer:  # 停止计时器
                self.timer.deactivate()
            time_display.set_text('00:00:00')  # 重置显示
            for inp in [hours, minutes, seconds]:  # 启用输入
                inp.enable()
            start_btn.enable()  # 恢复开始按钮

        # main
        with self.parent:
            ui.colors(
                primary='#4A90E2',  # 主色调
                secondary='#FFA726',  # 次要颜色
                accent='#7E57C2',  # 强调色
                positive='#43A047',  # 成功状态颜色
                negative='#E53935'  # 错误状态颜色
            )

            ui.query('body').classes('items-center')
            with ui.column().classes('items-center gap-4 w-full'):  # w-full 是关键
                ui.label('倒计时设置').classes('text-2xl')
                with ui.row().classes('items-center justify-center gap-4'):
                    hours = ui.number('小时', value=0, min=0, max=12, format='%d').classes('w-24')
                    minutes = ui.number('分钟', value=0, min=0, max=59, format='%d').classes('w-24')
                    seconds = ui.number('秒', value=0, min=0, max=59, format='%d').classes('w-24')
                time_display = ui.label('00:00:00').classes('text-4xl font-bold')
                # 开始按钮容器（关键：需要设为相对定位）
                with ui.button(color='positive').classes('relative px-8 rounded-full') as start_btn:
                    # 主按钮文本
                    ui.label('开始计时').classes('z-0')  # z-index 确保在底层

                    # fixme
                    # 右上角微型取消按钮（直接作为开始按钮的子元素）
                    cancel_btn = ui.button(icon='close', color='none').classes('''
                        absolute                      # 绝对定位
                        top-0 right-0                 # 定位到右上角
                        -translate-y-1/2 translate-x-1/2  # 中心点偏移
                        text-gray-300 
                        hover:text-gray-500
                        active:text-red-300
                        text-opacity-80
                        hover:text-opacity-100
                        text-[8px]                   # 更小字号
                        p-0                          # 无内边距
                        rounded-full
                        bg-white
                        shadow
                        transition-all
                        scale-50 hover:scale-75       # 大小控制
                        z-10                         # 确保在上层
                        cursor-pointer                # 明确可点击
                    ''')
                    cancel_btn.visible = False
                    cancel_btn.disable()
                ui.label('最大时长：12小时').classes('text-sm text-gray-500')

            start_btn.on('click', start_btn_on_click)
            cancel_btn.on('click', cancel_btn_on_click)


def init_widget(parent):
    Widget(parent).init_widget()
