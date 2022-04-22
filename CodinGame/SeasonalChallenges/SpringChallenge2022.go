package main

import (
	"fmt"
	"log"
	"math"
	"sort"
	"strconv"
)

type UnitType int

const (
	MonsterUnitType UnitType = 0
	Player0UnitType          = 1
	Player1UnitType          = 2
)

type Unit struct {
	ID       int
	UnitType UnitType
	PosX     int
	PosY     int
}

type ThreatType int

const (
	NoThreatType      ThreatType = 0
	Player0ThreatType            = 1
	Player1ThreatType            = 2
)

type Monster struct {
	Unit

	Health      int
	TrajectoryX int
	TrajectoryY int
	Threat      ThreatType
}

type Monsters []*Monster

type Hero struct {
	Unit
}

type Heroes []*Hero

type Player struct {
	Heroes Heroes
	Health int
	Mana   int
}

type Base struct {
	PosX int
	PosY int
}

type ErrorCode = string

const (
	ErrorCodeFmtScan ErrorCode = `unexpected error extracting scan: %s`
)

func retrieveMutableInformationFromFmtScan() (*Player, *Player, Monsters, error) {

	var playerInfo [][2]int
	{
		for i := 0; i < 2; i++ {
			// health: Each player's base health
			// mana: Ignore in the first league; Spend ten mana to cast a spell
			var health, mana int
			if _, err := fmt.Scan(&health, &mana); err != nil {
				return nil, nil, nil, fmt.Errorf(ErrorCodeFmtScan, err)
			}

			playerInfo = append(playerInfo, [2]int{health, mana})
		}
	}

	// entityCount: Amount of heroes and monsters you can see
	var entityCount int
	{
		if _, err := fmt.Scan(&entityCount); err != nil {
			return nil, nil, nil, fmt.Errorf(ErrorCodeFmtScan, err)
		}
	}

	var player0Heroes Heroes
	var player1Heroes Heroes
	var monsters Monsters
	{
		for i := 0; i < entityCount; i++ {
			// id: Unique identifier
			// type: 0=monster, 1=your hero, 2=opponent hero
			// x: Position of this entity
			// shieldLife: Ignore for this league; Count down until shield spell fades
			// isControlled: Ignore for this league; Equals 1 when this entity is under a control spell
			// health: Remaining health of this monster
			// vx: Trajectory of this monster
			// nearBase: 0=monster with no target yet, 1=monster targeting a base
			// threatFor: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
			var id, unitTypeInt, x, y, shieldLife, isControlled, health, vx, vy, nearBase, threatFor int
			if _, err := fmt.Scan(&id, &unitTypeInt, &x, &y, &shieldLife, &isControlled, &health, &vx, &vy, &nearBase, &threatFor); err != nil {
				return nil, nil, nil, fmt.Errorf(ErrorCodeFmtScan, err)
			}

			var unitType = UnitType(unitTypeInt)
			var threatType = ThreatType(threatFor)

			var unit = Unit{
				ID:       id,
				UnitType: unitType,
				PosX:     x,
				PosY:     y,
			}

			switch unitType {
			case MonsterUnitType:
				monsters = append(monsters, &Monster{
					Unit:        unit,
					Health:      health,
					TrajectoryX: vx,
					TrajectoryY: vy,
					Threat:      threatType,
				})
			case Player0UnitType:
				player0Heroes = append(player0Heroes, &Hero{
					Unit: unit,
				})
			case Player1UnitType:
				player1Heroes = append(player1Heroes, &Hero{
					Unit: unit,
				})
			}
		}
	}

	var player0 = &Player{
		Heroes: player0Heroes,
		Health: playerInfo[0][0],
		Mana:   playerInfo[0][1],
	}
	var player1 = &Player{
		Heroes: player1Heroes,
		Health: playerInfo[1][0],
		Mana:   playerInfo[1][1],
	}

	return player0, player1, monsters, nil
}

