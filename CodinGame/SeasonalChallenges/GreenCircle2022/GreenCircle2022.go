package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
)

/**
 * Complete the hackathon before your opponent by following the principles of Green IT
 **/

type GamePhase string

const (
	GamePhaseMove      GamePhase = "MOVE"
	GamePhaseGiveCard            = "GIVE_CARD"
	GamePhaseThrowCard           = "THROW_CARD"
	GamePhasePlayCard            = "PLAY_CARD"
	GamePhaseRelease             = "RELEASE"
)

// ---------------------------------------------------------------------------------------------------------------------
// -- Player -----------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------

type Player struct {
	Location                        int // id of the zone in which the player is located
	Score                           int
	PermanentDailyRoutineCards      int // Number of DAILY_ROUTINE the player has played. It allows them to take cards from the adjacent zones
	PermanentArchitectureStudyCards int // Number of ARCHITECTURE_STUDY the player has played. It allows them to draw more cards
}

type Players []Player

// ---------------------------------------------------------------------------------------------------------------------
// -- CardsCount -------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------

type CardsCountLocation string

const (
	CardsCountLocationHand              CardsCountLocation = "HAND"
	CardsCountLocationDraw                                 = "DRAW"
	CardsCountLocationDiscard                              = "DISCARD"
	CardsCountLocationOpponent                             = "OPPONENT_CARDS"
	CardsCountLocationAutomated                            = "AUTOMATED"
	CardsCountLocationOpponentAutomated                    = "OPPONENT_AUTOMATED"
)

type CardsCount struct {
	Location           CardsCountLocation
	Training           int
	Coding             int
	DailyRoutine       int
	TaskPrioritization int
	ArchitectureStudy  int
	ContinuousDelivery int
	CodeReview         int
	Refactoring        int
	Bonus              int
	TechnicalDebt      int
}

type CardsCounts struct {
	Hand              CardsCount
	Draw              CardsCount
	Discard           CardsCount
	Opponent          CardsCount
	Automated         CardsCount
	OpponentAutomated CardsCount
}

func (cardsCount *CardsCount) ShouldRelease(applications Applications) *Application {
	for _, application := range applications {
		log.Println(application)

		application.TrainingNeeded = Constrain(application.TrainingNeeded - cardsCount.Training*2)
		application.CodingNeeded = Constrain(application.CodingNeeded - cardsCount.Coding*2)
		application.DailyRoutineNeeded = Constrain(application.DailyRoutineNeeded - cardsCount.DailyRoutine*2)
		application.TaskPrioritizationNeeded = Constrain(application.TaskPrioritizationNeeded - cardsCount.TaskPrioritization*2)
		application.ArchitectureStudyNeeded = Constrain(application.ArchitectureStudyNeeded - cardsCount.ArchitectureStudy*2)
		application.ContinuousDeliveryNeeded = Constrain(application.ContinuousDeliveryNeeded - cardsCount.ContinuousDelivery*2)
		application.CodeReviewNeeded = Constrain(application.CodeReviewNeeded - cardsCount.CodeReview*2)
		application.RefactoringNeeded = Constrain(application.RefactoringNeeded - cardsCount.Refactoring*2)

		var total = 0

		total += application.TrainingNeeded
		total += application.CodingNeeded
		total += application.DailyRoutineNeeded
		total += application.TaskPrioritizationNeeded
		total += application.ArchitectureStudyNeeded
		total += application.ContinuousDeliveryNeeded
		total += application.CodeReviewNeeded
		total += application.RefactoringNeeded

		if total-2 <= cardsCount.Bonus {
			return &application
		}
	}

	return nil
}

