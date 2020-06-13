# Au Nanosnake DDA Code

Welcome to the Kopelman laboratory folder for nanosnake DDA computations and related analysis. Each folder has a scripts for different key functions involving DDA analysis. In short, folders involve:

1.) Shape file geometry generation

- Run `spheresolver1234x_1dpnm.py`
- Further instructions are inside code comments

2.) DDSCAT output spectral interpolation (dda_analysis)
- Run as a series of jupyter notebooks
- First examine `interpolator.ipynb` to interpolate DDA output to intermediate gap distnaces
- Second, use `best_lc_finder.ipynb` to fit spectral data from experimental UV-Vis

3.) DDSCAT job submission via Linux utilizing multiprocessing, where the # of cores can be customized, effective radius is specified, etc. (dda-runner)

- DDSCAT is "embarassingly parallel" across wavelengths, so wavelengths can be evenly divided amongst cores
- Included scripts are designed for parallelism on the Slurm or SGE job schedulers    
- Run with `python new_job.py`
- For help with run options use `python new_job.py --help`

For questions about the DDA scripts, please contact kopelman@umich.edu (Dr. Raoul Kopelman), ammclean@umich.edu (Alan McLean), and tgog@umich.edu (Tarun Gogineni) in one email. 
