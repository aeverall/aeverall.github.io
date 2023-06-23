---
layout: personalised
title: Astrophysics
permalink: /astro/
---

I did my PhD in astronomy at the Institute of Astronomy in Cambridge from 2018-2021. [Checkout my thesis](https://www.repository.cam.ac.uk/items/f80fe053-206b-4911-adc3-d893a191ad34).

I was co-PI of the Completeness of the Gaiaverse project with [Douglas Boubert](https://www.douglasboubert.com/). You can find out all about it at [gaiaverse.space](https://www.gaiaverse.space/).



## Completeness of the Gaiaverse

Gaia is a satellite which scans the sky continuously making a few scans of each star every month. The Gaia catalogue includes 2bn stars which is only ~2% of the total content of the Galaxy. We want to know given a faint star, what is the probability that Gaia would be able to measure the star and include it in the published catalogue, this is the "selection function".

Every scan has a probability, \\(\theta\\), of making an observation of the star. If 5 successful observations are recorded the star will be included in the published catalogue. Therefore the likelihood of a star having \\(k\\) observations is
<center>
$$ P(k | n, \theta, k\geq 5) =  
\begin{cases}  
\frac{1}{P(k\geq 5|n, \theta)} \binom{n}{k} \theta^k (1-\theta)^{n-k},  & k\geq 5 \\ 0, & \mathrm{otherwise} \end{cases}$$
</center>
where we have in the published catalogue the number of times every star is successfully detected \\(k\\) and we determined the number of times a star was scanned \\(n\\) as a function of position on the sky by modelling the satellite's orbit. We determine \\(\theta\\) as a function of stellar apparent magnitude using a beta prior and optimising across all stars. 

Given \\(\theta\\), the selection probability of any hypothetical star is 
<center>
$$ P(S|n,\theta) = \sum_{k=5}^n P(k | n). $$
</center>

When Gaia made a new data release in 2020, called EDR3, with an additional 2 years of satellite data, I made a quick estimate of the selection function by updating the number of scans \\(n\\) with the increased baseline of the satellite's orbit. 
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
      <div class="image">
        <!-- <img src="content/sf_healpix_dr3sfprob.png" alt="EDR3_SF"> -->
        <img src="{{site.baseurl}}/content/sf_dr2_vs_dr3.png">
      </div>
      <div class="text">
        In the figure at the top is the numnber of times Gaia scanned each position on the sky in DR2 (left) and EDR3 (right) and on the bottom is our estimate of the selection probability for a star of magnitude \(G=21\). The additional scans really improve Gaia's ability to detect faint stars.
      </div>
    </div>
  </body>
</html>

The main purpose of Gaia is to measure the dynamics of stars including their precise positions and velocities, however, only a subset of the total catalogue have these measurements accurately published. The selection function of a subset is
<center>
$$ P(S_\mathrm{subset} | x) = P(S_\mathrm{subset} | S_\mathrm{source}, x) \, P(S_\mathrm{source} | x) $$
</center>
where \\(S_\mathrm{source}\\) is the event of selection in the full source catalogue which I introduced above. 

We modelled the selection function of Gaia subsets using Needlets (a linear combination of spherical harmonics which are locally constrained) on the sky and a Gaussian Process prior as a function of colour and apparent magnitude. The data were aggregated into pixels on the sky and colour magnitude bins and the binomial likelihood function was used to optimise the model parameters
<center>
$$ \log L \propto \sum_{i=p,c,m} k_i\log(q_i) + (n_i-k_i)\log(1-q_i) $$
</center>
where \\(p,c,m\\) are the pixel, colour and magnitude bins and \\(q_i\\) is the model evaluated in the bin. In order to achieve the desired resolution of 2deg on the sky and 0.2mag, this model required 1.7million parameters to fit. We achieved this by accelerating the method with jit compiling using the python module numba to improve evaluation runtime and parallelizing across 80 cores. Even then this took a week to optimize. 

The selection function for the 1.4bn stars in with astrometry in Gaia is given below. The top row shows the fraction of Gaia stars with published astrometry across the sky in four magnitude bins. The second row is our model which resembles the input data very well and finally the residual between the data and the model shows strong agreement. The disagreements are in regions of the sky where the source density is so high that the selection probability falls off on sub-degree scales which we could not resolve e.g. in globular clusters.

<html>
  <style>
    img {
      max-width: 100%;
      max-height:100%;
    }
  </style>
  <body>
      <div class="image">
        <img src="{{site.baseurl}}/content/chisquare_astrometry_jmax5_nside64_M102_CGR1_lm0.3_B2.0_ncores88_3x4hpx.png">
      </div>
  </body>
</html>

<div class="publicationborder">
  Code:
  <ul style="margin-top:-5px;margin-bottom:-1px">
  <li> <a href="https://github.com/gaiaverse/scanninglaw">scanninglaw</a> - call number of scans as a function of position on the sky. </li>
  <li> <a href="https://github.com/gaiaverse/selectionfunctions">selectionfunctions</a> - call the selection functions. </li>
  <li> <a href="https://github.com/gaiaverse/selectionfunctiontoolbox">selectionfunctiontoolbox</a> - use the tools to build your own selection functions.</li>
  </ul>
</div> 
<br>
<div class="publicationborder">
  Publications:
  <ul style="margin-top:-5px;margin-bottom:-1px">
  <li> Douglas Boubert, <b>Andrew Everall</b> <i>et al.</i>  <a href="https://ui.adsabs.harvard.edu/abs/2020MNRAS.497.1826B/abstract">When and where were Gaia's eyes on the sky during DR2?</a> Sept 2020 </li>
  <li>  Douglas Boubert, <b>Andrew Everall</b> <i>et al.</i> <a href="https://ui.adsabs.harvard.edu/abs/2020MNRAS.497.4246B/abstract">What are the odds that a star is missing from Gaia DR2?</a> Oct 2020 <br> </li>
  <li> Douglas Boubert, <b>Andrew Everall</b> <i>et al.</i> <a href="https://ui.adsabs.harvard.edu/abs/2021MNRAS.501.2954B/abstract">Using hidden states to infer gaps, detection efficiencies, and the scanning law from the DR2 light curves.</a> Feb 2021 <br> </li>
  <li> <b>Andrew Everall</b>, Douglas Boubert <i>et al.</i> <a href="https://ui.adsabs.harvard.edu/abs/2022MNRAS.509.6205E/abstract">Astrometry and radial velocity sample selection functions in Gaia EDR3?</a> Feb 2022 </li>
  </ul>
</div>

<!-- ## _Gaia_ Astrometric Spread Function

<html>
  <style>
    img {
      max-width: 100%;
      max-height:100%;
    }
  </style>
  <body>
      <div class="image">
        <img src="{{site.baseurl}}/content/pred-vs-obs_covariance_corr_hpx_G18p1.png">
      </div>
  </body>
</html> -->


## Selection functions of Multifibre specrographs

Multifibre spectrographs are a type of ground-based telescope which takes spectra of bright stars by placing fibre-optic cables under a telescope at the focal position of the star of interest and feeding the light into a spectrometer. At these bright magnitudes all stars on the sky will be in photometric catalogues which can be used as a comparison set. We can work out the selection function of the telescopes by comparing with the photometric catalogues. To do this we start with Baye's theorem
<center>
$$ P(S|x) = \frac{P(x|S)P(S)}{P(x)} \approx \frac{f^\mathrm{spec}(x) \cdot N^\mathrm{spec}/N^\mathrm{phot}}{f^\mathrm{phot}(x)} $$
</center>
where \\(S\\) is the event of selection by the telescope for a star with properties \\(x\\). \\(f(x)\\) are the distributions of stars in the photometric and spectroscopic catalogues and we'll model these as a function of position on the sky, apparent magnitude and colour of the star.

I modelled the density distribution of the photometric catalogue (\\(f^\mathrm{phot}\\)) as a Gaussian Mixture Model (GMM) then also modelled the selection function (\\(P\(S\|x\)\\)) as another GMM. There are two reasons why GMMs are extremely favourable for this problem. You can analytially multiply two GMMs together and get another GMM (in this case multiplying \\(f^\mathrm{phot} \times P(S\|x) = f^\mathrm{spec}\\)). If we assume measurement uncertainties are Gaussian distributed we can also analytically marginalise over these which is allows deconvolution of the underlying density distribution.

I use a Poisson likelihood distribution to model the photometric and spectroscopic distributions
<center>
$$ \log L = \sum_i^N \log(f(x_i)) - \int \mathrm{d}x \, f(x) $$
</center>
which you can derive from a Poisson probability distribution. This is optimised for the photometric distribution then the spectroscopic distribution.

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
        The result is the distribution shown in the figure. The points are stars in the photometric catalogue with those also in the spectroscopic catalogue circled. The model marginalised over each dimension is shown using the purple regions for the photometric and orange for the spectroscopic. The measured distribution of sources is within the uncertainties of the modelled distribution.
      </div>
      <div class="image">
        <!-- <img src="content/sf_healpix_dr3sfprob.png" alt="EDR3_SF"> -->
        <img src="{{site.baseurl}}/content/MockSF_dist_cm-rave2_corrBIC.png">
      </div>
    </div>
  </body>
</html>


## Velocity distributions in the Galaxy

We want to know the distribution of mass in the Milky Way. This is actually a really hard problem. The biggest surveys only observe ~2% of stars in the Galaxy and over 80% of the mass is in the form of Dark Matter which is undetectable. So we need to make indirect observations and use gravity. Stars orbit the Milky Way under the gravitational pull so the distribution of stellar velocities tells us something about the gravitational field. Specifically, if stellar velocities are primarily dispersed towards the center of the galaxy, this suggests a spherical mass distribution. Alternatively velocities dispersed cylindrically implies an oblong (rugby ball) list distribution and dispersed vertically suggests a disky mass distribution. 

I used ~7million stars with measured astrometry and radial velocity. Distances were estimated from parallax using a prior which assumed a realistic velocity distribution. The velocity distribution was assumed to be Gaussian distributed inside any bin for which we maximised the likelihood function
<center>
$$ \log\mathcal{L} = -\frac{1}{2}\log(|2\pi \Lambda|) - \frac{1}{2}\sum_i^N (x_i-\mu)^T \Lambda_i (x_i - \mu) $$
</center>
where \\( \Lambda_i = C_i + \Sigma \\) and \\( C_i \\) is the measurement covariance matrix for star \\(i\\) and \\(\Sigma\\) is the velocity ellipsoid.

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
        The resulting ellipsoids, project into 2D are shown on the right here as a function of radius from the Galactic center \(R\) and height above the Galactic plane \(z\) (The sun is around \(R=8.27, z=0\)). I also estimated the overall tilting of the velocity ellipsoids under the model \(\alpha = \alpha_0 \arctan\left(\frac{|z|}{R}\right)\), where \(\alpha\) is the angle between the Galactic plane and the ellipsoid, using linear regression. I find \(\alpha_0 = 0.950 \pm 0.007\) suggesting a small but significant flattening of the ellipsoids.
      </div>
      <div class="image">
        <!-- <img src="content/sf_healpix_dr3sfprob.png" alt="EDR3_SF"> -->
        <img src="{{site.baseurl}}/content/rvs_ellipsoid-cov_sch_dbclean.png">
      </div>
    </div>
  </body>
</html>



<!-- ## Tracer Density of the Milky Way

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
      <div class="image">
        <img src="{{site.baseurl}}/content/mock_sys_sample4_1000000_007_thin_corner.png">
      </div>
      <div class="text">
        Mock parameter estimates
      </div>
    </div>
  </body>
</html> -->