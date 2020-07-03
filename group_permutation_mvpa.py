#!/usr/bin/env python

# acc1 = (perm1_subj1 + perm1_subj2 + prm1_subjN)/n (n is the
#start pymvpa
#remember to use ipython not python
from mvpa2.tutorial_suite import *
from mvpa2.suite import *
import numpy as np
import os
from glob import glob
import tempfile, shutil

#define where is the directory for all the data
datapath = '/Users/yishin/Documents/MVPA_analysis'

#define the file path for the hdf5 data
filepath = '/Users/yishin/Documents/MVPA_analysis/hdf5_IFG_feature'

#load the hdf5 data
ds_all = h5load(filepath)

#detrend the data
#_ = [poly_detrend(ds, polyord= 1, chunks_attr='chunks') for ds in ds_all]
#poly_detrend(ds, polyord= 1, chunks_attr='chunks')

#save a copy of the detrended data
#orig_ds = ds.copy()

#np.std(ds.samples, axis=0.001) == 0

#z-score each feature, using the mean and sdv from the rest condition as baseline
#zscore(ds, param_est=('targets', ['5']))
#zscore(ds, chunks_attr='chunks')
#zscore(ds)
_ = [zscore(ds) for ds in ds_all]


# inject the subject ID into all datasets
for i,sd in enumerate(ds_all):
    sd.sa['subject'] = np.repeat(i, len(sd))

# number of subjects
nsubjs = len(ds_all)
# number of categories
ncats = len(ds_all[0].UT)
# number of run
nruns = len(ds_all[0].UC)


#find events
#events = find_events(targets=ds.sa.targets, chunks=ds.sa.chunks)

#use only 'sem' and 'pho' samples from dataset
#events = [ev for ev in events if ev['targets'] in ['1', '2']]

#modify event start
#for ev in events: ev['onset'] += 3

#modify event duration (to see what happens after even is over)
#for ev in events: ev['duration'] = 3

#segment the original time series dataset into event related samples
#evds = eventrelated_dataset(ds, events=events)

#print evds
#print evds.shape

#define the classifier and partitioner
clf = LinearCSVMC() #SMLR(lm=0.01) #LinearNuSVMC(probability=1)

#define cv algorith (leave one run out)
partitioner = NFoldPartitioner(attr='chunks')

#feature selection
fsel = SensitivityBasedFeatureSelection(OneWayAnova(),FractionTailSelector(0.8, mode='select', tail='upper'))


#Do feature selection on the training data only
fclf = FeatureSelectionClassifier(clf,fsel)

# how often do we want to shuffle the data
repeater = Repeater(count=50)

# permute the training part of a dataset exactly ONCE
permutator = AttributePermutator('targets', limit={'partitions': 1}, count=1)

# CV with null-distribution estimation that permutes the training data for each fold independently
null_cv = CrossValidation(fclf,ChainNode([partitioner, permutator], space=partitioner.get_space()),postproc=mean_sample())

# Monte Carlo distribution estimator, MCNullDist will use the already created permutator to shuffle the targets and later on report the p-value from the left tail of the Null distribution, because we are going to compute errors and we are interested in them being lower than chance.
distr_est = MCNullDist(repeater, tail='left', measure=null_cv,enable_ca=['dist_samples'])

#Cross validation
#cvte = CrossValidation(fclf, splitter,enable_ca=['stats'])

# actual CV with H0 distribution estimation
cvte = CrossValidation(fclf, partitioner, postproc=mean_sample(),null_dist=distr_est, enable_ca=['stats'])

#cvte just for the accurate label, without bothering to permute
#cvte2 = CrossValidation(fclf, partitioner, enable_ca=['stats'])
#wsc_results = [cvte2(sd) for sd in ds_all]
#wsc_results = vstack(wsc_results)
#group_mean = np.mean(1-np.ravel(wsc_results))
#group_std = np.std(wsc_results) / np.sqrt(nsubjs - 1)

#apply the cross validation process on sd and store results in a sequence
wsc_results = [[cvte(sd), cvte.ca.null_prob, cvte.null_dist.ca.dist_samples] for sd in ds_all]

null_probs = [l[1] for l in wsc_results]
null_dists = [l[2] for l in wsc_results]
wsc_results = [l[0] for l in wsc_results]

wsc_results = vstack(wsc_results)
prob_results = vstack(null_probs)

#print group results to csv
np.savetxt('/Users/yishin/Documents/MVPA_analysis/prob_IPS_rule.csv', prob_results,delimiter=',')
np.savetxt('/Users/yishin/Documents/MVPA_analysis/acc_IPS_rule.csv', 1-np.ravel(wsc_results),delimiter=',')
np.savetxt('/Users/yishin/Documents/MVPA_analysis/null_IPS_rule.csv', null_dists,delimiter=',')

#print monte carlo results
print 'CV-accuracy:', 1-np.ravel(wsc_results)
print 'CV-grp-accuracy:', np.mean(1-np.ravel(wsc_results))
p = cvte.ca.null_prob
print 'Corresponding p-value:', np.asscalar(p)

#print performance
verbose(1, "Average classification accuracies:")
verbose(2, "within-subject: %.2f +/-%.3f"
        % (np.mean(wsc_results),
           np.std(wsc_results) / np.sqrt(nsubjs - 1)))

#ts = err.a.mapper.reversel(1-err.samples[0])
#map2nifti(ds,ts).to_filename('test_mapping.nii.gz')

#plotting
def make_null_dist_plot(dist_samples,empirical): pl.hist(dist_samples,bins=20,normed=True,alpha=0.8), pl.axvline(empirical,color='red'), pl.axvline(0.5,color='black',ls='--'), pl.xlim(0,1), pl.xlabel('Average cross-validated classification accuracy')
__ = pl.figure()
make_null_dist_plot(np.ravel(cvte.null_dist.ca.dist_samples),1-np.mean(wsc_results))
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