func (cardsCount *CardsCount) FinalRelease(applications Applications) *Application {
	for _, application := range applications {
		log.Println(application)

		application.TrainingNeeded = Constrain(application.TrainingNeeded - cardsCount.Training*2)
		application.CodingNeeded = Constrain(application.CodingNeeded - cardsCount.Coding*2)
		application.DailyRoutineNeeded = Constrain(application.DailyRoutineNeeded - cardsCount.DailyRoutine*2)
		application.TaskPrioritizationNeeded = Constrain(application.TaskPrioritizationNeeded - cardsCount.TaskPrioritization*2)
		application.ArchitectureStudyNeeded = Constrain(application.ArchitectureStudyNeeded - cardsCount.ArchitectureStudy*2)
		application.ContinuousDeliveryNeeded = Constrain(application.ContinuousDeliveryNeeded - cardsCount.ContinuousDelivery*2)
		application.CodeReviewNeeded = Constrain(application.CodeReviewNeeded - cardsCount.CodeReview*2)
		application.RefactoringNeeded = Constrain(application.RefactoringNeeded - cardsCount.Refactoring*2)

		var total = 0

		total += application.TrainingNeeded
		total += application.CodingNeeded
		total += application.DailyRoutineNeeded
		total += application.TaskPrioritizationNeeded
		total += application.ArchitectureStudyNeeded
		total += application.ContinuousDeliveryNeeded
		total += application.CodeReviewNeeded
		total += application.RefactoringNeeded

		if total <= cardsCount.Bonus {
			return &application
		}
	}

	return nil
}

// ---------------------------------------------------------------------------------------------------------------------
// -- Application ------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------

type Application struct {
	ApplicationID            int
	TrainingNeeded           int
	CodingNeeded             int
	DailyRoutineNeeded       int
	TaskPrioritizationNeeded int
	ArchitectureStudyNeeded  int
	ContinuousDeliveryNeeded int
	CodeReviewNeeded         int
	RefactoringNeeded        int
}

func (application Application) Pairing() [8]int {
	var result = [8][2]int{
		{application.TrainingNeeded, 0},
		{application.CodingNeeded, 1},
		{application.DailyRoutineNeeded, 2},
		{application.TaskPrioritizationNeeded, 3},
		{application.ArchitectureStudyNeeded, 4},
		{application.ContinuousDeliveryNeeded, 5},
		{application.CodeReviewNeeded, 6},
		{application.RefactoringNeeded, 7},
	}

	sort.Slice(result[:], func(i, j int) bool {
		return result[i][0] > result[j][0]
	})

	return [8]int{
		result[0][1],
		result[1][1],
		result[2][1],
		result[3][1],
		result[4][1],
		result[5][1],
		result[6][1],
		result[7][1],
	}
}

type Applications []Application

func (applications Applications) MostCommon() (applicationSum Application) {
	for _, application := range applications {
		applicationSum.TrainingNeeded += application.TrainingNeeded
		applicationSum.CodingNeeded += application.CodingNeeded
		applicationSum.DailyRoutineNeeded += application.DailyRoutineNeeded
		applicationSum.TaskPrioritizationNeeded += application.TaskPrioritizationNeeded
		applicationSum.ArchitectureStudyNeeded += application.ArchitectureStudyNeeded
		applicationSum.ContinuousDeliveryNeeded += application.ContinuousDeliveryNeeded
		applicationSum.CodeReviewNeeded += application.CodeReviewNeeded
		applicationSum.RefactoringNeeded += application.RefactoringNeeded
	}

	return applicationSum
}

func (applications Applications) NextCard(mainStruct MainStruct) {
	var gameLoop = mainStruct.GameLoop
	var player1 = mainStruct.Players[0]

	var pairing = applications.MostCommon().Pairing()

	if player1.Location != pairing[0] {
		gameLoop.Move(pairing[0])
	} else {
		gameLoop.Move(pairing[1])
	}
}

// ---------------------------------------------------------------------------------------------------------------------
// -- GameLoop ---------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------

type GameLoop struct {
	Scanner       *bufio.Scanner
	DrawableCards *Application
}

// -- Output ----------------------------------------------------------------------------------------------------------

func (gameLoop *GameLoop) Debug(text string) {
	log.Println(text)
}

func (gameLoop *GameLoop) Random() {
	fmt.Println("RANDOM")
}

func (gameLoop *GameLoop) Move(zoneID int) {
	fmt.Printf("MOVE %v\n", strconv.Itoa(zoneID))
}

func (gameLoop *GameLoop) Release(applicationID int) {
	fmt.Printf("RELEASE %v\n", applicationID)
}

func (gameLoop *GameLoop) Wait() {
	fmt.Println("WAIT")
}

