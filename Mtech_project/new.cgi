#!"C:\xampp\perl\bin\perl.exe"
use use CGI qw/:standard *table start_table/;
$cgiobject = new CGI;
print $cgiobject->header,
$cgiobject->start_html (

        -title=>'Perl Tutorials'
),
        $cgiobject->start_table ({-border=>'1', -align=>'left'}), "\n",

        $cgiobject->start_Tr,
                $cgiobject->start_td,
                "Orthologus Protein1",
                $cgiobject->end_td,
                $cgiobject->start_td,
                "Orthologus Protein2",
                $cgiobject->end_td,
				$cgiobject->start_td,
                "",
                $cgiobject->end_td,
        $cgiobject->end_Tr,
        $cgiobject->start_Tr,
                $cgiobject->start_td,
                "John",
                $cgiobject->end_td,
                $cgiobject->start_td,
                "Paul",
                $cgiobject->end_td,
        $cgiobject->end_Tr,
        $cgiobject->start_Tr,
                $cgiobject->start_td,
                "Todd",
                $cgiobject->end_td,
                $cgiobject->start_td,
                "Haul",
                $cgiobject->end_td,
        $cgiobject->end_Tr,
        $cgiobject->end_table, "\n",

$cgiobject->end_html;
exit;