<?php
$seq = $_POST['Nuc_seq'];
$prtn = $_POST['Prtn_seq'];
/* Function for creating randfiles start*/ 
function GeraHash($qtd){

$Caracteres = '0123456789ABCDEFGHIJKLMOPQRSTUVXWYZ';
$QuantidadeCaracteres = strlen($Caracteres);
$QuantidadeCaracteres--;

$Hash=NULL;
    for($x=1;$x<=$qtd;$x++){
        $Posicao = rand(0,$QuantidadeCaracteres);
        $Hash .= substr($Caracteres,$Posicao,1);
    }

return $Hash;
}

/*End of randname generation*/
$randname  = GeraHash(10);
//echo $randname;
system("mkdir ./quries/$randname");
system("chmod -R 777 ./sumeeth/quries/$randname");
system("mkdir ./quries/$randname/nucleicacid");
system("chmod -R 777 ./sumeeth/quries/$randname/nucleicacid");
system("mkdir ./quries/$randname/protein");
system("chmod -R 777 ./sumeeth/quries/$randname/protein");
file_put_contents("./quries/$randname/$randname",$seq);
system("chmod -R 777 ./sumeeth/quries/$randname/$randname");
file_put_contents("./quries/$randname/$randname"."_prtn",$prtn);
system("chmod -R 777 ./sumeeth/quries/$randname/$randname"."_prtn");
//system("cat ./quries/$randname/$randname | grep '>'");
system("mkdir ./quries/$randname/seq_aln");
system("sh split.sh $randname");
system("./muscle3.8.31_i86linux64 -in ./quries/$randname/$randname -clwout ./quries/$randname/$randname"."_msa");
$prtn_len=system("cat ./quries/$randname/list_prtn | grep -c \">\"");
//echo $prtn_len ."\n";
system("./auto_iteration.sh $randname $prtn_len");
include ('test_aln.php');
system("perl ./conversion.pl ./quries/$randname/$randname"."_msa > ./quries/$randname/$randname"."_conv");
system("perl ./comparison.pl ./quries/$randname/$randname"."_conv > ./quries/$randname/$randname"."_comp");
system("perl ./CodonUsage.pl ./quries/$randname/$randname >./quries/$randname/$randname"."_codon");
system("perl ./codon.pl ./quries/$randname/$randname"."_codon > ./quries/$randname/$randname"."_codonusage");
system("perl ./main.pl ./quries/$randname/$randname"."_comp > ./quries/$randname/$randname"."_main");


$file=file_get_contents("./quries/$randname/$randname"."_main","r");

$arr=split("\n",$file);
$prints=split("\t",$arr[1]);
echo "<legend><b>RESULTS: Job ID-"."$randname"." </b></legend>";
echo "<fieldset>";
echo "<h4 align=\"center\"><b><a href=./quries/$randname/$randname"."_codonusage>Codon Usage</a></b></h4>";
echo "<table align=\"center\" style=\"width:1000px\" border=\"1\">
     <tr>";
echo "<td><b>Orthologs</b></td><td><b>Orthologs</b></td><td><b>NCNS_D</b></td><td><b>CNS_D</b></td><td><b>SYN_D</b></td><td><b>NCNS_P</b></td><td><b>CNS_P</b></td><td><b>SYN_P</b></td><td><b>Dncns</b></td><td><b>Dcns</b></td><td><b>Dsyn</b></td><td><b>Dncns/Dcns</b></td><td><b>Dcns/Dsyn</b></td><td><b>Dncns/Dsyn</b></td></tr>";
$i=1;
while($arr[$i])
     	{   
       	$prints=split("\t",$arr[$i]);
       	echo "<tr><td>".$prints[0]."</td><td>".$prints[1]."</td><td>".$prints[2]."</td><td>".$prints[3]."</td><td>".$prints[4]."</td><td>".$prints[5]."</td><td>".   $prints[6]."</td><td>".$prints[7]."</td><td>".$prints[8]."</td><td>".$prints[9]."</td><td>".$prints[10]."</td><td>".$prints[11]."</td><td>".$prints[12]."</td><td>".$prints[13]."</td>
</tr>";
      $i++;
     }
     echo "</table>";
     echo "</fieldset>";

?>
