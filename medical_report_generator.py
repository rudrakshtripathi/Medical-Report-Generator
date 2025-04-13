import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import random
from fpdf import FPDF
import qrcode
import os

class MedicalReportGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Report Generator")
        self.root.geometry("900x1050")
        self.init_databases()
        self.setup_ui()

    def init_databases(self):
        self.hospitals = [
            {"name": "Dr. Lal PathLabs", "address": "Block E, Sector 18, Rohini, New Delhi 110085", "website": "www.lalpathlab.com", "cin": "1748990L1999PLQ06538B"},
            {"name": "Metropolis Healthcare", "address": "34, Industrial Area, Sion, Mumbai 400022", "website": "www.metropolisindia.com", "cin": "U85100MH2000PLC128045"}
        ]
        self.doctors = [
            {"name": "Dr. Baksh Choudhry", "qualification": "MD, Pathology", "designation": "Consultant Pathologist"},
            {"name": "Dr. A. Sharma", "qualification": "MD, Biochemistry", "designation": "Senior Pathologist"}
        ]
        self.tests = {
            "diabetes": {
                "name": "GLUCOSE TESTING",
                "parameters": [
                    {"name": "Glucose Fasting", "unit": "mg/dL", "range": "70-100"},
                    {"name": "Glucose Postprandial", "unit": "mg/dL", "range": "<140"}
                ],
                "notes": ["Fasting glucose ≥126 mg/dL suggests diabetes", "Postprandial glucose ≥200 mg/dL suggests diabetes"]
            },
            "headache": {
                "name": "HEADACHE PANEL",
                "parameters": [
                    {"name": "Blood Pressure", "unit": "mmHg", "range": "90/60-120/80"},
                    {"name": "Hemoglobin", "unit": "g/dL", "range": "12-16"}
                ],
                "notes": ["Severe headache with high BP requires immediate attention", "Consider migraine if recurrent headaches"]
            },
            "fever": {
                "name": "FEVER PROFILE",
                "parameters": [
                    {"name": "WBC Count", "unit": "cells/μL", "range": "4000-11000"},
                    {"name": "CRP", "unit": "mg/L", "range": "<5"}
                ],
                "notes": ["Viral infection likely if WBC normal or low", "Bacterial infection likely if WBC elevated"]
            }
        }
        self.collection_centers = ["Main Lab", "City Branch", "Town Center"]
        self.test_var = tk.StringVar()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # UI Elements
        ttk.Label(self.scrollable_frame, text="Medical Report Generator", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.scrollable_frame, text="Patient Name:").grid(row=1, column=0, sticky="w")
        self.name_entry = ttk.Entry(self.scrollable_frame)
        self.name_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(self.scrollable_frame, text="Age:").grid(row=2, column=0, sticky="w")
        self.age_entry = ttk.Entry(self.scrollable_frame)
        self.age_entry.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Label(self.scrollable_frame, text="Gender:").grid(row=3, column=0, sticky="w")
        self.gender_var = tk.StringVar()
        ttk.Radiobutton(self.scrollable_frame, text="Male", variable=self.gender_var, value="Male").grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(self.scrollable_frame, text="Female", variable=self.gender_var, value="Female").grid(row=3, column=1)

        ttk.Label(self.scrollable_frame, text="Select Test:").grid(row=4, column=0, sticky="w", pady=(15,5))
        test_options = ["Diabetes Screening", "Headache Evaluation", "Fever Profile"]
        self.test_combo = ttk.Combobox(self.scrollable_frame, textvariable=self.test_var, values=test_options)
        self.test_combo.grid(row=4, column=1, sticky="ew", pady=(15,5))

        ttk.Label(self.scrollable_frame, text="Bed Rest Days:").grid(row=5, column=0, sticky="w")
        self.rest_entry = ttk.Entry(self.scrollable_frame)
        self.rest_entry.grid(row=5, column=1, sticky="ew", pady=5)

        ttk.Button(self.scrollable_frame, text="Generate Report", command=self.generate_report).grid(row=6, column=0, columnspan=2, pady=10)

        self.report_text = tk.Text(self.scrollable_frame, height=25, width=90, wrap=tk.WORD, font=("Courier", 9))
        self.report_text.grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Button(self.scrollable_frame, text="Save as PDF", command=self.save_as_pdf).grid(row=8, column=0, columnspan=2, pady=10)

    def generate_test_value(self, range_str):
        if "/" in range_str and "-" in range_str:
            low_part, high_part = range_str.split("-")
            low_sys, low_dia = map(int, low_part.split("/"))
            high_sys, high_dia = map(int, high_part.split("/"))
            return f"{random.randint(low_sys, high_sys)}/{random.randint(low_dia, high_dia)}"
        elif "-" in range_str:
            low, high = map(float, range_str.split("-"))
            return round(random.uniform(low, high), 1)
        elif range_str.startswith("<"):
            max_val = float(range_str[1:])
            return round(random.uniform(max_val * 0.7, max_val * 0.95), 1)
        return range_str

    def generate_report(self):
        try:
            if not self.name_entry.get():
                raise ValueError("Please enter patient name")
            if not self.age_entry.get().isdigit():
                raise ValueError("Please enter valid age")
            if not self.gender_var.get():
                raise ValueError("Please select gender")
            if not self.test_var.get():
                raise ValueError("Please select a test")

            test_map = {
                "Diabetes Screening": "diabetes",
                "Headache Evaluation": "headache",
                "Fever Profile": "fever"
            }
            test_key = test_map.get(self.test_var.get())
            test_data = self.tests.get(test_key, {})

            self.hospital = random.choice(self.hospitals)
            self.doctor = random.choice(self.doctors)
            self.lab_no = f"LAB{random.randint(100000, 999999)}"
            self.collected_date = datetime.now().strftime("%d/%m/%Y %I:%M %p")
            self.reported_date = (datetime.now() + timedelta(hours=2)).strftime("%d/%m/%Y %I:%M %p")

            self.results = []
            for param in test_data.get("parameters", []):
                value = self.generate_test_value(param["range"])
                self.results.append({
                    "name": param["name"],
                    "value": value,
                    "unit": param["unit"],
                    "range": param["range"]
                })

            rest_days = self.rest_entry.get().strip()
            self.rest_days = rest_days if rest_days.isdigit() else "Not specified"

            report = f"""
{'='*90}
{self.hospital['name'].upper():^90}
{'Address: ' + self.hospital['address']:^90}
{'='*90}

Patient: {self.name_entry.get().upper()}
Age: {self.age_entry.get()} | Gender: {self.gender_var.get()}
Lab #: {self.lab_no} | Collected: {self.collected_date}
Reported: {self.reported_date}
Bed Rest Recommended: {self.rest_days} Days

{'Test Results':^90}
{'='*90}
{test_data['name']:^90}
{'='*90}
{'Test':<40}| {'Result':<15}| {'Range':<30}
{'-'*90}"""
            for result in self.results:
                report += f"\n{result['name']:<40}| {result['value']:<15}| {result['range']:<30}"

            report += f"\n\n{'Notes:':^90}\n"
            for note in test_data.get("notes", []):
                report += f"- {note}\n"

            report += f"""
{'='*90}
{'Physician: ' + self.doctor['name']:>90}
{'='*90}
{'FOR EDUCATIONAL PURPOSES ONLY':^90}
{'='*90}"""

            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, report)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_as_pdf(self):
        if not self.report_text.get(1.0, tk.END).strip():
            messagebox.showerror("Error", "No report to save")
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVu", size=9)

            for line in self.report_text.get(1.0, tk.END).split("\n"):
                pdf.multi_cell(0, 5, txt=line)

            # Generate and insert QR Code
            qr_data = f"{self.name_entry.get().upper()} | {self.lab_no}"
            qr_img = qrcode.make(qr_data)
            qr_filename = "qr_temp.png"
            qr_img.save(qr_filename)
            pdf.image(qr_filename, x=160, y=10, w=40)
            os.remove(qr_filename)

            filename = f"Medical_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(filename)
            messagebox.showinfo("Success", f"Report saved as {filename}")

            if os.name == 'nt':
                os.startfile(filename)
            else:
                os.system(f"xdg-open '{filename}'")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalReportGenerator(root)
    root.mainloop()
