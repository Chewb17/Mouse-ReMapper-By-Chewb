import subprocess
import sys

# Verifica e instala a biblioteca pynput, se necessário
try:
    import pynput
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput"])
    import pynput

# Verifica e instala a biblioteca PyQt5, se necessário
try:
    from PyQt5 import QtWidgets, QtGui, QtCore
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
    from PyQt5 import QtWidgets, QtGui, QtCore

from pynput import mouse, keyboard

# Cria controladores para teclado e mouse
keyboard_controller = keyboard.Controller()

# Variáveis globais para armazenar as teclas escolhidas
scroll_up_key = None
scroll_down_key = None
middle_click_key = None
side_button1_key = None
side_button2_key = None

# Listener global do mouse
mouse_listener = None

# Função para substituir a rolagem do mouse
def on_scroll(x, y, dx, dy):
    try:
        if dy > 0 and scroll_up_key:
            keyboard_controller.press(scroll_up_key)
            keyboard_controller.release(scroll_up_key)
        elif dy < 0 and scroll_down_key:
            keyboard_controller.press(scroll_down_key)
            keyboard_controller.release(scroll_down_key)
    except ValueError as e:
        print(f"Erro ao pressionar a tecla: {e}")

# Função para substituir os cliques dos botões do mouse
def on_click(x, y, button, pressed):
    try:
        if button == mouse.Button.middle and pressed and middle_click_key:
            keyboard_controller.press(middle_click_key)
            keyboard_controller.release(middle_click_key)
        elif button == mouse.Button.button8 and pressed and side_button1_key:  # Botão lateral 1
            keyboard_controller.press(side_button1_key)
            keyboard_controller.release(side_button1_key)
        elif button == mouse.Button.button9 and pressed and side_button2_key:  # Botão lateral 2
            keyboard_controller.press(side_button2_key)
            keyboard_controller.release(side_button2_key)
    except ValueError as e:
        print(f"Erro ao pressionar a tecla: {e}")

# Função para iniciar os listeners
def start_listeners():
    global mouse_listener
    if not mouse_listener:
        mouse_listener = mouse.Listener(on_scroll=on_scroll, on_click=on_click)
        mouse_listener.start()

# Função para parar os listeners
def stop_listeners():
    global mouse_listener
    if mouse_listener:
        mouse_listener.stop()
        mouse_listener = None

# Classe da aplicação PyQt5
class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mouse ReMapper by Chewb')

        # Define o tamanho da janela
        self.resize(400, 300)  # Largura: 400 pixels, Altura: 300 pixels

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # Labels e LineEdits para configurar as teclas
        self.scroll_up_label = QtWidgets.QLabel('Tecla para rolagem para cima:')
        self.scroll_up_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.scroll_up_label)
        layout.addWidget(self.scroll_up_edit)

        self.scroll_down_label = QtWidgets.QLabel('Tecla para rolagem para baixo:')
        self.scroll_down_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.scroll_down_label)
        layout.addWidget(self.scroll_down_edit)

        self.middle_click_label = QtWidgets.QLabel('Tecla para clique do meio:')
        self.middle_click_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.middle_click_label)
        layout.addWidget(self.middle_click_edit)

        self.side_button1_label = QtWidgets.QLabel('Tecla para botão lateral 1:')
        self.side_button1_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.side_button1_label)
        layout.addWidget(self.side_button1_edit)

        self.side_button2_label = QtWidgets.QLabel('Tecla para botão lateral 2:')
        self.side_button2_edit = QtWidgets.QLineEdit()
        layout.addWidget(self.side_button2_label)
        layout.addWidget(self.side_button2_edit)

        # Botão para iniciar o programa
        self.start_button = QtWidgets.QPushButton('Iniciar', self)
        self.start_button.clicked.connect(self.toggle_listeners)
        layout.addWidget(self.start_button)

        # Botão para parar o programa
        self.stop_button = QtWidgets.QPushButton('Parar', self)
        self.stop_button.clicked.connect(self.stop_program)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def toggle_listeners(self):
        if not mouse_listener:
            self.set_keys()
            self.start_button.setText('Em Execução')
            self.start_button.setStyleSheet('background-color: red')
        else:
            self.stop_program()
            self.start_button.setText('Iniciar')
            self.start_button.setStyleSheet('')  # Reseta a cor do botão

    def set_keys(self):
        global scroll_up_key, scroll_down_key, middle_click_key, side_button1_key, side_button2_key
        
        scroll_up_key = self.scroll_up_edit.text() or None
        scroll_down_key = self.scroll_down_edit.text() or None
        middle_click_key = self.middle_click_edit.text() or None
        side_button1_key = self.side_button1_edit.text() or None
        side_button2_key = self.side_button2_edit.text() or None

        start_listeners()

    def stop_program(self):
        stop_listeners()
        self.start_button.setText('Iniciar')
        self.start_button.setStyleSheet('')  # Reseta a cor do botão

# Função principal
def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
