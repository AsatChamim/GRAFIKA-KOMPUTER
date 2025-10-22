print("halo,graafika komputer")

#tipe data
x=100
y=50
warna = "red"

print("posisi titik:",x,y)
print("warna:", warna)

#input output
sisi = int(input("masukan panjang sisi: "))
warna = input ("masukan wara:")

print(f"persegi dengan sisi {sisi} berwarna {warna}")

#oprasi arit matika
x1,y1 = 10,20
x2,y2 = 30,50
dx = x2 - y1
dy = y2 - y1

print("selisish koordinat: ", dx,dy)

#kondidi dan looping
x=50
if x > 0:
    print("titik berada di sisi kanan sumbu Y")
else :
    print("titik berada di sisi kiri sumbu Y ")
for i in range (5):
    print("tititk ke: ", i)
  
  #fungsi
def sapa (nama):
    print ("halo,",nama, "selamat belajar grafikakomputer!")
sapa ("budiman")
sapa ("sinta")