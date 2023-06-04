package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

// ---------------------------------------------------------------------------------------------------------------------
// -- CellDistances ----------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------

type CellDistance struct {
	Cell     *Cell
	Distance int
	Path     Cells
}

func (cellDistance *CellDistance) IsMiddleCell(mainStruct *MainStruct, maxDistance int) (result bool) {
	var opponentBaseDistances = mainStruct.OpponentBases.ShowClosest(cellDistance.Cell, mainStruct, maxDistance)

	if len(opponentBaseDistances) < 1 {
		return false
	}

	var difference = opponentBaseDistances[0].Distance - cellDistance.Distance
	if difference == 0 || (difference > 0 && difference <= 2) || (difference < 0 && difference >= -2) {
		return true
	}

	return false
}

func (cellDistance *CellDistance) IsCloseCell(mainStruct *MainStruct, maxDistance int) (result bool) {
	var opponentBaseDistances = mainStruct.OpponentBases.ShowClosest(cellDistance.Cell, mainStruct, maxDistance)

	if len(opponentBaseDistances) < 1 {
		return true
	}

	if cellDistance.Distance < opponentBaseDistances[0].Distance {
		return true
	}

	return false
}

type CellDistances []CellDistance

func (distances CellDistances) Len() int {
	return len(distances)
}

func (distances CellDistances) Swap(i, j int) {
	distances[i], distances[j] = distances[j], distances[i]
}

func (distances CellDistances) Less(i, j int) bool {
	return distances[i].Distance < distances[j].Distance
}

// ---------------------------------------------------------------------------------------------------------------------
// -- Cell -------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------

type ResourceType int
type NeighID int
type CellIndex int

const (
	Null     ResourceType = 0
	Eggs                  = 1
	Crystals              = 2
)

const EmptyNeighbour = -1

type Cell struct {
	Index           CellIndex
	ResourceType    ResourceType
	InitialResource int
	Resources       int
	MyAnts          int
	OpponentAnts    int
	Neigh0          CellIndex
	Neigh1          CellIndex
	Neigh2          CellIndex
	Neigh3          CellIndex
	Neigh4          CellIndex
	Neigh5          CellIndex
	OpponentBase    bool
	MyBase          bool
}

type Cells []*Cell
type CellMap map[*Cell]bool

func (cell *Cell) DistanceTo(stopCell *Cell, mainStruct *MainStruct, maxDistance int) (distance int, path Cells) {
	type Node struct {
		cell     *Cell
		parent   *Node
		distance int
	}

	var queue = []*Node{{cell: cell}}
	var visited = make(map[*Cell]bool)
	visited[cell] = true
	var foundAmount = -1
	var foundPath Cells
	var foundDistance int
	var passed int

	for len(queue) > 0 {
		var currentNode = queue[0]
		visited[currentNode.cell] = true
		queue = queue[1:]

		if currentNode.cell == stopCell {
			passed += 1
			var newAmount int
			var newPath Cells
			var newDistance int

			for currentNode != nil {
				if currentNode.cell.ResourceType != Null {
					newAmount += 1
				}

				newDistance += 1
				newPath = append(newPath, currentNode.cell)
				currentNode = currentNode.parent
			}

			if newAmount > foundAmount && (foundDistance == 0 || newDistance <= foundDistance) {
				foundAmount = newAmount
				foundDistance = newDistance
				foundPath = newPath
			}

			continue
		} else if foundAmount > -1 {
			continue
		} else if maxDistance > 0 && currentNode.distance >= maxDistance {
			continue
		}

		for _, neighbor := range currentNode.cell.Neighbours(mainStruct) {
			var node = &Node{
				cell:     neighbor,
				parent:   currentNode,
				distance: currentNode.distance + 1,
			}

			if !visited[node.cell] {
				queue = append(queue, node)
			}
		}
	}

	return foundDistance, foundPath
}

func (cell *Cell) Neighbours(mainStruct *MainStruct) (cells Cells) {
	for _, neigh := range []CellIndex{cell.Neigh0, cell.Neigh1, cell.Neigh2, cell.Neigh3, cell.Neigh4, cell.Neigh5} {
		if neigh == EmptyNeighbour {
			continue
		}

		cells = append(cells, mainStruct.Cells[neigh])
	}

	return cells
}

