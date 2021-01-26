<?php
//$randname="AKZVHMT521";
system("ls -1 ./quries/$randname/seq_aln/*.aln.txt > ./quries/$randname/aln_list");
system("cat ./quries/$randname/aln_list | awk -F '/' '{print $5}'>./quries/$randname/file_name");
$file=file_get_contents("./quries/$randname/file_name","r");
$j =split("\n",$file);
$d =count($j);
for($i=0;$i<66;$i++)
{
 $l=file_get_contents("./quries/$randname/seq_aln/$j[$i]","r");
 $h=split("\n",$l);
$table[$i]= $h[15]."\t".$h[16]."\t".$h[23]."\n";
}
file_put_contents("./quries/$randname/table",$table);
?>
