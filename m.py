import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import matplotlib.pyplot as plt
import numpy as np

# Функция для очистки выражения
def clean_expression(expr):
    expr = expr.replace(',', '.')
    expr = re.sub(r'(\d)\s+(\d)', r'\1\2', expr)
    expr = expr.replace('..', '.')
    return expr

# Функция для добавления текста в поле ввода
def add_to_entry(text, entry):
    if text == 'Del':
        entry.text = entry.text[:-1]
    else:
        entry.text += text

# Функция для построения графика
def plot_graph(equation):
    equation = clean_expression(equation)

    try:
        x = np.linspace(-10, 10, 400)
        y = eval(equation)

        plt.figure(figsize=(8, 6))
        plt.plot(x, y, label=f'y = {equation}')
        plt.title('График функции')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.legend()
        plt.show()
    except Exception as e:
        show_popup("Ошибка", f"Ошибка при построении графика: {e}")

# Функция для вычисления выражения
def calculate(expression):
    expression = clean_expression(expression)

    try:
        result = eval(expression)
        show_popup("Результат", f"Результат: {result}")
    except Exception as e:
        show_popup("Ошибка", f"Ошибка при вычислении: {e}")

# Функция для отображения всплывающего окна
def show_popup(title, message):
    content = Label(text=message)
    popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
    popup.open()

class CalculatorApp(App):
    def __init__(self, **kwargs):
        super(CalculatorApp, self).__init__(**kwargs)
        self.entry = None

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(text="Введите выражение:", font_size=20)
        layout.add_widget(label)

        self.entry = TextInput(multiline=False, font_size=20, size_hint_y=None, height=50)
        layout.add_widget(self.entry)

        buttons_layout = GridLayout(cols=4, spacing=5, size_hint_y=None)
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'sqrt', '**', 'cos', 'sin',
            'x', 'y', 'Del', ')'
        ]

        for button in buttons:
            if button == '=':
                buttons_layout.add_widget(Button(text=button, font_size=20, on_press=lambda btn: calculate(self.entry.text)))
            elif button == 'sqrt':
                buttons_layout.add_widget(Button(text=button, font_size=20, on_press=lambda btn, b=button: add_to_entry(f'sqrt(', self.entry)))
            elif button == '**':
                buttons_layout.add_widget(Button(text=button, font_size=20, on_press=lambda btn, b=button: add_to_entry(f'**', self.entry)))
            elif button == 'cos':
                buttons_layout.add_widget(Button(text=button, font_size=20, on_press=lambda btn, b=button: add_to_entry(f'cos(', self.entry)))
            elif button == 'sin':
                buttons_layout.add_widget(Button(text=button, font_size=20, on_press=lambda btn, b=button: add_to_entry(f'sin(', self.entry)))
            else:
                buttons_layout.add_widget(Button(text=button, font_size=20, on_press=lambda btn, b=button: add_to_entry(b, self.entry)))

        scroll_view = ScrollView(size_hint=(1, None), size=(layout.width, layout.height * 0.6))
        scroll_view.add_widget(buttons_layout)
        layout.add_widget(scroll_view)

        plot_button = Button(text="Построить график", font_size=20, on_press=lambda btn: plot_graph(self.entry.text))
        layout.add_widget(plot_button)

        calculate_button = Button(text="Вычислить", font_size=20, on_press=lambda btn: calculate(self.entry.text))
        layout.add_widget(calculate_button)

        return layout

if __name__ == '__main__':
    CalculatorApp().run()