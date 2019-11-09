package main

import (
	"fmt"
	"io/ioutil"
	"path/filepath"
	"math/rand"
)

func readSudoku(filename string) ([][]byte, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	grid := group(filter(data), 9)
	return grid, nil
}

func filter(values []byte) []byte {
	filtered_values := make([]byte, 0)
	for _, v := range values {
		if (v >= '1' && v <= '9') || v == '.' {
			filtered_values = append(filtered_values, v)
		}
	}
	return filtered_values
}

func display(grid [][]byte) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid); j++ {
			fmt.Print(string(grid[i][j]))
		}
		fmt.Println()
	}
}

func group(values []byte, n int) [][]byte {
	group_values := make([][]byte, 0, n)

	val_num := len(values) / n

	for i := 0; i < val_num; i++{
        row := make([]byte, n)

		for j := 0; j < n; j++{
            row[j] = byte(values[n*i + j])
		}

        group_values = append(group_values, row)
	}

	return group_values
}

func getRow(grid [][]byte, row int) []byte {

	return grid[row]
}

func getCol(grid [][]byte, col int) []byte {
	var col_elements []byte

	for i := 0; i < len(grid); i++{
		col_elements = append(col_elements, grid[i][col])
	}

	return col_elements
}

func getBlock(grid [][]byte, row int, col int) []byte {
	var block_elements []byte
	row_begin := (row / 3) * 3
	col_begin := (col / 3) * 3

	for i := 0; i < 3; i++{
		for j := 0; j < 3; j++{
			block_elements = append(block_elements, grid[row_begin + i][col_begin + j])
		}
	}

	return block_elements
}

func findEmptyPosition(grid [][]byte) (int, int) {
	for i := 0; i < len(grid); i ++{
		for j := 0; j < len(grid[0]); j++{
			if grid[i][j] == '.'{
				return i, j
			}
		}
	}

	return -1, -1
}

func contains(values []byte, search byte) bool {
	for _, v := range values {
		if v == search {
			return true
		}
	}
	return false
}

func findPossibleValues(grid [][]byte, row int, col int) []byte {
	possible := make(map[byte]bool)

	//possible[byte]bool - byte это возможное значение, если bool = true

	for i := '1'; i <= '9'; i++{
		possible[byte(i)] = true
	}

	for _, i := range getCol(grid, col){
        if i != '.'{
            possible[byte(i)] = false
        }
	}
	for _, i := range getRow(grid, row){
        if i != '.'{
            possible[byte(i)] = false
        }
	}

	for _, i := range getBlock(grid, row, col){
        if i != '.'{
            possible[byte(i)] = false
        }
	}

	possible_values := make([]byte, 0)

	for val := range possible{

		if possible[val]{
			possible_values = append(possible_values, byte(val))
		}
	}


	return possible_values

}

func solve(grid [][]byte) ([][]byte, bool) {
	row, col := findEmptyPosition(grid)

	if row != -1{
		possible_vals := findPossibleValues(grid, row, col)

		for _, val := range possible_vals{
			grid[row][col] = byte(val)

			solution, status := solve(grid)

			if status{
				return solution, true
			}else{
				grid[row][col] = '.'
			}
		}
	}else{
		return grid, true
	}

	return nil, false
}

func checkSolution(grid [][]byte) bool {
	for col := 0; col < 9; col++{
		col_vals := getCol(grid, col)

		possible_vals := make(map[int]bool)

		count := 0

		for val := range col_vals {
			if val == '.'{
				return false
			}

	        if possible_vals[val] == false{
				possible_vals[val] = true
				count += 1
			}
	    }

		if count != 9{
			return false
		}
	}

	return true
}

func generateSudoku(N int) [][]byte {
	var grid [][]byte
	possible_coord := make(map[int] []byte)


	for i := byte(0); i < 9; i++{
		for j := byte(0); j < 9; j++{
			grid[i][j] = '.'

			possible_coord[int(9*i + j)] = append(possible_coord[int(9*i + j)], i)
			possible_coord[int(9*i + j)] = append(possible_coord[int(9*i + j)], j)
		}
	}

	grid, _ = solve(grid)

	N = 81 - N

	for  i := 0; i < N; i++{
		num := rand.Intn(len(possible_coord)-1)
		row, col := possible_coord[num][0], possible_coord[num][1]

		grid[row][col] = '.'

		delete(possible_coord, num)
	}

	return grid
}

func main() {
	puzzles, err := filepath.Glob("puzzle*.txt")
	if err != nil {
		fmt.Printf("Could not find any puzzles")
		return
	}
	for _, fname := range puzzles {
		go func(fname string) {
			grid, _ := readSudoku(fname)
			solution, _ := solve(grid)
			fmt.Println("Solution for", fname)
			display(solution)
		}(fname)
	}

	var input string
	fmt.Scanln(&input)
}
