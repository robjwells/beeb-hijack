# BBC Radio recording scripts

A Python module (bbcradio.py) and a handful of scripts to help you record and process BBC Radio programmes, written with Rogue Amoeba’s [Audio Hijack Pro][ahp] in mind.

[ahp]: http://rogueamoeba.com/audiohijackpro/

The main script is beebhijack, which acts as the interface to bbcradio.py. It has two modes: URL and details, which return the streaming URL for a programme’s most recent episode, and the title, date and track list for that episode, respectively.

The two AppleScripts are examples of what’s needed to bridge the gap between Python and Audio Hijack, which can run AppleScripts at the start and end of recording.

`Jazz Line-up URL.applescript` hands Audio Hijack the streaming URL for the latest episode of that programme, while `Process Jazz Line-Up.applescript` adds the recording to iTunes, renames it and adds the track list to the lyrics field.

## Requirements

*   Python 3
*   [docopt](http://docopt.org)
*   [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)

## Installation and usage

1.   Put bbcradio.py and beebhijack in a directory together.
2.   Grab the programme codes for those that you want to record from the end of their homepage URLs (here’s [Jazz Line-Up’s][jlu], for example).
3.   Add the codes to `PROG_DICT` in bbcradio.py under suitable keys.
4.   Create individual URL and details AppleScripts from the examples provided.
5.   Set up sessions in Audio Hijack, calling the URL AppleScript when recording starts and the processing AppleScript when recording ends.

[jlu]: http://www.bbc.co.uk/programmes/b006tnmw

For a more detailed description and an explanation of how the scripts work [see this blog post][rjw].

[rjw]: http://robjwells.com/post/72667571379/hijacking-the-bbc

## Acknowledgements

This project is based on Dr Drang’s [radio2][drang-r2] project, and owes a heavy debt to his work.

[drang-r2]: https://github.com/drdrang/radio2


## Licence

[MIT](http://opensource.org/licenses/MIT).

The post-processing script is an edited version of Dr Drang’s, which was based on a script by Rogue Amoeba that you can see near the end of the [Audio Hijack Pro manual][ahp-manual].

[ahp-manual]: http://www.rogueamoeba.com/audiohijackpro/download/AudioHijackProManual.pdf
