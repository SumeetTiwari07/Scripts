my ($comp, $randname) = @ARGV;
$k=0;
$ncns_d_mean=0;
$cns_d_mean=0;
$syn_d_mean=0;
$ncns_p_mean=0;
$cns_p_mean=0;
$syn_p_mean=0;
$Dncns_mean=0;
$Dcns_mean=0;
$R1_mean=0;
$R2_mean=0;
$R3_mean=0;
$Dsyn_mean=0;
@name1=();
@name2=();
@codon=();
@class=();
@seq1=();
@seq2=();
@aa1=();
@aa2=();
@count=();
open(FILE,$comp) or die "Can't open the $comp";
while($line = <FILE>)
	{
		chomp($line);
		($codon,$class,$seq1,$seq2,$aa1,$aa2,$name1,$name2) = split(/\s+/, $line);
		if($line =~/^This/)	
		{ 
			push(@name1,$name1);
			push(@name2,$name2);
			push(@count,$count);
			$count=0;				
			next;
		}	
		elsif(($class ne 'indel')&&($codon ne 'Codon#')&&($seq1 ne 'TAA')&&($seq1 ne 'TGA')&&($seq1 ne 'TAG'))
		{		
			$count+=1;						#Counting the total number of codons in single comparison.
			push(@codon,$codon);
			push(@class,$class);
			push(@seq1,$seq1);
			push(@seq2,$seq2);
			push(@aa1,$aa1);
			push(@aa2,$aa2);
		}	
		else
		{	
			next;			
		}
		
	}
 push(@count,$count);
close(FILE);
#opening the similarity file.
#$sim_input=$ARGV[0];
open(FILE,"./quries/".$randname."/table") or die "cannot open file";
while($line=<FILE>){
	chomp($line);
	$line=~s/\#|\d+:|\d+\/\d+|Similarity:|\(|\)|\%//g;
	$line=~s/^\s+//g;
	($prtn_name1,$prtn_name2,$similarity)=split(/\s+/,$line);
	push(@prtn_name1,$prtn_name1);
	push(@prtn_name2,$prtn_name2);
	push(@similarity,$similarity);
}
print  "Orthologs\tOrthologs\tNCNS_D\tCNS_D\tSYN_D\tNCNS_P\tCNS_P\tSYN_P\tDncns\tDcns\tDsyn\tDncns/Dcns\tDcns/Dsyn\tDncns/Dsyn\n";
for($i=1;$i<@count;$i++)
{	
	for($l=0;$l<@prtn_name1;$l++)
	{
          if(($name1[$i-1] eq $prtn_name1[$l])&&($name2[$i-1] eq $prtn_name2[$l]))
		{
		   $sim=$similarity[$l];				
		}
	}
print  $name1[$i-1]."\t".$name2[$i-1]."\t";	#name of the protein sequence compared 
$ncns_d=0;
$cns_d=0;
$syn_d=0;
$syn_p=0;
$ncns_p=0;
$cns_p=0;
	for($j=0;$j<$count[$i];$j++)
	{	
		open(CODON,$seq1[$k].".txt");
		while($line1=<CODON>){
		chomp($line1);
		#print $line1."\n";
		($sub,$p1,$p2,$p3)=split("\t",$line1);
		if($sub=~/NCNS/) 
		{
			$ncns_d+=$p1+$p2+$p3;
			$ncns_d_mean+=$p1+$p2+$p3;
		}
		elsif($sub=~/CNS/)
		{
			$cns_d+=$p1+$p2+$p3;
			$cns_d_mean+=$p1+$p2+$p3;
		}
		else
		{
			$syn_d+=$p1+$p2+$p3;
			$syn_d_mean+=$p1+$p2+$p3;
		}
	  }
	  close(CODON);
		if($aa1[$k] eq $aa2[$k])
		{	
			$syn_p+=1;
			$syn_p_mean+=1;
		}
		else
		{	
			if($sim>60)
			{
			 open(ASM,"asm.txt") or die "Cannot open asm.txt";
			}
			else{
			 open(ASM,"asm2.txt") or die "Cannot open asm2.txt"
			}
			while($asm=<ASM>){
			chomp($asm);
			($a,$b,$c,$d,$e,$f,$g)=split(/\s+/,$asm);
			if($a eq $aa1[$k])
			{	
				if(($aa2[$k] eq $b)||($aa2[$k] eq $c)||($aa2[$k] eq $d)||($aa2[$k] eq $e)||($aa2[$k] eq $f)||($aa2[$k] eq $g))
				{	
					$cns_p+=1;
					$cns_p_mean+=1;
				}	
				else
				{
					$ncns_p+=1;
					$ncns_p_mean+=1;
				}
			}
		
		  }
	 	}
	 close(ASM);		
	 $k=$k+1;
	}
if($ncns_d==0||$ncns_p==0){
$Dncns=0;
}
else{
$Dncns = ($ncns_p/$ncns_d);
$Dncns_mean+=$Dncns;
}
if($cns_d==0||$cns_p==0){
$Dcns=0;	
}
else{
$Dcns = ($cns_p/$cns_d);
$Dcns_mean+=$Dcns;
}
if($syn_d==0||$syn_p==0){
$Dsyn=0;
}
else{
$Dsyn = ($syn_p/$syn_d);
$Dsyn_mean+=$Dsyn;
}
if($Dncns==0||$Dcns==0){
		$R1=0;
	}
	else{
		$R1=($Dncns/$Dcns);
		$R1_mean+=$R1;
	}
if($Dsyn==0||$Dcns==0){
	$R2=0;
}
else{
$R2=($Dcns/$Dsyn);
$R2_mean+=$R2;
}
if($Dsyn==0||$Dncns==0){
		$R3=0;
	}
else{
$R3=($Dncns/$Dsyn);
$R3_mean+=$R3;
}
print sprintf("%.3f",$ncns_d)."\t".sprintf("%.3f",$cns_d)."\t".sprintf("%.3f",$syn_d)."\t".$ncns_p."\t".$cns_p."\t".$syn_p."\t".sprintf("%.3f",$Dncns)."\t".sprintf("%.3f",$Dcns)."\t".sprintf("%.3f",$Dsyn)."\t".sprintf("%.3f",$R1)."\t".sprintf("%.3f",$R2)."\t".sprintf("%.3f",$R3)."\n";
}
print  "Mean\t\t";
print sprintf("%.3f",($ncns_d_mean/scalar@name1))."\t".sprintf("%.3f",($cns_d_mean/scalar@name1))."\t".sprintf("%.3f",($syn_d_mean/scalar@name1))."\t".sprintf("%.3f",($ncns_p_mean/scalar@name1))."\t".sprintf("%.3f",($cns_p_mean/scalar@name1))."\t".sprintf("%.3f",($syn_p_mean/scalar@name1))."\t".sprintf("%.3f",($Dncns_mean/scalar@name1))."\t".sprintf("%.3f",($Dcns_mean/scalar@name1))."\t".sprintf("%.3f",($Dsyn_mean/scalar@name1))."\t".sprintf("%.3f",($R1_mean/scalar@name1))."\t".sprintf("%.3f",($R2_mean/scalar@name1))."\t".sprintf("%.3f",($R3_mean/scalar@name1))."\n"; 	

