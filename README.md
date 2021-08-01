## Stars-filtering
## General Info
This project parses database of stars given in .tsv format and perform filtering actions
## Setup
To run this project, directly clone or add all modules in your local machine, then run 'main'.
It will ask for input data, please input all required data (first line: ra, dec; second line: fov_h and fov_v; third line: N).
Make sure the program takes data from the right file. It reads 'cleaned_stars.tsv' (the big one) by default. If you want to change the file, you can do it via config.ini. Also make sure that .tsv file is located in the same folder.
## Output
When the program execution is done, it prints the time of execution, creates .csv file with a name of current timestamp and puts filtered data in that file.
## Additional Info
When the number of stars is ~ 5*10^5, execution time can vary from 0.5 to 10 seconds (depending on FOV and N). When the FOV is too large (It can only happen theoretically, in real life we have some limitations on FOV), execution time can take up to ~15 seconds.
