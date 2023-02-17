import numpy as np
import math
import matplotlib.pyplot as plt

#NOTE: make ideal and exp y's on the same units
#      and make wavelengths out of nm
def main():
    ideal_data = ideal()
    
    #exp_yn = (trial,sswvl)
    #graph exp find wavelengths for sswv
    #check data to find the intensity, replace
    exp_yn = [(black_body("BB7 300ms #5.txt"),800.178),
              (black_body("BB6 400ms #5.txt"),725.056),
              (black_body("BB5 500ms #5.txt"),690.113),
              (black_body("BB4 1s #5.txt"),630.193),
              (black_body("BB3 2s #5.txt"),595.116),
              (black_body("BB2 3s #5.txt"),575.054),
              (black_body("BB1 5s #5.txt"),550.012)]
    #exp_yn for each trial
    corrections_lst = []
    for trial in exp_yn:
        cn = correction(ideal_data, trial[0], trial[1]) 
        corrections_lst.append(cn)
    corrections_lst = np.array(corrections_lst)
    actual_spectrum = black_body("32ms #2 High Cloud Cover.txt")
    #multiply
    a_wavelength = np.array(actual_spectrum[0])
    a_intensities = np.array(actual_spectrum[1])
    cl_length = len(corrections_lst)
    sum_mult = 0
    for i in range (cl_length - 1):
        m1 = np.multiply(a_intensities, corrections_lst[i])
        sum_mult = np.add(sum_mult, m1)
    int_corrected = sum_mult/cl_length
    #graph both orignal and adjusted on same plot then normalize
    #multiply by each correction then add then divide by total"""
    both_graphs(a_wavelength, a_intensities, int_corrected)

def both_graphs(wavelengths, actual, corrected):
    # Initialise the subplot function using number of rows and columns
    max_a = np.max(actual)
    max_c = np.max(corrected)
    actual = actual/max_a
    corrected = corrected/max_c
    f = plt.figure()
    ax = f.add_subplot()
    plt.plot(wavelengths, actual, 'r', wavelengths, corrected, 'blue', linewidth=2.0)
    # Combine all the operations and display
    plt.show()

def planck(wavelength, temp):
    #temp in kelvin
    #print(wavelength)
    h = 6.62607015 * (10**(-34)) #planck's constant: m2 kg / s
    k = 1.380649 * (10**(-23)) #boltzmann constant: m2 kg s-2 K-1
    c = 299792458 #speed of light: m/s
    y1 = (2*h*c**2)/(wavelength**5)
    y2 = 1/(math.exp((h*c)/(k*temp*wavelength))-1)
    y = y1*y2
    return y

def ideal():
    #wavelengths for ideal, with spacing equal to experimental (list)
    temp = 1363.2 #in units of kelvin with +/- 0.1K
    wavelengths = np.linspace(3*10**-7, 8*10**-7, num=2047)
    intensities = []
    for wave in wavelengths:
        y = planck(wave, temp)
        intensities.append(y)
    return (wavelengths,intensities)
    
#plot ideal using ideal_wl, ideal_int = ideal()
def id_plot(wavelengths, intensities):
    f = plt.figure()
    ax = f.add_subplot()
    plt.plot(wavelengths, intensities, linewidth=2.0)
    plt.show()
    return

def black_body(file):
    wavelengths = []
    intensities = []
    with open(file) as f:
        for extra in range(14):
            next(f)
        for row in f:
            data = row.split()
            number0 = float(data[0])
            number1 = float(data[1])
            wavelengths.append(number0)
            intensities.append(number1)
            
    return (wavelengths,intensities)

def plot(wavelengths, intensities):
    lim = max(intensities)

    f = plt.figure()
    ax = f.add_subplot()
    ax.set(xlim=(340, 805),
           ylim=(0,lim+100))
    x_axis_spacing = np.arange(350, 805, 50, dtype=int)
    ax.set_xticks(x_axis_spacing)
    plt.plot(wavelengths, intensities, linewidth=2.0)
    plt.show()
    return

# Inputs: ideal list of y values
#         experimental list of y values
#         super saturated wavelength to have multiplicity of 1 after these
def correction(ideal, exp, sswvl):
    #normalize
    index = exp[0].index(sswvl)
    ideal = np.array(ideal[1])
    exp_i = np.array(exp[1])
    max_id = np.max(ideal)
    max_exp = np.max(exp_i)
    print(max_exp, max_id)
    ideal = np.divide(ideal, max_id)
    exp_i = np.divide(exp_i, max_exp)
    #replace the intensities after the cutoff to 1, so it does not have any affect when multiplying
    for i in range(len(ideal)):
        if (i >= index):
            ideal[i] = 1
            exp_i[i] = 1
    exp_i[exp_i == 0] = 1
    correction_lst = np.divide(ideal,exp_i)
    #print(correction_lst[1000:])
    #correction_lst = np.array(correction_lst)
    correction_lst[correction_lst == 0] = 1
    return correction_lst
    

if __name__=="__main__":
    main()
