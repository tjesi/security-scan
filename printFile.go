package main

import (
	"log"
	"os"
)

/*
printFile receice a list of foldernames, and check that
all of them exists. otherwise, create new folder. create
a new file and put it in the inner folder, and put the
content string in the new file.
*/

func printFile(folders []string, fileName, content string) {

	path := "."
	// Go through all foldernames, and create
	// a new folder if it doesn't exist
	for _, folder := range folders {
		path += "/" + folder
		if _, err := os.Stat(path); os.IsNotExist(err) {
			os.Mkdir(path, os.ModeDir)
		}
	}

	// Create a file (or overwrite if it exists)
	file, err := os.Create(path + "/" + fileName)

	// Output any errors
	if err != nil {
		log.Fatal(err)
	}

	// Write a string to the file
	file.WriteString(content)

	// Close the file
	file.Close()
}
