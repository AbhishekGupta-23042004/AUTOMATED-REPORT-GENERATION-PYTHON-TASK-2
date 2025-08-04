import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import os

# === Step 1: Load CSV File ===
file_path = "sample_data.csv"
if not os.path.exists(file_path):
    print("❌ Error: 'sample_data.csv' not found.")
    exit()

data = pd.read_csv(file_path)

# === Step 2: Analyze Numeric Data ===
numeric_data = data.select_dtypes(include=['int64', 'float64'])
summary = numeric_data.describe()

# === Step 3: Generate Bar Graph (Marks by Department) ===
avg_marks = data.groupby("Department")["Marks"].mean()
plt.figure(figsize=(6, 4))
avg_marks.plot(kind='bar', color='skyblue')
plt.title("Average Marks per Department")
plt.xlabel("Department")
plt.ylabel("Average Marks")
plt.tight_layout()
graph_file = "marks_by_dept.png"
plt.savefig(graph_file)
plt.close()

# === Step 4: Generate PDF ===
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="Student Performance Report", ln=True, align='C')
pdf.ln(10)

# Summary
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt=f"Total Students: {len(data)}", ln=True)
pdf.cell(200, 10, txt=f"Departments: {', '.join(data['Department'].unique())}", ln=True)
pdf.ln(5)

# === Include Graph ===
pdf.set_font("Arial", 'B', 12)
pdf.cell(200, 10, txt="Average Marks per Department:", ln=True)
pdf.image(graph_file, x=30, w=150)
pdf.ln(10)

# === Column-wise Statistics ===
pdf.set_font("Arial", 'B', 13)
pdf.cell(200, 10, txt="Overall Summary Statistics", ln=True)
pdf.set_font("Arial", size=11)

for column in summary.columns:
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"\nColumn: {column}", ln=True)
    pdf.set_font("Arial", size=11)
    for stat in summary.index:
        value = round(summary[column][stat], 2)
        pdf.cell(200, 8, txt=f"{stat.capitalize()}: {value}", ln=True)
    pdf.ln(2)

# === Step 5: Optional Per Department Section ===
pdf.set_font("Arial", 'B', 13)
pdf.cell(200, 12, txt="Department-wise Student Count", ln=True)

dept_counts = data['Department'].value_counts()
pdf.set_font("Arial", size=11)
for dept, count in dept_counts.items():
    pdf.cell(200, 8, txt=f"{dept}: {count} students", ln=True)

# === Output PDF ===
output_file = "student_report_with_graph.pdf"
pdf.output(output_file)
print(f"✅ PDF Report Generated: {output_file}")