func (monsters Monsters) FindClosest(heroes Heroes, base Base) (map[*Hero]*Monster, error) {
	var distanceFormula = func(x0, x1, y0, y1 int) float64 {
		return math.Sqrt(math.Pow(float64(x1-x0), 2) + math.Pow(float64(y1-y0), 2))
	}

	var heroesCopy = Heroes{heroes[0], heroes[1], heroes[2]}

	sort.Slice(monsters, func(i, j int) bool {
		return distanceFormula(
			monsters[i].PosX,
			base.PosX,
			monsters[i].PosY,
			base.PosY,
		) < distanceFormula(
			monsters[j].PosX,
			base.PosX,
			monsters[j].PosY,
			base.PosY,
		)
	})

	log.Println(*heroes[0])
	log.Println(*heroes[1])
	log.Println(*heroes[2])

	var result = map[*Hero]*Monster{}
	{
		for x, monster := range monsters {
			if x >= 3 {
				break
			}

			log.Println(*monster)

			var smallestDistance float64
			var smallestHero *Hero
			for _, hero := range heroesCopy {

				var distance = distanceFormula(
					monster.PosX,
					hero.PosX,
					monster.PosY,
					hero.PosY,
				)

				if smallestHero == nil || smallestDistance > distance {
					smallestHero = hero
					smallestDistance = distance
				}
			}

			for i, hero := range heroesCopy {
				if hero == smallestHero {
					heroesCopy = append(heroesCopy[:i], heroesCopy[i+1:]...)
					break
				}

			}

			log.Println(*smallestHero)

			result[smallestHero] = monster
		}
	}

	log.Println(len(result))
	return result, nil
}

func retrieveImmutableInformationFromFmtScan() (Base, int, error) {
	// baseX: The corner of the map representing your base
	var base Base
	{
		var baseX, baseY int
		if _, err := fmt.Scan(&baseX, &baseY); err != nil {
			log.Panicf(ErrorCodeFmtScan, err)
		}

		base = Base{
			PosX: baseX,
			PosY: baseY,
		}
	}

	// heroesPerPlayer: Always 3
	var heroesPerPlayer int
	{
		if _, err := fmt.Scan(&heroesPerPlayer); err != nil {
			log.Panicf(ErrorCodeFmtScan, err)
		}
	}

	return base, heroesPerPlayer, nil
}

func retrieveMutableInformationTest() (*Player, *Player, Monsters, error) {
	var monsters = []*Monster{
		{
			Unit: Unit{
				ID:       0,
				UnitType: 0,
				PosX:     0,
				PosY:     0,
			},

			Health:      0,
			TrajectoryX: 0,
			TrajectoryY: 0,
			Threat:      1,
		},
		{
			Unit: Unit{
				ID:       0,
				UnitType: 0,
				PosX:     0,
				PosY:     0,
			},

			Health:      0,
			TrajectoryX: 0,
			TrajectoryY: 0,
			Threat:      1,
		},
		{
			Unit: Unit{
				ID:       0,
				UnitType: 0,
				PosX:     0,
				PosY:     0,
			},

			Health:      0,
			TrajectoryX: 0,
			TrajectoryY: 0,
			Threat:      1,
		},
		{
			Unit: Unit{
				ID:       0,
				UnitType: 0,
				PosX:     0,
				PosY:     0,
			},

			Health:      0,
			TrajectoryX: 0,
			TrajectoryY: 0,
			Threat:      1,
		},
		{
			Unit: Unit{
				ID:       0,
				UnitType: 0,
				PosX:     0,
				PosY:     0,
			},

			Health:      0,
			TrajectoryX: 0,
			TrajectoryY: 0,
			Threat:      1,
		},
	}

	return nil, nil, monsters, nil
}

func main() {
	var retrieveImmutableInformation = retrieveImmutableInformationFromFmtScan
	var retrieveMutableInformation = retrieveMutableInformationFromFmtScan

	var base, _, _ = retrieveImmutableInformation()

	for {
		var player0, _ *Player
		var monsters Monsters
		{
			if result0, _, result2, err := retrieveMutableInformation(); err != nil {
				log.Panicf(`ExtractFmtScan: %s`, err)
			} else {
				player0 = result0
				// player1 = result1
				monsters = result2
			}
		}

		var directions map[*Hero]*Monster
		{
			if result, err := monsters.FindClosest(player0.Heroes, base); err != nil {
				log.Panicf(`monsters.FindClosest: %s`, err)
			} else {
				directions = result
			}
		}

		for _, hero := range player0.Heroes {
			if result, ok := directions[hero]; !ok {
				fmt.Println("WAIT")
			} else {
				var directionHero = *result
				fmt.Printf("MOVE %s %s\n", strconv.Itoa(directionHero.PosX), strconv.Itoa(directionHero.PosY))
			}
		}
	}
}
