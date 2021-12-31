/** @param {NS} ns **/

//-- Configuration ----------
var configLogHostInformation = true
var configLogFileName = "data.txt"
var configHomeName = "home"
var configCopyFilesFromHost = true
var configHackScript = "new_focus_hack.js"
var configGrowScript = "focus_grow.js"
var configWeakenScript = "focus_weaken.js"
var configGrowthPercentage = 20
var configTolerancePercentage = 10
var configTargetSecurityMinimum = 30
var configTargetHackChanceMinimum = 0.2
var configServerPurchaseSize = 11
var configScriptRamUsage = 1.75
var configSecurityCurrentMaximum = 30
var configSecurityMaximum = 30


async function logAndWrite(ns, text) {
	//-- Declarations ----------

	//-- Usage ----------
	if (configLogHostInformation == false) {
		return
	}

	ns.tprint(text);
	await ns.write(configLogFileName, "\n" + text, "a");
}

async function nukeFromHost(ns, hostName) {
	//-- Declarations ----------
	var portsOpenRequired = ns.getServerNumPortsRequired(hostName)
	var exposedPorts = 0
	var requiredHackLevel = ns.getServerRequiredHackingLevel(hostName)
	var currentHackLevel =  ns.getHackingLevel()

	//-- Usage ----------
	if (requiredHackLevel > currentHackLevel) {
		ns.tprint("Hacking level too low: " + currentHackLevel + "/" + requiredHackLevel)
		return false
	}
	
	if (ns.hasRootAccess(hostName) == true) {
		return true
	}

	if (ns.fileExists("HTTPWorm.exe", configHomeName)) {
		ns.httpworm(hostName)
		exposedPorts += 1
	}
	if (ns.fileExists("relaySMTP.exe", configHomeName)) {
		ns.relaysmtp(hostName)
		exposedPorts += 1
	}
	if (ns.fileExists("BruteSSH.exe", configHomeName)) {
		ns.brutessh(hostName)
		exposedPorts += 1
	}
	if (ns.fileExists("FTPCrack.exe", configHomeName)) {
		ns.ftpcrack(hostName)
		exposedPorts += 1
	}
	if (ns.fileExists("SQLInject.exe", configHomeName)) {
		ns.sqlinject(hostName)
		exposedPorts += 1
	}
	if (ns.getServerNumPortsRequired(hostName) > exposedPorts) {
		ns.tprint("Requires more ports to open: " + exposedPorts + "/" + portsOpenRequired)
		return false
	}

	ns.nuke(hostName)
	ns.tprint("Nuked host")

	return true
}

async function navigateConnections(ns) {
	//-- Declarations ----------
	var result = false
	var visitedHosts = [configHomeName]
	var depthSearchHosts = [] // js overwrites namespace variables when recursing
	var depthSearchIndex = [] // js overwrites namespace variables when recursing
	var accessableHosts = []

	//-- Usage ----------
	async function navigatorFromHost(hostName, depth) {
		//-- Declarations ----------
		var connectedHosts = ns.scan(hostName, true)
		depthSearchHosts.push(connectedHosts)
		depthSearchIndex.push(0)

		//-- Usage ----------
		for (depthSearchIndex[depth] = 0; depthSearchIndex[depth] < depthSearchHosts[depth].length; depthSearchIndex[depth]++) {
			var connectedHost = depthSearchHosts[depth][depthSearchIndex[depth]];

			if (visitedHosts.includes(connectedHost)) {
				continue
			}

			visitedHosts.push(connectedHost)

			result = await nukeFromHost(ns, connectedHost)

			if (result == false) {
				continue
			}

			accessableHosts.push(connectedHost)

			await navigatorFromHost(connectedHost, depth + 1);
		}

		depthSearchHosts.pop()
		depthSearchIndex.pop()
	}

	await navigatorFromHost(configHomeName, 0);
	return accessableHosts
}

function hostNamesOrdered(ns, hostNames) {
	var hostNamesMaxMoney = []
	for (var i = 0; i < hostNames.length; i++) {
		var hostName = hostNames[i]

		hostNamesMaxMoney.push([hostName, ns.getServerMaxMoney(hostName)])
	}

	hostNamesMaxMoney.sort(function (a, b) { return b[1] - a[1] })

	var results = []
	for (var i = 0; i < hostNamesMaxMoney.length; i++) {
		var hostNameMaxMoney = hostNamesMaxMoney[i]

		results.push(hostNameMaxMoney[0])
	}

	return results
}

