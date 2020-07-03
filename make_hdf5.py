from mvpa2.tutorial_suite import *
import numpy as np
import os
from glob import glob
import tempfile, shutil

#define where is the directory for all the data
datapath = 'Directory/MVPA_analysis'

#define the subject folder
path = os.path.join(datapath)

#load the attributes.txt
attr = SampleAttributes(os.path.join(datapath, 'attribute_miniblocks_feature_1.txt'))
attr2 = SampleAttributes(os.path.join(datapath, 'attribute_miniblocks_feature_2.txt'))

#load the dataset and assign targets, chunks, and a mask
ds1 = fmri_dataset(samples=os.path.join('subj101','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj101','IFG_binary_mask.nii'))
ds2 = fmri_dataset(samples=os.path.join('subj102','beta_feature_sm.nii.gz'),targets=attr2.targets,chunks=attr2.chunks, mask=os.path.join('subj102','IFG_binary_mask.nii'))
ds3 = fmri_dataset(samples=os.path.join('subj103','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj103','IFG_binary_mask.nii'))
ds4 = fmri_dataset(samples=os.path.join('subj105','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj105','IFG_binary_mask.nii'))
ds5 = fmri_dataset(samples=os.path.join('subj106','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj106','IFG_binary_mask.nii'))
ds6 = fmri_dataset(samples=os.path.join('subj107','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj107','IFG_binary_mask.nii'))
ds7 = fmri_dataset(samples=os.path.join('subj108','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj108','IFG_binary_mask.nii'))
ds8 = fmri_dataset(samples=os.path.join('subj109','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj109','IFG_binary_mask.nii'))
ds9 = fmri_dataset(samples=os.path.join('subj110','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj110','IFG_binary_mask.nii'))
ds10 = fmri_dataset(samples=os.path.join('subj113','beta_feature_sm.nii.gz'),targets=attr2.targets,chunks=attr2.chunks, mask=os.path.join('subj113','IFG_binary_mask.nii'))
ds11 = fmri_dataset(samples=os.path.join('subj114','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj114','IFG_binary_mask.nii'))
ds12 = fmri_dataset(samples=os.path.join('subj115','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj115','IFG_binary_mask.nii'))
ds13 = fmri_dataset(samples=os.path.join('subj116','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj116','IFG_binary_mask.nii'))
ds14 = fmri_dataset(samples=os.path.join('subj117','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj117','IFG_binary_mask.nii'))
ds15 = fmri_dataset(samples=os.path.join('subj121','beta_feature_sm.nii.gz'),targets=attr2.targets,chunks=attr2.chunks, mask=os.path.join('subj121','IFG_binary_mask.nii'))
ds16 = fmri_dataset(samples=os.path.join('subj122','beta_feature_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj122','IFG_binary_mask.nii'))


h5save('/Users/yishin/Documents/MVPA_analysis/hdf5_IFG_feature', [ds1, ds2, ds3, ds4, ds5, ds6, ds7, ds8, ds9, ds10, ds11, ds12, ds13, ds14, ds15, ds16])




from mvpa2.tutorial_suite import *
import numpy as np
import os
from glob import glob
import tempfile, shutil

#define where is the directory for all the data
datapath = '/Users/yishin/Documents/MVPA_analysis'

#define the subject folder
path = os.path.join(datapath)

#load the attributes.txt
attr = SampleAttributes(os.path.join(datapath, 'attribute_miniblocks_rule_1.txt'))
attr2 = SampleAttributes(os.path.join(datapath, 'attribute_miniblocks_rule_2.txt'))

#load the dataset and assign targets, chunks, and a mask
ds1 = fmri_dataset(samples=os.path.join('subj101','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj101','IFG_liberal_binary_mask.nii'))
ds2 = fmri_dataset(samples=os.path.join('subj102','beta_rule_sm.nii.gz'),targets=attr2.targets,chunks=attr2.chunks, mask=os.path.join('subj102','IFG_liberal_binary_mask.nii'))
ds3 = fmri_dataset(samples=os.path.join('subj103','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj103','IFG_liberal_binary_mask.nii'))
ds4 = fmri_dataset(samples=os.path.join('subj105','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj105','IFG_liberal_binary_mask.nii'))
ds5 = fmri_dataset(samples=os.path.join('subj106','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj106','IFG_liberal_binary_mask.nii'))
ds6 = fmri_dataset(samples=os.path.join('subj107','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj107','IFG_liberal_binary_mask.nii'))
ds7 = fmri_dataset(samples=os.path.join('subj108','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj108','IFG_liberal_binary_mask.nii'))
ds8 = fmri_dataset(samples=os.path.join('subj109','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj109','IFG_liberal_binary_mask.nii'))
ds9 = fmri_dataset(samples=os.path.join('subj110','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj110','IFG_liberal_binary_mask.nii'))
ds10 = fmri_dataset(samples=os.path.join('subj113','beta_rule_sm.nii.gz'),targets=attr2.targets,chunks=attr2.chunks, mask=os.path.join('subj113','IFG_liberal_binary_mask.nii'))
ds11 = fmri_dataset(samples=os.path.join('subj114','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj114','IFG_liberal_binary_mask.nii'))
ds12 = fmri_dataset(samples=os.path.join('subj115','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj115','IFG_liberal_binary_mask.nii'))
ds13 = fmri_dataset(samples=os.path.join('subj116','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj116','IFG_liberal_binary_mask.nii'))
ds14 = fmri_dataset(samples=os.path.join('subj117','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj117','IFG_liberal_binary_mask.nii'))
ds15 = fmri_dataset(samples=os.path.join('subj121','beta_rule_sm.nii.gz'),targets=attr2.targets,chunks=attr2.chunks, mask=os.path.join('subj121','IFG_liberal_binary_mask.nii'))
ds16 = fmri_dataset(samples=os.path.join('subj122','beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join('subj122','IFG_liberal_binary_mask.nii'))


h5save('/Users/yishin/Documents/MVPA_analysis/hdf5_n16', [ds1, ds2, ds3, ds4, ds5, ds6, ds7, ds8, ds9, ds11, ds12, ds13, ds14, ds15, ds16, ds10])