func BuildBoard(cells Cells) (board [][]*Cell) {
	for i := 0; i < 21; i++ {
		board = append(board, make([]*Cell, 21))
	}

	var x, y = 0, 0
	board[11][11] = cells[0]

	var notVisited = make(map[CellIndex]bool)
	for _, cell := range cells {
		notVisited[cell.Index] = true
	}

	for len(notVisited) > 0 {
		var visiting Cells
		for i, _ := range notVisited {
			visiting = append(visiting, cells[i])
		}
		notVisited = make(map[CellIndex]bool)

		for i, _ := range visiting {
			var cell = cells[i]
			var column []*Cell

			var found bool
			for x, column = range board {
				var boardCell *Cell
				for y, boardCell = range column {
					if boardCell != nil && cell.Index == boardCell.Index {
						found = true
						break
					}
				}

				if found {
					break
				}
			}

			if !found {
				notVisited[cell.Index] = true
				continue
			}

			if cell.Neigh0 != EmptyNeighbour {
				board[x+1][y] = cells[cell.Neigh0]
			}

			if cell.Neigh1 != EmptyNeighbour {
				board[x][y+1] = cells[cell.Neigh1]
			}

			if cell.Neigh2 != EmptyNeighbour {
				board[x-1][y+1] = cells[cell.Neigh2]
			}

			if cell.Neigh3 != EmptyNeighbour {
				board[x-1][y] = cells[cell.Neigh3]
			}

			if cell.Neigh4 != EmptyNeighbour {
				board[x][y-1] = cells[cell.Neigh4]
			}

			if cell.Neigh5 != EmptyNeighbour {
				board[x+1][y-1] = cells[cell.Neigh5]
			}
		}
	}

	var first0, last0 = 11, 11

	for i := 0; i < len(board); i++ {
		var exists bool

		for _, row := range board {
			if row[i] != nil {
				exists = true
				break
			}
		}

		if exists {
			if i < first0 {
				first0 = i
			} else if i > last0 {
				last0 = i
			}
		}
	}

	var first1, last1 = 11, 11

	for i := range board {
		board[i] = board[i][first0 : last0+1]

		var exists bool
		for _, cell := range board[i] {
			if cell != nil {
				exists = true
				break
			}
		}

		if exists {
			if i < first1 {
				first1 = i
			} else if i > last1 {
				last1 = i
			}
		}
	}

	board = board[first1 : last1+1]

	return board
}

func (cells Cells) findCells(resource ResourceType) (results Cells) {
	for _, cell := range cells {
		if cell.ResourceType == resource && cell.Resources > 0 {
			if cell.MyAnts > 0 || (cell.OpponentAnts == 0 || cell.Resources/cell.OpponentAnts > 2) {
				results = append(results, cell)
			}
		}
	}

	return results
}

func (cells Cells) CrystalCells() (results Cells) {
	return cells.findCells(Crystals)
}

func (cells Cells) EggCells() (results Cells) {
	return cells.findCells(Eggs)
}

func (cells Cells) CountCrystals() (result int) {
	for _, cell := range cells {
		if cell.ResourceType == Crystals {
			result += cell.InitialResource
		}
	}

	return result
}

func (cells Cells) CountMyAnts() (result int) {
	for _, cell := range cells {
		result += cell.MyAnts
	}

	return result
}

func (cells Cells) ShowClosest(startCell *Cell, mainStruct *MainStruct, maxDistance int) (cellDistances CellDistances) {
	for _, cell := range cells {
		var distance, path = startCell.DistanceTo(cell, mainStruct, maxDistance)

		if distance < 1 {
			continue
		}

		cellDistances = append(cellDistances, CellDistance{
			Cell:     cell,
			Distance: distance,
			Path:     path,
		})
	}

	sort.Sort(cellDistances)

	return cellDistances
}

// ---------------------------------------------------------------------------------------------------------------------
// -- Main -------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------

type MainStruct struct {
	GameLoop            *GameLoop
	Cells               Cells
	MyBases             Cells
	OpponentBases       Cells
	Turn                int
	MyScore             int
	OpponentScore       int
	MaxScore            int
	StateClosestEggDone bool
	MaxVisited          int
}

