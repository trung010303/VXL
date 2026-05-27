#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAX30102 - SCRIPT TONG HOP
Chi can chay 1 lan la xong tat ca phan tich, so sanh, danh gia, ve bieu do
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

print("\n" + "="*80)
print(" "*15 + "MAX30102 - PHAN TICH VA DANH GIA TONG HOP")
print(" "*15 + "Chi can chay 1 lan la xong tat ca!")
print("="*80)

# ========================================================================
# PHAN 1: KIEM TRA VA DOC DU LIEU
# ========================================================================
print("\n[PHAN 1] Kiem tra va doc du lieu...")

files_needed = ["max30102_test_1.csv", "max30102_test_2.csv", "reference_data.csv"]

for f in files_needed:
    if not os.path.exists(f):
        print(f"LOI: Khong tim thay {f}")
        print(f"Thu muc hien tai: {os.getcwd()}")
        exit(1)

try:
    df1 = pd.read_csv("max30102_test_1.csv")
    df2 = pd.read_csv("max30102_test_2.csv")
    ref = pd.read_csv("reference_data.csv")
    print(f"  OK - max30102_test_1.csv: {len(df1)} mau")
    print(f"  OK - max30102_test_2.csv: {len(df2)} mau")
    print(f"  OK - reference_data.csv: {len(ref)} mau")
except Exception as e:
    print(f"LOI doc file: {e}")
    exit(1)

# ========================================================================
# PHAN 2: TINH TOAN THONG KE
# ========================================================================
print("\n[PHAN 2] Tinh toan thong ke...")

# HR (BPM)
hr1_data = df1[(df1['Valid']==1) & (df1['HR_bpm'] > 0)]['HR_bpm']
hr2_data = df2[(df2['Valid']==1) & (df2['HR_bpm'] > 0)]['HR_bpm']

# SpO2
sp1_data = df1[(df1['Valid']==1) & (df1['SpO2_percent'] > 0)]['SpO2_percent']
sp2_data = df2[(df2['Valid']==1) & (df2['SpO2_percent'] > 0)]['SpO2_percent']

# Tham chieu
ref_hr = ref['Reference_BPM'].mean()
ref_sp = ref['Reference_SpO2'].mean()

# Gia tri test
hr1_mean = hr1_data.mean()
hr1_std = hr1_data.std()
hr2_mean = hr2_data.mean()
hr2_std = hr2_data.std()

sp1_mean = sp1_data.mean()
sp1_std = sp1_data.std()
sp2_mean = sp2_data.mean()
sp2_std = sp2_data.std()

# Sai so
error_hr1 = abs(hr1_mean - ref_hr)
error_hr2 = abs(hr2_mean - ref_hr)
error_sp1 = abs(sp1_mean - ref_sp)
error_sp2 = abs(sp2_mean - ref_sp)

# PASS/FAIL
test1_hr_pass = error_hr1 <= 5
test2_hr_pass = error_hr2 <= 5
test1_sp_pass = error_sp1 <= 2
test2_sp_pass = error_sp2 <= 2

print(f"  OK - Tinh toan xong!")

# ========================================================================
# PHAN 3: IN KET QUA CHI TIET
# ========================================================================
print("\n" + "="*80)
print("KET QUA PHAN TICH")
print("="*80)

print(f"\n1. NHIP TIM (BPM):")
print(f"   Test 1:        {hr1_mean:.1f} +/- {hr1_std:.2f} BPM")
print(f"   Test 2:        {hr2_mean:.1f} +/- {hr2_std:.2f} BPM")
print(f"   Tham chieu:    {ref_hr:.1f} BPM")
print(f"")
print(f"   Test 1 vs Tham chieu:")
print(f"     Sai so: +/- {error_hr1:.1f} BPM")
print(f"     Do chinh xac: {100 - (error_hr1/ref_hr*100):.1f}%")
print(f"     {'PASS ->' if test1_hr_pass else 'FAIL ->'} {'Dat tieu chuan' if test1_hr_pass else 'Khong dat'}")
print(f"")
print(f"   Test 2 vs Tham chieu:")
print(f"     Sai so: +/- {error_hr2:.1f} BPM")
print(f"     Do chinh xac: {100 - (error_hr2/ref_hr*100):.1f}%")
print(f"     {'PASS ->' if test2_hr_pass else 'FAIL ->'} {'Dat tieu chuan' if test2_hr_pass else 'Khong dat'}")

print(f"\n2. OXYBOA MAU (SpO2):")
print(f"   Test 1:        {sp1_mean:.2f} +/- {sp1_std:.3f}%")
print(f"   Test 2:        {sp2_mean:.2f} +/- {sp2_std:.3f}%")
print(f"   Tham chieu:    {ref_sp:.2f}%")
print(f"")
print(f"   Test 1 vs Tham chieu:")
print(f"     Sai so: +/- {error_sp1:.2f}%")
print(f"     Do chinh xac: {100 - (error_sp1/ref_sp*100):.2f}%")
print(f"     {'PASS ->' if test1_sp_pass else 'FAIL ->'} {'Dat tieu chuan' if test1_sp_pass else 'Khong dat'}")
print(f"")
print(f"   Test 2 vs Tham chieu:")
print(f"     Sai so: +/- {error_sp2:.2f}%")
print(f"     Do chinh xac: {100 - (error_sp2/ref_sp*100):.2f}%")
print(f"     {'PASS ->' if test2_sp_pass else 'FAIL ->'} {'Dat tieu chuan' if test2_sp_pass else 'Khong dat'}")

