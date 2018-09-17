package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
	"time"
)

func main() {
	start := time.Now()
	temp := time.Now()
	path := "./websites"
	duration := ""

	// check all files with url to websites we want to scan
	files, err := ioutil.ReadDir(path)
	if err != nil {
		log.Fatal(err)
	}

	// log the time we use to complete individial and complete scans
	date := time.Now().UTC().Format("2006-Jan-02")
	fmt.Printf("\nScan " + date + " started.\n\n")
	error := 1

	for _, file := range files {

		fmt.Printf("File " + file.Name() + " opened. \n\n")
		preload := ""
		sslError := ""

		for i, website := range readFile(path + "/" + file.Name()) {
			if website == "" {
				continue
			}

			// add metadata about website
			content := ""
			content += "list:" + file.Name()[:2] + "\n"
			content += "rank:" + strconv.Itoa(i+1) + "\n"
			content += "website:" + website + "\n"

			// add data about security headers
			content += securityHeaders(website, &preload)

			// error handling in case of no SSL
			if strings.Contains(content, "SSLerror") {
				fmt.Printf("#%d: "+website+" does not use HTTPS!\n\n", error)
				sslError += website + "\n"
				error++
			} else {
				// check certificate data if SSL connection
				content += https(website)
			}

			printFile([]string{"scan", date, file.Name()[:2]}, website+".txt", content)
		}

		// store metadata about the scan
		printFile([]string{"scan", date, "sslError"}, file.Name()[:2]+"-sslError.txt", sslError)
		printFile([]string{"scan", date, "preload"}, file.Name()[:2]+"-preload.txt", preload)

		fmt.Printf("\nFile " + file.Name() + " done in " + time.Since(temp).String() + ".\n\n")
		duration += file.Name()[:2] + ":" + time.Since(temp).String() + "\n"
		temp = time.Now()
	}
	printFile([]string{"scan", date, "meta"}, "duration.txt", duration)
	fmt.Printf("The scan is completed in " + time.Since(start).String() + ".\n\n")
}
