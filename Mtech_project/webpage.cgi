#!"C:\xampp\perl\bin\perl.exe"
use CGI qw(:standard :html3);
print "Content-type:text/html\n\n";
print"<html>
	  <head>
	  <img src="C:/xampp/cgi-bin/uoh.jpeg" style="margin-left:40;float:left;width:100px;height:100px"> 	
	  <body bgcolor="#E6E6FA">
      </head>
      <body>
      <center>
	  <h1> Tool for nucleotide and protein substitution analysis</h1>
      </center>
      <h2 style="margin-left:50;margin-top:200px">Enter the Sequence</h2>

	<form action="http://localhost/cgi-bin/test.pl" method="POST">
	<div style="margin-left:50px">
	<textarea rows="10",cols="100" name="Fastaseq" style="width: 600px; height:200px;"></textarea>
	<input type="submit"  name="submit" value ="Submit">
	</div>
	</form>
	</body>
	</html>";