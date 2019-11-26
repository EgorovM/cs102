package main

import (
    "math/rand"
    "reflect"
    "strconv"
    "bufio"
    "fmt"
    "os"
)

type GameOfLife struct{
    Rows int;
    Cols int;
    Prev_generation [][]int;
    Curr_generation [][]int;
    Max_generations float64;
    Generations int;
}


func display(grid [][]int){
    for i := 0; i < len(grid); i++{
        fmt.Println(grid[i]);
    }
    fmt.Println();
}


func make_grid(Rows int, Cols int) [][]int{
    var Grid = make([][]int, Rows)

    for i := 0; i < Rows; i++{
        Grid[i] = make([]int, Cols)
    }

    return Grid
}


func (s *GameOfLife) Init(rows, cols int, randomize bool, max_generations float64){
    s.Rows = rows;
    s.Cols = cols;
    s.Prev_generation = make_grid(rows, cols);
    s.Curr_generation = s.Create_grid(randomize);
    s.Max_generations = max_generations;
    s.Generations = 1;
}


func (s GameOfLife) Create_grid(randomize bool) ([][]int) {
    var Grid = make_grid(s.Rows, s.Cols)

    if randomize{
        for row := 0; row < s.Rows; row++{
            for col := 0; col < s.Cols; col++{
                Grid[row][col] = rand.Intn(2);
            }
        }
    }

    return Grid
}


func (s GameOfLife) Get_neighbours(x int, y int) ([]int, int){
    var neighbours [] int;
    var count int;

    for i := -1; i < 2; i++{
        for j := -1; j < 2; j++{
            if(x + i >= 0 && x + i < s.Rows && y + j >= 0 && y + j < s.Cols && (i != 0 || j != 0)){
                neighbours = append(neighbours, x + i, y + j);
                count += s.Curr_generation[x+i][y+j]
            }
        }
    }

    return neighbours, count
}


func (s GameOfLife) Get_next_generation() ([][]int){
    var new_grid = make_grid(s.Rows, s.Cols);

    for i := 0; i < s.Rows; i++{
        for j := 0; j < s.Cols; j++{
            _, count := s.Get_neighbours(i, j);

            if s.Curr_generation[i][j] == 0 && count == 3{
                new_grid[i][j] = 1;
            }else if(s.Curr_generation[i][j] == 1 && (count == 2 || count == 3)){
                new_grid[i][j] = 1;
            }
        }
    }

    return new_grid
}


func (s *GameOfLife) Step() {
    s.Prev_generation = s.Curr_generation;
    s.Curr_generation = s.Get_next_generation();
    s.Generations++;
}


func (s GameOfLife) Is_max_generations_exceed() (bool){
    return float64(s.Generations) > s.Max_generations
}


func (s GameOfLife) Is_changing() (bool){
    return !reflect.DeepEqual(s.Prev_generation,s.Curr_generation);
}


func (s GameOfLife) Save(filename string) {
    file, err := os.Create(filename);
    if err != nil {
    	return
    }

    for i := 0; i < s.Rows; i++{
        for j := 0; j < s.Cols; j++{
            file.Write([]byte(strconv.Itoa(s.Curr_generation[i][j])));
        }
        file.WriteString("\n");
    }

    defer file.Close();
}

func FromFile(filename string) (GameOfLife){
    var game GameOfLife;

    file, err := os.Open(filename);
    if err != nil {
    	return game;
    }

    defer file.Close();

    reader := bufio.NewReader(file)

    var grid_lines []string;

    line, _ := reader.ReadString('\n')

    for line != ""{
        grid_lines = append(grid_lines, line[:len(line)-1]);
        line, _ = reader.ReadString('\n')
    }

    game.Init(len(grid_lines), len(grid_lines[0]), false, 100);

    grid := make_grid(len(grid_lines), len(grid_lines[0]));

    for i := 0; i < len(grid_lines); i++{
        for j := 0; j < len(grid_lines[0]); j++{
            grid[i][j] = int(grid_lines[i][j]) - 48;
        }
    }
    game.Curr_generation = grid
    return game;
}