func (mainStruct *MainStruct) UpdateCells() {
	mainStruct.GameLoop.updateCells(mainStruct)
}

func (mainStruct *MainStruct) AllBases() (cells Cells) {
	return append(mainStruct.MyBases, mainStruct.OpponentBases...)
}

func (mainStruct *MainStruct) InterestingCells(orderByEggs bool) (cells Cells) {
	var ordering = append(mainStruct.Cells.EggCells(), mainStruct.Cells.CrystalCells()...)

	if !orderByEggs {
		ordering = append(mainStruct.Cells.CrystalCells(), mainStruct.Cells.EggCells()...)
	}

	for _, cell := range ordering {
		if cell.Resources > 0 {
			cells = append(cells, cell)
		}
	}

	return cells
}

func (mainStruct *MainStruct) PerformClosestEggs(eggs Cells, visited CellMap) (exit bool) {
	log.Println("PerformClosestEggs")
	if mainStruct.StateClosestEggDone || len(eggs) < 1 {
		return false
	}

	var missingEgg bool
	var partialEgg bool

	for _, base := range mainStruct.MyBases {
		var closestEggs = eggs.ShowClosest(base, mainStruct, 5)
		if len(closestEggs) < 1 {
			continue
		}

		var egg = closestEggs[0]

		if egg.Cell.Resources > 0 && egg.Distance <= 5 {
			visited[egg.Cell] = true
			mainStruct.joinPath(egg.Cell, egg.Path, visited, eggs, 0, 1, 2)
		} else {
			missingEgg = true
		}

		if egg.Cell.Resources*2 < egg.Cell.MyAnts {
			partialEgg = true
		}
	}

	if missingEgg {
		mainStruct.StateClosestEggDone = true
		return false
	} else if partialEgg || mainStruct.Turn > 5 {
		return false
	}

	return true
}

func (mainStruct *MainStruct) PerformMiddleEggs(eggs Cells, crystals Cells, visited CellMap) (exit bool) {
	log.Println("PerformMiddleEggs")

	if mainStruct.MaxScore < 200 || len(eggs) < 1 || mainStruct.Cells.CountMyAnts() >= 150 {
		return false
	}

	for _, base := range mainStruct.MyBases {
		for _, egg := range eggs.ShowClosest(base, mainStruct, 10) {
			if visited[egg.Cell] {
				continue
			}

			var result = egg.IsMiddleCell(mainStruct, 10)
			if result {
				mainStruct.joinPath(egg.Cell, egg.Path, visited, append(eggs, crystals...), 0, 3, 2)
				exit = true
				break
			}
		}
	}

	return exit
}

func (mainStruct *MainStruct) PerformRemainingEggs(eggs Cells, crystals Cells, visited CellMap) (exit bool) {
	log.Println("PerformRemainingEggs")

	if mainStruct.MaxScore < 200 {
		return false
	}

	for _, base := range mainStruct.MyBases {
		for _, egg := range eggs.ShowClosest(base, mainStruct, 10) {
			if visited[egg.Cell] {
				continue
			}

			if egg.IsCloseCell(mainStruct, 10) {
				mainStruct.joinPath(egg.Cell, egg.Path, visited, append(eggs, crystals...), 0, 3, 3)
				exit = true
			}
		}
	}

	return exit
}

func (mainStruct *MainStruct) PerformMiddleCrystals(crystals Cells, visited CellMap) (exit bool) {
	log.Println("PerformMiddleCrystals")

	for _, base := range mainStruct.MyBases {
		for _, crystal := range crystals.ShowClosest(base, mainStruct, 10) {
			if visited[crystal.Cell] {
				continue
			}

			if crystal.IsMiddleCell(mainStruct, 10) {
				mainStruct.joinPath(crystal.Cell, crystal.Path, visited, crystals, 0, 3, 3)
				exit = true
				break
			}
		}
	}

	return exit
}

