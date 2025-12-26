import matplotlib.pyplot as plt

# Titik awal dan akhir (ubah sesuai keinginanmu!)
x1, y1 = 1, 1
x2, y2 = 10, 5

# --------------------------
# Algoritma DDA
def dda(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)
    Xinc = dx / steps
    Yinc = dy / steps
    x, y = x1, y1
    for _ in range(int(steps) + 1):
        points.append((round(x), round(y)))
        x += Xinc
        y += Yinc
    return points

# Algoritma Bresenham
def bresenham(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    p = 2 * dy - dx
    x, y = x1, y1
    for _ in range(dx + 1):
        points.append((x, y))
        if p >= 0:
            y += 1 if y1 < y2 else -1
            p += 2 * (dy - dx)
        else:
            p += 2 * dy
        x += 1 if x1 < x2 else -1
    return points

# Persamaan Garis
def persamaan_garis(x1, y1, x2, y2):
    points = []
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    for x in range(x1, x2 + 1):
        y = round(m * x + c)
        points.append((x, y))
    return points

# --------------------------
# Ambil hasil titik dari 3 algoritma
dda_points = dda(x1, y1, x2, y2)
bres_points = bresenham(x1, y1, x2, y2)
eq_points = persamaan_garis(x1, y1, x2, y2)

# Gambar hasilnya
plt.figure(figsize=(8,6))
plt.plot(*zip(*dda_points), 'ro-', label='DDA')
plt.plot(*zip(*bres_points), 'go-', label='Bresenham')
plt.plot(*zip(*eq_points), 'bo-', label='Persamaan Garis')

plt.title('Perbandingan Algoritma Garis')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.legend()
plt.show()
