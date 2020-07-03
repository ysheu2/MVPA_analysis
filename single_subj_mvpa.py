#!/usr/bin/env python

import sys
if (sys.argv.__len__() < 2):
    print "\n\tusage: mvpa.py <subject>\n\n"
    sys.exit()
else:
    subject = sys.argv[1]

print "Subject is " + subject

#start pymvpa
from mvpa2.tutorial_suite import *
import numpy as np
import os
from glob import glob
import tempfile, shutil

#define where is the directory for all the data
datapath = '/Users/yishin/Documents/MVPA_analysis'

#define the subject folder
path = os.path.join(datapath, subject)

#load the attributes.txt
attr = SampleAttributes(os.path.join(datapath, 'attribute_miniblocks_rule_1.txt'))

#load the dataset and assign targets, chunks, and a mask
ds = fmri_dataset(samples=os.path.join(path,'beta_rule_sm.nii.gz'),targets=attr.targets,chunks=attr.chunks, mask=os.path.join(path,'IFG_liberal_binary_mask.nii'))

#check the shape of the dataset
print ds.shape

#detrend the data
poly_detrend(ds, polyord= 1, chunks_attr='chunks')

#save a copy of the detrended data
#orig_ds = ds.copy()

#np.std(ds.samples, axis=0.001) == 0

#z-score each feature, using the mean and sdv from the rest condition as baseline
#zscore(ds, param_est=('targets', ['5']))
#zscore(ds, chunks_attr='chunks')
#zscore(ds)

#find events
events = find_events(targets=ds.sa.targets, chunks=ds.sa.chunks)

#use only 'sem' and 'pho' samples from dataset
events = [ev for ev in events if ev['targets'] in ['1', '2']]

#modify event start
#for ev in events: ev['onset'] += 3

#modify event duration (to see what happens after even is over)
#for ev in events: ev['duration'] = 3

#segment the original time series dataset into event related samples
evds = eventrelated_dataset(ds, events=events)

#print evds
print evds.shape

#feature selection
fsel = SensitivityBasedFeatureSelection(OneWayAnova(),FractionTailSelector(0.8, mode='select', tail='upper'))


#define the classifier and partitioner
clf = LinearCSVMC() #SMLR(lm=0.01) #LinearNuSVMC(probability=1)
partitioner = NFoldPartitioner()

#Do feature selection on the training data only
fclf = FeatureSelectionClassifier(clf,fsel)

# how often do we want to shuffle the data
repeater = Repeater(count=500)

# permute the training part of a dataset exactly ONCE
permutator = AttributePermutator('targets', limit={'partitions': 1}, count=1)

# CV with null-distribution estimation that permutes the training data for each fold independently
null_cv = CrossValidation(fclf,ChainNode([partitioner, permutator], space=partitioner.get_space()),postproc=mean_sample())

# Monte Carlo distribution estimator
distr_est = MCNullDist(repeater, tail='left', measure=null_cv,enable_ca=['dist_samples'])

#Cross validation
#cvte = CrossValidation(fclf, splitter,enable_ca=['stats'])

# actual CV with H0 distribution estimation
cvte = CrossValidation(fclf, partitioner, postproc=mean_sample(),null_dist=distr_est, enable_ca=['stats'])

#apply the cross validation process on the evds
err = cvte(evds)

#print monte carlo results

print 'CV-accuracy:', 1-np.ravel(err)
p = cvte.ca.null_prob
print 'Corresponding p-value:', np.asscalar(p)

#ts = err.a.mapper.reversel(1-err.samples[0])
#map2nifti(ds,ts).to_filename('test_mapping.nii.gz')

#plotting
def make_null_dist_plot(dist_samples,empirical): pl.hist(dist_samples,bins=20,normed=True,alpha=0.8), pl.axvline(empirical,color='red'), pl.axvline(0.5,color='black',ls='--'), pl.xlim(0,1), pl.xlabel('Average cross-validated classification error')
__ = pl.figure()
make_null_dist_plot(np.ravel(cvte.null_dist.ca.dist_samples),np.asscalar(err))
pl.show()


def make_null_dist_plot(dist_samples,empirical): pl.hist(dist_samples,bins=20,normed=True,alpha=0.8), pl.axvline(empirical,color='red'), pl.axvline(0.5,color='black',ls='--'), pl.xlim(0,1), pl.xlabel('Average cross-validated classification error')
__ = pl.figure()
make_null_dist_plot(np.ravel(cv.null_dist.ca.dist_samples),np.asscalar(err))
pl.show()


print np.round(cvte.ca.stats.stats['ACC'],4)
print cvte.ca.stats.matrix
p = cvte.ca.null_prob
print np.asscalar(p)


#make_null_dist_plot(cvte.null_dist.ca.dist_samples, np.asscalar(err))

#sclf = SplitClassifier(fclf,enable_ca=['stats'])
#cv_sensana = sclf.get_sensitivity_analyzer()
#sens = cv_sensana(evds)
#print cv_sensana.clf.ca.stats.matrix

#sens_comb = sens.get_mapped(maxofabs_sample())
#map2nifti(ds,sens_comb).to_filename('test_mapping.nii.gz')





