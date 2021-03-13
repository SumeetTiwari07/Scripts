#load samples into table
import pandas as pd
configfile:"config1.yaml"

samples = pd.read_table(config["samples"], index_col="sample")
#print (samples)

rule all:
	input: expand("multiqc/{sample}", sample=list(samples.index))

rule QC1:
	input: lambda wildcards: samples.at[wildcards.sample,'fq1'], lambda wildcards: samples.at[wildcards.sample,'fq2']
        output: "QC/{sample}_1_fastqc.zip", "QC/{sample}_1_fastqc.html", "QC/{sample}_2_fastqc.zip", "QC/{sample}_2_fastqc.html"
        params: mydir="QC"
        shell: "fastqc {input} -o {params.mydir}"

rule AT:
	input: lambda wildcards: samples.at[wildcards.sample,'fq1'], lambda wildcards: samples.at[wildcards.sample,'fq2'], "QC/{sample}_2_fastqc.html"
	output: "AT/{sample}_1_val_1.fq.gz", "AT/{sample}_2_val_2.fq.gz"
	params: mydir="AT"
	shell: "trim_galore -q 20 --phred33 -o {params.mydir}  --paired {input[0]} {input[1]}"

rule QCAT:
	input: "AT/{sample}_1_val_1.fq.gz", "AT/{sample}_2_val_2.fq.gz"
        output: "QCAT/{sample}_1_val_1_fastqc.zip", "QCAT/{sample}_1_val_1_fastqc.html", "QCAT/{sample}_2_val_2_fastqc.zip", "QCAT/{sample}_2_val_2_fastqc.html"
        params: mydir="QCAT"
        shell: "fastqc {input} -o {params.mydir}"

rule assembly:
	input: "AT/{sample}_1_val_1.fq.gz", "AT/{sample}_2_val_2.fq.gz", "QCAT/{sample}_2_val_2_fastqc.html"
	output: "assembly/{sample}/contigs.fasta"
	params: mydir="assembly/{sample}"
	shell: "spades.py --sc -o {params.mydir} -1 {input[0]} -2 {input[1]} --careful --cov-cutoff 'auto' -t 16"

rule quast:
    	input: "assembly/{sample}/contigs.fasta"
    	output: "assembly_stats/{sample}/report.tsv"
        params: mydir="assembly_stats/{sample}"
    	shell: "quast -o {params.mydir} {input}"

rule annotation:
	input: "assembly_stats/{sample}/report.tsv", "assembly/{sample}/contigs.fasta"
    	output: "ref_annotation/{sample}"
        shell: "prokka --outdir {output} --prefix {wildcards.sample} {input[1]}"

rule multiqc:
   	input: "ref_annotation/{sample}", "assembly_stats/{sample}/report.tsv", "QCAT/{sample}_1_val_1_fastqc.zip", "QCAT/{sample}_2_val_2_fastqc.zip", "QC/{sample}_1_fastqc.zip", "QC/{sample}_2_fastqc.zip"
   	output: "multiqc/{sample}"
	params: mydir="multiqc/{sample}"
	shell: "multiqc -d -s -o {params.mydir} {input[0]} {input[1]} {input[2]} {input[3]} {input[4]} {input[5]}"
