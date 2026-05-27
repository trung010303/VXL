#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PHAN TICH NANG CAO - Correlation + ANOVA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

print("\n" + "="*80)
print(" "*15 + "PHAN TICH NANG CAO - CORRELATION + ANOVA")
print("="*80)

# ===== DOC DU LIEU =====
print("\n[1/3] Doc du lieu...")
df1 = pd.read_csv("max30102_test_1.csv")
df2 = pd.read_csv("max30102_test_2.csv")
ref = pd.read_csv("reference_data.csv")
print("  OK - Doc xong!")

# ===== PHAN 1: CORRELATION ANALYSIS =====
print("\n" + "="*80)
print("PHAN 1: PHAN TICH TUONG QUAN (CORRELATION)")
print("="*80)

print("\n[2/3] Tinh correlation...")

# Correlation trong Test 1
corr_ir_red_1 = df1['IR_Value'].corr(df1['Red_Value'])
corr_hr_spo2_1 = df1[(df1['HR_bpm'] > 0) & (df1['SpO2_percent'] > 0)]['HR_bpm'].corr(
    df1[(df1['HR_bpm'] > 0) & (df1['SpO2_percent'] > 0)]['SpO2_percent'])
corr_time_hr_1 = df1[(df1['HR_bpm'] > 0)]['Time_ms'].corr(df1[(df1['HR_bpm'] > 0)]['HR_bpm'])

# Correlation trong Test 2
corr_ir_red_2 = df2['IR_Value'].corr(df2['Red_Value'])
corr_hr_spo2_2 = df2[(df2['HR_bpm'] > 0) & (df2['SpO2_percent'] > 0)]['HR_bpm'].corr(
    df2[(df2['HR_bpm'] > 0) & (df2['SpO2_percent'] > 0)]['SpO2_percent'])
corr_time_hr_2 = df2[(df2['HR_bpm'] > 0)]['Time_ms'].corr(df2[(df2['HR_bpm'] > 0)]['HR_bpm'])

print(f"\nTEST 1:")
print(f"  IR vs Red:    {corr_ir_red_1:.4f}")
print(f"    -> {'Rat manh (>0.9)' if abs(corr_ir_red_1) > 0.9 else 'Manh (0.7-0.9)' if abs(corr_ir_red_1) > 0.7 else 'Trung binh' if abs(corr_ir_red_1) > 0.5 else 'Yeu'}")
print(f"  HR vs SpO2:   {corr_hr_spo2_1:.4f}")
print(f"    -> {'Rat manh (>0.9)' if abs(corr_hr_spo2_1) > 0.9 else 'Manh (0.7-0.9)' if abs(corr_hr_spo2_1) > 0.7 else 'Trung binh' if abs(corr_hr_spo2_1) > 0.5 else 'Yeu'}")
print(f"  Thoi gian vs HR: {corr_time_hr_1:.4f}")
print(f"    -> {'Rat manh (>0.9)' if abs(corr_time_hr_1) > 0.9 else 'Manh (0.7-0.9)' if abs(corr_time_hr_1) > 0.7 else 'Trung binh' if abs(corr_time_hr_1) > 0.5 else 'Yeu'}")

print(f"\nTEST 2:")
print(f"  IR vs Red:    {corr_ir_red_2:.4f}")
print(f"    -> {'Rat manh (>0.9)' if abs(corr_ir_red_2) > 0.9 else 'Manh (0.7-0.9)' if abs(corr_ir_red_2) > 0.7 else 'Trung binh' if abs(corr_ir_red_2) > 0.5 else 'Yeu'}")
print(f"  HR vs SpO2:   {corr_hr_spo2_2:.4f}")
print(f"    -> {'Rat manh (>0.9)' if abs(corr_hr_spo2_2) > 0.9 else 'Manh (0.7-0.9)' if abs(corr_hr_spo2_2) > 0.7 else 'Trung binh' if abs(corr_hr_spo2_2) > 0.5 else 'Yeu'}")
print(f"  Thoi gian vs HR: {corr_time_hr_2:.4f}")
print(f"    -> {'Rat manh (>0.9)' if abs(corr_time_hr_2) > 0.9 else 'Manh (0.7-0.9)' if abs(corr_time_hr_2) > 0.7 else 'Trung binh' if abs(corr_time_hr_2) > 0.5 else 'Yeu'}")

print(f"\nGhi chu:")
print(f"  Correlation range: -1.0 (dao chieu) -> 0 (khong lien quan) -> 1.0 (tuyen tinh)")
print(f"  > 0.7 = Manh")
print(f"  0.5 - 0.7 = Trung binh")
print(f"  < 0.5 = Yeu")

# ===== VE BIEU DO CORRELATION =====
print(f"\n[Dang ve bieu do correlation...]")

# Scatter plot IR vs Red - Test 1
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('PHAN TICH TUONG QUAN (CORRELATION)', fontsize=16, fontweight='bold')

