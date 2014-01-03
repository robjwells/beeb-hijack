property programme : "jazz line-up"
property python_script : "\"/Users/robjwells/Programming/Python/BBC Radio AHP/beebhijack\""

on process(theArgs)
	set saveTID to AppleScript's text item delimiters
	set AppleScript's text item delimiters to {"|"}
	
	set details to the text items of (do shell script python_script & " details '" & programme & "'")
	
	set AppleScript's text item delimiters to saveTID
	
	set track_name to (item 1 of details) & ": " & (item 2 of details)
	set track_list to item 3 of details
	
	tell application "iTunes"
		set recording to item 1 of theArgs
		set imported_track to (add recording)
		
		delay 60 -- Give iTunes a chance to get going
		
		set name of imported_track to track_name
		set bookmarkable of imported_track to true
		set shufflable of imported_track to false
		set lyrics of imported_track to track_list
		add (get location of imported_track) to playlist "Radio 3 Jazz"
	end tell
end process
