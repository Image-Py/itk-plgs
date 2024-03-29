# -*- coding: utf-8 -*
import SimpleITK as sitk
from sciapp.action import Filter, Simple
import numpy as np

class CannyMagnitude(Filter):
	title = 'ITK Canny EdgeDetection'
	note = ['all', 'auto_msk', 'auto_snap', '2float', 'preview']
	para = {'sigma':1.0, 'low_threshold':10, 'high_threshold':20}
	view = [(float, 'sigma', (0,10), 1,  'sigma', 'pix'),
			('slide', 'low_threshold', (0,50), 4, 'low_threshold'),
			('slide', 'high_threshold', (0,50), 4, 'high_threshold')]

	def run(self, ips, snap, img, para = None):
		img = sitk.GetImageFromArray(snap)
		img = sitk.CannyEdgeDetection(img, para['low_threshold'], para['high_threshold'], [para['sigma']]*2)
		return sitk.GetArrayFromImage(img)*ips.range[1]

plgs = [CannyMagnitude]