# IR vs Red Test 1
axes[0, 0].scatter(df1['IR_Value'], df1['Red_Value'], alpha=0.6, s=50, color='purple')
z1 = np.polyfit(df1['IR_Value'], df1['Red_Value'], 1)
p1 = np.poly1d(z1)
axes[0, 0].plot(df1['IR_Value'], p1(df1['IR_Value']), "r--", linewidth=2)
axes[0, 0].set_title(f'IR vs Red (Test 1)\nCorrelation: {corr_ir_red_1:.4f}', fontweight='bold')
axes[0, 0].set_xlabel('IR Signal (LSB)')
axes[0, 0].set_ylabel('Red Signal (LSB)')
axes[0, 0].grid(True, alpha=0.3)

# IR vs Red Test 2
axes[0, 1].scatter(df2['IR_Value'], df2['Red_Value'], alpha=0.6, s=50, color='green')
z2 = np.polyfit(df2['IR_Value'], df2['Red_Value'], 1)
p2 = np.poly1d(z2)
axes[0, 1].plot(df2['IR_Value'], p2(df2['IR_Value']), "r--", linewidth=2)
axes[0, 1].set_title(f'IR vs Red (Test 2)\nCorrelation: {corr_ir_red_2:.4f}', fontweight='bold')
axes[0, 1].set_xlabel('IR Signal (LSB)')
axes[0, 1].set_ylabel('Red Signal (LSB)')
axes[0, 1].grid(True, alpha=0.3)

# HR vs SpO2 Test 1
hr1_valid = df1[(df1['HR_bpm'] > 0) & (df1['SpO2_percent'] > 0)]['HR_bpm']
spo2_1_valid = df1[(df1['HR_bpm'] > 0) & (df1['SpO2_percent'] > 0)]['SpO2_percent']
axes[0, 2].scatter(hr1_valid, spo2_1_valid, alpha=0.6, s=50, color='red')
if len(hr1_valid) > 1:
    z3 = np.polyfit(hr1_valid, spo2_1_valid, 1)
    p3 = np.poly1d(z3)
    axes[0, 2].plot(hr1_valid, p3(hr1_valid), "b--", linewidth=2)
axes[0, 2].set_title(f'HR vs SpO2 (Test 1)\nCorrelation: {corr_hr_spo2_1:.4f}', fontweight='bold')
axes[0, 2].set_xlabel('HR (BPM)')
axes[0, 2].set_ylabel('SpO2 (%)')
axes[0, 2].grid(True, alpha=0.3)

# HR vs SpO2 Test 2
hr2_valid = df2[(df2['HR_bpm'] > 0) & (df2['SpO2_percent'] > 0)]['HR_bpm']
spo2_2_valid = df2[(df2['HR_bpm'] > 0) & (df2['SpO2_percent'] > 0)]['SpO2_percent']
axes[1, 0].scatter(hr2_valid, spo2_2_valid, alpha=0.6, s=50, color='orange')
if len(hr2_valid) > 1:
    z4 = np.polyfit(hr2_valid, spo2_2_valid, 1)
    p4 = np.poly1d(z4)
    axes[1, 0].plot(hr2_valid, p4(hr2_valid), "b--", linewidth=2)
axes[1, 0].set_title(f'HR vs SpO2 (Test 2)\nCorrelation: {corr_hr_spo2_2:.4f}', fontweight='bold')
axes[1, 0].set_xlabel('HR (BPM)')
axes[1, 0].set_ylabel('SpO2 (%)')
axes[1, 0].grid(True, alpha=0.3)

# Time vs HR Test 1
axes[1, 1].scatter(df1[df1['HR_bpm'] > 0]['Time_ms']/1000, 
                   df1[df1['HR_bpm'] > 0]['HR_bpm'], alpha=0.6, s=50, color='blue')
axes[1, 1].set_title(f'Thoi gian vs HR (Test 1)\nCorrelation: {corr_time_hr_1:.4f}', fontweight='bold')
axes[1, 1].set_xlabel('Thoi gian (s)')
axes[1, 1].set_ylabel('HR (BPM)')
axes[1, 1].grid(True, alpha=0.3)

# Time vs HR Test 2
axes[1, 2].scatter(df2[df2['HR_bpm'] > 0]['Time_ms']/1000, 
                   df2[df2['HR_bpm'] > 0]['HR_bpm'], alpha=0.6, s=50, color='cyan')
axes[1, 2].set_title(f'Thoi gian vs HR (Test 2)\nCorrelation: {corr_time_hr_2:.4f}', fontweight='bold')
axes[1, 2].set_xlabel('Thoi gian (s)')
axes[1, 2].set_ylabel('HR (BPM)')
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('ADVANCED_01_Correlation.png', dpi=150, bbox_inches='tight')
plt.show()

# ===== PHAN 2: ANOVA ANALYSIS =====
print("\n" + "="*80)
print("PHAN 2: SO SANH NHOM (ANOVA)")
print("="*80)

