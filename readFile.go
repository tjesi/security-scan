package main

import (
    "fmt"
    "io/ioutil"
    "strings"
)

func readFile(fileName string) []string {
    b, err := ioutil.ReadFile(fileName)

    if err != nil {
        fmt.Print(err)
    }

    return strings.Split(strings.TrimSpace(string(b)), "\n")
}
