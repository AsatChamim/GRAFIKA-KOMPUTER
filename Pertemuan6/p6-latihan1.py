# FUNGSI UNTUK MENGGAMBAR TITIK DI TURTLE
import turtle

def draw_points(points, scale=20):
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()

    # gambar sumbu bantu (opsional)
    turtle.goto(0, 0)
    turtle.dot(6, "red")

    for x, y in points:
        turtle.goto(x * scale, y * scale)
        turtle.dot(6, "black")  # titik piksel

    turtle.done()


# ALGORITMA MIDPOINT CIRCLE
def midpoint_circle(r):
    points = []
    x = 0
    y = r
    p = 1 - r

    # tambahkan titik awal
    points.append((x, y))

    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

        # simpan 8 titik simetris
        points.extend([
            (x, y),
            (y, x),
            (-x, y),
            (-y, x),
            (x, -y),
            (y, -x),
            (-x, -y),
            (-y, -x),
        ])

    return points


# MENJALANKAN PROGRAM (radius 6)
r = 6
points = midpoint_circle(r)
draw_points(points)