function bestHostNameValueFromHostNames(ns, hostNames) {
	//-- Declarations ----------

	//-- Usage ----------
	var hostNames = hostNamesOrdered(ns, hostNames)

	for (var i = 0; i < hostNames.length; i++) {
		//-- Declarations ----------
		var hostName = hostNames[i]

		var securityCurrent = ns.getServerSecurityLevel(hostName)
		var securityMinimum = ns.getServerMinSecurityLevel(hostName)
		var hackChance = ns.hackAnalyzeChance(hostName)

		//-- Usage ----------
		if (securityMinimum >= configTargetSecurityMinimum) {
			continue
		} else if (securityCurrent >= configSecurityCurrentMaximum) {
			continue
		} else if (hackChance <= 0.000005) {
			continue
		}

		return hostName
	}

	return null
}

async function prepareWeakenHostName(ns, hostName) {
	var securityReducePerWeaken = ns.weakenAnalyze(1)
	var securityCurrent = ns.getServerSecurityLevel(hostName)
	var securityMinimum = ns.getServerMinSecurityLevel(hostName)
	
	var weakenRamUsage = ns.getScriptRam(configWeakenScript, configHomeName)

	if (securityCurrent - securityMinimum > securityReducePerWeaken) {
		return {Threads: 0, SleepTime: 0}
	} 

	var weakenThreads = Math.ceil((securityCurrent - securityMinimum) / securityReducePerWeaken)	
	var weakenTime = ns.getWeakenTime(hostName).toFixed(4)

	await logAndWrite(ns, "security current:    " + securityCurrent)
	await logAndWrite(ns, "security minimum:    " + securityMinimum)
	await logAndWrite(ns, "weaken reduction:    " + securityReducePerWeaken)
	await logAndWrite(ns, "allocating threads:  " + weakenThreads)

	if (weakenThreads == 0) {
		ns.tprint("skipping weaken preparation")
		return null
	}

	await logAndWrite(ns, "completed in:       ", weakenTime)
	return {Threads: weakenThreads, SleepTime: weakenTime}
}

async function prepareGrowHostName(ns, hostName) {
	var moneyMaximum = ns.getServerMaxMoney(hostName)
	var moneyCurrent = ns.getServerMoneyAvailable(hostName)
	var moneyDifference = 0
	var tolerancePercentage = configTolerancePercentage / 10
	var securityReducePerWeaken = ns.weakenAnalyze(1)
	var securityGrowPerGrow = ns.growthAnalyzeSecurity(1)

	if (moneyCurrent == 0) {
		moneyDifference = moneyMaximum
	} else {
	    moneyDifference = moneyMaximum / moneyCurrent
	}

	if (moneyDifference == 0 ) {
		await logAndWrite(ns, "skipping growth preparation")
		return null
	}
	
	//---- Time ----------
	var growThreads = Math.ceil(ns.growthAnalyze(hostName, moneyDifference))
	growThreads = Math.round(growThreads + growThreads * tolerancePercentage)

	var weakenThreads = Math.round((growThreads * securityGrowPerGrow) / securityReducePerWeaken)
	weakenThreads = Math.round(weakenThreads + weakenThreads * tolerancePercentage)

	var growRamUsage = ns.getScriptRam(configGrowScript, configHomeName)

	var growTime = ns.getGrowTime(hostName).toFixed(4)

	await logAndWrite(ns, "money maximum:  " + moneyMaximum)
	await logAndWrite(ns, "money current:  " + moneyCurrent)
	await logAndWrite(ns, "money difference:  " + (moneyMaximum - moneyCurrent))
	await logAndWrite(ns, "money saturation: " + (moneyCurrent / moneyMaximum * 100).toFixed(2) + "%")
	await logAndWrite(ns, "allocating grow threads:  " + growThreads)
	await logAndWrite(ns, "allocating weaken threads:  " + weakenThreads)

	if (moneyDifference <= configGrowthPercentage / 100) {
		await logAndWrite(ns, "skipping growth preparation")
		return
	}
	
	await logAndWrite(ns, "completed in:       ", growTime)
	return {GrowThreads: growThreads, WeakenThreads: weakenThreads, SleepTime: growTime}
}

