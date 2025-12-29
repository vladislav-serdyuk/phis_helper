import math
import random

from scipy.signal import find_peaks, peak_widths
import matplotlib.pyplot as plt

h = 6.62607015*10**(-34)
c = 299792458
pi = 3.1415926536

async def calc_translate(from_: str, to: str, data: float) -> float:
    convertors_to_energy = {'e': lambda e: e, 'l': lambda l: h*c/(l/10**9), 'f': lambda v: h*(v*10**12)}
    convertors_from_energy = {'e': lambda e: e, 'l': lambda e: h*c/e*10**9, 'f': lambda e: e/h/10**12}
    energy = convertors_to_energy[from_](data)
    return convertors_from_energy[to](energy)


async def calc_fluence(power: float, diameter: float) -> float:
    r = diameter/1000/2
    s = pi*r*r
    return power/s

async def calc_spector(spector_data: str) -> tuple[str, float, float]:
    data = [row.split(' ') for row in spector_data.split('\n')]
    data_float = []
    for row in data:
        if len(row) != 2:
            continue
        x, y = row
        try:
            data_float.append((float(x), float(y)))
        except ValueError:
            continue
    data_float.sort()
    data_x, data_y = [], []
    for row in data_float:
        if len(row) != 2:
            continue
        x, y = row
        data_x.append(float(x))
        data_y.append(float(y))
    peaks, _ = find_peaks(data_y)
    _, width_heights, left_ips, right_ips = peak_widths(data_y, peaks, rel_height=0.5)
    plt.plot(data_x, data_y)
    peaks_y = [data_y[peak] for peak in peaks]
    plt.plot([data_x[peak] for peak in peaks], peaks_y, 'x')
    def convert_ip(ip):
        return data_x[math.floor(ip)]*(1 - math.modf(ip)[0]) + data_x[math.ceil(ip)]*math.modf(ip)[0]
    plt.hlines(width_heights, list(map(convert_ip, left_ips)), list(map(convert_ip, right_ips)), color="C2")
    file = f'spector_{''.join([str(random.randint(0, 9)) for _ in range(10)])}.png'
    plt.savefig(file)
    max_peak = max(enumerate(peaks), key=lambda peak: data_y[peak[1]])[0]
    return file, data_x[peaks[max_peak]], convert_ip(right_ips[max_peak]) - convert_ip(left_ips[max_peak])
