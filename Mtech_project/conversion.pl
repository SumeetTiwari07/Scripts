#Conversion of msa to fasta.aln
my $input=$ARGV[0];
open(FILE,$input) or die "Cannot open the $input";
while($line =<FILE>)
{
	($name,$seq) = split(/\s+/, $line);
	$seq2=$seq;
	$seq2=~s/\d//g;
	$seq2=~s/\://g;
	$seq2=~s/\*//g;
	$seq2=~s/\.//g;
	$seq2=~s///g;
	if($seq2 ne /\W/g)
		{
			push(@seq1,$seq2);
		}
	if($name ne /\W/g)
		{
			push(@name,$name);
		}
}
push(@name1,$name[1]);
for($i=1;$i<@name;$i++)
	{
		if($name[1] ne $name[$i+1])
			{ 
				push (@name1,$name[$i+1]);
			}
		else
			{
				last;
			}
 }
 for($i=0;$i<@name1;$i++)
	{
		for($j=1;$j<@seq1;$j++)
			{
				if($name1[$i] eq $name[$j])
					{
						@{seq2.$i}[$i].= $seq1[$j];
					}
			}
	}
close(FILE);
#open(out,">","C:\\xampp\\cgi-bin\\Conversion_output\\$files[$f]") or die "Cannot write fasta ouptut";
for($i=0;$i<@name1;$i++)
 {
  print ">".$name1[$i]."\n";
  print @{seq2.$i}[$i]."\n"; 
 }

