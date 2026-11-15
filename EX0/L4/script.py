import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "vtc.txt"      # File -> Export data as Text (from the .dc plot window)
OUT_FILE = "vtc.png"
VDD = 5.0

# LTspice exports tab-separated text: column 0 = VIN, column 1 = V(vout)
df = pd.read_csv(DATA_FILE, sep="\t")
vin = df.iloc[:, 0].to_numpy(dtype=float)
vout = df.iloc[:, 1].to_numpy(dtype=float)

# Vm: first point where VOUT falls through VDD/2, linearly interpolated
target = VDD / 2
i = np.argmax(vout <= target)              # first index at or below VDD/2
x0, x1 = vin[i - 1], vin[i]
y0, y1 = vout[i - 1], vout[i]
vm = x0 + (target - y0) * (x1 - x0) / (y1 - y0)
print(f"Vm = {vm:.3f} V")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(vin, vout, color="tab:green", label="V(vout)")
ax.axhline(target, color="gray", linestyle=":", linewidth=1)
ax.axvline(vm, color="gray", linestyle=":", linewidth=1)
ax.plot(vm, target, "ro", label=f"$V_m$ = {vm:.2f} V")
ax.annotate(f"$V_m$ = {vm:.2f} V", xy=(vm, target),
            xytext=(vm + 0.4, target + 0.6),
            arrowprops=dict(arrowstyle="->"))

ax.set_xlabel("$V_{IN}$ (V)")
ax.set_ylabel("$V_{OUT}$ (V)")
ax.set_title("CMOS inverter VTC (2N7000 / BS250, VDD = 5 V)")
ax.grid(True)
ax.legend()
fig.tight_layout()
fig.savefig(OUT_FILE, dpi=300)
plt.show()