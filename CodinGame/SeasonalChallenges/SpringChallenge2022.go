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

type PatrolSwitch struct {
	Options [][2]int
	Index   int
}

var hero0AttackingPatrol = PatrolSwitch{
	Options: [][2]int{{1000, 4500}, {4500, 1000}},
	Index:   0,
}

var hero0FarmingPatrol = PatrolSwitch{
	Options: [][2]int{{7500, 6500}, {11000, 2000}},
	Index:   0,
}

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

// -- PatrolSwitch ----------
func (patrolSwitch *PatrolSwitch) Switch() {
	if patrolSwitch.Index == 0 {
		patrolSwitch.Index = len(patrolSwitch.Options) - 1
	} else {
		patrolSwitch.Index -= 1
	}
}

func (patrolSwitch PatrolSwitch) Option() (int, int) {
	var option = patrolSwitch.Options[patrolSwitch.Index]
	return option[0], option[1]
}

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

func (hero Hero) AttackMostThreateningMonsterShared(monsters Monsters, base Base, friend *Hero) *Monster {
	if len(monsters) == 0 {
		return nil
	}

	monsters.OrderByCoordinate(base.PosX, base.PosY)

	for _, monster := range monsters {
		if monster.Distance(base.PosX, base.PosY) >= ThreatValue {
			continue
		} else if monster.Distance(friend.PosX, friend.PosY) <= 2000 {
			continue
		} else {
			return monster
		}
	}

	return nil
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
		} else if monster.Health <= 16 {
			continue
		} else if monster.ShieldLife != 0 {
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
	if monster.Distance(base.PosX, base.PosY) > 3800 {
		return false
	} else if monster.ShieldLife != 0 {
		return false
	} else if monster.Distance(hero.PosX, hero.PosY) > 1100 {
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

func (hero Hero) TheyAreAnnoying(base Base, opponentHeroes Heroes) *Hero {
	for _, opponentHero := range opponentHeroes {
		if opponentHero.Distance(hero.PosX, hero.PosY) > 500 {
			continue
		} else if opponentHero.Distance(base.PosX, base.PosY) < 4500 {
			return opponentHero
		}
	}

	return nil
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
		} else if monster.Distance(hero.PosX, hero.PosY) >= 1100 {
			break
		} else if monster.ShieldLife != 0 {
			continue
		} else {
			selectedMonster = monster
			break
		}
	}

	return selectedMonster
}

