sub codon2aa
 {
 my ($codon) =@_;
 $codon = uc $codon;
 my(%genetic_code) =
 ( 
  $codon=>'-',
  'TCA' =>'S',
  'TCC' =>'S',
  'TCG' =>'S',
  'TCT' =>'S',
  'TTC' =>'F',
  'TTT' =>'F',
  'TTA' =>'L',
  'TTG' =>'L',
  'TAC' =>'Y',
  'TAT' =>'Y',
  'TAA' =>'Z',
  'TAG' =>'Z',
  'TGC' =>'C',
  'TGT' =>'C',
  'TGA' =>'Z',
  'TGG' =>'W',
  'CAA' =>'Q',
  'CAT' =>'H',
  'CAG' =>'Q',
  'CAC' =>'H',
  'CGA' =>'R',
  'CGT' =>'R',
  'CGG' =>'R',
  'CGC' =>'R',
  'CTA' =>'L',
  'CTT' =>'L',
  'CTG' =>'L',
  'CTC' =>'L',
  'CCA' =>'P',
  'CCT' =>'P',
  'CCG' =>'P',
  'CCC' =>'P',
  'ATA' =>'I',
  'ATT' =>'I',
  'ATG' =>'M',
  'ATC' =>'I',
  'AGA' =>'R',
  'AGT' =>'S',
  'AGG' =>'R',
  'AGC' =>'S',
  'ACA' =>'T',
  'ACT' =>'T',
  'ACG' =>'T',
  'ACC' =>'T',
  'AAA' =>'K',
  'AAT' =>'N',
  'AAG' =>'K',
  'AAC' =>'N',
  'GTA' =>'V',
  'GTT' =>'V',
  'GTG' =>'V',
  'GTC' =>'V',
  'GGA' =>'G',
  'GGT' =>'G',
  'GGG' =>'G',
  'GGC' =>'G',
  'GCA' =>'A',
  'GCT' =>'A',
  'GCG' =>'A',
  'GCC' =>'A',
  'GAA' =>'E',
  'GAT' =>'D',
  'GAG' =>'E',
  'GAC' =>'D',
  );
  if(exists $genetic_code{$codon})
	{
		return $genetic_code{$codon};
	}
	
}
	
1;
	