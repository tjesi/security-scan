package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

/*
readFile receive the name of a file, and return the content as
a list of strings where each line in the original file is split
into new elements in the list
*/

func readFile(fileName string) []string {
	b, err := ioutil.ReadFile(fileName)

	if err != nil {
		fmt.Print(err)
	}

	return strings.Split(strings.TrimSpace(string(b)), "\n")
}
