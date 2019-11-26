package main

import (
	tm "github.com/buger/goterm"
    "os"
    "fmt"
    "time"
)


func run(life GameOfLife) (bool){
    tm.Clear()
    tm.MoveCursor(0, 0)

    box := tm.NewBox(life.Cols + 4, life.Rows + 2, 0)

    for i := 0; i < len(life.Curr_generation); i++{
        for j := 0; j < len(life.Curr_generation); j++{
            if life.Curr_generation[i][j] == 1{
                fmt.Fprint(box, "*")
            }else{
                fmt.Fprint(box, " ")
            }
        }
        fmt.Fprint(box, "\n")
    }

    tm.Print(box.String())
	tm.Flush()

    return life.Is_changing()
}


func main() {
    var rows,cols int;
    fmt.Print("Введите размеры поля через пробел: ")
    fmt.Fscan(os.Stdin, &rows, &cols)
    fmt.Print("Рандомное поле(0/1)? ")

    var randomize bool
    fmt.Fscan(os.Stdin, &randomize)

    var life GameOfLife;
    life.Init(rows, cols, randomize, 1000)

    for run(life){
        life.Step();
        time.Sleep(400 * time.Millisecond)
    }
}