print(f"\n[Tinh ANOVA...]")

# Lay du lieu
hr1_data = df1[(df1['Valid']==1) & (df1['HR_bpm'] > 0)]['HR_bpm'].values
hr2_data = df2[(df2['Valid']==1) & (df2['HR_bpm'] > 0)]['HR_bpm'].values
ref_hr_data = ref['Reference_BPM'].values

sp1_data = df1[(df1['Valid']==1) & (df1['SpO2_percent'] > 0)]['SpO2_percent'].values
sp2_data = df2[(df2['Valid']==1) & (df2['SpO2_percent'] > 0)]['SpO2_percent'].values
ref_sp_data = ref['Reference_SpO2'].values

# ANOVA cho HR
f_stat_hr, p_value_hr = stats.f_oneway(hr1_data, hr2_data, ref_hr_data)
# ANOVA cho SpO2
f_stat_sp, p_value_sp = stats.f_oneway(sp1_data, sp2_data, ref_sp_data)

print(f"\nANOVA - NHIP TIM (HR):")
print(f"  F-statistic: {f_stat_hr:.4f}")
print(f"  P-value: {p_value_hr:.4f}")
if p_value_hr < 0.05:
    print(f"  Ket luan: Co su khac biet CO Y NGHIA (p < 0.05)")
else:
    print(f"  Ket luan: KHONG co su khac biet (p >= 0.05) - 3 nhom la nhu nhau")

print(f"\nANOVA - OXYBOA MAU (SpO2):")
print(f"  F-statistic: {f_stat_sp:.4f}")
print(f"  P-value: {p_value_sp:.4f}")
if p_value_sp < 0.05:
    print(f"  Ket luan: Co su khac biet CO Y NGHIA (p < 0.05)")
else:
    print(f"  Ket luan: KHONG co su khac biet (p >= 0.05) - 3 nhom la nhu nhau")

print(f"\nGhi chu:")
print(f"  P-value < 0.05 = Khac biet (Co y nghia thong ke)")
print(f"  P-value >= 0.05 = Khong khac biet (3 nhom la nhu nhau)")

# ===== VE BIEU DO ANOVA =====
print(f"\n[Dang ve bieu do ANOVA...]")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('PHAN TICH ANOVA - SO SANH CUA 3 NHOM', fontsize=16, fontweight='bold')

# Box plot HR
data_hr = [hr1_data, hr2_data, ref_hr_data]
bp1 = axes[0].boxplot(data_hr, labels=['Test 1', 'Test 2', 'Tham chieu'], patch_artist=True)
for patch, color in zip(bp1['boxes'], ['lightblue', 'lightgreen', 'lightcoral']):
    patch.set_facecolor(color)
axes[0].set_title(f'ANOVA - Nhip tim (HR)\nF={f_stat_hr:.2f}, P-value={p_value_hr:.4f}', fontweight='bold')
axes[0].set_ylabel('HR (BPM)')
axes[0].grid(True, alpha=0.3, axis='y')
axes[0].axhline(y=np.mean(ref_hr_data), color='red', linestyle='--', alpha=0.5, label='Tham chieu TB')
axes[0].legend()

# Box plot SpO2
data_sp = [sp1_data, sp2_data, ref_sp_data]
bp2 = axes[1].boxplot(data_sp, labels=['Test 1', 'Test 2', 'Tham chieu'], patch_artist=True)
for patch, color in zip(bp2['boxes'], ['lightcoral', 'lightyellow', 'lightblue']):
    patch.set_facecolor(color)
axes[1].set_title(f'ANOVA - Oxyboa mau (SpO2)\nF={f_stat_sp:.2f}, P-value={p_value_sp:.4f}', fontweight='bold')
axes[1].set_ylabel('SpO2 (%)')
axes[1].grid(True, alpha=0.3, axis='y')
axes[1].axhline(y=np.mean(ref_sp_data), color='red', linestyle='--', alpha=0.5, label='Tham chieu TB')
axes[1].legend()

plt.tight_layout()
plt.savefig('ADVANCED_02_ANOVA.png', dpi=150, bbox_inches='tight')
plt.show()

# ===== HOAN THANH =====
print("\n" + "="*80)
print("HOAN THANH PHAN TICH NANG CAO!")
print("="*80)

print(f"\nFile bieu do da tao:")
print(f"  1. ADVANCED_01_Correlation.png")
print(f"  2. ADVANCED_02_ANOVA.png")

print(f"\nTOM TAT:")
print(f"  - Correlation: Xem moi quan he giua cac bien")
print(f"  - ANOVA: So sanh 3 nhom (Test1, Test2, Reference)")
print(f"  - Neu P-value < 0.05: 3 nhom co khac nhau")
print(f"  - Neu P-value >= 0.05: 3 nhom la nhu nhau")

print("\n" + "="*80 + "\n")

input("Nhan phim bat ky de thoat...")
