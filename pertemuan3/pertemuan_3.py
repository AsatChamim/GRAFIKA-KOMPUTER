for y in range (0, 5):
    for x in range (0, 10):
        print(".", end="")
    print()
    
print("\n" + "="*35 + "\n")

#peraktikum titik koordinat
import math 
#soal 1
x1 = float(input("Masukkan koordinat x1: "))
y1 = float(input("Masukkan koordinat y1: "))
x2 = float(input("Masukkan koordinat x2: "))
y2 = float(input("Masukkan koordinat y2: "))

jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
if x1 > 0 and y1 > 0:
    kuadran = "Kuadran I"
elif x1 < 0 and y1 > 0:
    kuadran = "Kuadran II"
elif x1 < 0 and y1 < 0:
    kuadran = "Kuadran III"
elif x1 > 0 and y1 < 0:
    kuadran = "Kuadran IV"
elif x1 == 0 and y1 == 0:
    kuadran = "Titik Pusat (0,0)"
elif x1 == 0:
    kuadran = "Berada di Sumbu Y"
elif y1 == 0:
    kuadran = "Berada di Sumbu X"
print(f"Titik pertama: ({x1}, {y1})")
print(f"Titik kedua  : ({x2}, {y2})")
print(f"Jarak antara dua titik = {jarak:.2f}")
print(f"Titik pertama berada di: {kuadran}")

print("\n" + "="*35 + "\n")

#soal 2
lebar = 10
tinggi = 5
x_titik = 3
y_titik = 2

print("=== Simulasi Koordinat 10x5 ===")
for y in range(tinggi - 1, -1, -1):
    for x in range(lebar):
        if x == x_titik and y == y_titik:
            print("X", end="") 
        else:
            print(".", end="")  
    print()
    
#representasi Gambar
# soal 1: Grid 10x10
print("\n" + "="*35 + "\n")
rows, cols = 10, 10  # ukuran grid
grid = [["." for _ in range(cols)] for _ in range(rows)]
grid[4][6] = "X"
for row in grid:
    print(" ".join(row))
    
print("\n" + "="*35 + "\n")
# Soal 2: Menggambar garis dari (0,0) ke (5,3)
x1, y1 = 0, 0
x2, y2 = 5, 3

dx = x2 - x1
dy = y2 - y1
steps = max(abs(dx), abs(dy))
x_inc = dx / steps
y_inc = dy / steps

x, y = x1, y1

print("Titik-titik koordinat garis dari (0,0) ke (5,3):")
for i in range(steps + 1):
    print(f"({round(x)}, {round(y)})")
    x += x_inc
    y += y_inc

