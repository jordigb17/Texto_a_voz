import newspaper as nwp #--Sirve para extraer y analizar contenido de noticias
import gtts #--Convierte texto a voz
import re #--Trabajar con expresiones regulares
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit, QProgressDialog, QMessageBox)
import sys

def is_url(string):
    'Saber si el texto es una url'
    #INPUT
    #--cadena
    #OUTPUT
    #--True(es url) o False(No es url)

    # Patrón para una URL
    patron = re.compile(
        r'^(https?://)?'  # Protocolo (http o https) opcional
        r'([a-zA-Z0-9.-]+)\.'  # Dominio
        r'([a-zA-Z]{2,})'  # Extensión (.com, .org)
        r'(:[0-9]{1,5})?'  # Puerto opcional
        r'(/.*)?$'  # Ruta opcional
    )
    return bool(patron.match(string))

def convert(string):
    if is_url(string):
        #Crear objeto del artículo
        url = nwp.Article(string,language = 'es') #--Indicar idioma español (es)

        #Descargar i analizar
        url.download()
        url.parse()
        content = url.text #Escribir el texto
    else: 
        content = string #Cambio de nombre al texto para que tengan el mismo nombre
        
    #Crear objeto
    tts = gtts.gTTS(text = content,lang='es', slow=False)

    #Abrir ventana temporal mientras se convierte a audio el texto
    progress = QProgressDialog('Convirtiendo a audio...', None, 0, 0)
    progress.setWindowTitle('Procesando')
    progress.setWindowModality(Qt.ApplicationModal)
    progress.setCancelButton(None)
    progress.show()

    #Guardar el archivo como 'archivo.mp3
    tts.save('archivo.mp3')

    progress.close()  # Cierra el cuadro cuando termina

    QMessageBox.information(None, "Proceso Completo", "Texto convertido a audio (archivo.mp3).")
    

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Convertidor')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet('background-color: #2C2F33;')

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Etiqueta de título
        title = QLabel('Convertidor de texto a voz')
        title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(title)

        # Etiqueta de instrucciones
        instructions = QLabel("Copia y pega el texto o URL")
        instructions.setFont(QFont('Arial', 14))
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("color: #CCCCCC;")
        layout.addWidget(instructions)

        # Caja de texto para ingresar el texto
        self.text_input = QTextEdit()
        self.text_input.setFont(QFont("Arial", 12))
        self.text_input.setStyleSheet("background-color: #FFFFFF; color: #000000; padding: 10px;")
        self.text_input.setPlaceholderText("Escribe o pega el texto o URL aquí...")  # Marcador de posición
        layout.addWidget(self.text_input)

        # Botón para guardar el texto
        save_button = QPushButton("Guardar Texto")
        save_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        save_button.setStyleSheet("background-color: #7289DA; color: #FFFFFF; padding: 10px; border-radius: 5px;")
        save_button.clicked.connect(self.save_text)  # Conectar el botón con la función de guardado
        layout.addWidget(save_button)

        # Asignar el layout al widget central
        central_widget.setLayout(layout)

    def save_text(self):
        """Función para guardar el texto en un archivo .txt"""
        string = self.text_input.toPlainText()  # Obtener el texto del QTextEdit
        convert(string)


        
    
# Inicializar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())



      