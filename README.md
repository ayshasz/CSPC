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

**Partner Reproducibility**
- I shared my CSPC repository with a partner who cloned it and created the environment from environment.yml. First,there was  an issue with Conda recognizing the environment, but after activating and deactivating Conda, the environment worked correctly. The tests then ran successfully without any changes to the repository files.

## PW1 --- Lab B:

- The data shows that the number of particles decreasing over time. The observed data is close to the analytical decay law, but not exactly the same. 
The Snakemake pipeline uses the CSV data and `plot.py` to create `figure.png`.


## PW2 --- Lab A: Motion from Tracking Data
- The mean acceleration from the free-fall data was -8.58 m/s², which is reasonably close to the expected value of -9.81 m/s². The acceleration was very noisy because taking derivatives makes the measurement noise larger.

After integrating the acceleration back to velocity and then to position, the recovered position was close to the original position. The largest difference between them was 0.785 m. This shows that integration can reduce the effect of the noise

BONUS: For the 2D trajectory, I calculated the velocity in the x and y directions using np.gradient(). I then calculated the speed using sqrt(vx**2 + vy**2) and plotted the trajectory and speed over time.