print(f"\n3. CHAT LUONG DU LIEU:")
valid1 = (df1['Valid']==1).sum() / len(df1) * 100
valid2 = (df2['Valid']==1).sum() / len(df2) * 100
print(f"   Test 1 valid rate: {valid1:.1f}%")
print(f"   Test 2 valid rate: {valid2:.1f}%")

# ========================================================================
# PHAN 4: VE BIEU DO
# ========================================================================
print(f"\n[PHAN 3] Ve bieu do...")

fig, axes = plt.subplots(3, 2, figsize=(14, 10))
fig.suptitle('MAX30102 - Phan tich tong hop', fontsize=16, fontweight='bold')

# HR - Test 1
axes[0, 0].plot(df1['Time_ms']/1000, df1['HR_bpm'], 'o-', color='blue', linewidth=1.5, markersize=5)
axes[0, 0].axhline(y=hr1_mean, color='blue', linestyle='--', alpha=0.7, label=f'Test: {hr1_mean:.1f}')
axes[0, 0].axhline(y=ref_hr, color='red', linestyle='--', alpha=0.7, label=f'Ref: {ref_hr:.1f}')
axes[0, 0].set_title('HR - Test 1', fontweight='bold', fontsize=12)
axes[0, 0].set_ylabel('BPM')
axes[0, 0].legend(fontsize=9)
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_ylim([65, 85])

# HR - Test 2
axes[0, 1].plot(df2['Time_ms']/1000, df2['HR_bpm'], 'o-', color='green', linewidth=1.5, markersize=5)
axes[0, 1].axhline(y=hr2_mean, color='green', linestyle='--', alpha=0.7, label=f'Test: {hr2_mean:.1f}')
axes[0, 1].axhline(y=ref_hr, color='red', linestyle='--', alpha=0.7, label=f'Ref: {ref_hr:.1f}')
axes[0, 1].set_title('HR - Test 2', fontweight='bold', fontsize=12)
axes[0, 1].set_ylabel('BPM')
axes[0, 1].legend(fontsize=9)
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].set_ylim([65, 85])

# SpO2 - Test 1
axes[1, 0].plot(df1['Time_ms']/1000, df1['SpO2_percent'], 'o-', color='red', linewidth=1.5, markersize=5)
axes[1, 0].axhline(y=sp1_mean, color='red', linestyle='--', alpha=0.7, label=f'Test: {sp1_mean:.2f}%')
axes[1, 0].axhline(y=ref_sp, color='blue', linestyle='--', alpha=0.7, label=f'Ref: {ref_sp:.2f}%')
axes[1, 0].set_title('SpO2 - Test 1', fontweight='bold', fontsize=12)
axes[1, 0].set_ylabel('SpO2 (%)')
axes[1, 0].legend(fontsize=9)
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].set_ylim([94, 100])

# SpO2 - Test 2
axes[1, 1].plot(df2['Time_ms']/1000, df2['SpO2_percent'], 'o-', color='orange', linewidth=1.5, markersize=5)
axes[1, 1].axhline(y=sp2_mean, color='orange', linestyle='--', alpha=0.7, label=f'Test: {sp2_mean:.2f}%')
axes[1, 1].axhline(y=ref_sp, color='blue', linestyle='--', alpha=0.7, label=f'Ref: {ref_sp:.2f}%')
axes[1, 1].set_title('SpO2 - Test 2', fontweight='bold', fontsize=12)
axes[1, 1].set_ylabel('SpO2 (%)')
axes[1, 1].legend(fontsize=9)
axes[1, 1].grid(True, alpha=0.3)
axes[1, 1].set_ylim([94, 100])

# IR & Red - Test 1
axes[2, 0].plot(df1['Time_ms']/1000, df1['IR_Value'], 'o-', color='purple', linewidth=1.5, markersize=4, alpha=0.7, label='IR')
axes[2, 0].plot(df1['Time_ms']/1000, df1['Red_Value'], 's-', color='brown', linewidth=1.5, markersize=4, alpha=0.7, label='Red')
axes[2, 0].set_title('IR & Red - Test 1', fontweight='bold', fontsize=12)
axes[2, 0].set_ylabel('ADC Value (LSB)')
axes[2, 0].set_xlabel('Thoi gian (s)')
axes[2, 0].legend(fontsize=9)
axes[2, 0].grid(True, alpha=0.3)

