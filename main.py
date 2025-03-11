import sys
import os
import pandas as pd
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QRadioButton, QButtonGroup, QTableWidget, QTableWidgetItem,
    QHeaderView, QDoubleSpinBox, QTabWidget, QGridLayout
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt

class TipCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LJ's Tipper")
        self.setGeometry(100, 100, 1000, 700)
        self.processed_data = {}
        self.selected_files = []  
        self.employee_inputs = {}
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        logo_path = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(__file__)), 'assets', 'lumberjillslogo.png')
        logo_label = QLabel()
        pixmap = QPixmap(logo_path).scaled(100, 100, Qt.KeepAspectRatio)
        logo_label.setPixmap(pixmap)
        main_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        title_label = QLabel("LJ's Tipper")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        self.file_button = QPushButton("Select Timecard Files")
        self.file_button.clicked.connect(self.select_files)
        main_layout.addWidget(self.file_button)

        method_layout = QHBoxLayout()
        method_label = QLabel("Tip Splitting Method:")
        method_layout.addWidget(method_label)
        self.method_group = QButtonGroup()
        self.daily_percentage_radio = QRadioButton("Daily Percentage")
        self.even_split_radio = QRadioButton("Even Split")
        self.custom_split_radio = QRadioButton("Custom Split")
        self.method_group.addButton(self.daily_percentage_radio, 1)
        self.method_group.addButton(self.even_split_radio, 2)
        self.method_group.addButton(self.custom_split_radio, 3)
        method_layout.addWidget(self.daily_percentage_radio)
        method_layout.addWidget(self.even_split_radio)
        method_layout.addWidget(self.custom_split_radio)
        self.daily_percentage_radio.setChecked(True)
        self.method_group.buttonClicked.connect(self.update_summary_ui)  
        main_layout.addLayout(method_layout)

        self.calculate_button = QPushButton("CALCULATE TIPS")
        self.calculate_button.clicked.connect(self.calculate_tips)
        main_layout.addWidget(self.calculate_button)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        self.summary_widget = QWidget()
        self.summary_layout = QVBoxLayout(self.summary_widget)
        self.summary_label = QLabel("Summary")
        self.summary_layout.addWidget(self.summary_label)
        self.tabs.addTab(self.summary_widget, "Summary")

        self.output_widget = QWidget()
        output_layout = QVBoxLayout(self.output_widget)
        self.output_table = QTableWidget()
        self.output_table.setColumnCount(4)
        self.output_table.setHorizontalHeaderLabels(["Date", "Employee", "Hours", "Tip for the Day"])
        self.output_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        output_layout.addWidget(self.output_table)
        self.tabs.addTab(self.output_widget, "Detailed Daily Output")

        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #2b2b2b; color: #ffffff; }
            QPushButton { background-color: #4a4a4a; border: 1px solid #646464; padding: 5px; }
            QPushButton:hover { background-color: #5a5a5a; }
            QRadioButton, QLabel { color: #ffffff; }
            QTableWidget { background-color: #3a3a3a; color: #ffffff; }
            QHeaderView::section { background-color: #4a4a4a; color: #ffffff; }
        """)

        self.update_summary_ui()  

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Timecard Files", "", "CSV and Excel files (*.csv *.xlsx *.xls)")
        if files:
            self.selected_files = files
            self.processed_data = {}
            self.update_output()
            self.update_summary_ui()

    def process_files(self, files):
        self.processed_data = {
            "daily_tips": [],
            "total_tips": 0,
            "employees": set(),
        }
        for file in files:
            filename = os.path.basename(file)
            try:
                if filename.endswith('.csv'):
                    data = pd.read_csv(file)
                elif filename.endswith(('.xlsx', '.xls')):
                    data = pd.read_excel(file)
                else:
                    continue
            except Exception as e:
                self.show_message(f"Error processing {filename}: {e}")
                continue

            data['Transaction tips'] = data['Transaction tips'].replace(r'[\$,]', '', regex=True).astype(float)

            try:
                tips = data['Transaction tips'].sum()
                total_hours = data['Regular hours'].sum()
            except Exception as e:
                self.show_message(f"Error processing {filename}: {e}")
                continue

            try:
                date = filename.split('_')[1].split('.')[0]
            except IndexError:
                date = "Unknown"

            for _, row in data.iterrows():
                employee_name = f"{row['First name']} {row['Last name']}"
                hours = row['Regular hours']
                cut = (hours / total_hours) * tips if total_hours > 0 else 0.0

                tip_daily = {
                    'Date': date,
                    'Employee': employee_name,
                    'Hours': hours,
                    'Tip for the Day': round(cut, 2)
                }
                self.processed_data["daily_tips"].append(tip_daily)
                self.processed_data["employees"].add(employee_name)
                self.processed_data["total_tips"] += cut

        self.update_output()

    def calculate_tips(self):
        if not self.selected_files:
            self.show_message("Please select at least one file.")
            return
        self.process_files(self.selected_files)
        self.update_summary_ui()

    def update_summary_ui(self):
        while self.summary_layout.count() > 1:
            item = self.summary_layout.takeAt(1)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if not self.selected_files:
            self.show_message("Please select files.")
        elif not self.processed_data:
            self.show_message("Please click 'CALCULATE TIPS' to process.")
        else:
            method = self.method_group.checkedButton().text()
            if method == "Daily Percentage":
                df = pd.DataFrame(self.processed_data["daily_tips"])
                df_summary = df.groupby("Employee", as_index=False)[["Hours", "Tip for the Day"]].sum()
                self.summary_table = QTableWidget()
                self.summary_table.setColumnCount(3)
                self.summary_table.setHorizontalHeaderLabels(["Employee", "Total Hours", "Total Tips"])
                self.summary_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.display_summary(df_summary, ["Employee", "Total Hours", "Total Tips"])
                self.summary_layout.addWidget(self.summary_table)
            elif method == "Even Split":
                total_tips = self.processed_data["total_tips"]
                eligible_employees = [emp for emp in self.processed_data["employees"] if emp != "Jill Forbes"]
                if eligible_employees:
                    even_share = total_tips / len(eligible_employees)
                    even_split_df = pd.DataFrame({
                        "Employee": eligible_employees,
                        "Tip Share": [round(even_share, 2)] * len(eligible_employees)
                    })
                    self.summary_table = QTableWidget()
                    self.summary_table.setColumnCount(2)
                    self.summary_table.setHorizontalHeaderLabels(["Employee", "Tip Share"])
                    self.summary_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.display_summary(even_split_df, ["Employee", "Tip Share"])
                    self.summary_layout.addWidget(self.summary_table)
                else:
                    self.show_message("No eligible employees for even split.")
            elif method == "Custom Split":
                custom_widget = QWidget()
                custom_layout = QVBoxLayout(custom_widget)
                custom_layout.addWidget(QLabel(f"Total Tips: {self.processed_data['total_tips']:.2f}"))
                self.remaining_label = QLabel(f"Remaining Tips: {self.processed_data['total_tips']:.2f}")
                custom_layout.addWidget(self.remaining_label)
                grid = QGridLayout()
                self.employee_inputs = {}
                for i, emp in enumerate(self.processed_data["employees"]):
                    label = QLabel(emp)
                    spinbox = QDoubleSpinBox()
                    spinbox.setRange(0, self.processed_data["total_tips"])
                    spinbox.setValue(0)
                    spinbox.valueChanged.connect(self.update_remaining_tips)
                    self.employee_inputs[emp] = spinbox
                    grid.addWidget(label, i, 0)
                    grid.addWidget(spinbox, i, 1)
                custom_layout.addLayout(grid)
                self.summary_layout.addWidget(custom_widget)

    def update_output(self):
        self.output_table.setRowCount(0)
        for row_data in self.processed_data.get("daily_tips", []):
            row = self.output_table.rowCount()
            self.output_table.insertRow(row)
            self.output_table.setItem(row, 0, QTableWidgetItem(row_data['Date']))
            self.output_table.setItem(row, 1, QTableWidgetItem(row_data['Employee']))
            self.output_table.setItem(row, 2, QTableWidgetItem(str(row_data['Hours'])))
            self.output_table.setItem(row, 3, QTableWidgetItem(f"{row_data['Tip for the Day']:.2f}"))

    def display_summary(self, df, headers):
        self.summary_table.setColumnCount(len(headers))
        self.summary_table.setRowCount(0)
        self.summary_table.setHorizontalHeaderLabels(headers)
        for _, row in df.iterrows():
            row_pos = self.summary_table.rowCount()
            self.summary_table.insertRow(row_pos)
            for col, header in enumerate(headers):
                value = row.get(header if header != "Total Tips" else "Tip for the Day", row.get("Tip Share", "N/A"))
                self.summary_table.setItem(row_pos, col, QTableWidgetItem(str(value)))

    def update_remaining_tips(self):
        allocated = sum(spinbox.value() for spinbox in self.employee_inputs.values())
        remaining = self.processed_data["total_tips"] - allocated
        self.remaining_label.setText(f"Remaining Tips: {remaining:.2f}")

    def show_message(self, message):
        while self.summary_layout.count() > 1:
            item = self.summary_layout.takeAt(1)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        label = QLabel(message)
        self.summary_layout.addWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TipCalculatorApp()
    window.show()
    sys.exit(app.exec())