from sciapp.action import dataio
import SimpleITK as sitk
import numpy as np

def readall(path):
	image = sitk.ReadImage(path)
	arr = sitk.GetArrayFromImage(image)
	if arr.dtype == np.int16:
		arr = arr.astype(np.int32)
	return arr

def read(path):return readall(path)[0]

def write(path, img):
	sitk.WriteImage(sitk.GetImageFromArray(img), path)

dataio.ReaderManager.add('dcm', read, 'img')
dataio.WriterManager.add('dcm', write, 'img')

class OpenDCM(dataio.Reader):
	title = 'DICOM Open'
	tag = 'img'
	filt = ['dcm']

class SaveDCM(dataio.ImageWriter):
	title = 'DICOM Save'
	tag = 'img'
	filt = ['dcm']

dataio.ReaderManager.add('ima', read, 'img')
dataio.WriterManager.add('ima', write, 'img')

class OpenIMA(dataio.Reader):
	title = 'IMA Open'
	tag = 'img'
	filt = ['ima']

class SaveIMA(dataio.ImageWriter):
	title = 'IMA Save'
	tag = 'img'
	filt = ['ima']

dataio.ReaderManager.add('nii', readall, 'imgs')
dataio.WriterManager.add('nii', write, 'imgs')
dataio.ReaderManager.add('nii.gz', readall, 'imgs')
dataio.WriterManager.add('nii.gz', write, 'imgs')

class OpenNII(dataio.Reader):
	title = 'NII Open'
	tag = 'imgs'
	filt = ['nii', 'nii.gz']

class SaveNII(dataio.ImageWriter):
	title = 'NII Save'
	tag = 'imgs'
	filt = ['nii', 'nii.gz']

plgs = [OpenDCM, SaveDCM, '-', OpenIMA, SaveIMA, '-', OpenNII, SaveNII]
