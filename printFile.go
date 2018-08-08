package main

import (
  "log"
  "os"
)

// FILE I/O
func printFile(folders []string, fileName, content string) {
  
  path := "."
  for _,folder := range folders {
    path += "/" + folder
    if _, err := os.Stat(path); os.IsNotExist(err) {
      os.Mkdir(path, os.ModeDir)
    }
  }

	// Create a file
	file, err := os.Create(path+"/"+fileName)

	// Output any errors
	if err != nil {
		log.Fatal(err)
	}

	// Write a string to the file
  file.WriteString(content)

	// Close the file
	file.Close()
}
