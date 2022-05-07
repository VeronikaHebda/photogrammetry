import math as m
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc
#from tkinker import Tk
#window = Tk()
#window.title('Fotogrametria projekt 1')

# print("Podaj GSD:")
# GSD = float(input())
# print("Podaj minimalne pokrycie podłużne p%:")
# p = float(input())
# print("Podaj minimalne pokrycie poprzeczne q%:")  # dluzszy to poprzek
# q = float(input())
# print("Podaj Dx:")
# Dx = float(input())
# print("Podaj Dy:")
# Dy = float(input())
#niech uzytkownik poda x i y poczatek obszaru opracowania

Dx = 19090
Dy = 17219
GSD = 25
p = float(60)
q = float(30)
x = 10000
y = 10000


# konwersja mikselow z mikrometrow na milimetry
class Samolot:
    def __init__(self, Vmin, Vmax, pulap, t):
        self.Vmin = Vmin / 3.6  # [m/s]
        self.Vmax = Vmax / 3.6  # [m/s]
        self.pulap = pulap  # [m]
        self.t = t  # [h]


class Kamera:
    def __init__(self, lx, ly, px, f, s):
        # lx to krotszy bok
        self.lx = min(lx, ly)
        self.ly = max(lx, ly)
        self.px = px  # [mikrometr]
        self.f = f * 1000  # [milimetr] 1 cm to 10mm, cm razy 10, 1 mm to 1000mikro
        self.s = s  # [s]


Cesna402 = Samolot(132, 428, 8200, 5)
CesnaT206HNAVIII = Samolot(100, 280, 4785, 5)
VulcanAirP68Obeserver2 = Samolot(135, 275, 6100, 6)
TencamMMA = Samolot(120, 267, 4572, 6)

ZIDMCII250 = Kamera(16768, 14016, 5.6, 112, 2.3)
LeicaDMCIII = Kamera(25728, 14592, 3.9, 92, 1.9)
UltraCamFalconM270 = Kamera(17310, 11310, 6.0, 70, 1.35)
UltraCamEagleM3 = Kamera(26460, 17004, 4.0, 80, 1.5)
ZIDMCII = Kamera(15552, 14144, 5.6, 92, 1.8)

kamera = ZIDMCII
samolot = TencamMMA


def obliczenia(GSD, p, q, Dx, Dy, kamera, samolot):
    W = GSD * kamera.f / kamera.px
    Lx = kamera.lx * GSD / 100
    Ly = kamera.ly * GSD / 100  # zeby gsd bylo w metrach
    print("Lx i Ly", round(Lx, 0), round(Ly, 0))
    Bx = Lx * (100 - p) / 100
    By = Ly * (100 - q) / 100
    print("Bx,By", round(Bx, 0), round(By, 0))
    Nx = Dx / Bx + 4
    Ny = Dy / By  # [m]/[]

    Nx_gora = m.ceil(Nx)
    Ny_gora = m.ceil(Ny)
    print("Zaokraglona ilosc szeregow i rzedow", Nx_gora, Ny_gora)

    nowe_bx = Dx / (Nx_gora - 4)
    nowe_by = Dy / Ny_gora
    print("Nowe Bx i By", round(nowe_bx, 0), round(nowe_by, 0))

    nowe_p = 100 - (nowe_bx * 100 / Lx)
    nowe_q = 100 - (nowe_by * 100 / Ly)

    print("Nowe p i q", round(nowe_p, 1), round(nowe_q, 1))

    if kamera.s > Bx / samolot.Vmin:
        print("Predkosc maksymalna samolotu jest za mała")

    N = Nx_gora * Ny_gora
    return N, int(Nx_gora), int(Ny_gora), Lx, Ly, nowe_bx, nowe_by #nx to ilosc zdjec w szeregu, ny to liczba szeregow


N, Nx, Ny, Lx, Ly, Bx, By = obliczenia(GSD, p, q, Dx, Dy, kamera, samolot)
print("Ilosc zdjec", N)

figure, axes = plt.subplots()
# point1 = [1, 2]
# point2 = [3, 4]
# x_values = [point1[0], point2[0]]
# y_values = [point1[1], point2[1]]
# axes.plot(x_values, y_values)



r = 150

y_kol = y + By/2
y_zdj = y_kol - Ly/2
tabx_luk = [x - 2 * Bx + Bx/2, x - 2 * Bx + Bx/2 + (Nx-1) * Bx]
taby_luk = []
axes.add_patch(Rectangle((x, y),Dx,Dy, color = '#80ff00', alpha = 0.7))
for j in range (Ny):
    x_kol = x - 2 * Bx + Bx/2
    x_zdj = x_kol - Lx/2
    tabx = []
    taby = []
    for i in range (Nx):
        axes.add_patch(Rectangle((x_zdj, y_zdj), Lx, Ly, edgecolor='violet', facecolor='none', ))
        tabx.append(x_kol)
        taby.append(y_kol)
        x_kol = x_kol + Bx
        x_zdj = x_zdj + Bx
    axes.plot(tabx,taby, color = 'black', marker='o',linestyle='dashed',linewidth=1, markersize=5)
    taby_luk.append(y_kol)
    y_kol = y_kol + By
    y_zdj = y_zdj + By



for i in range(0,len(taby_luk)-1):
    if i%2 == 0:
        luk = matplotlib.patches.Arc((tabx_luk[0], (taby_luk[i] + taby_luk[i+1]) / 2), 3000, By, 180, 270, 90,
                                 color = 'black',linestyle='dashed')
        axes.add_patch(luk)
    else:
        luk = matplotlib.patches.Arc((tabx_luk[1], (taby_luk[i] + taby_luk[i + 1]) / 2), 3000, By, 180, 90, 270,
                                 color = 'black',linestyle='dashed')
        axes.add_patch(luk)


axes.autoscale(enable = True)

plt.show()
# napisac jeszcze zeby uzytkownik wprowadzil pierwsze miejsce zdjecia