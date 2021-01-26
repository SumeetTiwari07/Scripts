cd ./quries/$1/
cat $1 | grep ">" > list_nucleic
cat $1_prtn | grep ">" > list_prtn
awk '/^>/{s=++d".txt"} {print > s}' $1
mv *.txt ./nucleicacid/
awk '/^>/{s=++d".txt"} {print > s}' $1_prtn
mv *.txt ./protein/
cd ../../


