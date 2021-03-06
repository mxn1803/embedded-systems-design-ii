"""Adds two numbers provided by the user.

A PyQt4 application that accepts two numbers and calculates their sum.
"""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

import sys

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (
    QApplication,
    QWidget,
    QGridLayout,
    QLineEdit,
    QSizePolicy,
    QPushButton,
    QLabel
)

from adder import Adder

class AdderWidget(QWidget):
    """Wraps a PyQt4 application around the Adder class."""

    def __init__(self):
        super(AdderWidget, self).__init__()

        # instantiate adder
        self.adder = Adder()

        self.__build_ui()

    def __handle_submit(self):
        a = self.a_input.text()
        b = self.b_input.text()
        result = self.adder.add(a, b)
        self.output.setText(str(result))

    def __build_ui(self):
        self.__decorate()
    
        # these values are dynamic
        self.a_input = self.__q_line_edit('0')
        self.b_input = self.__q_line_edit('0')
        self.output = self.__q_line_edit('0', False)

        a_input_label = self.__q_label('Input A:')
        b_input_label = self.__q_label('Input B:')
        output_label = self.__q_label('Output:')
        
        btn = self.__q_push_button('Get Sum')

        layout = QGridLayout()
        layout.addWidget(a_input_label, 0, 0)
        layout.addWidget(self.a_input, 0, 1)
        layout.addWidget(b_input_label, 1, 0)
        layout.addWidget(self.b_input, 1, 1)
        layout.addWidget(btn, 0, 2, 2, 1)
        layout.addWidget(output_label, 2, 0)
        layout.addWidget(self.output, 2, 1, 1, 2)

        btn.clicked.connect(lambda: self.__handle_submit())
        
        self.setLayout(layout)
        self.show()

    def __decorate(self):
        self.setWindowTitle('Adder')
        self.setFixedSize(720, 240)
        self.move(640, 480)

    def __q_line_edit(self, text, editable=True):
        qle = QLineEdit(text)
        qle.setTextMargins(8, 8, 8, 8)
        qle.setAlignment(Qt.AlignRight)
        qle.setReadOnly(not editable)
        qle.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        return qle

    def __q_push_button(self, text):
        qpb = QPushButton(text)
        qpb.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        qpb.setStyleSheet('background-color: #8fd485;')
        return qpb

    def __q_label(self, text):
        ql = QLabel(text)
        ql.setAlignment(Qt.AlignCenter)
        ql.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        return ql


def main():
    app = QApplication(sys.argv)
    adderWidget = AdderWidget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()