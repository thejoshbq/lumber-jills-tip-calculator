# Lumber Jill's Tip Calculator

**Lumber Jill's Tip Calculator** is a standalone desktop application designed for Lumber Jill's Axe Throwing Lounge to calculate and distribute tips among employees based on timecard data from CSV or Excel files. Built with Python and PySide6, it offers a modern, user-friendly interface with a dark theme, supporting three tip-splitting methods: Daily Percentage, Even Split, and Custom Split.

## Features

- **File Import**: Load timecard data from multiple `.csv`, `.xlsx`, or `.xls` files.
- **Tip Splitting Methods**:
  - **Daily Percentage**: Distributes tips daily based on hours worked.
  - **Even Split**: Divides total tips evenly among employees (excluding "Jill Forbes").
  - **Custom Split**: Allows manual tip allocation with real-time remaining tip tracking.
- **Tabbed Interface**: Displays detailed daily output and summary data in separate tabs.
- **Modern UI**: Dark-themed interface with customizable button sizes and (optional) icons.
- **Cross-Platform**: Runs on Windows, macOS, and Linux as a standalone executable.

## Using the Prebuilt Executable

1. **Download**: Obtain the executable from the Releases page (e.g., lumberjills-tipper.exe for Windows or LJ's Tipper.app for macOS).
2. **Run**: Double-click the executable file to launch the application. Ensure the assets folder with lumberjillslogo.png is in the same directory as the executable.

## Usage

1. **Launch the Application**:
    - Open `Lumber Jill's Tip Calculator` via the executable.
2. **Select Timecard Files**:
    - Click the "Select Timecard Files" button.
    - Choose one or more `.csv`, `.xlsx`, or `.xls` files containing timecard data with columns: `First name`, `Last name`, `Regular hours`, and `Transaction tips`.
3. **Calculate Tips**:
    - Click "CALCULATE TIPS" to process the selected files.
    - The "Detailed Daily Output" tab will display individual daily tip allocations.
4. **Choose a Tip Splitting Method**:
    - Use the radio buttons to select:
        - **Daily Percentage**: View total hours and tips per employee in the "Summary" tab.
        - **Even Split**: See an even distribution of total tips (excluding "Jill Forbes") in the "Summary" tab.
        - **Custom Split**: Manually allocate tips using input boxes in the "Summary" tab, with real-time tracking of remaining tips.
    - Switch methods anytime to update the "Summary" tab dynamically.
5. **Review Results**:
    - Toggle between the "Summary" and "Detailed Daily Output" tabs to analyze tip distributions.

## File Format

Timecard files should include the following columns:

- `First name`: Employee’s first name.
- `Last name`: Employee’s last name.
- `Regular hours`: Hours worked per day.
- `Transaction tips`: Tips earned per day (can include $ or , symbols, which are automatically removed).

## Example File Name Format

- `timecard_2023-10-01.csv`: The date is extracted from the filename (e.g., `2023-10-01`) for daily tip tracking.

## Troubleshooting

- `No Data Displayed`: Ensure your timecard files match the required format and are not empty.
- `Missing Logo`: Verify the assets/lumberjillslogo.png file is included in the same directory as the executable or source file.
- `Errors on Startup`: Check the terminal (if running from source) for missing dependencies or file access issues.

<br><br>
<div style="text-align: center; padding: 10px;">
  <h2>Copyright & License</h2>
  <p>© 2025 LogisTech. All rights reserved.</p>
  <p>This project is licensed under the <a href="https://github.com/LogisTechLLC/REACHER-Suite?tab=MIT-1-ov-file"><strong>LICENSE</strong></a>.</p>
  <p>For more information, please contact the author at <a href="mailto:thejoshbq@proton.me"><i>thejoshbq@proton.me</i></a>
</div>

<div style="text-align: center; padding: 10px; background-color: #333; color: white;">
    <p><i>"The heavens declare the glory of God, and the sky above proclaims his handiwork."</i>
    <p>Psalm 19:1</p>
</div>
