import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib.transforms import Affine2D

# ================= LOAD GAMBAR =================
img = mpimg.imread("spongebob.jpg")

# ================= SETUP FIGURE =================
fig, axs = plt.subplots(2, 2, figsize=(9, 7))

def setup_axis(ax, title):
    ax.set_title(title, fontsize=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_yticks(np.arange(0, 101, 10))
    ax.grid(True)

# =================================================
# 1. TRANSLASI
# =================================================
ax = axs[0, 0]
setup_axis(ax, "1. Translasi (dx = 20, dy = 0)")

# sebelum
ax.imshow(img, extent=(10, 30, 10, 30))

# sesudah
ax.imshow(
    img,
    extent=(10, 30, 10, 30),
    transform=Affine2D().translate(20, 0) + ax.transData
)

# titik & panah
ax.scatter([10, 30], [5, 5], color="red")
ax.text(8, 3, "(10,5)", fontsize=8)
ax.text(28, 3, "(30,5)", fontsize=8)

ax.annotate(
    "",
    xy=(30, 5),
    xytext=(10, 5),
    arrowprops=dict(arrowstyle="->", linewidth=1.5)
)

# =================================================
# 2. ROTASI
# =================================================
ax = axs[0, 1]
setup_axis(ax, "2. Rotasi 30°")

ax.imshow(
    img,
    extent=(40, 60, 10, 30),
    transform=Affine2D().rotate_deg_around(50, 20, 30) + ax.transData
)

# =================================================
# 3. SCALING
# =================================================
ax = axs[1, 0]
setup_axis(ax, "3. Skala 1.5x")

ax.imshow(
    img,
    extent=(10, 30, 40, 60),
    transform=Affine2D().scale(1.5, 1.5) + ax.transData
)

# =================================================
# 4. REFLEKSI
# =================================================
ax = axs[1, 1]
setup_axis(ax, "4. Refleksi terhadap sumbu-Y")

# sumbu-Y
sumbu_y = 50
ax.axvline(x=sumbu_y, linestyle="--", linewidth=1)
ax.text(sumbu_y + 1, 95, "Sumbu-Y", fontsize=8)

# koordinat titik
x_awal, y_awal = 40, 20
x_akhir = 2 * sumbu_y - x_awal
y_akhir = y_awal

# gambar sebelum
ax.imshow(img, extent=(30, 50, 40, 60))
ax.text(32, 62, "Sebelum", fontsize=8)

# gambar sesudah
ax.imshow(
    img,
    extent=(30, 50, 40, 60),
    transform=Affine2D().scale(-1, 1).translate(2 * sumbu_y, 0) + ax.transData
)
ax.text(62, 62, "Sesudah", fontsize=8)

# titik sebelum & sesudah
ax.scatter([x_awal, x_akhir], [y_awal, y_akhir], color="red")
ax.text(x_awal - 6, y_awal - 4, f"({x_awal},{y_awal})", fontsize=8)
ax.text(x_akhir + 1, y_akhir - 4, f"({x_akhir},{y_akhir})", fontsize=8)

# panah pencerminan
ax.annotate(
    "",
    xy=(x_akhir, y_akhir),
    xytext=(x_awal, y_awal),
    arrowprops=dict(arrowstyle="<->", linewidth=1.5)
)

plt.tight_layout()
plt.show()
