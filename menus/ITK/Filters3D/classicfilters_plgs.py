# -*- coding: utf-8 -*
import SimpleITK as sitk
from sciapp.action import Filter, Simple
import numpy as np

class DiscreteGaussian3D(Simple):
	title = 'ITK Discrete Gaussian 3D'
	note = ['all', 'stack3d']
	para = {'sigma':1.0}
	view = [(float, 'sigma', (0,10), 1, 'sigma', 'pix')]

	def run(self, ips, imgs, para = None):
		itkimgs = sitk.GetImageFromArray(imgs)
		itkimgs = sitk.DiscreteGaussian(itkimgs, para['sigma'])
		imgs[:] = sitk.GetArrayFromImage(itkimgs)
		
class GradientMagnitude3D(Simple):
	title = 'ITK Gradient Magnitude 3D'
	note = ['all', 'stack3d']

	def run(self, ips, imgs, para = None):
		itkimgs = sitk.GetImageFromArray(imgs)
		itkimgs = sitk.GradientMagnitude(itkimgs)
		imgs[:] = sitk.GetArrayFromImage(itkimgs)

plgs = [DiscreteGaussian3D, GradientMagnitude3D]