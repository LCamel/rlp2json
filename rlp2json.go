package main

import (
	"encoding/hex"
	"fmt"
	"os"
)

func main() {
	var h = os.Args[1]
	var ba, err = hex.DecodeString(h)
	if err != nil {
		panic("bad input")
	}
	parse(ba, 0)
}
func parse(ba []byte, pos int) int {
	var b byte = ba[pos]
        pos++
	if b >= 0xC0 {
		fmt.Print("[")
		var len int
		len, pos = getLen(ba, pos, int(b-0xC0))
		if len > 0 {
			var done = pos + len
			for {
				pos = parse(ba, pos)
				if pos == done {
					break
				}
				fmt.Print(",")
			}
		}
		fmt.Print("]")
	} else {
		fmt.Print("\"")
		var len int
		if b < 0x80 {
			fmt.Printf("%02x", b)
		} else {
			len, pos = getLen(ba, pos, int(b-0x80))
			for i := 0; i < len; i++ {
				fmt.Printf("%02x", ba[pos])
				pos++
			}
		}
		fmt.Print("\"")
	}
	return pos
}
func getLen(ba []byte, pos int, len int) (int, int) {
	if len >= 0x38 {
		var lenLen int = int(len - 0x38 + 1)
		len = 0
		for i := 0; i < lenLen; i++ {
			len = len*256 + int(ba[pos])
			pos++
		}
	}
	return len, pos
}
