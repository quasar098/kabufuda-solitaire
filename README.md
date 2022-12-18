# kabafuda solitaire

![demo.png](assets/demo.png)

(from last call bbs)

the assets are ripped from last call bbs

the game is about piracy anyway so i think this is the "correct" usage of last call bbs

## how to play:

### goal:

get all of the same numbered card ontop of each other

### important:

- in regular solitaire you alternate colors and stack them in descending order.
here, you group them up with the same card (all 1s together, all 2s together, etc)

- you cannot take a complete stack (4 of the same) by itself and move it. 
it is locked into place forever

- also, there is no undo move. the entire point of the game is to
plan ahead of time your moves

- this game is treeware. that's "tree" ware, not free ware.
if you enjoyed the game, plant a tree near you (and recommend last call bbs to a friend)

### free slots:

this depends on difficulty

- expert starts with 1 free slots
- hard starts with 2 free slots
- normal starts with 3 free slots
- easy starts with all 4 free slots

you can unlock free slots by making complete stacks (4 of the same) by themselves 
in the bottom 8 slots (not the top 4)

### build instructions:

1) Install the necessary python packages with `pip install -r requirements.txt`
2) Check that it runs from source by running the main.py file
3) Install PyInstaller module
4) Navigate in cmd or bash to the root directory of this project
5) Run `PyInstaller main.py --clean --onefile --noconsole --add-data "./assets;assets"`
**NOTE:** you need to replace the ; with : on unix systems
   

#### build command explained:

The `--clean` part of the build command helps the executable be not flagged as a virus by Windows Defender

The `--onefile` makes it all one file instead of a dll nightmare

The `--noconsole` starts the pygame window without a console alongside it

The `--add-data` part takes the assets folder and bundles it with the executable
