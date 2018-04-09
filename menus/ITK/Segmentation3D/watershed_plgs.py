# -*- coding: utf-8 -*
import SimpleITK as sitk
from imagepy.core.engine import Filter, Simple
import numpy as np

class UPWatershed(Simple):
	title = 'ITK Up Down Watershed 3D'
	note = ['all', 'stack3d', 'preview']
	modal = False

	def load(self, ips):
		minv, maxv = ips.range
		self.para = {'thr1':minv, 'thr2':maxv}
		self.view = [('slide', (minv, maxv), 4, 'Low', 'thr1'),
			('slide', (minv,maxv), 4, 'High', 'thr2')]
		self.buflut = ips.lut
		ips.lut = ips.lut.copy()
		return True

	def cancel(self, ips):
		ips.lut = self.buflut
		ips.update = 'pix'

	def preview(self, ips, para):
		ips.lut[:] = self.buflut
		minv, maxv = ips.range
		lim1 = (para['thr1']-minv)*255/(maxv-minv)
		lim2 = (para['thr2']-minv)*255/(maxv-minv)
		ips.lut[:int(lim1)] = [0,255,0]
		ips.lut[int(lim2):] = [255,0,0]
		ips.update = 'pix'

	#process
	def run(self, ips, imgs, para = None):
		itkimgs = sitk.GetImageFromArray(imgs)
		itkimgs = sitk.GradientMagnitude(itkimgs)
		msk = np.zeros_like(imgs)
		msk[imgs>para['thr2']] = 1
		msk[imgs<para['thr1']] = 2
		itkmarker = sitk.GetImageFromArray(msk)
		lineimg = sitk.MorphologicalWatershedFromMarkers(itkimgs, itkmarker)
		rst = sitk.GetArrayFromImage(lineimg)
		ips.lut = self.buflut
		imgs[:] = np.where(rst==1, ips.range[1], 0)

plgs = [UPWatershed]