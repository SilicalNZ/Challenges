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

	ShieldLife int
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

type GameLoop struct {
	Player0Base Base
	Player1Base Base
}

type ErrorCode = string

const (
	ErrorCodeFmtScan ErrorCode = `unexpected error extracting scan: %s`
)

const ThreatValue = 7000

var rotateTextCounter = 0

// -- FUNCTIONS ----------

// -- Utilities ----------
func rotateText() string {
	var ct = rotateTextCounter % 20

	var text = "SILI"
	for i := 0; i < ct; i++ {
		text = "_" + text
	}

	for i := 0; i < 20-ct; i++ {
		text = text + "_"
	}

	return text
}

func distanceFormula(x0, x1, y0, y1 int) float64 {
	return math.Sqrt(math.Pow(float64(x1-x0), 2) + math.Pow(float64(y1-y0), 2))
}

// -- Behaviour ----------
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

				ShieldLife: shieldLife,
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

// -- METHODS ----------

// -- Base ----------
func (base Base) distanceFrom(x0, y0 int) (int, int) {
	return int(math.Abs(float64(base.PosX - x0))), int(math.Abs(float64(base.PosY - y0)))
}

// -- GameLoop ----------
func (gameLoop GameLoop) Wait() {
	fmt.Printf("WAIT %s\n", rotateText)
}

func (gameLoop GameLoop) Move(x0, x1 int) {
	fmt.Printf("MOVE %s %s %s\n", strconv.Itoa(x0), strconv.Itoa(x1), rotateText())
}

func (gameLoop GameLoop) SpellControl(monsterID, x0, x1 int) {
	fmt.Printf("SPELL CONTROL %s %s %s %s\n", strconv.Itoa(monsterID), strconv.Itoa(x0), strconv.Itoa(x1), rotateText())
}

func (gameLoop GameLoop) SpellWind(x0, x1 int) {
	fmt.Printf("SPELL WIND %s %s %s\n", strconv.Itoa(x0), strconv.Itoa(x1), rotateText())
}

func (gameLoop GameLoop) SpellShield(monsterID int) {
	fmt.Printf("SPELL SHIELD  %s %s\n", strconv.Itoa(monsterID), rotateText())
}

// -- Monster ----------
func (monster Monster) Distance(x0, y0 int) float64 {
	return distanceFormula(monster.PosX, x0, monster.PosY, y0)
}

func (monsters Monsters) OrderByCoordinate(x0, y0 int) Monsters {
	sort.Slice(monsters, func(i, j int) bool {
		return monsters[i].Distance(x0, y0) < monsters[j].Distance(x0, y0)
	})

	return monsters
}

// -- Hero ----------
func (hero Hero) AttackMostThreateningMonster(monsters Monsters, base Base) *Monster {
	if len(monsters) == 0 {
		return nil
	}

	monsters.OrderByCoordinate(base.PosX, base.PosY)

	var selectedMonster = monsters[0]

	if selectedMonster.Distance(base.PosX, base.PosY) >= ThreatValue {
		return nil
	} else {
		return selectedMonster
	}
}

func (hero Hero) RedirectMonster(monsters Monsters, base Base) *Monster {
	if len(monsters) == 0 {
		return nil
	}

	monsters.OrderByCoordinate(hero.PosX, hero.PosY)

	var selectedMonster *Monster
	for _, monster := range monsters {
		if monster.Threat == Player1ThreatType {
			continue
		} else if monster.Health < 10 {
			continue
		} else if monster.Distance(hero.PosX, hero.PosY) > 2200 {
			continue
		} else if monster.Distance(base.PosX, base.PosY) < 7000 {
			continue
		} else {
			selectedMonster = monster
			break
		}
	}

	return selectedMonster
}

func (hero Hero) WindAttackMonsterDefensive(monster Monster, base Base) bool {
	if monster.Distance(base.PosX, base.PosY) > 3000 {
		return false
	} else if monster.ShieldLife != 0 {
		return false
	} else if monster.Distance(hero.PosX, hero.PosY) > 1500 {
		return false
	} else {
		return true
	}
}

func (hero Hero) WanderAttackMonster(monsters Monsters, base Base, opponentBase Base) *Monster {
	monsters.OrderByCoordinate(hero.PosX, hero.PosY)

	var selectedMonster *Monster
	for _, monster := range monsters {
		if monster.Threat == Player1ThreatType {
			continue
		} else if monster.Distance(opponentBase.PosX, opponentBase.PosY) < 6000 {
			continue
		} else if monster.Distance(base.PosX, base.PosY) < 7000 {
			continue
		} else {
			selectedMonster = monster
			break
		}
	}

	return selectedMonster
}

