import turtle

# =====================================================================
# 1. FUNGSI DASAR MENGGAMBAR PIXEL
# =====================================================================
def draw_pixel(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.dot(3)

# =====================================================================
# 2. ALGORITMA GARIS BRESENHAM
# =====================================================================
def draw_line_bresenham(x1, y1, x2, y2):
    x, y = x1, y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1

    if dy <= dx:
        p = 2 * dy - dx
        for _ in range(dx):
            draw_pixel(x, y)
            x += sx
            if p >= 0:
                y += sy
                p -= 2 * dx
            p += 2 * dy
    else:
        p = 2 * dx - dy
        for _ in range(dy):
            draw_pixel(x, y)
            y += sy
            if p >= 0:
                x += sx
                p -= 2 * dy
            p += 2 * dx

    draw_pixel(x2, y2)

# =====================================================================
# 3. ALGORITMA MIDPOINT CIRCLE
# =====================================================================
def draw_circle_midpoint(xc, yc, r):
    x = 0
    y = r
    p = 1 - r

    def plot_circle_points(xc, yc, x, y):
        draw_pixel(xc + x, yc + y)
        draw_pixel(xc - x, yc + y)
        draw_pixel(xc + x, yc - y)
        draw_pixel(xc - x, yc - y)
        draw_pixel(xc + y, yc + x)
        draw_pixel(xc - y, yc + x)
        draw_pixel(xc + y, yc - x)
        draw_pixel(xc - y, yc - x)

    plot_circle_points(xc, yc, x, y)

    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        plot_circle_points(xc, yc, x, y)

# =====================================================================
# 4. POLIGON DENGAN ALGORITMA BRESENHAM
# =====================================================================
def draw_polygon(points):
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        draw_line_bresenham(x1, y1, x2, y2)

# =====================================================================
# 5. PROGRAM UTAMA
# =====================================================================
turtle.speed(0)
turtle.hideturtle()

# ============================
# 1. Garis Bresenham di tengah bawah
# ============================
draw_line_bresenham(-200, -180, 200, -180)

# ============================
# 2. Lingkaran di atas garis bagian kiri
# ============================
draw_circle_midpoint(-120, 0, 80)

# ============================
# 3. Poligon Segi 5 (Pentagon) di atas garis kanan
# ============================
pentagon_points = [
    (140, 30),    # kiri bawah
    (220, 30),    # kanan bawah
    (250, 90),    # kanan atas
    (180, 150),   # puncak
    (110, 90)     # kiri atas
]

draw_polygon(pentagon_points)

turtle.done()
