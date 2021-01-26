#!"C:\xampp\perl\bin\perl.exe"
my $in=@ARGV[0];
@codon=();
@aa=();
@freq=();
@percent=();
@prtn_name=();
@file=();
open(FILE,$in) or die "Can't open the $in";
while($line=<FILE>){
chomp($line);
push(@file,$line);
if(($line=~/^ProteinName:/)||($line=~/^Codon/))
{
next;
}
else 
{
	($codon,$aa,$freq,$percent)=split(/\t+/,$line);
	push(@codon,$codon);
	push(@aa,$aa);
	push(@freq,$freq);
	push(@percent,$percent);
}
}
#push(@c,$c);
@prtn_name=grep(/^Protein/,@file);
@codon_all=("GCT","GCC","GCA","GCG","TTT","TTC","TTA","TTG","CTT","CTC","CTA","CTG","ATT","ATC","ATA",
            "ATG","GTT","GTC","GTA","GTG","TCT","TCC","TCA","TCG","AGT","AGC","CCT","CCC","CCA","CCG",
            "ACT","ACC","ACA","ACG","TAT","TAC","TAA","TAG","TGA","CAT","CAC","CAA","CAG","AAT","AAC",
            "AAA","AAG","GAT","GAC","GAA","GAG","TGT","TGC","TGG","CGT","CGC","CGA","CGG","AGA","AGG",
            "GGT","GGC","GGA","GGG");

for($i=0;$i<@prtn_name;$i++){
($a,$prtn[$i])=split(/\s+/,$prtn_name[$i]);
}
print "Protein name"."\t";
for($i=0;$i<@prtn;$i++)
{	
	print $prtn[$i]."\t"; 
}
print "\nCodon\taa\t";

for($i=0;$i<@prtn;$i++){
print "freq %usage\t";
}
print "\n";
for($j=0;$j<@codon_all;$j++){
   print $codon_all[$j]."\t".$aa[$j]."\t";
    for($k=0;$k<@aa;$k++){
	if($codon_all[$j] eq $codon[$k]){
		print $freq[$k]."\t".$percent[$k]."\t";
		}
   }
   print "\n";
}		
