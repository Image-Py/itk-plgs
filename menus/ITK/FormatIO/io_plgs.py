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
	filt = ['DCM']

class SaveDCM(fileio.Writer):
	title = 'DICOM Save'
	filt = ['DCM']

ReaderManager.add('nii', (readall,))
WriterManager.add('nii', (write,))
class OpenNII(fileio.Reader):
	title = 'NII Open'
	filt = ['NII']

class SaveNII(fileio.Reader):
	title = 'NII Save'
	filt = ['NII']

plgs = [OpenDCM, SaveDCM, '-', OpenNII, SaveNII]