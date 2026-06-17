# AOS and miniAOS Bias Characterization Cookbook

[![Binder](http://binder.mypythia.org/badge_logo.svg)](http://binder.mypythia.org/v2/gh/rcjackson/bnf-aos-bias-characterization/main?labpath=notebooks)

This ARM Cookbook characterizes the measurement bias between the ARM Aerosol Observing System (AOS) and the miniaturized miniAOS suite deployed at the Bankhead National Forest (BNF) AMF3 site, covering the November 2024–April 2025 deployment.

## Motivation

The full AOS occupies two seatainers and draws substantial power, which limits where and how quickly it can be deployed. The miniAOS is a smaller, lower-power subset of instruments built to measure aerosol size distributions in places the full AOS cannot easily go (towers, difficult terrain, tight spaces). BNF is the **first** miniAOS deployment, so its measurements need to be validated against the co-located reference AOS before the miniAOS can be trusted on its own.

These notebooks show how to do that validation: load the ARM datastreams, align instruments that sample at different rates, apply data-quality filtering, and quantify the bias between two instrument pairs — both as integrated total number concentration and as the full size-resolved distribution — and how that bias varies over time and with ambient conditions.

The two instrument pairs compared throughout are:

- **mSEMS (miniAOS) vs. SMPS (AOS)** — both size particles by **electrical mobility** diameter, so close agreement is expected; residual differences point to calibration or flow-rate drift.
- **OPC (miniAOS) vs. APS (AOS)** — **optical** vs. **aerodynamic** diameter, so a systematic, physically-meaningful offset is expected.

## Authors

[Bobby Jackson](https://github.com/rcjackson), Ashish Singh

### Contributors

<a href="https://github.com/rcjackson/bnf-aos-bias-characterization/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=rcjackson/bnf-aos-bias-characterization" />
</a>

## Structure

This cookbook is organized as two companion notebooks in the `notebooks/` directory.

### 1. Number concentration (`bnf-aos-miniaos-number-concentration.ipynb`)

Compares **integrated total particle number concentration** ($N$) between the two instrument pairs. It loads the four ARM datastreams, resamples them to a common 1-minute grid and inner-joins on time, filters using Data Quality Reports (DQRs), and fits linear regressions of miniAOS vs. AOS concentration. The bias is broken out by month and across four deployment sub-periods (Nov, Dec–Jan, Feb–Mar, Apr), and examined as a function of temperature, relative humidity, and wind speed.

### 2. Size distributions (`bnf-aos-miniaos-size-distribution.ipynb`)

Extends the comparison to the **size-resolved** number distribution ($dN/d\log D_p$) to reveal whether bias is uniform or concentrated in particular size ranges. It compares the sub-micron range (mSEMS vs. SMPS, 10–337 nm) and the super-micron range (OPC vs. APS), rebinning the two instruments of each pair onto a shared diameter grid (via the `align_size_distributions.py` helper) before computing mean distributions and ratios, again across the same four deployment periods. It also generates daily, weekly, and per-event diagnostic plots.

## Running the Notebooks

You can run these notebooks either via [Binder](https://mybinder.org/) or on your own machine.

> **Data access:** The notebooks download ARM datastreams from [ARM Data Discovery](https://adc.arm.gov/discovery/) using `act.discovery.download_arm_data`. You will need a free [ARM account](https://adc.arm.gov/) and must set the `ARM_USERNAME` and `ARM_PASSWORD` environment variables (or substitute your credentials in the download cells) before running.

### Running on Binder

The simplest way to interact with a Jupyter Notebook is through [Binder](https://mybinder.org/), which runs a [Jupyter Book](https://jupyterbook.org) in the cloud. Navigate to the top-right corner of any page you are viewing, click the rocket-ship icon, and select "launch Binder". After a moment you will be presented with an interactive notebook whose code cells you can execute with {kbd}`Shift`\+{kbd}`Enter`. See [Getting Started with Jupyter](https://foundations.projectpythia.org/foundations/getting-started-jupyter.html) for details.

### Running on Your Own Machine

1. Clone the repository:

   ```bash
   git clone https://github.com/rcjackson/bnf-aos-bias-characterization.git
   ```

1. Move into the repository directory:

   ```bash
   cd bnf-aos-bias-characterization
   ```

1. Create and activate the conda environment from `environment.yml`:

   ```bash
   conda env create -f environment.yml
   conda activate arm-cookbook-dev
   ```

1. Move into the `notebooks` directory and start JupyterLab:

   ```bash
   cd notebooks/
   jupyter lab
   ```
