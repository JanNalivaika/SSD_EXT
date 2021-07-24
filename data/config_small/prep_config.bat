
REM file prep_config.bat
REM 
REM prepare the small configuration for the app
REM 
REM in this small configuration the trainig and the validation data already generated
REM
REM to be started from folder data/config_samll

REM prep Training set
set folder=..\trset\
del %folder%*.png
del %folder%*.npy

copy .\training_set\* %folder%


REM prep Validation set
set folder=..\valset\
del %folder%*.png
del %folder%*.npy

copy .\validation_set\* %folder%


pause