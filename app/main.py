# app.py
from openai_client import analyze_cv
from prompts import cv_analysis_prompt
from pdf_reader import read_pdf

cv_text = read_pdf("examples/cv.pdf")

prompt = cv_analysis_prompt(cv_text)
analysis = analyze_cv(prompt)

print("\n=== ANÁLISE DO CURRÍCULO ===\n")
print(analysis)
