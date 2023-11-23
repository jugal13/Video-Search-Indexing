# video-search-indexing

Tasks:
1. Consider one channel of each frame (Y), convert each value (float to int (ceil)) of the frame to a string, and concatenate all of them (around 100k values per frame). (Pooja)
2. Use a hash function to convert the above string to a 256-bit hash. (Sanjay)
3. What DB to use? Store all hash values in a DB and index it (Pratheeksha)
4. Searching the db for an exact matching frame and using a player to display. (Jugal)

One time setup:
python mongo_setup.py

Make sure to start your mongod server by locating mongod from the bin folder and creating a data folder
./mongod --dbpath /usr/local/data

Reference

https://github.com/oaubert/python-vlc/blob/master/examples/tkvlc.py
