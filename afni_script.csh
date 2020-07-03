#!/bin/tcsh

if ( $#argv > 0 ) then
    set subjects = ( $argv )
else
    #set subjects = (subj101 subj103 subj105 subj106 subj107 subj108 subj109 subj110 subj114 subj115 subj116 subj117 subj122)
    set subjects = (subj122)
endif

#===========================================================================
# Above command will run script for all our subjects - ED, EE, EF - one after
# the other if, when we execute the script, we type: ./@analyze_ht05 ED EE EF.
# If we type ./@analyze_ht05 or tcsh @analyze_ht05, it'll run the script only
# for subject ED.  The user will then have to go back and edit the script so
# that 'set subjects' = EE and then EF, and then run the script for each subj.
#===========================================================================
    
foreach subj ($subjects)
    
    cd $subj

    #======================================================================
    # time shift our datasets
    #======================================================================    
 
    foreach run ( `count -digits 1 1 5`)
	    3dTshift -verbose			 \
		     -TR 2s                     \
		     -Fourier                   \
		     -tpattern seqplus           \
		     -prefix r{$run}_st.nii.gz \
		      run{$run}/bold.nii.gz

		 
	# store run data in runs_orig directory

    
    #======================================================================
    # volume register to the middle volume (128), and save the displacement
    # file for later counfound regressor
    #======================================================================    

	3dvolreg -verbose			\
		 -maxdisp1D maxdisp_r{$run}.txt \
		 -Fourier                       \
		 -1Dfile ort_motion_r{$run}.1D  \
		 -prefix  r{$run}_vr.nii.gz	\
		 r{$run}_st.nii.gz

	# store run data in runs_orig directory
    #======================================================================
    # smoothing
    # 
    #======================================================================    
	   
		  3dmerge -1blur_rms 8			\
		  -doall 				\
		  -prefix r{$run}_bl.nii.gz	\
		  r{$run}_vr.nii.gz

    
    #======================================================================
    # 3dDespike
    # 
    #======================================================================    
	   
	 #3dDespike -prefix r{$run}_pp.nii.gz \
		   #r{$run}_vr.nii.gz

    #======================================================================
    # 3dDetrend
    # 
    #======================================================================    
	   
	 #3dDetrend -verb \
		   #-polort 2\
		   #-vector ort_motion_r{$run}.1D \
		   #-prefix r{$run}_dt.nii.gz \
		   #r{$run}_pp.nii.gz
		   
    end

    #======================================================================
    # first make 3D mean bold image for each run, then make a 4D mask for each run, 
    # then clean the skull of filtered image and then spatial normalization to the EPI template
    #======================================================================    
	
    foreach run ( `count -digits 1 1 5` )

	3dTstat -prefix mean_r{$run}.nii.gz r{$run}_bl.nii.gz
	3dAutomask -prefix mask_r{$run}.nii.gz r{$run}_bl.nii.gz
    end

    #======================================================================
    # for visualization
    # 
    #=====================================================================
	3dTstat -prefix mean_underly.nii.gz r1_vr.nii.gz
	3dcalc -a mean_underly.nii.gz -b mask_r1.nii.gz -expr 'a*b' -prefix bet_mean_underly.nii.gz
    #======================================================================
    # create a mask enveloping masks of the individual runs
    #====================================================================== 
    
    3dcalc -a mask_r1.nii.gz -b mask_r2.nii.gz -c mask_r3.nii.gz	\
	   -d mask_r4.nii.gz -e mask_r5.nii.gz			\
	   -expr 'step(a+b+c+d+e)'			\
	   -prefix full_mask.nii.gz

    #======================================================================
    # re-scale each run's baseline to 100.
    # E.g., If baseline is 100, and result of 3dcalc on one voxel is 106, then
    # we can say that at that voxel shows a 6% increase is signal activity
    # relative to baseline.
    # Use full_mask to remove non-brain
    #======================================================================

    foreach run ( `count -digits 1 1 5` )

    3dcalc -a r{$run}_bl.nii.gz   \
    -b mean_r{$run}.nii.gz            \
    -c full_mask.nii.gz              \
    -expr "(a/b * 100) * c"         \
    -prefix scaled_r{$run}.nii.gz

    \rm mean_r{$run}.nii.gz

    end
    #======================================================================
    # Now we can concatenate our 5 runs (1,2,3,4,5) with 3dTcat. note that if use detrend, then dt
    #======================================================================
    3dTcat -prefix all_runs.nii.gz  \
        scaled_r1.nii.gz            \
	scaled_r2.nii.gz \
	scaled_r3.nii.gz \
	scaled_r4.nii.gz \
	scaled_r5.nii.gz
   
    #======================================================================
    # Now we want to make afni format of files. note if use detrend, then dt
    #======================================================================
    #foreach run ( `count -digits 1 1 5` )

	#3dcopy r{$run}_vr.nii.gz r{$run}_vr

	#3dcopy IFG_binary_mask.nii IFG_binary_mask+orig

    #end

    #======================================================================
    # removing extra files
    #======================================================================

    foreach run ( `count -digits 1 1 5` )
    rm r{$run}_st.nii.gz
    rm r{$run}_vr.nii.gz
    rm r{$run}_bl.nii.gz
    rm scaled_r{$run}.nii.gz
    end

    cd ..

end
