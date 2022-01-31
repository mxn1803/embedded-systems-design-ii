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

        # instantiate binocular
        self.__binocular = Binocular()

        self.__build_ui()

    def __handle_submit(self, scalar=1.0):
        x1, y1 = str(self.__x1_input.text()), str(self.__y1_input.text())
        x2, y2 = str(self.__x2_input.text()), str(self.__y2_input.text())
        (x, y, z, d), err = self.__binocular.position((x1, y1), (x2, y2))
        # print (x1, y1), (x2, y2), ' | ', (x, y, z, d), err
        
        if err:
            self.__error_output.setText(str(err))
            self.__x_output.setText('ERR')
            self.__y_output.setText('ERR')
            self.__z_output.setText('ERR')
            self.__d_output.setText('ERR')
        elif (x1, y1) == (x2, y2):
            self.__error_output.setText(str(err))
            self.__x_output.setText('INF')
            self.__y_output.setText('INF')
            self.__z_output.setText('INF')
            self.__d_output.setText('0.0')
        else:
            coord_fmt_str = '{:.3f}' if scalar < 1.0 else '{:.0f}'
            d_fmt_str = '{:.3f}' if scalar < 1.0 else '{:.1f}'
            self.__error_output.setText('Nothing to report.')
            self.__x_output.setText(coord_fmt_str.format(x * scalar))
            self.__y_output.setText(coord_fmt_str.format(y * scalar))
            self.__z_output.setText(coord_fmt_str.format(z * scalar))
            self.__d_output.setText(d_fmt_str.format(d * scalar))

    def __handle_unit_change(self):
        # print self.__x_output_label.text(), self.__y_output_label.text(), self.__z_output_label.text(), self.__d_output_label.text()
        if self.__m_unit_option.isChecked():
            self.__handle_submit(0.001)
            self.__x_output_label.setText('m')
            self.__y_output_label.setText('m')
            self.__z_output_label.setText('m')
            self.__d_output_label.setText('m')
        elif self.__cm_unit_option.isChecked():
            self.__handle_submit(0.1)
            self.__x_output_label.setText('cm')
            self.__y_output_label.setText('cm')
            self.__z_output_label.setText('cm')
            self.__d_output_label.setText('cm')
        elif self.__mm_unit_option.isChecked():
            self.__handle_submit(1.0)
            self.__x_output_label.setText('mm')
            self.__y_output_label.setText('mm')
            self.__z_output_label.setText('mm')
            self.__d_output_label.setText('mm')
        elif self.__ft_unit_option.isChecked():
            self.__handle_submit(0.00328084)
            self.__x_output_label.setText('ft')
            self.__y_output_label.setText('ft')
            self.__z_output_label.setText('ft')
            self.__d_output_label.setText('ft')
        elif self.__in_unit_option.isChecked():
            self.__handle_submit(0.393701)
            self.__x_output_label.setText('in')
            self.__y_output_label.setText('in')
            self.__z_output_label.setText('in')
            self.__d_output_label.setText('in')

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
        self.__error_output = self.__q_line_edit(
            'Hello, there!',
            False,
            Qt.AlignLeft
        )

        # labels
        self.__x_output_label = self.__q_label('mm')
        self.__y_output_label = self.__q_label('mm')
        self.__z_output_label = self.__q_label('mm')
        self.__d_output_label = self.__q_label('mm')

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
            (self.__x_output, self.__x_output_label),
            (self.__y_output, self.__y_output_label),
            (self.__z_output, self.__z_output_label),
            (self.__d_output, self.__d_output_label),
            self.__error_output,
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
        self.__m_unit_option.clicked.connect(
            lambda: self.__handle_unit_change()
        )
        self.__cm_unit_option.clicked.connect(
            lambda: self.__handle_unit_change()
        )
        self.__mm_unit_option.clicked.connect(
            lambda: self.__handle_unit_change()
        )
        self.__ft_unit_option.clicked.connect(
            lambda: self.__handle_unit_change()
        )
        self.__in_unit_option.clicked.connect(
            lambda: self.__handle_unit_change()
        )

        quit_sc = QShortcut(QKeySequence('Ctrl+Q'), self)
        quit_sc.activated.connect(QApplication.instance().quit)
        
        self.setLayout(main_layout)
        self.show()

    # window manipulation
    def __decorate(self):
        self.setWindowTitle("Binocular - A Computer's Window to the World")
        # self.setFixedSize(1360, 800)
        self.move(640, 480)

    # components
    def __q_line_edit(self, text, editable=True, alignment=Qt.AlignRight):
        qle = QLineEdit(text)
        qle.setTextMargins(8, 8, 8, 8)
        qle.setAlignment(alignment)
        qle.setReadOnly(not editable)
        return qle

    def __q_push_button(self, text):
        qpb = QPushButton(text)
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

        # print xqle[1].text()

        line_edit_layout = QVBoxLayout()
        line_edit_layout.addLayout(
            self.__line_edit_with_units_layout(xqle[0], xqle[1].text())
        )
        line_edit_layout.addLayout(
            self.__line_edit_with_units_layout(yqle[0], yqle[1].text())
        )
        line_edit_layout.addLayout(
            self.__line_edit_with_units_layout(zqle[0], zqle[1].text())
        )
        line_edit_layout.addLayout(
            self.__line_edit_with_units_layout(dqle[0], dqle[1].text())
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

    def __lhs_layout(self, left_pair, right_pair, locate_btn, eqle):
        layout = QVBoxLayout()
        layout.addLayout(self.__input_layout(left_pair, right_pair))
        layout.addLayout(self.__submit_button_layout(locate_btn))
        # layout.addLayout(self.__instructions_layout())
        layout.addWidget(eqle)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 16, 0)
        return layout

    def __rhs_layout(self, xqle, yqle, zqle, dqle, qrbs):
        layout = QVBoxLayout()
        layout.addLayout(self.__output_layout(xqle, yqle, zqle, dqle))
        # layout.addLayout(self.__unit_options_layout(*qrbs))
        layout.setAlignment(Qt.AlignTop)
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
        eqle,
        qrbs
    ):
        layout = QHBoxLayout()
        layout.addLayout(
            self.__lhs_layout(left_pair, right_pair, locate_btn, eqle)
        )
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