#!/bin/bash

# this script file is for GA based least square minimization program

# comment - sourya
#basedir='../DATASET/influenzaA_fulllength_H3N2_HA/'

# add - sourya
basedir='../../DATASETS_USED_FOR_EXECUTION/DATASET_FOR_GA_LS_NJ/influenzaA_fulllength_H3N2_HA/2012/'

# find the folders within this base directory
# the folders are basically the years 
for Dir in $(find $basedir -type d); 
do
  FolderName=$Dir
  if [ $FolderName == $basedir ]; then
    continue
  fi
  # append the last character as / if it is not done already
  [[ $FolderName != */ ]] && FolderName="$FolderName"/
  echo 'outer folder: ' $FolderName
  
  # comment - sourya
  ## now find the folders within this folder
  ## within these folders, datasets are contained
  #for Dir in $(find $FolderName -type d); 
  #do
  #  WorkingDir=$Dir
  #  if [ $WorkingDir == $FolderName ]; then
  #    continue
  #  fi    
  #  # append the last character as / if it is not done already
  #  [[ $WorkingDir != */ ]] && WorkingDir="$WorkingDir"/
  #  echo 'working directory : ' $WorkingDir
  # end comment - sourya
  
  # add - sourya
  WorkingDir=$FolderName
  echo 'working directory : ' $WorkingDir
  # end add - sourya
  
    # now append the distance matrix filename which is to be provided as an input to the executable
    input_file_distmat="$WorkingDir"inp_distance_matrix.mat
    outputtextfile="$WorkingDir"complete_output_description.txt
    #echo 'outputtextfile: ', $outputtextfile
    # now start twaking about various GA paramters
    # in several for loops the execution will run
    popsize=50
    maxpopsize=250
    steppopsize=50
    while [ $popsize -le ${maxpopsize} ]
    do
      gen=50
      maxgen=150
      stepgen=50
      while [ $gen -le $maxgen ]
      do
	sel=0
	maxsel=2
	stepsel=1
	while [ $sel -le $maxsel ]
	do
	  #fracprevgen=0.05
	  #maxfracprevgen=0.5
	  #stepfracprevgen=0.05
	  #while [ $fracprevgen -le $maxfracprevgen ]
	  #do
	    if [ $sel -eq 2 ]; then 
	      elit=1
	      stepelit=4
	      maxelit=5
	      while [ $elit -le $maxelit ]
	      do     
		#outputtextfile="$WorkingDir""Population_"$popsize"_Generations_"$gen"_Ranking_Selection_Elitism_Count_"$elit"_Fraction_Prev_Gen_0.05/complete_output_description.txt" 
		# execute the command
		#./GA_LS_MAIN.py -i $input_file_distmat -p $popsize -g $gen -s $sel -f $fracprevgen -e $elit > $outputtextfile
		./GA_LS_MAIN.py -i $input_file_distmat -p $popsize -g $gen -s $sel -e $elit >>$outputtextfile
		elit=`expr $elit + $stepelit`
	      done
	    else
	      #if [ $sel -eq 1 ]; then 
		#outputtextfile="$WorkingDir""Population_"$popsize"_Generations_"$gen"_Ranking_Selection_No_Elitism_Fraction_Prev_Gen_0.05/complete_output_description.txt" 
	      #else
		#outputtextfile="$WorkingDir""Population_"$popsize"_Generations_"$gen"_Tournament_Selection_No_Elitism_Fraction_Prev_Gen_0.05/complete_output_description.txt" 
	      #fi
	      # execute the command
	      #./GA_LS_MAIN.py -i $input_file_distmat -p $popsize -g $gen -s $sel -f $fracprevgen > $outputtextfile
	      ./GA_LS_MAIN.py -i $input_file_distmat -p $popsize -g $gen -s $sel >>$outputtextfile
	    fi
	    #fracprevgen=`expr $fracprevgen + $stepfracprevgen`
	  #done
	  sel=`expr $sel + $stepsel`
	done
	gen=`expr $gen + $stepgen`
      done
      popsize=`expr $popsize + $steppopsize`
    done
  # comment - sourya
  #done
  # end comment - sourya
done
