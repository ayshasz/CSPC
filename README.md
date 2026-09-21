# CSPC - Computer Science for Physics and Chemistry

My coursework repository. Each practical is under PW<n>/Lab <X>/.

## Setup
Create the environment for a given lab:
conda env create -f PW<n>/Lab\ <X>/environment.yml
conda activate cspc
---


## PW1 - Lab A: Reproducible Foundations

**What I built:**
- Set up the CSPC repo structure with Conda and Git and wrote a decay simulation with tests and a speed test comparing Python loops to NumPy.

**Speed comparison (loop vs NumPy):**
- loop : 4.169049744999938 s
- numpy : 0.00026662800019039423 s
- speed-up: 15636.203782134267 x faster

**Tests:** all passing? (yes / no) == yes

**Conclusion:**
- I learned how to use Git branches and merges, create a Conda environment and run automated tests with pytest. The NumPy implementation was noticeably faster than the pure-Python loop. 