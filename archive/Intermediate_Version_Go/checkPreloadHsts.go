package main

import "strings"

/*
checkPreloadHSTS receive the name of a website and name of preloaded
HSTS list from Google or Firefox (or others) and return true if the
website is in the list. this check is performed if the website does
not send a HSTS-header when connecting, in case it was submitted to
the preloaded lists early. the website are always supposed to send
a HSTS-header if this is the case, but it doesn't always do that
in practice
*/

func checkPreloadHSTS(website, hstsFile string) bool {
	websites := readFile(hstsFile)

	for _, line := range websites {
		if strings.Contains(line, strings.ToLower(website)) {
			if strings.Contains(strings.Split(line, ", ")[1], "1") {
				return true
			}
		}
	}
	return false
}
