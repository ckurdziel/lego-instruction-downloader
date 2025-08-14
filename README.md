# Lego Instruction Downloader
I have a ton of lego sets and all the instruction booklets take up a lot of space. I wanted to download all of them into PDF form. Lego doesn't have an easy API for this so we need to use the Brickset API (v3) to accomplish this.
Given a text file sets.txt with all of my set numbers in it, hit the Brickset API and return a list of instruction PDFs. Limit these to US PDFs only (typically these have v39 in the description). Download and sort these into folders for each set.
