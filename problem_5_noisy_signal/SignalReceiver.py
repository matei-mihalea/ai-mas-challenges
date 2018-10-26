import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

parser = argparse.ArgumentParser(description='Test number')
parser.add_argument('test_no', metavar='N', type=int, help='Test number.')


class SignalReceiver:
	def __init__(self, test_no):
		assert 1 <= test_no <= 5, "Invalid test number."
		f_real = open('Tests/Test' + str(test_no) + '_real')
		f_noisy = open('Tests/Test' + str(test_no))

		self.__noisy_values = [float(i) for i in f_noisy.readlines()]
		self.__real_values = [float(i) for i in f_real.readlines()]
		self.__c_index = 0
		self.__total_error = 0

	def get_value(self):
		'''
		Gets next noisy value from device. This must be called before push_value.
		:return: (float) device value, None if the device is closed.
		'''
		if self.__c_index >= len(self.__noisy_values):
			return None

		val = self.__noisy_values[self.__c_index]
		self.__c_index = self.__c_index + 1
		return val

	def push_value(self, c_val):
		'''
		Computes the error between the real signal and the corrected value.
		:param c_val: corrected value.
		:return: (float) error value, None if the device is closed.
		'''

		if self.__c_index - 1 >= len(self.__real_values):
			return None

		error = abs(self.__real_values[self.__c_index - 1] - c_val)
		self.__total_error += error
		return error

	def get_error(self):
		return self.__total_error

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

if __name__ == "__main__":
	'''
	Dumb example of usage.
	'''
	args = parser.parse_args()
	sr = SignalReceiver(args.test_no)



	vals = []
	index_vals = [0]
	count = 1

	i_val = sr.get_value()
	vals.append(i_val)

	while i_val:
		ret_val = i_val

		if count > 51:
			size = count
			if count % 2 == 0:
				size = count - 1
			vals_aprox = savgol_filter(vals, 51, 3) # window size 51, polynomial order 3

			
			ret_val = (vals_aprox[count-1] + vals[len(vals)-1]) / 2 # medie valoare reala si valoare aproximare
			

		print(sr.push_value(ret_val))
		i_val = sr.get_value()

		count += 1
		vals.append(i_val)

		if count > 100:
			count -= 1
			vals.pop(0)
	print('Total error: ' + str(sr.get_error()))
