import turtle
def draw_polygon(vertices):
    all_points = []
    n = len(vertices)

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        all_points.extend(draw_line(x1, y1, x2, y2))

    return all_points


# ==========================================
# 4. FUNGSI MENGGAMBAR TITIK DENGAN TURTLE
# ==========================================

def draw_points(points, scale=20):
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()

    for x, y in points:
        turtle.goto(x * scale, y * scale)
        turtle.dot(6, "black")

    turtle.done()