func (hero Hero) ShieldDefensive(opponentHeroes Heroes) bool {
	if hero.ShieldLife != 0 {
		return false
	}

	for _, opponentHero := range opponentHeroes {
		if opponentHero.Distance(hero.PosX, hero.PosY) < 2200 {
			return true
		}
	}

	return false
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

type Director struct {
	gameLoop GameLoop
	hero0    *Hero
	hero1    *Hero
	hero2    *Hero
	monsters Monsters
	player0  *Player
	player1  *Player
}

func Hero0Attacking(request Director) {
	if result := request.hero0.ShieldDefensive(request.player1.Heroes); result == true && request.player0.Mana >= 50 {
		request.gameLoop.SpellShield(request.hero0.ID)
	} else if result := request.hero0.ShieldMonster(request.monsters, request.gameLoop.Player1Base); result != nil && request.player0.Mana >= 50 {
		var monster = *result

		request.gameLoop.SpellShield(monster.ID)
	} else if result := request.hero0.WindAttackMonsterOffensive(request.monsters, request.gameLoop.Player1Base); result != nil && request.player0.Mana >= 50 {
		request.gameLoop.SpellWind(request.gameLoop.Player1Base.PosX, request.gameLoop.Player1Base.PosY)
	} else if result := request.hero0.RedirectMonster(request.monsters, request.gameLoop.Player0Base); result != nil && request.player0.Mana >= 70 {
		var monster = *result

		request.gameLoop.SpellControl(monster.ID, request.gameLoop.Player1Base.PosX, request.gameLoop.Player1Base.PosY)
	} else {
		if request.hero0.Distance(request.gameLoop.Player1Base.distanceFrom(hero0AttackingPatrol.Option())) < 500 {
			hero0AttackingPatrol.Switch()
		}

		request.gameLoop.Move(request.gameLoop.Player1Base.distanceFrom(hero0AttackingPatrol.Option()))
	}
}

func Hero0Farming(request Director) {
	if result := request.hero0.WanderAttackMonster(request.monsters, request.gameLoop.Player0Base, request.gameLoop.Player1Base); result != nil {
		var monster = *result

		request.gameLoop.Move(monster.PosX, monster.PosY)
	} else {
		if request.hero0.Distance(request.gameLoop.Player1Base.distanceFrom(hero0FarmingPatrol.Option())) < 500 {
			hero0AttackingPatrol.Switch()
		}

		request.gameLoop.Move(request.gameLoop.Player1Base.distanceFrom(hero0FarmingPatrol.Option()))
	}
}

func Hero1Farming(request Director) {
	if result := request.hero1.ShieldDefensive(request.player1.Heroes); result == true && request.player0.Mana >= 30 {
		request.gameLoop.SpellShield(request.hero1.ID)
	} else if result := request.hero1.TheyAreAnnoying(request.gameLoop.Player0Base, request.player1.Heroes); result != nil {
		request.gameLoop.SpellWind(request.gameLoop.Player1Base.PosX, request.gameLoop.Player1Base.PosX)
	} else if result := request.hero1.AttackMostThreateningMonster(request.monsters, request.gameLoop.Player0Base); result != nil {
		var monster = *result

		if request.hero1.WindAttackMonsterDefensive(monster, request.gameLoop.Player0Base) {
			request.gameLoop.SpellWind(request.gameLoop.Player1Base.PosX, request.gameLoop.Player1Base.PosY)
		} else {
			request.gameLoop.Move(monster.PosX, monster.PosY)
		}
	} else if result := request.hero1.WanderAttackMonster(request.monsters, request.gameLoop.Player0Base, request.gameLoop.Player1Base); result != nil {
		var monster = *result

		request.gameLoop.Move(monster.PosX, monster.PosY)
	} else {
		request.gameLoop.Move(request.gameLoop.Player0Base.distanceFrom(4500, 2000))
	}
}

func Hero1DefensiveFarming(request Director) {
	if result := request.hero1.ShieldDefensive(request.player1.Heroes); result == true && request.player0.Mana >= 30 {
		request.gameLoop.SpellShield(request.hero1.ID)
	} else if result := request.hero1.TheyAreAnnoying(request.gameLoop.Player0Base, request.player1.Heroes); result != nil {
		request.gameLoop.SpellWind(request.gameLoop.Player1Base.PosX, request.gameLoop.Player1Base.PosX)
	} else if result := request.hero1.AttackMostThreateningMonster(request.monsters, request.gameLoop.Player0Base); result != nil {
		var monster = *result

		if request.hero1.WindAttackMonsterDefensive(monster, request.gameLoop.Player0Base) {
			request.gameLoop.SpellWind(request.gameLoop.Player1Base.PosX, request.gameLoop.Player1Base.PosY)
		} else {
			request.gameLoop.Move(monster.PosX, monster.PosY)
		}
	} else if result := request.hero1.WanderAttackMonster(request.monsters, request.gameLoop.Player0Base, request.gameLoop.Player1Base); result != nil {
		var monster = *result

		request.gameLoop.Move(monster.PosX, monster.PosY)
	} else if request.hero1.Distance(request.gameLoop.Player0Base.distanceFrom(3500, 500)) > 2000 {
		request.gameLoop.Move(request.gameLoop.Player0Base.distanceFrom(3500, 500))
	} else {
		request.gameLoop.Move(request.gameLoop.Player0Base.distanceFrom(3500, 500))
	}
}

func Hero2Farming(request Director) {
	if result := request.hero2.ShieldDefensive(request.player1.Heroes); result == true && request.player0.Mana >= 30 {
		request.gameLoop.SpellShield(request.hero2.ID)
	} else if result := request.hero2.AttackMostThreateningMonsterShared(request.monsters, request.gameLoop.Player0Base, request.hero1); result != nil {
		var monster = *result

		if request.hero2.Distance(request.hero1.PosX, request.hero1.PosX) > 200 && request.hero2.WindAttackMonsterDefensive(monster, request.gameLoop.Player0Base) {
			request.gameLoop.SpellWind(request.gameLoop.Player1Base.PosX, request.gameLoop.Player1Base.PosY)
		} else {
			request.gameLoop.Move(monster.PosX, monster.PosY)
		}
	} else {
		request.gameLoop.Move(request.gameLoop.Player0Base.distanceFrom(2000, 4500))
	}
}

func Hero2DefensiveFarming(request Director) {
	if result := request.hero2.ShieldDefensive(request.player1.Heroes); result == true && request.player0.Mana >= 30 {
		request.gameLoop.SpellShield(request.hero2.ID)
	} else if result := request.hero2.AttackMostThreateningMonster(request.monsters, request.gameLoop.Player0Base); result != nil {
		var monster = *result

		if request.hero2.Distance(request.hero1.PosX, request.hero1.PosX) > 200 && request.hero2.WindAttackMonsterDefensive(monster, request.gameLoop.Player0Base) {
			request.gameLoop.SpellWind(request.gameLoop.Player1Base.PosX, request.gameLoop.Player1Base.PosY)
		} else {
			request.gameLoop.Move(monster.PosX, monster.PosY)
		}
	} else if request.hero2.Distance(request.gameLoop.Player0Base.distanceFrom(500, 3500)) > 2000 {
		request.gameLoop.Move(request.gameLoop.Player0Base.distanceFrom(500, 3500))
	} else {
		request.gameLoop.Move(request.gameLoop.Player0Base.distanceFrom(500, 3500))
	}
}

func PassiveFarming(request Director) {
	// Hero0 Action
	if rotateTextCounter <= 10 {
		request.gameLoop.Move(request.gameLoop.Player1Base.distanceFrom(8000, 4000))
	} else if 200 <= rotateTextCounter || rotateTextCounter <= 105 {
		Hero0Farming(request)
	} else {
		Hero0Attacking(request)
	}

	if rotateTextCounter <= 90 {
		Hero1Farming(request)
		Hero2Farming(request)
	} else {
		Hero1DefensiveFarming(request)
		Hero2DefensiveFarming(request)
	}
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

	for {
		var player0, player1 *Player
		var monsters Monsters
		{
			if result0, result1, result2, err := retrieveMutableInformation(); err != nil {
				log.Panicf(`ExtractFmtScan: %s`, err)
			} else {
				player0 = result0
				player1 = result1
				monsters = result2
			}
		}

		var hero0 = player0.Heroes[0]
		var hero1 = player0.Heroes[1]
		var hero2 = player0.Heroes[2]

		var orchestratorRequest = Director{
			gameLoop: gameLoop,
			hero0:    hero0,
			hero1:    hero1,
			hero2:    hero2,
			monsters: monsters,
			player0:  player0,
			player1:  player1,
		}

		PassiveFarming(orchestratorRequest)
		// ropeAnEnemy(orchestratorRequest)

		rotateTextCounter += 1
	}
}
