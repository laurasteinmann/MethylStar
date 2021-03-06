#!/bin/bash
curr_dir="$(dirname "$0")"
com1=$(awk '/^\[/ { } /=/ { print $0 }' config/pipeline.conf > $curr_dir/tmp.conf)
. $curr_dir/tmp.conf



#R CMD BATCH $result_pipeline $genome_name --save output.log
Rscript ./src/bash/methimpute.R $result_pipeline $genome_ref $genome_name $tmp_rdata $intermediate $fit_output $enrichment_plot $full_report $context_report $intermediate_mode --no-save --no-restore --verbose 

# check if everyfiles finished, then delete queue list 
if [ -z $(comm -23 <(sort -u $tmp_meth_out/list-files.lst) <(sort -u $tmp_meth_out/file-processed.lst)) ]  
then
	com=$(sed -i "s/st_methimpute=.*/st_methimpute=2/g" config/pipeline.conf)
	remove=$(rm $tmp_meth_out/file-processed.lst)
fi

# docker part 
if $docker_mode; 
then
	perm=$(chmod 777 -R $result_pipeline)
fi