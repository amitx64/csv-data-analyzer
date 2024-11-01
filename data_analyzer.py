import sys
import pandas as pd
import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QFileDialog,
)

from pyqtgraph import PlotWidget


class DataAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = None
        self.setWindowTitle("Data Analyzer")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QHBoxLayout()

        # Left panel layout
        left_panel = QVBoxLayout()

        # Input for CSV file location
        self.csv_input = QLineEdit(self)
        self.csv_input.setPlaceholderText("CSV file path")
        left_panel.addWidget(self.csv_input, alignment=Qt.AlignLeft)

        # Browse button
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_csv)
        left_panel.addWidget(self.browse_button, alignment=Qt.AlignLeft)

        # Left panel for variable selection
        self.variable_list = QListWidget()
        self.variable_list.setSelectionMode(QListWidget.MultiSelection)
        left_panel.addWidget(
                                QLabel("Select Variables to Plot:"),
                                alignment=Qt.AlignLeft
                            )
        left_panel.addWidget(self.variable_list, alignment=Qt.AlignLeft)

        # Button to plot selected variables
        self.plot_button = QPushButton("Plot Selected Variables")
        self.plot_button.clicked.connect(self.plot_variables)
        left_panel.addWidget(self.plot_button, alignment=Qt.AlignLeft)

        # Button to clear the plot
        self.clear_button = QPushButton("Clear Plot")
        self.clear_button.clicked.connect(self.clear_plot)
        left_panel.addWidget(self.clear_button, alignment=Qt.AlignLeft)

        # Add left panel to the main layout
        main_layout.addLayout(left_panel)

        # Plot area
        self.plot_widget = PlotWidget()
        self.plot_widget.addLegend()  # Add legend for multiple variables
        main_layout.addWidget(self.plot_widget)

        # Set the main widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Mouse event handlers
        self.start_pos = None
        self.rect_item = None

        # Enable grid lines
        self.plot_widget.showGrid(x=True, y=True)

    def browse_csv(self):
        """Open a file dialog to select a CSV file."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if filename:
            self.csv_input.setText(filename)
            self.load_csv()

    def load_csv(self):
        """Load the CSV file and populate variable list."""
        filename = self.csv_input.text()
        try:
            self.data = pd.read_csv(filename)
            self.variable_list.clear()
            # Populate variable list excluding the timestamp column
            self.variable_list.addItems(self.data.columns[1:].tolist())  # Exclude the first column (timestamp)
            print(f"Loaded data from {filename}")
        except Exception as e:
            print(f"Error loading CSV: {e}")

    def plot_variables(self):
        """Plot selected variables."""
        if self.data is None:
            print("No data loaded.")
            return

        selected_items = self.variable_list.selectedItems()
        if not selected_items:
            print("No variable selected.")
            return

        # Clear previous plots
        self.plot_widget.clear()
        self.plot_widget.addLegend()  # Re-add legend for new plots

        # Define colors for each variable
        colors = ['r', 'g', 'b', 'yellow', 'magenta', 'cyan',
                  'orange', 'purple', 'brown', 'pink', 'lime',
                  'teal', 'navy', 'grey', 'violet', 'maroon', 'turquoise',
                  'gold', 'indigo', 'coral']
        color_count = len(colors)

        # Plot each selected variable with different colors
        for index, item in enumerate(selected_items):
            variable_name = item.text()
            color = colors[index % color_count]  # Cycle through colors
            pen = pg.mkPen(color=color, width=2)  # Create a pen with the specified color
            self.plot_widget.plot(
                self.data.index,
                self.data[variable_name],
                pen=pen,
                name=variable_name
            )

        self.plot_widget.setTitle("Value Graph")
        self.plot_widget.setLabel('left', 'Value')
        self.plot_widget.setLabel('bottom', 'Index')

    def clear_plot(self):
        """Clear the plot."""
        self.plot_widget.clear()
        self.plot_widget.setTitle("")


if __name__ == "__main__":
    # Start the application
    app = QApplication(sys.argv)
    analyzer = DataAnalyzer()
    analyzer.show()
    sys.exit(app.exec_())
