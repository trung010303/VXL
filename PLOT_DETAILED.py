#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ve bieu do MAX30102 - Tung bieu do mot, co chu thich chi tiet
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

print("Doc du lieu...")

# Doc file
df1 = pd.read_csv("max30102_test_1.csv")
df2 = pd.read_csv("max30102_test_2.csv")
ref = pd.read_csv("reference_data.csv")

# Tinh toan
hr1 = df1[(df1['Valid']==1) & (df1['HR_bpm'] > 0)]['HR_bpm']
hr2 = df2[(df2['Valid']==1) & (df2['HR_bpm'] > 0)]['HR_bpm']
sp1 = df1[(df1['Valid']==1) & (df1['SpO2_percent'] > 0)]['SpO2_percent']
sp2 = df2[(df2['Valid']==1) & (df2['SpO2_percent'] > 0)]['SpO2_percent']

ref_hr = ref['Reference_BPM'].mean()
ref_sp = ref['Reference_SpO2'].mean()

hr1_mean = hr1.mean()
hr2_mean = hr2.mean()
sp1_mean = sp1.mean()
sp2_mean = sp2.mean()

error_hr1 = abs(hr1_mean - ref_hr)
error_hr2 = abs(hr2_mean - ref_hr)
error_sp1 = abs(sp1_mean - ref_sp)
error_sp2 = abs(sp2_mean - ref_sp)

print("Da chuan bi xong!\n")

# ========================================================================
# BIEU DO 1: HR TEST 1
# ========================================================================
print("[1/6] Ve bieu do HR Test 1...")
fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(df1['Time_ms']/1000, df1['HR_bpm'], 'o-', color='blue', linewidth=2, markersize=6, label='Gia tri do duoc')
ax.axhline(y=hr1_mean, color='blue', linestyle='--', linewidth=2, alpha=0.7, label=f'Trung binh Test 1: {hr1_mean:.1f} BPM')
ax.axhline(y=ref_hr, color='red', linestyle='--', linewidth=2, alpha=0.7, label=f'Tham chieu (Binh thuong): {ref_hr:.1f} BPM')

# Chu thich
ax.fill_between([0, 6], ref_hr-5, ref_hr+5, alpha=0.1, color='green', label='Vung chap nhan (+/- 5 BPM)')

