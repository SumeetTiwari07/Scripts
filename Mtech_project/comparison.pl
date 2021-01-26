$len_dna=0;
use module1;
my $conver=$ARGV[0];
open(F,$conver) or die "Cannot open file $conver";
while($line=<F>){
chomp($line);
$seq1=$line;
if($seq1=~/\>/)
{
	$seq1=~s/\W//g;
	push(@name,$seq1);
	$seq.=($seq1);
}
else
{
	$seq.=uc($seq1);
}
if($line=~ /\>/)
	{
		$line=~s/\>//g;
		$line=~s/\|//g;
		#$line=~s/\d//g;
		$line=~s/girefNP_.//g;
		$line=~s/girefMN_.//g;
		$line=~s/\[/\t/g;
		@sub=split(/\t/,$line);
		$sub[0]=~s/^\s*//g;
		$sub[0]=~s/\s*$//g;
		push(@name1,$sub[0]);
	}
}

for($i=0;$i<@name;$i++){
$seq=~ s/$name[$i]/\t/g;
}
@seq=split('\t',$seq);

for($j=1;$j<@seq;$j++)
{
	$len_dna=length($seq[$j]);
	for($i=0;$i<$len_dna;$i+=3)
	{
		push(@{codon.$j},substr($seq[$j],$i,3));
		push(@{aa.$j},codon2aa(substr($seq[$j],$i,3)));
	}
}
close(F); 
#open (OUT,">","C:\\xampp\\cgi-bin\\comparison\\$file[$f]") or die "cannot write file $file[$f]";
for($j=1;$j<(@seq-1);$j++)
{
	for($k=($j+1);$k<@seq;$k++)	
	{
		print  "This\tis\tcomparison\t$j\tx\t$k\t$name1[$j-1]\t$name1[$k-1]\n";
		print  "Codon#\tclass\tcodon1\tcodon2\taa1\taa2\n";
		for($i=0;$i<@{codon.$j};$i++)
		{
			print  ($i+1);
			if((@{aa.$j}[$i] eq '-')||(@{aa.$k}[$i] eq '-'))
				{
					print  "\tindel\t";
				}
			elsif((@{codon.$j}[$i] eq @{codon.$k}[$i]) && (@{aa.$j}[$i] eq @{aa.$k}[$i]))
				{
					print  "\tidentity\t";
				}
			elsif((@{codon.$j}[$i] ne @{codon.$k}[$i]) && (@{aa.$j}[$i] eq @{aa.$k}[$i]))
				{
					print  "\tsynon\t";
				}
			else
				{
					print  "\tnonsynon\t";	
				}
			print  @{codon.$j}[$i]."\t";
			print  @{codon.$k}[$i]."\t";
			print  @{aa.$j}[$i]."\t";
			print  @{aa.$k}[$i]."\n";
		}
	}
}		

