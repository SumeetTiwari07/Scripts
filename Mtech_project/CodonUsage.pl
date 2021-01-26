#!"C:\xampp\perl\bin\perl.exe"
#use CGI qw(:standard :html3);
use module1;
#print "Content-type:text/html\n\n";#give command line input
my $input =@ARGV[0];
	@seq=();
	@seq_name=();
	open(FILE,$input) or die "Can't open the $input";
	while($line=<FILE>){
	chomp($line);
	if($line=~/^>/){
	push(@seq,$seq);	
	$seq=();
	$line=~s/\>//g;
	push(@seq_name,$line);
	next;
  	}
else
	{
	 $seq.=$line;
	}
}
push(@seq,$seq);
close(FILE);
@codon_all=("GCT","GCC","GCA","GCG","TTT","TTC","TTA","TTG","CTT","CTC","CTA","CTG","ATT","ATC","ATA",
            "ATG","GTT","GTC","GTA","GTG","TCT","TCC","TCA","TCG","AGT","AGC","CCT","CCC","CCA","CCG",
            "ACT","ACC","ACA","ACG","TAT","TAC","TAA","TAG","TGA","CAT","CAC","CAA","CAG","AAT","AAC",
            "AAA","AAG","GAT","GAC","GAA","GAG","TGT","TGC","TGG","CGT","CGC","CGA","CGG","AGA","AGG",
            "GGT","GGC","GGA","GGG");
@aa_all=("A","A","A","A","F","F","L","L","L","L","L","L","I","I","I","M","V","V","V","V","S","S","S","S","S","S",
		 "P","P","P","P","T","T","T","T","Y","Y","Z","Z","Z","H","H","Q","Q","N","N","K","K","D","D","E","E","C",
		 "C","W","R","R","R","R","R","R","G","G","G","G");
#@{seq.$i}=different array assigned to different sequences.
for($i=1;$i<@seq;$i++){
  for($j=0;$j<length($seq[$i]);$j+=3)
	{	
	   $codon=substr($seq[$i],$j,3);
	   push(@{seq.$i},$codon);
	   push(@{aa.$i},codon2aa(substr($seq[$i],$j,3)));
	}
print  "ProteinName:\t$seq_name[$i-1]\n";
print  "Codon\taa\tfreq\tpercent\n";
 for($k=0;$k<@codon_all;$k++)
 {
  $freq=0;
  $aa=0;
  for($l=0;$l<@{seq.$i};$l++)
   {
    if($codon_all[$k] eq @{seq.$i}[$l]){
	  $freq+=1;
	}
	else{
	 $freq+=0;
	}
   if($aa_all[$k] eq @{aa.$i}[$l]){
     $aa+=1;
   }
    else{
	 $aa+=0;
	}   
   }
if($aa==0){
$c=0;
}else{  
  $c=($freq/$aa)*100;
} 
  print $codon_all[$k]."\t".$aa_all[$k]."\t".$freq."\t".sprintf("%.2f",$c)."\n";
 } 
}