ax.set_title('NHIP TIM (BPM) - TEST 1', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Thoi gian (giay)', fontsize=12, fontweight='bold')
ax.set_ylabel('Nhip tim (BPM)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=11, loc='best')
ax.set_ylim([65, 85])

# Them text chu thich
textstr = f'Sai so: ±{error_hr1:.1f} BPM\nDo chinh xac: {100 - (error_hr1/ref_hr*100):.1f}%\nTrang thai: {"PASS ✓" if error_hr1 <= 5 else "FAIL ✗"}'
ax.text(0.98, 0.05, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('01_HR_Test1.png', dpi=150, bbox_inches='tight')
plt.show()

# ========================================================================
# BIEU DO 2: HR TEST 2
# ========================================================================
print("[2/6] Ve bieu do HR Test 2...")
fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(df2['Time_ms']/1000, df2['HR_bpm'], 'o-', color='green', linewidth=2, markersize=6, label='Gia tri do duoc')
ax.axhline(y=hr2_mean, color='green', linestyle='--', linewidth=2, alpha=0.7, label=f'Trung binh Test 2: {hr2_mean:.1f} BPM')
ax.axhline(y=ref_hr, color='red', linestyle='--', linewidth=2, alpha=0.7, label=f'Tham chieu (Binh thuong): {ref_hr:.1f} BPM')

# Chu thich
ax.fill_between([0, 6], ref_hr-5, ref_hr+5, alpha=0.1, color='green', label='Vung chap nhan (+/- 5 BPM)')

ax.set_title('NHIP TIM (BPM) - TEST 2', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Thoi gian (giay)', fontsize=12, fontweight='bold')
ax.set_ylabel('Nhip tim (BPM)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=11, loc='best')
ax.set_ylim([65, 85])

# Them text chu thich
textstr = f'Sai so: ±{error_hr2:.1f} BPM\nDo chinh xac: {100 - (error_hr2/ref_hr*100):.1f}%\nTrang thai: {"PASS ✓" if error_hr2 <= 5 else "FAIL ✗"}'
ax.text(0.98, 0.05, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('02_HR_Test2.png', dpi=150, bbox_inches='tight')
plt.show()

# ========================================================================
# BIEU DO 3: SpO2 TEST 1
# ========================================================================
print("[3/6] Ve bieu do SpO2 Test 1...")
fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(df1['Time_ms']/1000, df1['SpO2_percent'], 'o-', color='red', linewidth=2, markersize=6, label='Gia tri do duoc')
ax.axhline(y=sp1_mean, color='red', linestyle='--', linewidth=2, alpha=0.7, label=f'Trung binh Test 1: {sp1_mean:.2f}%')
ax.axhline(y=ref_sp, color='blue', linestyle='--', linewidth=2, alpha=0.7, label=f'Tham chieu (Binh thuong): {ref_sp:.2f}%')

# Chu thich
ax.fill_between([0, 6], ref_sp-2, ref_sp+2, alpha=0.1, color='green', label='Vung chap nhan (+/- 2%)')

ax.set_title('OXYBOA MAU (SpO2) - TEST 1', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Thoi gian (giay)', fontsize=12, fontweight='bold')
ax.set_ylabel('Oxyboa mau (%)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=11, loc='best')
ax.set_ylim([94, 100])

# Them text chu thich
textstr = f'Sai so: ±{error_sp1:.2f}%\nDo chinh xac: {100 - (error_sp1/ref_sp*100):.2f}%\nTrang thai: {"PASS ✓" if error_sp1 <= 2 else "FAIL ✗"}'
ax.text(0.98, 0.05, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.tight_layout()
plt.savefig('03_SpO2_Test1.png', dpi=150, bbox_inches='tight')
plt.show()

# ========================================================================
# BIEU DO 4: SpO2 TEST 2
# ========================================================================
print("[4/6] Ve bieu do SpO2 Test 2...")
fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(df2['Time_ms']/1000, df2['SpO2_percent'], 'o-', color='orange', linewidth=2, markersize=6, label='Gia tri do duoc')
ax.axhline(y=sp2_mean, color='orange', linestyle='--', linewidth=2, alpha=0.7, label=f'Trung binh Test 2: {sp2_mean:.2f}%')
ax.axhline(y=ref_sp, color='blue', linestyle='--', linewidth=2, alpha=0.7, label=f'Tham chieu (Binh thuong): {ref_sp:.2f}%')

# Chu thich
ax.fill_between([0, 6], ref_sp-2, ref_sp+2, alpha=0.1, color='green', label='Vung chap nhan (+/- 2%)')

ax.set_title('OXYBOA MAU (SpO2) - TEST 2', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Thoi gian (giay)', fontsize=12, fontweight='bold')
ax.set_ylabel('Oxyboa mau (%)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=11, loc='best')
ax.set_ylim([94, 100])

# Them text chu thich
textstr = f'Sai so: ±{error_sp2:.2f}%\nDo chinh xac: {100 - (error_sp2/ref_sp*100):.2f}%\nTrang thai: {"PASS ✓" if error_sp2 <= 2 else "FAIL ✗"}'
ax.text(0.98, 0.05, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.tight_layout()
plt.savefig('04_SpO2_Test2.png', dpi=150, bbox_inches='tight')
plt.show()

# ========================================================================
# BIEU DO 5: TIN HIEU IR & RED TEST 1
# ========================================================================
print("[5/6] Ve bieu do IR & Red Test 1...")
fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(df1['Time_ms']/1000, df1['IR_Value'], 'o-', color='purple', linewidth=2, markersize=5, label='IR (Hong ngoai)', alpha=0.8)
ax.plot(df1['Time_ms']/1000, df1['Red_Value'], 's-', color='brown', linewidth=2, markersize=5, label='Red (Do)', alpha=0.8)

ax.set_title('TIN HIEU LED - TEST 1 (IR & Red)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Thoi gian (giay)', fontsize=12, fontweight='bold')
ax.set_ylabel('Gia tri ADC (LSB)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=11, loc='best')

# Them text chu thich
ratio = df1['Red_Value'].mean() / df1['IR_Value'].mean()
textstr = f'Trung binh IR: {df1["IR_Value"].mean():.0f} LSB\nTrung binh Red: {df1["Red_Value"].mean():.0f} LSB\nTi le Red/IR: {ratio:.4f}\nTi le toi uu: 0.4 - 0.6'
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='left',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('05_IR_Red_Test1.png', dpi=150, bbox_inches='tight')
plt.show()

# ========================================================================
# BIEU DO 6: TIN HIEU IR & RED TEST 2
# ========================================================================
print("[6/6] Ve bieu do IR & Red Test 2...")
fig, ax = plt.subplots(figsize=(12, 7))

ax.plot(df2['Time_ms']/1000, df2['IR_Value'], 'o-', color='purple', linewidth=2, markersize=5, label='IR (Hong ngoai)', alpha=0.8)
ax.plot(df2['Time_ms']/1000, df2['Red_Value'], 's-', color='brown', linewidth=2, markersize=5, label='Red (Do)', alpha=0.8)

ax.set_title('TIN HIEU LED - TEST 2 (IR & Red)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Thoi gian (giay)', fontsize=12, fontweight='bold')
ax.set_ylabel('Gia tri ADC (LSB)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=11, loc='best')

# Them text chu thich
ratio = df2['Red_Value'].mean() / df2['IR_Value'].mean()
textstr = f'Trung binh IR: {df2["IR_Value"].mean():.0f} LSB\nTrung binh Red: {df2["Red_Value"].mean():.0f} LSB\nTi le Red/IR: {ratio:.4f}\nTi le toi uu: 0.4 - 0.6'
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='left',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('06_IR_Red_Test2.png', dpi=150, bbox_inches='tight')
plt.show()

# ========================================================================
# HOAN THANH
# ========================================================================
print("\n" + "="*80)
print("HOAN THANH!")
print("="*80)
print("\nCac file bieu do da duoc tao:")
print("  1. 01_HR_Test1.png")
print("  2. 02_HR_Test2.png")
print("  3. 03_SpO2_Test1.png")
print("  4. 04_SpO2_Test2.png")
print("  5. 05_IR_Red_Test1.png")
print("  6. 06_IR_Red_Test2.png")
print("\nMoi bieu do se hien len tung cai mot.")
print("\n" + "="*80 + "\n")

input("Nhan phim bat ky de thoat...")