func (hero Hero) ShieldMonster(monsters Monsters, opponentBase Base) *Monster {
	monsters.OrderByCoordinate(hero.PosX, hero.PosY)

	var selectedMonster *Monster
	for _, monster := range monsters {
		if monster.Threat != Player1ThreatType {
			continue
		} else if monster.Health < 10 {
			continue
		} else if monster.Distance(hero.PosX, hero.PosY) >= 1700 {
			break
		} else if monster.Distance(opponentBase.PosX, opponentBase.PosY) > 4000 {
			continue
		} else {
			selectedMonster = monster
			break
		}
	}

	return selectedMonster
}

func (hero Hero) WindAttackMonsterOffensive(monsters Monsters, opponentBase Base) *Monster {
	monsters.OrderByCoordinate(hero.PosX, hero.PosY)

	var selectedMonster *Monster
	for _, monster := range monsters {
		if monster.Threat != Player1ThreatType {
			continue
		} else if monster.Health < 10 {
			continue
		} else if monster.Distance(hero.PosX, hero.PosY) >= 2200 {
			break
		} else if monster.Distance(opponentBase.PosX, opponentBase.PosY) < 3800 || monster.Distance(opponentBase.PosX, opponentBase.PosY) > monster.Distance(hero.PosX, hero.PosY) {
			continue
		} else if monster.ShieldLife != 0 {
			continue
		} else {
			selectedMonster = monster
			break
		}
	}

	return selectedMonster
}

func (hero Hero) Distance(x0, y0 int) float64 {
	return distanceFormula(hero.PosX, x0, hero.PosY, y0)
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

func main() {
	var retrieveImmutableInformation = retrieveImmutableInformationFromFmtScan
	var retrieveMutableInformation = retrieveMutableInformationFromFmtScan

	var base, _, _ = retrieveImmutableInformation()

	var opponentBase Base
	{
		if base.PosX == 0 {
			opponentBase = Base{
				PosX: 17630,
				PosY: 9000,
			}
		} else {
			opponentBase = Base{
				PosX: 0,
				PosY: 0,
			}
		}
	}

	var gameLoop = GameLoop{
		Player0Base: base,
		Player1Base: opponentBase,
	}

	var ct = 0
	var patrolSwitch = 0
	var patrolOptions = [2][2]int{{5000, 8000}, {11000, 1000}}

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

		var hero0 = player0.Heroes[0]
		var hero1 = player0.Heroes[1]
		var hero2 = player0.Heroes[2]

		// Hero0 Action
		if ct <= 3 {
			gameLoop.Move(gameLoop.Player1Base.distanceFrom(5000, 2000))
		} else if result := hero0.WanderAttackMonster(monsters, gameLoop.Player0Base, gameLoop.Player1Base); result != nil {
			var monster = *result

			gameLoop.Move(monster.PosX, monster.PosY)
		} else {
			gameLoop.Move(gameLoop.Player1Base.distanceFrom(2500, 5000))
		}

		// Hero1 Action
		if result := hero1.AttackMostThreateningMonster(monsters, gameLoop.Player0Base); result != nil {
			var monster = *result

			if hero1.WindAttackMonsterDefensive(monster, gameLoop.Player0Base) {
				gameLoop.SpellWind(gameLoop.Player1Base.PosX, gameLoop.Player1Base.PosY)
			} else {
				gameLoop.Move(monster.PosX, monster.PosY)
			}
		} else {
			if hero0.Distance(patrolOptions[patrolSwitch][0], patrolOptions[patrolSwitch][1]) < 1000 {
				patrolSwitch = int(math.Abs(float64(patrolSwitch - 1)))
			}

			gameLoop.Move(patrolOptions[patrolSwitch][0], patrolOptions[patrolSwitch][1])
		}

		// Hero2 Action
		if result := hero2.AttackMostThreateningMonster(monsters, gameLoop.Player0Base); result != nil {
			var monster = *result

			if hero2.Distance(hero1.PosX, hero2.PosX) > 200 && hero1.WindAttackMonsterDefensive(monster, gameLoop.Player0Base) {
				gameLoop.SpellWind(gameLoop.Player1Base.PosX, gameLoop.Player1Base.PosY)
			} else {
				gameLoop.Move(monster.PosX, monster.PosY)
			}
		} else {
			gameLoop.Move(gameLoop.Player0Base.distanceFrom(2000, 4500))
		}

		ct += 1
		rotateTextCounter += 1
	}
}