async function allocateHostName(ns, hostName) {
	//-- Declarations ----------
	var moneyGainPerHack = ns.hackAnalyze(hostName)
	var securityGrowPerGrow = ns.growthAnalyzeSecurity(1)
	var securityGrowPerHack = ns.hackAnalyzeSecurity(1)
	var securityReducePerWeaken = ns.weakenAnalyze(1)
	var tolerancePercentage = configTolerancePercentage / 10
	var timeForHack = ns.getHackTime(hostName) / 1000
	var timeForGrow = ns.getGrowTime(hostName) / 1000
	var timeForWeaken = ns.getWeakenTime(hostName) / 1000
	timeForHack = parseInt(timeForHack)
	timeForGrow = parseInt(timeForGrow)
	timeForWeaken = parseInt(timeForWeaken)
	var hackSuccessChance = ns.hackAnalyzeChance(hostName)
	var securityMinimum = ns.getServerMinSecurityLevel(hostName)
	var moneyMaximum = ns.getServerMaxMoney(hostName)
	var ramMaximum = ns.getServerMaxRam(hostName)

	//-- Usage ----------

	await logAndWrite(ns, "hack time: " + timeForHack, "s")
	await logAndWrite(ns, "grow time: " + timeForGrow, "s")
	await logAndWrite(ns, "weaken time: " + timeForWeaken, "s")

	//---- Time ----------
	var hackReducer =   1
	var growReducer =   1
	var weakenReducer = 1
	if (timeForWeaken > timeForGrow) {
		growReducer = timeForGrow / timeForWeaken
		hackReducer = timeForHack / timeForWeaken 
	} else {
		weakenReducer = timeForWeaken / timeForGrow 
		hackReducer = timeForHack / timeForGrow
	}

	await logAndWrite(ns, "hack reducer:   " + hackReducer)
	await logAndWrite(ns, "grow reducer:   " + growReducer)
	await logAndWrite(ns, "weaken reducer: " + weakenReducer)

	//---- Threads ----------
	var hackThreads = Math.round(configGrowthPercentage / (moneyGainPerHack * 100))

	var growThreads = ns.growthAnalyze(hostName, 1 + configGrowthPercentage / 100)
	growThreads = Math.round(growThreads + growThreads * tolerancePercentage)

	var weakenThreads = Math.round((growThreads * securityGrowPerGrow + hackThreads * securityGrowPerHack) / securityReducePerWeaken)
	weakenThreads = Math.round(weakenThreads + weakenThreads * tolerancePercentage)

	await logAndWrite(ns, "hack threads:   " + hackThreads)
	await logAndWrite(ns, "grow threads:   " + growThreads)
	await logAndWrite(ns, "weaken threads: " + weakenThreads)

	hackThreads = parseInt(hackThreads * hackReducer)
	growThreads = parseInt(growThreads * growReducer)
	weakenThreads = parseInt(weakenThreads * weakenReducer)

	await logAndWrite(ns, "hack threads:   " + hackThreads)
	await logAndWrite(ns, "grow threads:   " + growThreads)
	await logAndWrite(ns, "weaken threads: " + weakenThreads)

	var threadTotal = hackThreads + growThreads + weakenThreads

	//-- Return ----------
	return {HackThreads: hackThreads, GrowThreads: growThreads, WeakenThreads: weakenThreads, TotalThreads: threadTotal}
}

async function assignThreads(ns, hostName, scriptName, target, acceptedThreads, loops) {
	//-- Declarations ----------
	var scriptRamUsage = ns.getScriptRam(scriptName, configHomeName)
	var ram = ns.getServerMaxRam(hostName) - ns.getServerUsedRam(hostName)
	
	if (hostName == configHomeName) {
		ram = ns.getServerMaxRam(configHomeName) - 15
	}

	var usableThreads = parseInt(ram / scriptRamUsage)
	var remainingThreads = acceptedThreads
	var assignedThreads = 0

	//-- Usage ----------
	if (usableThreads <= 0 || Number.isNaN(acceptedThreads)) {
		return remainingThreads
	}

	await logAndWrite(ns, usableThreads, " ", acceptedThreads)
	if (acceptedThreads >= usableThreads) {
		assignedThreads = usableThreads
		remainingThreads -= usableThreads
	} else {
		assignedThreads = usableThreads
		remainingThreads = 0
	}
	ns.tprint(remainingThreads)

	if (assignedThreads <= 0) {
		throw Error("some math went wrong, cannot assign 0 threads")
	}

	await ns.scp(scriptName, configHomeName, hostName)
	await logAndWrite(ns, "Host: " + hostName + ", Script: " + scriptName + ", Target: " + target)
	ns.exec(scriptName, hostName, assignedThreads, target, loops)
	return remainingThreads
}

