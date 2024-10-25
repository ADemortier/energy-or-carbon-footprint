#!/bin/bash
if [ -z "$1" ]
then
      echo "Usage: grep_tei_kwh.sh outputfilename (will be appended with tei.txt and kwh.txt)"
      echo "It will collect all TEI values from step 2 from current directory, recursively"
      echo "Typically you should run that script from a subdirectory within your xpout folder on HPC"
else
      echo $PWD > ${1}_tei.txt
      echo $PWD > ${1}_kwh.txt
      echo $PWD > ${1}_Elapsedtime.txt
      for file in `find . -name \*.1 -print`
        do
          echo -n $file " "  >> ${1}_tei.txt
          grep -m2 TEI $file| tail -n1 >> ${1}_tei.txt
          echo "" >> ${1}_tei.txt #newline
          echo -n $file " "  >> ${1}_Elapsedtime.txt
          grep -m2 'Elapsed time' $file| tail -n1 >> ${1}_Elapsedtime.txt
          echo "" >> ${1}_Elapsedtime.txt #newline
          echo -n $file " "  >> ${1}_kwh.txt
          grep -m1 pmi_proxy $file >> ${1}_kwh.txt
          echo "" >> ${1}_kwh.txt #newline
        done
      mv ${1}_kwh.txt ~/EcoStats/
      mv ${1}_tei.txt ~/EcoStats/
      mv ${1}_Elapsedtime.txt ~/EcoStats/
fi
