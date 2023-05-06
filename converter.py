import sys
from PyQt6 import QtGui, QtWidgets, QtCore
from art import text2art
import requests

class CurrencyConverter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.currencies = ["USD", "EUR", "GBP", "JPY"]
        self.init_ui()
        self.get_exchange_rates()

    def init_ui(self):
        self.setWindowTitle("Currency Converter")
        self.setFixedSize(500, 300)

        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        self.tab_widget = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.converter_tab = QtWidgets.QWidget()
        self.ascii_art_tab = QtWidgets.QWidget()
        self.random_numbers_tab = QtWidgets.QWidget()

        self.tab_widget.addTab(self.converter_tab, "Converter")
        self.tab_widget.addTab(self.ascii_art_tab, "ASCII Art")
        self.tab_widget.addTab(self.random_numbers_tab, "Random Numbers")

        self.favorites_label = QtWidgets.QLabel("Favorite Currencies:")
        self.favorites_dropdown = QtWidgets.QComboBox()
        self.favorites_dropdown.addItems(["None"] + self.currencies)
        self.favorites_dropdown.currentIndexChanged.connect(self.update_favorites)
        main_layout.addWidget(self.favorites_label)
        main_layout.addWidget(self.favorites_dropdown)

        self.setup_converter_tab()
        self.setup_ascii_art_tab()
        self.setup_random_numbers_tab()


    def setup_converter_tab(self):
        grid = QtWidgets.QGridLayout()
        self.converter_tab.setLayout(grid)

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

    def setup_ascii_art_tab(self):
        layout = QtWidgets.QVBoxLayout()
        self.ascii_art_tab.setLayout(layout)

        self.ascii_art_input_label = QtWidgets.QLabel("Enter text:")
        self.ascii_art_input = QtWidgets.QLineEdit()

        self.ascii_art_output_label = QtWidgets.QLabel("ASCII Art:")
        self.ascii_art_output = QtWidgets.QPlainTextEdit()
        self.ascii_art_output.setReadOnly(True)

        self.ascii_art_generate_button = QtWidgets.QPushButton("Generate")
        self.ascii_art_generate_button.clicked.connect(self.generate_ascii_art)

        layout.addWidget(self.ascii_art_input_label)
        layout.addWidget(self.ascii_art_input)
        layout.addWidget(self.ascii_art_output_label)
        layout.addWidget(self.ascii_art_output)
        layout.addWidget(self.ascii_art_generate_button)

    def generate_ascii_art(self):
        input_text = self.ascii_art_input.text()
        if input_text:
            try:
                ascii_art = text2art(input_text)
                self.ascii_art_output.setPlainText(ascii_art)
            except Exception as e:
                self.ascii_art_output.setPlainText("Error generating ASCII art: {}".format(e))
        else:
            self.ascii_art_output.setPlainText("Please enter text to generate ASCII art.")


    def setup_random_numbers_tab(self):
        layout = QtWidgets.QVBoxLayout()
        self.random_numbers_tab.setLayout(layout)

        self.random_numbers_label = QtWidgets.QLabel("Random numbers:")
        self.random_numbers_text = QtWidgets.QPlainTextEdit()
        self.random_numbers_text.setReadOnly(True)

        self.min_value_label = QtWidgets.QLabel("Minimum value:")
        self.min_value_input = QtWidgets.QLineEdit()
        self.min_value_input.setValidator(QtGui.QIntValidator())

        self.max_value_label = QtWidgets.QLabel("Maximum value:")
        self.max_value_input = QtWidgets.QLineEdit()
        self.max_value_input.setValidator(QtGui.QIntValidator())

        self.generate_button = QtWidgets.QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_random_numbers)

        layout.addWidget(self.min_value_label)
        layout.addWidget(self.min_value_input)
        layout.addWidget(self.max_value_label)
        layout.addWidget(self.max_value_input)
        layout.addWidget(self.random_numbers_label)
        layout.addWidget(self.random_numbers_text)
        layout.addWidget(self.generate_button)


    def generate_random_numbers(self):
        import random
        min_value = int(self.min_value_input.text() or 1)
        max_value = int(self.max_value_input.text() or 100)
        random_numbers = [random.randint(min_value, max_value) for _ in range(9)]
        outlier = random.randint(min_value - 10, max_value + 10)
        random_numbers.append(outlier)
        random.shuffle(random_numbers)
        self.random_numbers_text.setPlainText(", ".join(map(str, random_numbers)))

    def update_favorites(self):
        selected_favorite = self.favorites_dropdown.currentText()
        if selected_favorite != "None":
            self.from_currency_dropdown.clear()
            self.to_currency_dropdown.clear()

            reordered_currencies = [selected_favorite] + [currency for currency in self.currencies if currency != selected_favorite]
            self.from_currency_dropdown.addItems(reordered_currencies)
            self.to_currency_dropdown.addItems(reordered_currencies)
            self.to_currency_dropdown.setCurrentIndex(1)


    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    currency_converter = CurrencyConverter()
    currency_converter.show()
    sys.exit(app.exec())