func (gameLoop *GameLoop) Give(cardType string) {
	fmt.Printf("GIVE %v\n", cardType)
}

func (gameLoop *GameLoop) Throw(cardType string) {
	fmt.Printf("THROW %v\n", cardType)
}

func (gameLoop *GameLoop) Training() {
	fmt.Println("TRAINING")
}

func (gameLoop *GameLoop) Coding() {
	fmt.Println("CODING")
}

func (gameLoop *GameLoop) DailyRoutine() {
	fmt.Println("DAILY_ROUTINE")
}

func (gameLoop *GameLoop) TaskPrioritization(cardTypeToThrow string) {
	fmt.Printf("TASK_PRIORITIZATION %v\n", cardTypeToThrow)
}

func (gameLoop *GameLoop) ArchitectureStudy() {
	fmt.Println("ARCHITECTURE_STUDY")
}

func (gameLoop *GameLoop) ContinuousDeliver(cardTypeToAutomate string) {
	fmt.Printf("CONTINUOUS_DELIVERY %v\n", cardTypeToAutomate)
}

func (gameLoop *GameLoop) CodeReview() {
	fmt.Println("CODE_REVIEW")
}

func (gameLoop *GameLoop) Refactoring() {
	fmt.Println("REFACTORING")
}

// -- Input ----------------------------------------------------------------------------------------------------------

func (gameLoop *GameLoop) scan(items ...interface{}) {
	gameLoop.Scanner.Scan()
	fmt.Sscan(gameLoop.Scanner.Text(), items...)
}

func (gameLoop *GameLoop) getApplications() (results Applications) {
	var applicationsCount int
	gameLoop.scan(&applicationsCount)

	for i := 0; i < applicationsCount; i++ {
		var objectType string
		var id, trainingNeeded, codingNeeded, dailyRoutineNeeded, taskPrioritizationNeeded, architectureStudyNeeded, continuousDeliveryNeeded, codeReviewNeeded, refactoringNeeded int
		gameLoop.scan(&objectType, &id, &trainingNeeded, &codingNeeded, &dailyRoutineNeeded, &taskPrioritizationNeeded, &architectureStudyNeeded, &continuousDeliveryNeeded, &codeReviewNeeded, &refactoringNeeded)

		results = append(results, Application{
			ApplicationID:            id,
			TrainingNeeded:           trainingNeeded,
			CodingNeeded:             codingNeeded,
			DailyRoutineNeeded:       dailyRoutineNeeded,
			TaskPrioritizationNeeded: taskPrioritizationNeeded,
			ArchitectureStudyNeeded:  architectureStudyNeeded,
			ContinuousDeliveryNeeded: continuousDeliveryNeeded,
			CodeReviewNeeded:         codeReviewNeeded,
			RefactoringNeeded:        refactoringNeeded,
		})
	}

	return results
}

func (gameLoop *GameLoop) getGamePhase() (result GamePhase) {
	gameLoop.scan(&result)

	return result
}

func (gameLoop *GameLoop) getPlayers() (results Players) {
	for i := 0; i < 2; i++ {
		var playerLocation, playerScore, playerPermanentDailyRoutineCards, playerPermanentArchitectureStudyCards int
		gameLoop.scan(&playerLocation, &playerScore, &playerPermanentDailyRoutineCards, &playerPermanentArchitectureStudyCards)

		results = append(results, Player{
			Location:                        playerLocation,
			Score:                           playerScore,
			PermanentDailyRoutineCards:      playerPermanentDailyRoutineCards,
			PermanentArchitectureStudyCards: playerPermanentArchitectureStudyCards,
		})
	}

	return results
}

