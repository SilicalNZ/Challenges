package main

import (
	"bufio"
	"context"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
)

func main() {
	game := NewGame()

	for {
		game.InputGameTurn()
		commands := ""

		for _, snakeBot := range game.Me.SnakeBots {
			goal := snakeBot.Closest(game.Grid.PowerSources)
			game.Debug(false, snakeBot.ID, goal)

			directionName, path := game.SnakePath(&SnakePathReq{
				Goal:        goal,
				SnakeCoords: snakeBot.Body,
			})

			game.Debug(false, directionName, path)

			if directionName != "" {
				commands += fmt.Sprintf("%v %s;", snakeBot.ID, directionName)
			}
		}

		if commands != "" {
			fmt.Println(commands)
		} else {
			fmt.Println("WAIT")
		}
	}
}

type Game struct {
	MyID    PlayerID
	Me      *Player
	Them    *Player
	Grid    *Grid
	scanner *bufio.Scanner
}

type Direction string

const (
	DirectionUp    Direction = "UP"
	DirectionDown  Direction = "DOWN"
	DirectionRight Direction = "RIGHT"
	DirectionLeft  Direction = "LEFT"
)

func NewGame() *Game {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)

	g := &Game{
		scanner: scanner,
		Me:      &Player{},
		Them:    &Player{},
	}

	g.MyID = PlayerID(g.scanInt("myId"))
	g.Grid = NewGrid(g.scanLine, g.scanInt("width"), g.scanInt("height"))

	snakebotsPerPlayer := g.scanInt("snakebotsPerPlayer")

	for i := 0; i < snakebotsPerPlayer; i++ {
		g.Me.SnakeBotIDs = append(g.Me.SnakeBotIDs, SnakeBotID(g.scanInt("snakebotsPerPlayer Me")))
	}

	for i := 0; i < snakebotsPerPlayer; i++ {
		g.Them.SnakeBotIDs = append(g.Them.SnakeBotIDs, SnakeBotID(g.scanInt("snakebotsPerPlayer Them")))
	}

	return g
}

func (g *Game) InputGameTurn() {
	g.Grid.PowerSources = nil
	powerSourcesCount := g.scanInt("powerSourceCount")
	for i := 0; i < powerSourcesCount; i++ {
		xy := strings.Split(g.scanLine("powerSourceCount X Y"), " ")
		x, _ := strconv.Atoi(xy[0])
		y, _ := strconv.Atoi(xy[1])

		g.Grid.PowerSources = append(g.Grid.PowerSources, Coordinate{
			X: x,
			Y: y,
		})
	}

	g.Them.SnakeBots = nil
	g.Me.SnakeBots = nil
	snakeBotsCount := g.scanInt("snakebotCount")
	for i := 0; i < snakeBotsCount; i++ {
		text := strings.Split(g.scanLine("snakebotId body"), " ")
		id, _ := strconv.Atoi(text[0])

		s := &SnakeBot{
			ID: SnakeBotID(id),
		}

		for _, xys := range strings.Split(text[1], ":") {
			xy := strings.Split(xys, ",")
			x, _ := strconv.Atoi(xy[0])
			y, _ := strconv.Atoi(xy[1])

			s.Body = append(s.Body, Coordinate{
				X: x,
				Y: y,
			})
		}

		if g.Me.ContainsSnakeBotID(s.ID) {
			g.Me.SnakeBots = append(g.Me.SnakeBots, s)
		} else {
			g.Them.SnakeBots = append(g.Them.SnakeBots, s)
		}
	}
}

func (g *Game) scanLine(debug string) string {
	g.scanner.Scan()
	text := g.scanner.Text()

	g.Debug(true, debug+" : "+text)

	return text
}

func (g *Game) scanInt(debug string) int {
	var v int
	_, _ = fmt.Sscan(g.scanLine(debug), &v)
	return v
}

func (g *Game) Debug(disable bool, a ...any) {
	if !disable {
		_, _ = fmt.Fprintln(os.Stderr, a...)
	}
}

type GridCell string

const (
	GridCellPlatform GridCell = "#"
	GridCellFree     GridCell = "."
)

type Grid struct {
	Cells         [][]GridCell
	PowerSources  []Coordinate
	Width, Height int
}

// TODO: Gravity
// TODO: Kill other snakes and don't get killed

func NewGrid(scanLine func(debug string) string, width int, height int) *Grid {
	grid := &Grid{
		Width:  width,
		Height: height,
	}

	for i := 0; i < height; i++ {
		var line []GridCell

		text := scanLine("width characters")

		_, _ = fmt.Fprintln(os.Stderr, text)

		for _, j := range text {
			line = append(line, GridCell(j))
		}

		grid.Cells = append(grid.Cells, line)
	}

	return grid
}

type SnakePathReq struct {
	Goal          Coordinate
	SnakeCoords   []Coordinate // Head is at [0]
	Path          []Coordinate
	Depth         int
	Visited       map[Coordinate]bool
	ReadVisited   func(coordinate Coordinate) bool
	AppendVisited func(coordinate Coordinate)
}

func (g *Game) SnakePath(req *SnakePathReq) (Direction, []Coordinate) {
	req.Visited = make(map[Coordinate]bool)

	mx := sync.Mutex{}
	req.AppendVisited = func(coordinate Coordinate) {
		mx.Lock()
		req.Visited[coordinate] = true
		mx.Unlock()
	}

	req.ReadVisited = func(coordinate Coordinate) bool {
		mx.Lock()
		v := req.Visited[coordinate]
		mx.Unlock()
		return v
	}

	ctx, cancel := context.WithCancel(context.Background())

	ch := g.snakePathGen(ctx, req)

	defer cancel()

	res := <-ch

	return res.Direction, res.Path
}

