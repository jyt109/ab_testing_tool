This is a tool that will develop into a full-blown ab-testing tool kit.

##Current state

- Hard coded ``preprocessing()`` to clean ``data/sample.csv``
- Can only test 2 variants
- Finished power calculations and minimum sample size calculations in ``power_functions.py``
- Implemented and tested z-test to test 2 proportions
- Chi-sqaure test in ``chi.py`` has to be cleaned and corrected and moved into the main code

## To-do

- Make interface to setup A/B test easily
- Dashboard to visualize conversion as it goes
- Visualize distribution from z-test, power calc and significance
- Adapt to test for multi-variant
