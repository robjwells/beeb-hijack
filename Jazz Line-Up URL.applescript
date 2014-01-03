property programme : "jazz line-up"
property python_script : "\"/Users/robjwells/Programming/Python/BBC Radio AHP/beebhijack\""

return (do shell script python_script & " url '" & programme & "'")