type SnakePathGenResp struct {
	Finished  bool
	Direction Direction
	Path      []Coordinate
}

const DepthLimit = 20

// TOOD: Gravity is only -1, not actually reaching the flooor

func (g *Game) snakePathGen(ctx context.Context, req *SnakePathReq) <-chan SnakePathGenResp {
	ch := make(chan SnakePathGenResp)
	head := req.SnakeCoords[0]
	directions := map[Direction]Coordinate{
		DirectionRight: {X: 1, Y: 0},
		DirectionLeft:  {X: -1, Y: 0},
		DirectionDown:  {X: 0, Y: 1},
		DirectionUp:    {X: 0, Y: -1},
	}

	go func() {
		defer func() {
			close(ch)
		}()

		select {
		case <-ctx.Done():
			return
		default:
		}

		nextChannels := make(map[Direction]<-chan SnakePathGenResp)

		for directionName, direction := range directions {
			next := head.Combine(direction)

			if req.ReadVisited(next) {
				continue
			}

			req.AppendVisited(next)

			if next.X == req.Goal.X && next.Y == req.Goal.Y {
				ch <- SnakePathGenResp{
					Finished:  true,
					Direction: directionName,
					Path:      append(req.Path, next),
				}

				return
			}

			if g.IsWall(next) {
				continue
			}

			if g.IsSnake(next) {
				continue
			}

			nextSnake := append([]Coordinate{next}, req.SnakeCoords[:len(req.SnakeCoords)-1]...)

			if !g.HasWallBeneath(nextSnake) {
				for _, coord := range nextSnake {
					coord.X--
					coord.Y++
				}
			}

			if req.Depth >= DepthLimit {
				continue
			}

			nextChannels[directionName] = g.snakePathGen(ctx, &SnakePathReq{
				Goal:          req.Goal,
				SnakeCoords:   nextSnake,
				Path:          append(req.Path, next),
				Depth:         req.Depth + 1,
				Visited:       req.Visited,
				AppendVisited: req.AppendVisited,
				ReadVisited:   req.ReadVisited,
			})
		}

		for len(nextChannels) > 0 {
			newNextChannels := make(map[Direction]<-chan SnakePathGenResp)

			for directionName, nextChannel := range nextChannels {
				resp := <-nextChannel

				if resp.Direction != "" {
					ch <- SnakePathGenResp{
						Finished:  true,
						Direction: directionName,
						Path:      resp.Path,
					}

					return
				}

				if !resp.Finished {
					newNextChannels[directionName] = nextChannel

					ch <- SnakePathGenResp{}
				}
			}

			nextChannels = newNextChannels
		}

		ch <- SnakePathGenResp{
			Finished: true,
		}
	}()

	return ch
}

func (g *Game) IsWall(p Coordinate) bool {
	if p.Y >= 0 && p.Y < g.Grid.Height && p.X >= 0 && p.X < g.Grid.Width {
		return g.Grid.Cells[p.Y][p.X] == GridCellPlatform
	}

	return false
}

func (g *Game) HasWallBeneath(coords []Coordinate) bool {
	for _, coord := range coords {
		if coord.Y+1 >= 0 && coord.Y+1 < g.Grid.Height && coord.X >= 0 && coord.X < g.Grid.Width {
			return g.Grid.Cells[coord.Y+1][coord.X] == GridCellPlatform
		}
	}

	return false
}

func (g *Game) IsPowerCell(p Coordinate) bool {
	for _, powerSource := range g.Grid.PowerSources {
		if p.X >= 0 && p.X == powerSource.X && p.Y >= 0 && p.Y == powerSource.Y {
			return true
		}
	}

	return true
}

func (g *Game) IsSnake(p Coordinate) bool {
	//for _, snakeBot := range  {
	//	if p.Equal(snakeBot.Head()) { // We want to eat them
	//		return true
	//	}
	//}

	for _, snakeBot := range append(g.Them.SnakeBots, g.Me.SnakeBots...) {
		if p.IsInside(snakeBot.Body) {
			return true
		}
	}

	return false
}

type PlayerID int

type Player struct {
	ID          PlayerID
	SnakeBotIDs []SnakeBotID
	SnakeBots   []*SnakeBot
}

type SnakeBotID int

func (p Player) ContainsSnakeBotID(id SnakeBotID) bool {
	for _, botID := range p.SnakeBotIDs {
		if botID == id {
			return true
		}
	}
	return false
}

type SnakeBot struct {
	ID   SnakeBotID
	Body []Coordinate
}

func (s *SnakeBot) Head() Coordinate {
	return s.Body[0]
}

func (s *SnakeBot) Closest(coords []Coordinate) Coordinate {
	head := s.Body[len(s.Body)-1]
	var distance int
	var closestCoord Coordinate

	for _, coord := range coords {
		newDistance := coord.Distance(head)

		if distance == 0 || newDistance < distance {
			distance = newDistance
			closestCoord = coord
		}
	}

	return closestCoord
}

type Coordinate struct {
	X int
	Y int
}

func (c Coordinate) Equal(o Coordinate) bool {
	return c.X == o.X && c.Y == o.Y
}

func (c Coordinate) Combine(c2 Coordinate) Coordinate {
	return Coordinate{
		X: c.X + c2.X,
		Y: c.Y + c2.Y,
	}
}

func (c Coordinate) Distance(c2 Coordinate) int {
	return (c.X-c2.X)*(c.X-c2.X) + (c.Y-c2.Y)*(c.Y-c2.Y)
}

func (c Coordinate) IsInside(coords []Coordinate) bool {
	for _, coord := range coords {
		if c.X == coord.X && c.Y == coord.Y {
			return true
		}
	}

	return false
}
