# Tracking Software

## 3D Suite

### Creating 3D model
Currently done manually. trufi 3D coronal iso1 ref DICOM are exported to USB and into Slicer.

In Slicer the following settings are applied
- Filtering - Denoising - Median Image Filter 2,2,2
- Segment Editor - Either use only Thresholding, or grow from seeds.
- Export to STL, replace or add file in STL_MODEL folder. The program loads the latest (most up to date) file in the folder.