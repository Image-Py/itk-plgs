# -*- coding: utf-8 -*
import SimpleITK as sitk
from sciapp.action import Filter, Simple
import numpy as np

class GradientMagnitude(Filter):
	title = 'ITK Gradient Magnitude'
	note = ['all', 'auto_msk', 'auto_snap']

	def run(self, ips, snap, img, para = None):
		img = sitk.GetImageFromArray(img)
		img = sitk.GradientMagnitude(img)
		return sitk.GetArrayFromImage(img)

class DiscreteGaussian(Filter):
	title = 'ITK Discrete Gaussian'
	note = ['all', 'auto_msk', 'auto_snap', 'preview']
	para = {'sigma':1.0}
	view = [(float, 'sigma', (0,10), 1,  'sigma', 'pix')]

	def run(self, ips, snap, img, para = None):
		itkimg = sitk.GetImageFromArray(snap)
		itkimg = sitk.DiscreteGaussian(itkimg, para['sigma'])
		return sitk.GetArrayFromImage(itkimg)

plgs = [GradientMagnitude, DiscreteGaussian]