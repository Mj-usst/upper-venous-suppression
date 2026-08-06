# DICOM/PACS deployment workflow

A local institutional deployment may use the following workflow:

1. receive the MRL DICOM series from the scanner or PACS;
2. convert the selected MRL phase to the nnU-Net input format;
3. run venous-mask prediction;
4. generate venous-suppressed and venous-highlighted outputs;
5. preserve image orientation, voxel spacing, and slice-position metadata;
6. export the processed images as derived DICOM series with new series identifiers;
7. retain the original clinical series unchanged.

Hospital-specific PACS settings, including AE titles, network addresses, ports, authentication information, and routing rules, are not included.
