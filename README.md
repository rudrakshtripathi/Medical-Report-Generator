# 🏥 Medical Report Generator

A Python-based desktop application to generate realistic medical reports in PDF format using a simple GUI. Built with **Tkinter**, it allows users to enter patient details, diagnoses, and bed rest days. It then generates a professional-looking PDF, including a QR code and Unicode font support.

---

## 📦 Features

- 🖥️ User-friendly GUI using Tkinter
- 📄 Realistic Medical Report PDF generation
- 🔠 Unicode support via `DejaVuSans.ttf`
- 🔳 QR Code embedded in the report for quick reference
- 📅 Automatic timestamped filenames
- 🛏️ Input for bed rest days included in the report
- 💾 Save reports in an organized folder

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/medical-report-generator.git
cd medical-report-generator
```
## 2. Install dependencies
```bash
pip install reportlab qrcode pillow
```
## 3. Add the required font
Download DejaVuSans.ttf from: https://fontlibrary.org/en/font/dejavu-sans
Place the DejaVuSans.ttf file in the project directory (same as the Python script)

4. Run the application
```bash
python medical_report_generator.py
```
## 📂 Project Structure
```bash
medical-report-generator/
├── main.py                 # Main application script
├── DejaVuSans.ttf          # Unicode font (place here)
├── generated_reports/      # Auto-created folder for PDFs
├── screenshots/            # (Optional) UI screenshots
└── README.md               # This file
```
## 🖨️ PDF Output Includes:
  1. Hospital details
  2. Patient name, age, gender
  3. Diagnosis information
  4. Number of bed rest days
  5. QR code for validation
  6. Date and time

## 🛠️ Built With
  1. Python 3
  2. Tkinter
  3. ReportLab
  4. Pillow (PIL)
  4. qrcode

## 📃 License
This project is licensed under the MIT License.

## 🙌 Acknowledgements
  DejaVu Fonts
  Font Library
  ReportLab, Pillow, and QRCode Python libraries

## Created with ❤️ by Rudraksh Tripathi





