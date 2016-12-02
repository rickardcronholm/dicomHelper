import dicom
import numpy as np


def cast_gamma_as_RD(dcm, gamma, coords):
    gamma = np.transpose(gamma, (2, 1, 0))
    if int(dcm.Rows) != int(gamma.shape[1]) or int(dcm.Columns) != int(gamma.shape[2]) or int(dcm.NumberOfFrames) != int(gamma.shape[0]):
        dcm.Rows = gamma.shape[1]
        dcm.Columns = gamma.shape[2]
        dcm.NumberOfFrames = gamma.shape[0]
        dcm.ImagePositionPatient = map(str, [coords[0][0], coords[1][0], coords[2][0]])
        dcm.GridFrameOffsetVector = map(str, [x - coords[2][0] for x in coords[2].tolist()])

    # set dose type and pixel representation
    dcm.DoseType = 'ERROR'
    # convert to uint32 using dcm.DoseGridScaling
    unwVal = 0.0  # value to set unwanted elements to
    gamma[gamma < 0] = unwVal  # get rid of negative values
    gamma[np.isinf(gamma)] = unwVal  # set inf to value
    gamma = (gamma / float(dcm.DoseGridScaling)).astype('uint32')

    # PixelData
    dcm.PixelData = gamma.tostring()

    #update UID
    dcm.SOPInstanceUID = dicom.UID.generate_uid()

    return dcm