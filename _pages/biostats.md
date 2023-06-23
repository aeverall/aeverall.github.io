---
layout: personalised
title: Biostatistics
permalink: /biostats/
---

I am using whole genome sequencing data from the [100k Genomes Project](https://www.genomicsengland.co.uk/initiatives/100000-genomes-project) to determine the mutations which drive cancer progression and are targetable by available therapies.


### Mutation Signatures

The DNA in our cells is frequently mutated due to exogenous processes such as UV exposure and smoking and endogenous processes like replication errors. In a cancer tumour the mutations in the progenitor cell are present in all daughter cells and we can count them. The mutation counts are the sum of the mutation processes taking place and we want to find the contribution of each process to each patient's tumour. 

I took 10,983 whole genome sequenced tumour samples, aggregated the mutations and decomposed the underlying mutation processes using nonnegative matrix factorisation (NMF). The mutation counts are decomposed as
<center>
$$ Q = A^T\,S $$
</center>
where \\(Q\\) are the mutation counts, \\(A\\) are the process activities in each sample and \\(S\\) are the mutational spectra due to the process called the signatures.

<html>
  <style>
   .imagecontainer {
     display: grid;
     align-items: center;
     grid-template-columns: 1fr 1fr;
     column-gap: 5px;
    }
    img {
      max-width: 100%;
      max-height:100%;
    }
  </style>
  <body>
    <div class="imagecontainer">
      <div class="text">
        This figure shows the activities of each signature (labelled SBS1, SBS2...) in each cancer type. For example, SBS4 is a signature of smoking driven by chemicals such as PAHs and is predominantly present in lung cancers. For the structural variants (SVs) I selected the appropriate number of signatures to include using the minimum Akaike Information Criterion (AIC)
        <center>
        $$ AIC = 2K(N+M) - 2\left[ M\log(A^T\,S) - A^T\,S \right]$$
        </center>
        based on a poisson likelihood function with \(K\) the number of processes, \(N\) the number of samples and \(M\) the number of mutation types.
      </div>
      <div class="image">
        <!-- <img src="content/sf_healpix_dr3sfprob.png" alt="EDR3_SF"> -->
        <img src="{{site.baseurl}}/content/signature_sizes_alltypes_vertical.png">
      </div>
    </div>
  </body>
</html>

I wanted to know the etiology of these signatures. This can be done by modelling the activities against other measurable parameters such as treatment exposures and sample gene inactivations with negative binomial generalised linear models (GLMs). However, the activities are not well approximated by a negative binomial distribution in many cases so this can lead to inflation of false positive associations. In the figure below we create three mock samples by (i) resampling from a negative binomial GLM (ii) resampling the target from the covariates (iii) permuting the target variable. The Wilks likelihood ratio (red points) significantly inflates the false positive rate for cases (ii) and (iii) to ~40%. 

<html>
  <style>
   .imagecontainer {
     display: grid;
     align-items: center;
     grid-template-columns: 1fr 1fr;
     column-gap: 5px;
    }
    img {
      max-width: 100%;
      max-height:100%;
    }
  </style>
  <body>
      <div class="image">
        <!-- <img src="content/sf_healpix_dr3sfprob.png" alt="EDR3_SF"> -->
        <img src="{{site.baseurl}}/content/mock_gene_qqplots_x3.png">
      </div>
  </body>
</html>

I implemented a method called distilled conditional randomised testing (dCRT) which resamples the target variable as a function of covariates many times to generate a null distribution of fits then compares the true fit with the null distribution. This reduces the false positive rate from 40% to 0.1% as shown by the blue points.


### Polygenic scores

Our germline DNA is the sequence we are born with prior to any mutational processes acting on our cells. It is predictive of hereditary traits such as height, eye colour or susceptibility to particular diseases such as many cancers. 

Information from all relevant variants across the genome can be aggregated to generate a single polygenic score (PGS) which is a measure of an individual's predisposition to a given trait. In the simplest case this can be calculated as
<center>
$$ \mathrm{PGS}_i = \sum_j \hat{\beta}_j \, G_{i,j} $$
</center>
where \\(\hat{\beta_{j}}\\) are the association coefficients between variant \\(j\\) and the trait usually estimated from a large cohort and \\(G_{i,j}\\) is the germline variant for participant \\(i\\) at position \\(j\\) with values 0 (homozygous reference), 1 (heterozygous) or 2 (homozygous alternate). I evaluated this for a series of traits for over 10k participants of the 100,000 Genomes Projects. The figure below shows the distribution of PGS evaluated for cancer traits with the blue violins showing participants who have been diagnosed with the given cancer and red showing all other participants. Germline genetics provide a weak prediction of an individual's risk of being diagnosed with a particilar cancer.

<html>
  <style>
    img {
      max-width: 100%;
      max-height:100%;
    }
  </style>
  <body>
      <div class="image">
        <!-- <img src="content/sf_healpix_dr3sfprob.png" alt="EDR3_SF"> -->
        <img src="{{site.baseurl}}/content/cancer_prs_violins.png">
      </div>
  </body>
</html>