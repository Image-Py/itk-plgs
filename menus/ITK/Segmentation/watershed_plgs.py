# -*- coding: utf-8 -*
import SimpleITK as sitk
from imagepy.core.engine import Filter, Simple
import numpy as np

class UPWatershed(Filter):
	title = 'ITK Up Down Watershed'
	note = ['all', 'auto_msk', 'auto_snap', 'preview']
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
	def run(self, ips, snap, img, para = None):
		itkimgs = sitk.GetImageFromArray(img)
		itkimgs = sitk.GradientMagnitude(itkimgs)
		msk = np.zeros_like(img)
		msk[img>para['thr2']] = 1
		msk[img<para['thr1']] = 2
		itkmarker = sitk.GetImageFromArray(msk)
		lineimg = sitk.MorphologicalWatershedFromMarkers(itkimgs, itkmarker)
		rst = sitk.GetArrayFromImage(lineimg)
		ips.lut = self.buflut
		return np.where(rst==1, ips.range[1], 0)

class WatershedRoi(Filter):
	title = 'ITK Watershed Manual Marker'
	note = ['8-bit', 'not_slice', 'auto_snap', 'req_roi']
	
	para = {'sigma':2}
	view = [(int, (0,10), 0,  'sigma', 'sigma', 'pix')]
	
	def run(self, ips, snap, img, para = None):
		itkimg = sitk.GetImageFromArray(img)
		itkimg = sitk.DiscreteGaussian(itkimg, para['sigma'])
		itkimg = sitk.GradientMagnitude(itkimg)
		itkmarker = sitk.GetImageFromArray(ips.get_msk().astype(np.uint16))
		itkmarker = sitk.ConnectedComponent(itkmarker, fullyConnected=True)
		lineimg = sitk.MorphologicalWatershedFromMarkers(itkimg, itkmarker, markWatershedLine=True)
		labels = sitk.GetArrayFromImage(lineimg)
		return np.where(labels==0, ips.range[1], 0)

plgs = [UPWatershed, WatershedRoi]