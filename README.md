# vhbb_styling

Okay, so you're going to need to do the following to install.

```bash
cmsrel CMSSW_8_4_0
cd CMSSW_8_4_0/src/
cmsenv
virtualenv -p "$(which python)" venv
source venv/bin/activate
git clone git@github.com:swang373/vhbb_styling.git
cd vhbb_styling/vhbbtools/
python setup.py install
cd ../pubstyle
```

Inside the pubstyle directory, you'll see the Example1 folder where I demonstrated that my refactored code works exactly like what the pub comm released. They provided myMacro.py, I tested my code using myMacro_vhbbstyle.py.

The important points are using the construct:
```python
with CMSCanvas() as canvas:
    pass
```
and 
```python
canvas.decorate()
```
The second call is a bound method, but don't be fooled! It modifies the current gPad underneath and doesn't necessarily have to modify the canvas. For instance, I use it just to modify the top pad in the plots. I'll turn it into a standalone function later.

Poke around the other directories to see what I did. You'll see a common approach in the scripts, tailored to each set of plots which are close enough to each other to be used as consistent input. The logic flows from top to bottom in short blocks of context. Every line in there is intentional, and sometimes comments denote features that need to be turned on or off depending on the plot to restyle. You may have to run the script once on a plot, uncomment or recomment, then rerun on a different plot. I wish it were more elegant, but so it goes.

To run stuff, it's just
```bash
python restyle.py
```
You'll find that restyle.py is more or less a template present in each folder. Change the transform_upper_pad() and transform_lower_pad() functions as you need. The restyle() function takes the path to the .root file and in general shouldn't need to be modified except in instances of global option changes. Way below in the main area of the script is where you fiddle around with what path the function should take.

If you ever exit and need to set up again, just do
```bash

cmsenv
source venv/bin/activate
```
