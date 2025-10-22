#praktikum 1
x= 50
y= 100
warna = "merah"
print (f"koordinat titik ({x},{y}) dengan warna {warna},")

#praktikum2
x = int (input ("masukan nilai x: "))
y = int (input ("masukan nilai y: "))
warna = input ("masukan warna: ")
print (F" titik berada di ({x},{y}) dan warna {warna}.")

#pratikum3
x = int(input("masukan nilai x:"))

if x >0:
    print ("titik di kanan layar.")
elif x <0:
    print ("titik di kiri layar. ")
else :
    print ("titik di tengah. ")

print ("menampilan 5 titik")
for i in range (1, 6):
    print (F"titik ke-{i}")
    
#praktikum4
import math
def hitung_jarak (x1,y1,x2,y2):
    jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return jarak

hasil = hitung_jarak (0,0,3,4)
print(F"jarak antara dua titik: {hasil}")

#praktikum5

titik_list = [(0, 0), (50, 50), (100, 0)]
print(f"List Titik: {titik_list}")
for titik in titik_list:
    print(f"Titik: ({titik[0]}, {titik[1]})")

print("\n" + "="*35 + "\n")
pusat = (0, 0)
print(f"Nilai 'pusat': {pusat}")
print(f"Titik pusat adalah: ({pusat[0]}, {pusat[1]})")
print("\n" + "="*35 + "\n")
objek_atribut = {"x": 10, "y": 20, "warna": "biru"}
print(f"Dictionary Atribut: {objek_atribut}")
x_koordinat = objek_atribut["x"]
y_koordinat = objek_atribut["y"]
warna_objek = objek_atribut["warna"]

print(f"Titik ({x_koordinat},{y_koordinat}) berwarna {warna_objek}.")