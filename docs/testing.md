# Testing
Speculator uses unit tests for nearly every function defined in the features and utility packages.
In addition, integration tests are used when combining unit tested functions to create a core feature.
Integration tests should not be used until each component has been successfully unit tested.  This ensures a higher probability of success as a whole, and helps pinpoint the root of the cause when debugging.

## Running Unit/Integration Tests
```
cd $SPECULATOR_PATH/speculator/tests
python -m unittest discover
```
This test must run successfully with zero errors before pushing to master.

## Travis-CI
Every pull request is checked through Travis-CI before being merged, validating functionality across all systems and eliminating any special local configurations.