function beingTargeted(ns, hostNames, target) {
	for (var i = 0; i < hostNames.length; i++) {
		var hostName = hostNames[i]

		var weakenScript = ns.getRunningScript(configWeakenScript, hostName)
		if (growScript != null && weakenScript.args[0] == target) {
			return true
		}
		var growScript = ns.getRunningScript(configGrowScript, hostName)
		if (growScript != null && growScript.args[0] == target) {
			return true
		}
		var hackScript = ns.getRunningScript(configHackScript, hostName)
		if (growScript != null && weakenScript.args[0] == target) {
			return true
		}
	}

	return false
}

async function assignHostsToSpecificThreads(ns, hostNames, target, script, threads) {
	var ramTotal = ramTotalFromHostNames(ns, hostNames)
	var scriptRamUsage = ns.getScriptRam(configGrowScript, configHomeName)

	if (ramTotal > threads) {
			ramTotal
	} 

	for (var j = 0; j < hostNames.length; j++) {
		var result = await assignThreads(ns, hostNames[j], configWeakenScript, target, weakenThreads, 1)
		if (result == 0) {
			break
		} else {
			weakenThreads = result
		}
	}
}

async function weakenTarget(ns, hostNames, target) {
	await logAndWrite(ns, "weakening: " + target)
	var weakenTask = await prepareWeakenHostName(ns, target)
	if (weakenTask === null) {
		return {WeakenThreads: 0, TimeTaken: 0}
	}

	var weakenThreads = weakenTask.Threads
	var timeForWeaken = ns.getWeakenTime(target) / 1000
	timeForWeaken = Math.ceil(timeForWeaken + 0.5)

	var ramTotal = ramTotalFromHostNames(ns, hostNames)
	var scriptRamUsage = ns.getScriptRam(configGrowScript, configHomeName)

	var scriptRamUsage = ns.getScriptRam(configWeakenScript, configHomeName)
	var usableThreads = parseInt(ramTotal / scriptRamUsage)
	var threadRepetitions = 1
	if (usableThreads < weakenThreads) {
		threadRepetitions = Math.ceil(weakenThreads / usableThreads)
	}

	for (var j = 0; j < hostNames.length; j++) {
		var result = await assignThreads(ns, hostNames[j], configWeakenScript, target, weakenThreads, threadRepetitions)
		if (result == 0) {
			break
		} else {
			weakenThreads = result
		}
	}

	return {WeakenThreads: weakenThreads, TimeTaken: timeForWeaken}
}

async function growTarget(ns, hostNames, target) {
	await logAndWrite(ns, "growing: " + target)
	var growTask = await prepareGrowHostName(ns, target)
	if (growTask === null) {
		return {GrowThreads: 0, TimeTaken: 0}
	}

	var weakenThreads = growTask.WeakenThreads
	var growThreads = growTask.GrowThreads
	var timeForGrow = ns.getGrowTime(target) / 1000
	timeForGrow = Math.ceil(timeForGrow + 0.5)
	
	var ramTotal = ramTotalFromHostNames(ns, hostNames)
	var scriptRamUsage = ns.getScriptRam(configGrowScript, configHomeName)
	var scriptRamUsage = ns.getScriptRam(configWeakenScript, configHomeName)
	var usableThreads = parseInt(ramTotal / scriptRamUsage)
	var threadRepetitions = 1
	if (usableThreads < weakenThreads) {
		threadRepetitions = Math.ceil((weakenThreads + growThreads) / usableThreads)
	}
	weakenThreads = parseInt(weakenThreads / threadRepetitions)
	growThreads = parseInt(growThreads / threadRepetitions)

	for (var i = 0; i < hostNames.length; i++) {
		ns.tprint("weaken1: ", weakenThreads)
		ns.tprint("grow1: ", growThreads)
		var hostName = hostNames[i]
		var scriptRamUsage = ns.getScriptRam(configGrowScript, configHomeName)
		var ram = ns.getServerMaxRam(hostName) - ns.getServerUsedRam(hostName)
		
		if (hostName == configHomeName) {
			ram = ns.getServerMaxRam(configHomeName) - 15
		}

		var usableThreads = parseInt(ram / scriptRamUsage)

		var assignedGrowThreads = usableThreads
		var assignedWeakenThreads = 0
		
		if (assignedGrowThreads > growThreads) {
			assignedWeakenThreads += assignedGrowThreads - growThreads
			assignedGrowThreads = growThreads
		} 
		if (assignedWeakenThreads > weakenThreads) {
			assignedWeakenThreads = weakenThreads
		}

		if (assignedGrowThreads !== 0) {
			await assignThreads(ns, hostName, configGrowScript, target, assignedGrowThreads, threadRepetitions)
		}
		if (assignedWeakenThreads !== 0) {
			await assignThreads(ns, hostName, configWeakenScript, target, assignedWeakenThreads, threadRepetitions)
		}
		
		weakenThreads -= assignedWeakenThreads
		growThreads -= assignedGrowThreads
		ns.tprint("weaken2: ", weakenThreads)
		ns.tprint("grow2: ", growThreads)
		if (growThreads == 0 && weakenThreads == 0) {
			break
		}
	}

	return {GrowThreads: growThreads, TimeTaken: timeForGrow}
}

