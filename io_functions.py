#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:45:42 2019

@author: miguel
"""
import numpy as np
from astropy.io import fits
import sys


class Read:
    def __init__(self, I_cube_name="", Q_cube_name="", U_cube_name="", freq_file_name="", numpy_file=""):
        self.I_cube_name = I_cube_name
        self.Q_cube_name = Q_cube_name
        self.U_cube_name = U_cube_name
        self.freq_file_name = freq_file_name
        self.numpy_file = numpy_file
    # this has to be separated

    def readCube(self, file="", memmap=False):
        try:
            hdu = fits.open(file, memmap=memmap)
        except FileNotFoundError:
            print("FileNotFoundError: The I FITS file cannot be found")
            sys.exit(1)

        print("FITS shape: ", hdu[0].data.shape)

        image = hdu[0].data
        hdu.close()
        return image

    def readIQU(self, memmap=False):
        files = [self.I_cube_name, self.Q_cube_name, self.U_cube_name]
        IQU = []
        for file in files:
            IQU.append(self.readCube(file=file, memmap=memmap))

        return IQU[0], IQU[1], IQU[2]



    def readNumpyFile(self):
        try:
            np_array = np.load(self.numpy_file)
        except FileNotFoundError:
            print("FileNotFoundError: The numpy file cannot be found")
            sys.exit(1)

        Q = np_array[:, :, 0]
        U = np_array[:, :, 1]

        return Q, U

    def readHeader(self):
        f_filename = self.Q_cube_name
        hdul_image = fits.open(name=f_filename)
        header = hdul_image[0].header
        hdul_image.close()
        return header

    def getFileNFrequencies(self):
        f_filename = self.freq_file_name
        try:
            with open(f_filename, "r") as f:
                freqs = f.readlines()
                freqs[:] = [freq.rstrip("\n") for freq in freqs]
                freqs[:] = [float(freq) for freq in freqs]
                f.close()
        except:
            print("Cannot open file")
            sys.exit(1)
        freqs = np.array(freqs)
        return freqs

    def readFreqsNumpyFile(self):
    	filename = self.freq_file_name
    	freqs = np.load(filename)
    	return freqs


class Write:

    def __init__(self, output=""):
        self.output = output

    def writeCube(self, cube, header, nphi, phi, dphi, memmap=False):
        header['NAXIS3'] = (nphi, 'Length of Faraday depth axis')
        header['CTYPE3'] = 'Phi'
        header['CDELT3'] = dphi
        header['CUNIT3'] = 'rad/m/m'
        header['CRVAL3'] = phi[0]
	
        fits.writeto(self.output, data=cube, header=header,overwrite=True)
 