# IR & Red - Test 2
axes[2, 1].plot(df2['Time_ms']/1000, df2['IR_Value'], 'o-', color='purple', linewidth=1.5, markersize=4, alpha=0.7, label='IR')
axes[2, 1].plot(df2['Time_ms']/1000, df2['Red_Value'], 's-', color='brown', linewidth=1.5, markersize=4, alpha=0.7, label='Red')
axes[2, 1].set_title('IR & Red - Test 2', fontweight='bold', fontsize=12)
axes[2, 1].set_ylabel('ADC Value (LSB)')
axes[2, 1].set_xlabel('Thoi gian (s)')
axes[2, 1].legend(fontsize=9)
axes[2, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('MAX30102_FULL_ANALYSIS.png', dpi=150, bbox_inches='tight')
print(f"  OK - Bieu do da luu: MAX30102_FULL_ANALYSIS.png")

try:
    plt.show()
except:
    pass

# ========================================================================
# PHAN 4: DANH GIA VA KET LUAN
# ========================================================================
print("\n" + "="*80)
print("DANH GIA VA KET LUAN")
print("="*80)

print(f"\nTEST 1:")
if test1_hr_pass and test1_sp_pass:
    print(f"  PASSED - Dat tieu chuan cao")
    test1_result = "PASSED"
else:
    print(f"  FAILED - Khong dat tieu chuan")
    test1_result = "FAILED"

print(f"\nTEST 2:")
if test2_hr_pass and test2_sp_pass:
    print(f"  PASSED - Dat tieu chuan cao")
    test2_result = "PASSED"
else:
    print(f"  FAILED - Khong dat tieu chuan")
    test2_result = "FAILED"

print(f"\nTONG QUAN:")
if test1_result == "PASSED" and test2_result == "PASSED":
    print(f"  EXCELLENT - MAX30102 hoat dong tot!")
    overall = "EXCELLENT"
elif test1_result == "PASSED" or test2_result == "PASSED":
    print(f"  GOOD - MAX30102 hoat dong khong xa")
    overall = "GOOD"
else:
    print(f"  FAIR - MAX30102 can cai thien")
    overall = "FAIR"

# ========================================================================
# PHAN 5: LUU KET QUA VAO FILE
# ========================================================================
print(f"\n[PHAN 4] Luu ket qua vao file...")

with open('MAX30102_RESULT.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write(" "*20 + "MAX30102 ANALYSIS REPORT\n")
    f.write("="*80 + "\n\n")
    
    f.write("HEART RATE (BPM)\n")
    f.write("-"*80 + "\n")
    f.write(f"Test 1: {hr1_mean:.1f} BPM\n")
    f.write(f"  vs Reference {ref_hr:.1f} BPM\n")
    f.write(f"  Error: +/- {error_hr1:.1f} BPM ({100 - (error_hr1/ref_hr*100):.1f}% accuracy)\n")
    f.write(f"  {'PASS' if test1_hr_pass else 'FAIL'}\n\n")
    
    f.write(f"Test 2: {hr2_mean:.1f} BPM\n")
    f.write(f"  vs Reference {ref_hr:.1f} BPM\n")
    f.write(f"  Error: +/- {error_hr2:.1f} BPM ({100 - (error_hr2/ref_hr*100):.1f}% accuracy)\n")
    f.write(f"  {'PASS' if test2_hr_pass else 'FAIL'}\n\n")
    
    f.write("OXYGEN SATURATION (SpO2)\n")
    f.write("-"*80 + "\n")
    f.write(f"Test 1: {sp1_mean:.2f}%\n")
    f.write(f"  vs Reference {ref_sp:.2f}%\n")
    f.write(f"  Error: +/- {error_sp1:.2f}% ({100 - (error_sp1/ref_sp*100):.2f}% accuracy)\n")
    f.write(f"  {'PASS' if test1_sp_pass else 'FAIL'}\n\n")
    
    f.write(f"Test 2: {sp2_mean:.2f}%\n")
    f.write(f"  vs Reference {ref_sp:.2f}%\n")
    f.write(f"  Error: +/- {error_sp2:.2f}% ({100 - (error_sp2/ref_sp*100):.2f}% accuracy)\n")
    f.write(f"  {'PASS' if test2_sp_pass else 'FAIL'}\n\n")
    
    f.write("CONCLUSION\n")
    f.write("-"*80 + "\n")
    f.write(f"Test 1: {test1_result}\n")
    f.write(f"Test 2: {test2_result}\n")
    f.write(f"Overall: {overall}\n")

print(f"  OK - Ket qua da luu: MAX30102_RESULT.txt")

# ========================================================================
# KET THUC
# ========================================================================
print("\n" + "="*80)
print(" "*20 + "PHAN TICH HOAN THANH!")
print("="*80)

print(f"\nCac file duoc tao:")
print(f"  1. MAX30102_FULL_ANALYSIS.png - Bieu do")
print(f"  2. MAX30102_RESULT.txt - Ket qua chi tiet")

print(f"\nDanh gia cuoi cung: {overall}")

print("\n" + "="*80 + "\n")

input("Nhan phim bat ky de thoat...")
