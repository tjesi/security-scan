package main

import "strings"

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
