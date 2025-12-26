import matplotlib.pyplot as plt

# Algoritma Garis dengan DDA
def dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    xs, ys = [], []
    for _ in range(steps):
        xs.append(x)
        ys.append(y)
        x += x_inc
        y += y_inc
    return xs, ys

# Algoritma lingkaran
def midpoint_circle(xc, yc, r):
    x, y = 0, r
    p = 1 - r
    pts = []
    while x <= y:
        pts += [
            (xc+x, yc+y), (xc-x, yc+y),
            (xc+x, yc-y), (xc-x, yc-y),
            (xc+y, yc+x), (xc-y, yc+x),
            (xc+y, yc-x), (xc-y, yc-x)
        ]
        x += 1
        if p < 0:
            p += 2*x + 1
        else:
            y -= 1
            p += 2*(x-y) + 1
    return zip(*pts)

# gambar Poligon 
def polygon(points):
    xs, ys = [], []
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % len(points)]
        x, y = dda(x1, y1, x2, y2)
        xs += x
        ys += y
    return xs, ys


# a;goritma Refleksi Sumbu y
def reflect_y(points):
    return [(-x, y) for x, y in points]

# output canvas
plt.figure(figsize=(12,6))
plt.axis("equal")
plt.axis("off")
plt.xlim(-220, 220)
plt.ylim(0, 220)

x, y = dda(0, 0, 0, 220)
plt.plot(x, y, linestyle="--", color="gray")
plt.text(5, 195, "Sumbu Y (x = 0)", fontsize=9, color="gray")

# gedung sekolah 2D
gedung = [(60,50),(140,50),(140,130),(60,130)]
atap = [(50,130),(100,170),(150,130)]
pintu = [(90,50),(110,50),(110,90),(90,90)]

for obj, col in [(gedung,"#d6eaf8"), (atap,"#c0392b"), (pintu,"#935116")]:
    plt.fill(*zip(*obj), color=col)
    x, y = polygon(obj)
    plt.plot(x, y, color="black")

plt.text(75, 25, "Objek Asli", fontsize=10)

# Hasil setelah di Refleksi
gedung_r = reflect_y(gedung)
atap_r = reflect_y(atap)
pintu_r = reflect_y(pintu)

for obj, col in [(gedung_r,"#fadbd8"), (atap_r,"#a93226"), (pintu_r,"#784212")]:
    plt.fill(*zip(*obj), color=col)
    x, y = polygon(obj)
    plt.plot(x, y, color="black")

plt.text(-135, 25, "Hasil Refleksi", fontsize=10)

# Matahari 
sun_x, sun_y = 140, 200
x, y = midpoint_circle(sun_x, sun_y, 12)
plt.scatter(x, y, s=8, color="orange")

sun_reflect = reflect_y([(sun_x, sun_y)])[0]
x, y = midpoint_circle(sun_reflect[0], sun_reflect[1], 12)
plt.scatter(x, y, s=8, color="orange")

# =========================
# Judul
# =========================
plt.title("Refleksi gedung sekolah 2D")
plt.show()
