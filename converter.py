import sys
from PyQt6 import QtGui, QtWidgets, QtCore
import requests

class CurrencyConverter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.get_exchange_rates()

    def init_ui(self):
        self.setWindowTitle("Currency Converter")
        self.setFixedSize(300, 200)

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        self.amount_label = QtWidgets.QLabel("Amount:")
        self.from_currency_label = QtWidgets.QLabel("From:")
        self.to_currency_label = QtWidgets.QLabel("To:")
        self.result_label = QtWidgets.QLabel("Result:")

        self.amount_input = QtWidgets.QLineEdit()
        self.amount_input.setValidator(QtGui.QDoubleValidator())

        self.from_currency_dropdown = QtWidgets.QComboBox()
        self.to_currency_dropdown = QtWidgets.QComboBox()

        self.result_display = QtWidgets.QLineEdit()
        self.result_display.setReadOnly(True)

        self.convert_button = QtWidgets.QPushButton("Convert")
        self.convert_button.clicked.connect(self.perform_conversion)

        currencies = ["USD", "EUR", "GBP", "JPY"]

        self.from_currency_dropdown.addItems(currencies)
        self.to_currency_dropdown.addItems(currencies)
        self.to_currency_dropdown.setCurrentIndex(1)

        grid.addWidget(self.amount_label, 0, 0)
        grid.addWidget(self.amount_input, 0, 1)
        grid.addWidget(self.from_currency_label, 1, 0)
        grid.addWidget(self.from_currency_dropdown, 1, 1)
        grid.addWidget(self.to_currency_label, 2, 0)
        grid.addWidget(self.to_currency_dropdown, 2, 1)
        grid.addWidget(self.convert_button, 3, 0)
        grid.addWidget(self.result_label, 3, 1)
        grid.addWidget(self.result_display, 4, 1)

    def get_exchange_rates(self):
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            self.exchange_rates = response.json()["rates"]
        except Exception as e:
            print("Error fetching exchange rates:", e)
            self.exchange_rates = {"USD": 1.0, "EUR": 0.85, "GBP": 0.75, "JPY": 110.0}

    def perform_conversion(self):
        amount = float(self.amount_input.text())
        from_currency = self.from_currency_dropdown.currentText()
        to_currency = self.to_currency_dropdown.currentText()

        amount_in_usd = amount / self.exchange_rates[str(from_currency)]
        result = amount_in_usd * self.exchange_rates[str(to_currency)]

        # Bug #1: Incorrect rounding of the result
        self.result_display.setText("{:.4f}".format(result))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    currency_converter = CurrencyConverter()
    currency_converter.show()
    sys.exit(app.exec())

