# Training protocol

## Lower-extremity pretraining

The source-domain model is trained with 3D nnU-Net using the lower-extremity dataset:

```text
Dataset025_leg
fold_0
checkpoint_best.pth
```

## Upper-extremity training from scratch

```bash
bash scripts/03_train_scratch.sh \
  --dataset-id 29 \
  --fold 0 \
  --config 3d_fullres
```

## Upper-extremity fine-tuning

```bash
bash scripts/04_finetune_from_lower_limb.sh \
  --target-dataset-id 38 \
  --fold 0 \
  --config 3d_fullres \
  --pretrained-checkpoint "$nnUNet_results/Dataset025_leg/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_0/checkpoint_best.pth"
```

The fine-tuning command uses:

```text
nnUNetv2_train TARGET_DATASET_ID 3d_fullres 0 -pretrained_weights PRETRAINED_CHECKPOINT
```

Learning-curve experiments use upper-extremity training subsets of 1, 2, 5, 10, 20, 40, 80, and 127 patients. All dynamic phases from the same patient must remain in the same partition.
