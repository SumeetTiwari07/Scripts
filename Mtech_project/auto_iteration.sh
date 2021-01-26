#!/bin/bash
for (( i = 1; i < $2; i++ ))      ### Outer for loop ###
do
    z=$(($i+1));
    for (( j = $z ; j <= $2; j++ )) ### Inner for loop ###
    do
	echo $i "	"$j         
 perl emboss_needle_soaplite.pl --asequence ./quries/$1/protein/$i.txt --bsequence ./quries/$1/protein/$j.txt --email sumeet.kumartt\@gmail.com --outfile ./quries/$1/seq_aln/$i$j
    done
 
  echo "" #### print the new line ###
done