func (mainStruct *MainStruct) PerformRemainingCrystals(crystals Cells, visited CellMap) (exit bool) {
	for _, base := range mainStruct.MyBases {
		for _, crystal := range crystals.ShowClosest(base, mainStruct, 10) {
			if visited[crystal.Cell] {
				continue
			}

			if crystal.IsCloseCell(mainStruct, 0) {
				mainStruct.joinPath(crystal.Cell, crystal.Path, visited, crystals, 0, 3, 3)
				exit = true
			}

			if len(visited) > mainStruct.MaxVisited {
				return true
			}
		}
	}

	return exit
}

func (mainStruct *MainStruct) Perform() {
	var crystals = mainStruct.Cells.CrystalCells()
	var eggs = mainStruct.Cells.EggCells()
	var visited = make(CellMap)

	if mainStruct.PerformClosestEggs(eggs, visited) {
		mainStruct.GameLoop.Message("Closest Eggs")
		return
	} else if mainStruct.PerformMiddleEggs(eggs, crystals, visited) && len(visited) >= mainStruct.MaxVisited {
		mainStruct.GameLoop.Message("Middle Eggs")
		return
	} else if mainStruct.PerformRemainingEggs(eggs, crystals, visited) && len(visited) >= mainStruct.MaxVisited {
		mainStruct.GameLoop.Message("Remaining Eggs")
		return
	} else if mainStruct.PerformMiddleCrystals(crystals, visited) && len(visited) >= mainStruct.MaxVisited {
		mainStruct.GameLoop.Message("Middle Crystals")
		return
	} else if mainStruct.PerformRemainingCrystals(crystals, visited) {
		mainStruct.GameLoop.Message("Remaining Crystals")
		return
	} else {
		mainStruct.GameLoop.Message("Give Up")
		return
	}
}

func (mainStruct *MainStruct) joinPath(visitingCell *Cell, path Cells, visited map[*Cell]bool, interestingCells Cells, depth int, maxDepth int, maxDistance int) {
	if depth > maxDepth {
		return
	}

	visited[visitingCell] = true
	var potentialCells = make(map[*Cell]Cells)

	for x, step := range path {
		var strength = 10
		for _, neigh := range step.Neighbours(mainStruct) {
			if step.MyAnts < 5 && neigh.MyAnts > step.MyAnts && float64(neigh.MyAnts)/float64(step.MyAnts) > 3 {
				strength = 20
				break
			}
		}
		mainStruct.GameLoop.Beacon(step.Index, strength)

		if x != 0 && x != len(path)-1 && x%2 == 0 {
			continue
		}

		for _, cell := range interestingCells {
			if visited[cell] {
				continue
			}

			if cell == step {
				visited[cell] = true
				continue
			}

			var distance, newPath = cell.DistanceTo(step, mainStruct, maxDistance)

			if distance > 0 && distance <= maxDistance && (len(potentialCells[cell]) == 0 || len(potentialCells[cell]) > distance) {
				potentialCells[cell] = newPath
			}
		}
	}

	if len(visited) >= mainStruct.MaxVisited {
		return
	}

	for cell, path := range potentialCells {
		if visited[cell] {
			continue
		}

		mainStruct.joinPath(cell, path, visited, interestingCells, depth+1, maxDepth, maxDistance)
	}
}

// ---------------------------------------------------------------------------------------------------------------------
// -- GameLoop ---------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------

type GameLoop struct {
	Scanner *bufio.Scanner
	output  []string
}

// -- Output -----------------------------------------------------------------------------------------------------------

func (gameLoop *GameLoop) Debug(text interface{}) {
	log.Println(fmt.Sprint(text))
}

func (gameLoop *GameLoop) appendOutput(text string) {
	gameLoop.output = append(gameLoop.output, text)
}

func (gameLoop *GameLoop) Wait() {
	fmt.Println("WAIT")
	gameLoop.output = nil
}

func (gameLoop *GameLoop) Line(sourceIdx, targetIdx CellIndex, strength int) {
	gameLoop.appendOutput(fmt.Sprintf("LINE %v %v %v", sourceIdx, targetIdx, strength))
}

func (gameLoop *GameLoop) Beacon(cellID CellIndex, strength int) {
	gameLoop.appendOutput(fmt.Sprintf("BEACON %v %v", cellID, strength))
}

func (gameLoop *GameLoop) Message(text string) {
	gameLoop.appendOutput(fmt.Sprintf("MESSAGE %v", text))
}

