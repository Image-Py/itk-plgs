from imagepy.core.util import fileio
from imagepy.core.manager import ReaderManager, WriterManager
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

ReaderManager.add('dcm', read)
WriterManager.add('dcm', write)

class OpenDCM(fileio.Reader):
	title = 'DICOM Open'
	filt = ['dcm']

class SaveDCM(fileio.Writer):
	title = 'DICOM Save'
	filt = ['dcm']

ReaderManager.add('ima', read)
WriterManager.add('ima', write)

class OpenIMA(fileio.Reader):
	title = 'IMA Open'
	filt = ['ima']

class SaveIMA(fileio.Writer):
	title = 'IMA Save'
	filt = ['ima']

ReaderManager.add('nii', readall, tag='imgs')
WriterManager.add('nii', write, tag='imgs')
ReaderManager.add('nii.gz', readall, tag='imgs')
WriterManager.add('nii.gz', write, tag='imgs')

class OpenNII(fileio.Reader):
	title = 'NII Open'
	filt = ['nii', 'nii.gz']

class SaveNII(fileio.Writer):
	title = 'NII Save'
	filt = ['nii', 'nii.gz']

plgs = [OpenDCM, SaveDCM, '-', OpenIMA, SaveIMA, '-', OpenNII, SaveNII]