function ramTotalFromHostNames(ns, hostNames) {
	//-- Declarations ----------
	var ramTotal = 0

	//-- Usage ----------
	for (var i = 0; i < hostNames.length; i++) {
		//-- Declarations ----------
		var hostName = hostNames[i]

		if (hostName == configHomeName) {
			var result = parseInt(ns.getServerMaxRam(configHomeName) - ns.getServerUsedRam(hostName) - 15)
			if (result > 0) {
				ramTotal += result
			}
		} else {
			ramTotal += ns.getServerMaxRam(hostName) - ns.getServerUsedRam(hostName)
		}		
	}

	return ramTotal
}

async function distributeThreads(ns, target, hostNames) {
	//-- Declarations ----------
	var threadDistribution = await allocateHostName(ns, target)

	var ramTotal = ramTotalFromHostNames(ns, hostNames)
	var threadsTotal = parseInt(ramTotal / configScriptRamUsage)

	var weakenThreads = null
	var growThreads = null
	var hackThreads = null
	if (threadsTotal < threadDistribution.TotalThreads) {
		var weakenPercentage = threadDistribution.WeakenThreads / threadDistribution.TotalThreads
		var weakenThreads = parseInt(threadsTotal * weakenPercentage)

		var growPercentage = threadDistribution.GrowThreads / threadDistribution.TotalThreads
		var growThreads = parseInt(threadsTotal * growPercentage)

		var hackPercentage = threadDistribution.HackThreads / threadDistribution.TotalThreads
		var hackThreads = parseInt(threadsTotal * hackPercentage)
	} else {
		weakenThreads = threadDistribution.WeakenThreads
		growThreads = threadDistribution.GrowThreads
		hackThreads = threadDistribution.HackThreads
	}

	await logAndWrite(ns, threadsTotal)

	//-- Usages ----------
	for (var i = 0; i < hostNames.length; i++) {
		//-- Declarations ----------
		var hostName = hostNames[i]

		if (ns.getServerMaxRam(hostName) - ns.getServerUsedRam(hostName) < configScriptRamUsage) {
			continue
		}

		await logAndWrite(ns, "===========================")
		await logAndWrite(ns, hostName)
		
		//-- Usages ----------

		await logAndWrite(ns, weakenThreads)
		await logAndWrite(ns, growThreads)
		await logAndWrite(ns, hackThreads)
	
		growThreads = await assignThreads(ns, hostName, configGrowScript, target, growThreads, 0)
		weakenThreads = await assignThreads(ns, hostName, configWeakenScript, target, weakenThreads, 0)
		HackThreads = await assignThreads(ns, hostName, configHackScript, target, hackThreads, 0)
	}
}


export async function main(ns) {
	await ns.write(configLogFileName, ":)\n", "w");
	await logAndWrite(ns, "running")			
	var hostNames = await navigateConnections(ns)
	ns.tprint(hostNames)

	var target = undefined
	if (ns.args.length != 1) {
		target = bestHostNameValueFromHostNames(ns, hostNames)
	} else {
		target = ns.args[0]
	}
	
	while (true) {
		var result = await weakenTarget(ns, hostNames, target)
		ns.tprint(result)
		if (result.WeakenThreads <= 0) {
			break
		}

		ns.tprint("sleeping for: " + result.TimeTaken)
		await ns.sleep(result.TimeTaken * 1000)
	}
	ns.tprint("FINISHED WEAKENING")

	while (true) {
		var result = await growTarget(ns, hostNames, target)
			ns.tprint(result)
		ns.tprint(result)
		if (result.GrowThreads <= 0 ) {
			break
		}
		ns.tprint("sleeping for: " + result.TimeTaken)
		await ns.sleep(result.TimeTaken * 1000)
	}
	ns.tprint("FINISHED GROWING")

	await distributeThreads(ns, target, hostNames)
}