func (gameLoop *GameLoop) getCardsCount() (results CardsCounts) {
	var cardLocationsCount int
	gameLoop.scan(&cardLocationsCount)

	for i := 0; i < cardLocationsCount; i++ {
		var cardsLocation CardsCountLocation
		var trainingCardsCount, codingCardsCount, dailyRoutineCardsCount, taskPrioritizationCardsCount, architectureStudyCardsCount, continuousDeliveryCardsCount, codeReviewCardsCount, refactoringCardsCount, bonusCardsCount, technicalDebtCardsCount int
		gameLoop.scan(&cardsLocation, &trainingCardsCount, &codingCardsCount, &dailyRoutineCardsCount, &taskPrioritizationCardsCount, &architectureStudyCardsCount, &continuousDeliveryCardsCount, &codeReviewCardsCount, &refactoringCardsCount, &bonusCardsCount, &technicalDebtCardsCount)

		var cardsCount = CardsCount{
			Location:           cardsLocation,
			Training:           trainingCardsCount,
			Coding:             codingCardsCount,
			DailyRoutine:       dailyRoutineCardsCount,
			TaskPrioritization: taskPrioritizationCardsCount,
			ArchitectureStudy:  architectureStudyCardsCount,
			ContinuousDelivery: continuousDeliveryCardsCount,
			CodeReview:         codeReviewCardsCount,
			Refactoring:        refactoringCardsCount,
			Bonus:              bonusCardsCount,
			TechnicalDebt:      technicalDebtCardsCount,
		}

		if cardsCount.Location == CardsCountLocationHand {
			results.Hand = cardsCount
		} else if cardsCount.Location == CardsCountLocationDraw {
			results.Draw = cardsCount
		} else if cardsCount.Location == CardsCountLocationDiscard {
			results.Discard = cardsCount
		} else if cardsCount.Location == CardsCountLocationOpponent {
			results.Opponent = cardsCount
		}
	}

	return results
}

func (gameLoop *GameLoop) getPossibleMoves() (results []string) {
	var possibleMovesCount int
	gameLoop.scan(&possibleMovesCount)

	for i := 0; i < possibleMovesCount; i++ {
		var possibleMove string
		gameLoop.scan(&possibleMove)

		results = append(results, possibleMove)
	}

	return results
}

func (gameLoop *GameLoop) getInput() (mainStruct MainStruct) {
	mainStruct.GameLoop = gameLoop
	mainStruct.GamePhase = gameLoop.getGamePhase()
	mainStruct.Applications = gameLoop.getApplications()
	mainStruct.Players = gameLoop.getPlayers()
	mainStruct.CardsCounts = gameLoop.getCardsCount()
	mainStruct.PossibleMoves = gameLoop.getPossibleMoves()

	return mainStruct
}

// ---------------------------------------------------------------------------------------------------------------------
// -- Utils ------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------

func Constrain(x int) int {
	return int(math.Max(0, float64(x)))
}

// ---------------------------------------------------------------------------------------------------------------------
// -- Main -------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------

type MainStruct struct {
	GameLoop      *GameLoop
	GamePhase     GamePhase
	Applications  Applications
	Players       Players
	CardsCounts   CardsCounts
	PossibleMoves []string
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 1000000), 1000000)
	var gameLoop = &GameLoop{
		Scanner: scanner,
		DrawableCards: &Application{
			TrainingNeeded:           5,
			CodingNeeded:             5,
			DailyRoutineNeeded:       5,
			TaskPrioritizationNeeded: 5,
			ArchitectureStudyNeeded:  5,
			ContinuousDeliveryNeeded: 5,
			CodeReviewNeeded:         5,
			RefactoringNeeded:        5,
		},
	}

	for {
		var mainStruct = gameLoop.getInput()

		log.Println(1, mainStruct.GamePhase)
		log.Println(2, mainStruct.Applications)
		log.Println(3, mainStruct.Players)
		log.Println(4, mainStruct.CardsCounts)
		log.Println(5, mainStruct.PossibleMoves)

		_ = mainStruct

		if mainStruct.GamePhase == GamePhaseMove {
			mainStruct.Applications.NextCard(mainStruct)
		} else if mainStruct.GamePhase == GamePhaseRelease {
			if mainStruct.Players[0].Score >= 4 {
				result := mainStruct.CardsCounts.Hand.FinalRelease(mainStruct.Applications)
				if result != nil {
					gameLoop.Release(result.ApplicationID)
				} else {
					gameLoop.Wait()
				}
			} else if result := mainStruct.CardsCounts.Hand.ShouldRelease(mainStruct.Applications); result != nil {
				gameLoop.Release(result.ApplicationID)
			} else {
				gameLoop.Wait()
			}
		} else {
			gameLoop.Random()
		}
	}
}
