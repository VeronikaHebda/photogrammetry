import math as m


print("Podaj GSD:")
GSD = float(input())
print("Podaj minimalne pokrycie podłużne p%:")
p = float(input())
print("Podaj minimalne pokrycie poprzeczne q%:") #dluzszy to poprzek
q = float(input())
print("Podaj Dx:")
Dx = float(input())
print("Podaj Dy:")
Dy = float(input())
#konwersja mikselow z mikrometrow na milimetry
class Samolot:
    def __init__(self, Vmin, Vmax, pulap, t):
        self.Vmin = Vmin / 3.6  #[m/s]
        self.Vmax = Vmax / 3.6  #[m/s]
        self.pulap = pulap      #[m]
        self.t = t              #[h]
class Kamera:
    def __init__(self, lx, ly, px, f, s):
        #lx to krotszy bok
        self.lx = min(lx,ly)
        self.ly = max(lx,ly)
        self.px = px            #[mikrometr]
        self.f = f*1000         #[milimetr] 1 cm to 10mm, cm razy 10, 1 mm to 1000mikro
        self.s = s              #[s]

Cesna402 = Samolot(132,428,8200,5)
CesnaT206HNAVIII = Samolot(100,280,4785,5)
VulcanAirP68Obeserver2 = Samolot(135,275,6100,6)
TencamMMA = Samolot(120,267,4572,6)

ZIDMCII250 = Kamera(16768, 14016, 5.6, 112, 2.3)
LeicaDMCIII = Kamera(25728,14592, 3.9, 92, 1.9)
UltraCamFalconM270 = Kamera(17310, 11310, 6.0, 70, 1.35)
UltraCamEagleM3 = Kamera(26460, 17004, 4.0, 80, 1.5)

kamera = LeicaDMCIII
samolot = TencamMMA
def obliczenia(GSD, p, q, Dx, Dy, kamera, samolot):
    W = GSD * kamera.f/kamera.px
    Lx = kamera.lx * GSD / 100
    Ly = kamera.ly * GSD / 100 #zeby gsd bylo w metrach
    print(Lx,Ly)
    Bx = Lx * (100-p)/100
    By = Ly * (100-q)/100

    Nx = Dx/Bx + 4
    Ny = Dy / By  # [m]/[]
    print(Nx,Ny)
    #zwiekszyc ny i nx w gore, zwiekszona wartosc podzielic przez poczatkowa i pomnozyc procentowo p i q
    Nx_gora = m.ceil(Nx)
    Ny_gora = m.ceil(Ny)

    nowe_p = Nx_gora/Nx * p
    nowe_q = Ny_gora/Ny * q

    print(nowe_p, nowe_q)
    if kamera.s > Bx/samolot.Vmin:
        print("błąd")

    N = Nx_gora * Ny_gora
    return N

N = obliczenia(GSD, p, q, Dx, Dy, kamera, samolot)
print(N)