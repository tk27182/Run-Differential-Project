# Run-Differential-Project


Code to analyze run differential over time for teams

## Analysis Plan

1. Collect data from a single season to start, then over multiple seasons
2. Check and see at which game the gradient stops changing (make histogram)
3. Do basic curve fitting (think temperature curve data)
4. Use LSTM to predict next values
5. Use LSTM to predict final value
  a. drop months, weeks, days in advance
  b. see if AUC drops off
6. Try LCGA or GMM (might not work if the curves are not linear)
7. Could also try Hierarchical clustering

