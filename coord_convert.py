#!/usr/bin/env python


import math
import numpy as np
 

def convert_coord(lat,lon):

	# Convert latitude and longitude to   
	# spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0

	# coordonnes du point traduire
	phi = lat * degrees_to_radians
	l = lon * degrees_to_radians

	# variables
	# systme WGS84
	a = 6378137				# demi grand axe de l ellipsoide (m)
	e = 0.08181919106		# premire excentricit de l ellipsoide
	f = 1/298.257223563		# Inverse flattening
	N0 = 0					# 0 for North and 10 000 km for south
	k0 = 0.9996
	E0 = 500000

	# paramtres de projections
	l0 = -81 * degrees_to_radians		# longitude de rfrence

	# preliminary values
	n = f / (2 - f)
	A = a / (1 + n) * (1 + n*n/4 + n*n*n*n/64 + n*n*n*n*n*n/256)

	alpha1 = 1/2 * n - 2/3 * n*n + 5/16 * n*n*n
	alpha2 = 13/48 * n*n - 5/3 * n*n*n
	alpha3 = 61/240 * n*n*n

	t = np.sinh(np.arctanh(np.sin(phi)) - 2*np.sqrt(n)/(1+n) * np.arctanh(2*np.sqrt(n)/(1+n)*np.sin(phi)))
	eta = np.arctanh(np.sin(l-l0)/np.sqrt(1+t*t))
	xi = np.arctan(t/np.cos(l-l0))

	#UTM coordinates
	E = E0 + k0*A * (eta + alpha1 * np.cos(2*xi)*np.sinh(2*eta) + alpha2 * np.cos(2*2*xi)*np.sinh(2*2*eta) + alpha3 * np.cos(2*3*xi)*np.sinh(2*3*eta))
	N = N0 + k0*A * (xi + alpha1 * np.sin(2*xi)*np.cosh(2*eta) + alpha2 * np.sin(2*2*xi)*np.cosh(2*2*eta) + alpha3 * np.sin(2*3*xi)*np.cosh(2*3*eta))	

	return E,N


def convert_proj(X,Y):

	# convert latitude and longitude to   
	# spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0

	# variables
	# systme WGS84
	a = 6378137				# demi grand axe de l ellipsoide (m)
	e = 0.08181919106		# premire excentricit de l ellipsoide
	f = 1/298.257223563		# Inverse flattening
	N0 = 0					# 0 for North and 10 000 km for south
	k0 = 0.9996
	E0 = 500000

	# paramtres de projections
	l0 = -81 * degrees_to_radians		# longitude de rfrence

	# preliminary values
	n = f / (2 - f)
	A = a / (1 + n) * (1 + n*n/4 + n*n*n*n/64 + n*n*n*n*n*n/256)

	beta1 = 1/2 * n - 2/3 * n*n + 37/96 * n*n*n
	beta2 = 1/48 * n*n + 1/15 * n*n*n
	beta3 = 17/480 * n*n*n

	delta1 = 2 * n - 2/3 * n*n - 2 * n*n*n
	delta2 = 7/3 * n*n - 8/5 * n*n*n
	delta3 = 56/15 * n*n*n

	eta = (Y - N0) / (k0 * A)
	nu = (X - E0) / (k0 * A)

	eta_p = eta - ( beta1*np.sin(2*1*eta)*np.cosh(2*1*nu) + beta2*np.sin(2*2*eta)*np.cosh(2*2*nu) + beta3*np.sin(2*3*eta)*np.cosh(2*3*nu) ) 
	nu_p = nu - ( beta1*np.cos(2*1*eta)*np.sinh(2*1*nu) + beta2*np.cos(2*2*eta)*np.sinh(2*2*nu) + beta3*np.cos(2*3*eta)*np.sinh(2*3*nu) )

	xi = np.arcsin( np.sin(eta_p) / np.cosh(nu_p) )

	# lat/lon coordinates
	
	phi = xi + ( delta1*np.sin(2*1*xi) + delta2*np.sin(2*2*xi) + delta3*np.sin(2*3*xi) )
	l = l0 + np.arctan( np.sinh(nu_p) / np.cos(eta_p) )

	# coordonnes du point traduire
	lat = phi/degrees_to_radians
	lon = l/degrees_to_radians

	return lat, lon

