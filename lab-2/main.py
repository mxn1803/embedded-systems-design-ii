"""Calculates position of an object in 3D space given two (x, y) coordinates.

A PyQt4 application that accepts two (x, y) coordinate pairs of a centroid from
a perspective of a binocular vision setup and determines the position of the
centroid in 3D space.
"""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

import sys

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLineEdit,
    QSizePolicy,
    QPushButton,
    QRadioButton,
    QLabel,
    QKeySequence,
    QShortcut
)

from binocular import Binocular

class BinocularWidget(QWidget):
    """Wraps a PyQt4 application around the Binocular class."""

    def __init__(self):
        super(BinocularWidget, self).__init__()

        # instantiate adder
        # self.adder = Adder()

        self.__build_ui()

    def __handle_submit(self):
        pass
        # a = self.a_input.text()
        # b = self.b_input.text()
        # result = self.adder.add(a, b)
        # self.output.setText(str(result))

    def __build_ui(self):
        self.__decorate()

        # input fields
        self.__x1_input = self.__q_line_edit('476')
        self.__y1_input = self.__q_line_edit('240')
        self.__x2_input = self.__q_line_edit('276')
        self.__y2_input = self.__q_line_edit('240')

        # output fields
        self.__x_output = self.__q_line_edit('30', False)
        self.__y_output = self.__q_line_edit('0', False)
        self.__z_output = self.__q_line_edit('300', False)
        self.__d_output = self.__q_line_edit('1.2', False)

        # submission
        self.__locate_btn = self.__q_push_button('Locate')

        # output configuration
        self.__m_unit_option = self.__q_radio_button('m')
        self.__cm_unit_option = self.__q_radio_button('cm')
        self.__mm_unit_option = self.__q_radio_button('mm', True)
        self.__ft_unit_option = self.__q_radio_button('ft')
        self.__in_unit_option = self.__q_radio_button('in')

        # layouts
        main_layout = self.__main_layout(
            (self.__x1_input, self.__y1_input),
            (self.__x2_input, self.__y2_input),
            self.__locate_btn,
            self.__x_output,
            self.__y_output,
            self.__z_output,
            self.__d_output,
            (
                self.__m_unit_option,
                self.__cm_unit_option,
                self.__mm_unit_option,
                self.__ft_unit_option,
                self.__in_unit_option
            )
        )

        # actions
        self.__locate_btn.clicked.connect(lambda: self.__handle_submit())

        quit_sc = QShortcut(QKeySequence('Ctrl+Q'), self)
        quit_sc.activated.connect(QApplication.instance().quit)
        
        self.setLayout(main_layout)
        self.show()

    # window manipulation
    def __decorate(self):
        self.setWindowTitle("Binocular - A Computer's Window to the World")
        self.setFixedSize(1360, 800)
        self.move(640, 480)

    # components
    def __q_line_edit(self, text, editable=True):
        qle = QLineEdit(text)
        qle.setTextMargins(8, 8, 8, 8)
        qle.setAlignment(Qt.AlignRight)
        qle.setReadOnly(not editable)
        # qle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return qle

    def __q_push_button(self, text):
        qpb = QPushButton(text)
        # qpb.setStyleSheet('background-color: #8fd485; padding: 1em;')
        qpb.setStyleSheet('QPushButton {'
                          '    border: none;'
                          '    background-color: #8fd485;'
                          '    color: #000;'
                          '    padding: 0.6em;'
                          '    border-radius: 0.4em;'
                          '    width: 40%;'
                          '}'
                          'QPushButton::hover {'
                          '    background-color: #6db263;'
                          '    color: #fff;'
                          '}')
        return qpb

    def __q_radio_button(self, text, checked=False):
        qrb = QRadioButton(text)
        qrb.setChecked(checked)
        qrb.setStyleSheet('QRadioButton {'
                          '    spacing: 0.6em;'
                          '    padding: 0.2em;'
                          '}'
                          'QRadioButton::hover {'
                          '    background-color: #ccc;'
                          '}')
        return qrb

    def __q_label(self, text, wrap=False):
        ql = QLabel(text)
        ql.setWordWrap(wrap)
        return ql

    # layout sections
    def __section_label_layout(self, text='My Section'):
        layout = QHBoxLayout()
        layout.addWidget(self.__q_label(text))
        return layout

    def __line_edit_with_units_layout(self, le, units='units'):
        layout = QHBoxLayout()
        layout.addWidget(le)
        layout.addWidget(self.__q_label(units))
        return layout

    def __centroid_layout(self, xqle, yqle, idx=0):
        idx = str(idx + 1)

        layout = QHBoxLayout()
        layout.addWidget(self.__q_label('x{}:'.format(idx)))
        layout.addLayout(self.__line_edit_with_units_layout(xqle, 'px'))
        layout.addWidget(self.__q_label('y{}:'.format(idx)))
        layout.addLayout(self.__line_edit_with_units_layout(yqle, 'px'))
        return layout

    def __input_layout(self, left_pair, right_pair):
        section_label_layout = self.__section_label_layout('Centroid data:')
        centroid_1_layout = self.__centroid_layout(
            left_pair[0],
            left_pair[1],
            0
        )
        centroid_2_layout = self.__centroid_layout(
            right_pair[0],
            right_pair[1],
            1
        )

        layout = QVBoxLayout()
        layout.addLayout(section_label_layout)
        layout.addLayout(centroid_1_layout)
        layout.addLayout(centroid_2_layout)
        # layout.setSpacing(16)
        return layout

    def __unit_options_layout(self, *qrbs):
        section_label_layout = self.__section_label_layout('Select a unit:')

        radio_button_layout = QVBoxLayout()

        for qrb in qrbs:
            radio_button_layout.addWidget(qrb)

        layout = QVBoxLayout()
        layout.addLayout(section_label_layout)
        layout.addLayout(radio_button_layout)
        layout.setSpacing(16)
        return layout

    def __output_layout(self, xqle, yqle, zqle, dqle):
        section_label_layout = self.__section_label_layout('Results:')

        line_edit_label_layout = QVBoxLayout()
        line_edit_label_layout.addWidget(self.__q_label('X:'))
        line_edit_label_layout.addWidget(self.__q_label('Y:'))
        line_edit_label_layout.addWidget(self.__q_label('Z:'))
        line_edit_label_layout.addWidget(self.__q_label('Disparity:'))

        line_edit_layout = QVBoxLayout()
        line_edit_layout.addLayout(
            self.__line_edit_with_units_layout(xqle, 'mm')
        )
        line_edit_layout.addLayout(
            self.__line_edit_with_units_layout(yqle, 'mm')
        )
        line_edit_layout.addLayout(
            self.__line_edit_with_units_layout(zqle, 'mm')
        )
        line_edit_layout.addLayout(
            self.__line_edit_with_units_layout(dqle, 'mm')
        )

        layout = QGridLayout()
        layout.addLayout(section_label_layout, 0, 0, 1, 2)
        layout.addLayout(line_edit_label_layout, 1, 0)
        layout.addLayout(line_edit_layout, 1, 1)
        layout.setSpacing(16)
        return layout

    def __submit_button_layout(self, qpb):
        layout = QHBoxLayout()
        layout.addWidget(qpb)
        return layout

    def __instructions_layout(self):
        section_label_layout = self.__section_label_layout('Instructions:')
        layout = QVBoxLayout()
        layout.addLayout(section_label_layout)
        layout.addWidget(self.__q_label('Binocular vision gives us the'
            ' ability to see an object from two perspectives. Using these'
            ' principles, we can teach a computer the concept of "depth" with'
            ' some basic mathematics. Enter the X and Y coordinates of a point'
            ' in space from two 2D perspectives. The results can be converted'
            ' on the fly using the radio buttons.', True))
        return layout

    def __lhs_layout(self, left_pair, right_pair, locate_btn):
        layout = QVBoxLayout()
        layout.addLayout(self.__input_layout(left_pair, right_pair))
        layout.addLayout(self.__submit_button_layout(locate_btn))
        layout.addLayout(self.__instructions_layout())
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 16, 0)
        return layout

    def __rhs_layout(self, xqle, yqle, zqle, dqle, qrbs):
        layout = QVBoxLayout()
        layout.addLayout(self.__output_layout(xqle, yqle, zqle, dqle))
        layout.addLayout(self.__unit_options_layout(*qrbs))
        layout.setContentsMargins(16, 0, 0, 0)
        return layout

    def __main_layout(
        self,
        left_pair,
        right_pair,
        locate_btn,
        xqle,
        yqle,
        zqle,
        dqle,
        qrbs
    ):
        layout = QHBoxLayout()
        layout.addLayout(self.__lhs_layout(left_pair, right_pair, locate_btn))
        layout.addLayout(self.__rhs_layout(xqle, yqle, zqle, dqle, qrbs))
        layout.setContentsMargins(64, 64, 64, 64)
        layout.setSpacing(32)
        return layout

def main():
    app = QApplication(sys.argv)
    binocularWidget = BinocularWidget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()