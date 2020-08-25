# Stata module

## Note about this repo

Important note! 

This repo is using Git LFS (Large File Storage) to handle `.dta`, `.csv`, and other large data files. 

To pull from this repo, you should first install `git-lfs` on the command line with:
```
git lfs install
```

To track new large file types, use a command similar to this:
```
git lfs track '*.csv'
```

To push 

Read more about Git LFS [here](https://towardsdatascience.com/uploading-large-files-to-github-dbef518fa1a) and [here](https://git-lfs.github.com/).



## Usage

In the python file you would like to use this Stata module in, first add this line after the imports section ([source](https://www.kite.com/python/answers/how-to-import-a-class-from-another-file-in-python)):
```
sys.path.append("relative-path-to-stata-functionality-directory")
```

Then import the class from the file:
```
from stata import Stata
```

Then, you can instantiate a stata object:
```
my_stata = Stata()
output = my_stata.load_dta(dta_file)
```

## Testing

To run our tests, cd into the testing directory, and run the command:
```
python .\test-stata.py > .\output\open-stata.log        # for windows
python ./test-stata.py > ./output/open-stata.log        # for mac/linux
```

`testing/test-stata.py` tests the creation of a `stata` object and all methods implemented in `stata.py`

The output can be compared to `real-stata-output.log`, a log file produced on [date] , by running `testing/comparison/comparison.do`.