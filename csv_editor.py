import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, 
    QTableWidgetItem, QFileDialog, QVBoxLayout, QWidget, 
    QPushButton, QMessageBox, QInputDialog, QHBoxLayout,
    QLabel, QHeaderView
)
from PyQt6.QtCore import Qt

class CSVEditor(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Editor")
        self.setGeometry(100, 100, 900, 600)
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)
        
        # Add title
        title_label = QLabel("CSV Editor")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #015562; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title_label)
        
        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Buttons
        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.load_csv)
        self.load_button.setMinimumHeight(40)
        button_layout.addWidget(self.load_button)
        
        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)
        self.add_row_button.setMinimumHeight(40)
        button_layout.addWidget(self.add_row_button)

        self.add_column_button = QPushButton("Add Column")
        self.add_column_button.clicked.connect(self.add_column)
        self.add_column_button.setMinimumHeight(40)
        button_layout.addWidget(self.add_column_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        self.save_button.setMinimumHeight(40)
        button_layout.addWidget(self.save_button)
        
        self.layout.addLayout(button_layout)
        
        # Table widget
        self.table_widget = QTableWidget()
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.setAlternatingRowColors(True) #different colors in every row 
        self.layout.addWidget(self.table_widget)
        
        # Status message
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.status_label)
        
        self.df = pd.DataFrame()
        
        # Simple style application
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                color: #333;
            }
            QPushButton {
                background-color: #3d8d99  ;
                color: white;
                border-radius: 4px;
                padding: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #015562  ;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f9f9f9;
                gridline-color: #ddd;
                border: 1px solid #ddd;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        """)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.update_table()
                self.status_label.setText(f"File loaded: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV file: {e}")
                self.status_label.setText("File loading failed")

    def update_table(self):
        self.table_widget.setRowCount(self.df.shape[0])
        self.table_widget.setColumnCount(self.df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(self.df.columns)

        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))

    def save_table_to_dataframe(self):
        for i in range(self.table_widget.rowCount()):
            for j in range(self.table_widget.columnCount()):
                item = self.table_widget.item(i, j)
                if item is not None:
                    self.df.iat[i, j] = item.text()
                else:
                    self.df.iat[i, j] = ""

    def add_row(self):
        if not self.df.empty:
            self.save_table_to_dataframe()
            self.df.loc[len(self.df)] = [""] * self.df.shape[1]
            self.update_table()
            self.status_label.setText("New row added")
        else:
            QMessageBox.warning(self, "Warning", "You need to load a CSV file first.")

    def add_column(self):
        if not self.df.empty:
            self.save_table_to_dataframe()
            column_name, ok = QInputDialog.getText(self, "Add Column", "Enter column name:")
            if ok and column_name:
                self.df[column_name] = [""] * self.df.shape[0]
                self.update_table()
                self.status_label.setText(f"New column added: {column_name}")
            else:
                QMessageBox.warning(self, "Input Error", "Please enter a valid column name.")
        else:
            QMessageBox.warning(self, "Warning", "You need to load a CSV file first.")

    def save(self):
        if self.df.empty:
            QMessageBox.warning(self, "Warning", "No data to save.")
            return
            
        self.save_table_to_dataframe()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.df.to_csv(file_path, index=False)
                QMessageBox.information(self, "Success", "CSV file saved successfully!")
                self.status_label.setText(f"File saved: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save CSV file: {e}")
                self.status_label.setText("File saving failed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CSVEditor()
    window.show()
    sys.exit(app.exec())