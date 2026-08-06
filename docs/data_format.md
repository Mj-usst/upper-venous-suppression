# Data format

LympClear follows the nnU-Net v2 data convention.

## Folder structure

```text
nnUNet_raw/
└── Dataset038_finetune127/
    ├── dataset.json
    ├── imagesTr/
    │   ├── case001_0000.nii.gz
    │   └── case002_0000.nii.gz
    ├── labelsTr/
    │   ├── case001.nii.gz
    │   └── case002.nii.gz
    └── imagesTs/
        └── case101_0000.nii.gz
```

## Channel and label definitions

The input contains one postcontrast T1-weighted MRL channel:

```json
{
  "channel_names": {"0": "postcontrast_T1w_MRL"},
  "labels": {"background": 0, "vein": 1},
  "file_ending": ".nii.gz"
}
```

## Dynamic phases

All dynamic phases from the same patient must remain in the same training, validation, or test partition to prevent information leakage. Phase 6 corresponds to the 30-minute postcontrast acquisition when phase 0 is precontrast.

## Privacy

Clinical images, manual masks, and patient-level metadata must be stored outside the repository.
