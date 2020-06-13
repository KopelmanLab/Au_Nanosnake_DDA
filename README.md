# Au Nanosnake DDA Code

Welcome to the Kopelman laboratory folder for nanosnake DDA computations and related analysis. Each folder has a scripts for different key functions involving DDA analysis. In short, folders involve:

1.) Shape file geometry generation

- Further instructions are inside code comments

2.) DDSCAT output spectral interpolation (dda_analysis)

3.) DDSCAT job submission via Linux utilizing multiprocessing, where the # of cores can be customized, effective radius is specified, etc. (dda-runner)

- DDSCAT is "embarassingly parallel" across wavelengths, so wavelengths can be evenly divided amongst cores
- Included scripts are designed for parallelism on the Slurm or SGE job schedulers    
- Run with `python new_job.py`
- For help with run options use `python new_job.py --help`

For questions about the DDA scripts, please contact kopelman@umich.edu (Dr. Raoul Kopelman), ammclean@umich.edu (Alan McLean), and tgog@umich.edu (Tarun Gogineni) in one email. 