func (gameLoop *GameLoop) Commit() {
	if len(gameLoop.output) < 1 {
		gameLoop.Wait()
	} else {
		fmt.Println(strings.Join(gameLoop.output, ";"))
		gameLoop.output = nil
	}
}

// -- Input ------------------------------------------------------------------------------------------------------------

func (gameLoop *GameLoop) scan(items ...interface{}) {
	fmt.Sscan(gameLoop.scanText(), items...)
}

func (gameLoop *GameLoop) scanText() (results string) {
	gameLoop.Scanner.Scan()
	return gameLoop.Scanner.Text()
}

func (gameLoop *GameLoop) getScores() (myScore, opponentScore int) {
	gameLoop.scan(&myScore, &opponentScore)

	return myScore, opponentScore
}

func (gameLoop *GameLoop) getCells() (results Cells) {
	var cellsCount int
	gameLoop.scan(&cellsCount)

	for i := 0; i < cellsCount; i++ {
		var resourceType ResourceType
		var initialResources int
		var neigh0, neigh1, neigh2, neigh3, neigh4, neigh5 NeighID
		gameLoop.scan(&resourceType, &initialResources, &neigh0, &neigh1, &neigh2, &neigh3, &neigh4, &neigh5)

		results = append(results, &Cell{
			Index:           CellIndex(i),
			ResourceType:    resourceType,
			InitialResource: initialResources,
			MyAnts:          0,
			OpponentAnts:    0,
			Neigh0:          CellIndex(neigh0),
			Neigh1:          CellIndex(neigh1),
			Neigh2:          CellIndex(neigh2),
			Neigh3:          CellIndex(neigh3),
			Neigh4:          CellIndex(neigh4),
			Neigh5:          CellIndex(neigh5),
		})
	}

	return results
}

func (gameLoop *GameLoop) getBaseIndexes(cells Cells) (myBases, opponentBases Cells) {
	var basesCount int
	gameLoop.scan(&basesCount)

	var inputs []string
	var cell *Cell

	inputs = strings.Split(gameLoop.scanText(), " ")
	for i := 0; i < basesCount; i++ {
		result, _ := strconv.ParseInt(inputs[i], 10, 32)
		cell = cells[result]
		cell.MyBase = true
		myBases = append(myBases, cell)
	}

	inputs = strings.Split(gameLoop.scanText(), " ")
	for i := 0; i < basesCount; i++ {
		result, _ := strconv.ParseInt(inputs[i], 10, 32)
		cell = cells[result]
		cell.OpponentBase = true
		opponentBases = append(opponentBases, cell)
	}

	return myBases, opponentBases
}

func (gameLoop *GameLoop) updateCell(cell *Cell) {
	var resources, myAnts, oppAnts int
	gameLoop.scan(&resources, &myAnts, &oppAnts)

	cell.Resources = resources
	cell.MyAnts = myAnts
	cell.OpponentAnts = oppAnts
}

func (gameLoop *GameLoop) updateCells(mainStruct *MainStruct) {
	mainStruct.MyScore, mainStruct.OpponentScore = gameLoop.getScores()

	for i := range mainStruct.Cells {
		gameLoop.updateCell(mainStruct.Cells[i])
	}
}

func (gameLoop *GameLoop) GetInput() (mainStruct MainStruct) {
	mainStruct.GameLoop = gameLoop
	mainStruct.Cells = gameLoop.getCells()
	mainStruct.MyBases, mainStruct.OpponentBases = gameLoop.getBaseIndexes(mainStruct.Cells)
	mainStruct.MaxScore = mainStruct.Cells.CountCrystals()
	mainStruct.MaxVisited = 3

	if mainStruct.MaxScore > 200 {
		mainStruct.MaxVisited = 5
	}

	return mainStruct
}

// -- Main -------------------------------------------------------------------------------------------------------------

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)

	var gameLoop = GameLoop{Scanner: scanner}
	var mainStruct = gameLoop.GetInput()

	for {
		mainStruct.UpdateCells()
		mainStruct.Turn++

		mainStruct.Perform()

		mainStruct.GameLoop.Commit()
	}
}
