#!/usr/bin/perl
use CGI qw(:standard :html3);
use module1;
#print "content-type:text/plain \n\n";
print "Content-type:text/html\n\n";
my $seq=param("Fastaseq");
my $total = $seq =~ tr/>/>/;
print "Working";
#print $total; 
=if ($total==1)
{
  print "<html>
         <body bgcolor=\"#E6E6FA\">
         <h1>Note: Not enough sequences for comparision</h1>
         </body>
         </html>";
}
elsif($total==0)
{
  print "<html>
         <body bgcolor=\"#E6E6FA\">
         <h1>error:No input found!</h1>
         </body>
         </html>";
}
else
=cut
#{
   mkdir(User_input,);		#creating the Output directory for keeping the input file submitted by the user at interface
   open(FASTA,">","/User_input/input.txt");
   print FASTA $seq;
   close(FASTA);
#}
=opendir(User_dir,'User_input') or die "Cannot opend input dir";
   @input=readdir(User_dir);
   close(User_dir);
   for($i=2;$i<@input;$i++)
   {
     system("C:/xampp/cgi-bin/muscle3.8.31_i86win32.exe -in C:/xampp/cgi-bin/User_input/$input[$i] -clwout C:/xampp/cgi-bin/alignment/$input[$i]");
     system("conversion.pl 2>asd.log") and die "Cannot execute";
     system("comparison.pl 2>sad.log") and die "Cannot execute";
     system("main.pl 2>error.log") and die "Cannot execute";
	 #system("CodonUsage.pl 2>error.log") and die "Cannot execute";
	}
   opendir(F,'Final');
   @final=readdir(F);
   close(F);
   for($i=2;$i<@final;$i++){
   open(FILE,"C:\\xampp\\cgi-bin\\Final\\$final[$i]") or die"file cannot open";
   while($line1=<FILE>)
	{
		push(@aa,$line1); 
	}
  close(FILE);
  $rowcount=&combination($total)+2;
  for ($i=0;$i<$rowcount;$i++)
  {
    if ($i==0){ $t="<table  border=\"1\" style=\"width:50%\">";$s="";}
    $aa[$i]=~s/\t/<\/td><td>/g;
    $ss=$t."<tr><td>".$aa[$i]."</td></tr>";
    $t="";
    $s=$s.$ss;
    if ($i== ($rowcount-1)) {$end="</table>";$s=join( "", $s,$end);}
  }
  print "<html>	
         <body bgcolor=\"#E6E6FA\">
		 <h1>Result</h1>
		 <style>	
		 h2{
		 color:blue;
		 font-family: \"Times New Roman\", Georgia, Serif;;
		 font-size:100%;
		 }
		 </style>
		 $s
		 <h2><a href=\"http://localhost/cgi-bin/CodonUsage.pl\">Click here</a> to download codon usage</h2>
         </body>
         </html>";   
}
}
#This function is used for generating the number of rows.
sub combination
{
  my $var=shift;
  return &fact($var)/(&fact(2)* &fact($var-2));
}
sub fact
{
  my $arg = shift;
  if ($arg == 1){return 1;}
  else{return $arg * fact($arg - 1);}
}
=cut
