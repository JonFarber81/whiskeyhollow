---
title: Game Systems
---

[← Home](index.md)

# Game Systems

## The city

Kansas City is split into districts. Each one belongs to a faction:

| District | What's there | Home of |
|---|---|---|
| **Westport** | City Hall's turf | Pendergast Machine |
| **Union Station** | Rail hub, ideal for smuggling | Union Station Crew |
| **River Market** | Old warehouses by the Missouri River | River Market Syndicate |
| **18th & Vine** | Jazz clubs and speakeasies | The Jazz District Co. |
| **West Bottoms** | Meatpacking and industry | Kansas City PD |

Most locations are generated fresh each visit using BSP room-and-corridor generation. A few story locations are hand-built and the same every time:

- **Union Station Interior**: a crew boss fight and smuggling deliveries
- **The Blue Room**: a Jazz District speakeasy for social jobs
- **River Market Warehouse**: Syndicate headquarters and heist targets
- **KC Police Precinct**: assassination jobs and the evidence room

## Factions

| Faction | What they do |
|---|---|
| **Pendergast Machine** | Tom Pendergast runs the city from City Hall: judges, cops, and contracts. |
| **Union Station Crew** | They move product by rail, truck, and barge. If it comes into KC, they take a cut. |
| **River Market Syndicate** | Warehouses, muscle, and wholesale. They prefer brute force. |
| **The Jazz District Co.** | Speakeasies and front businesses on 18th & Vine, used to launder money. |
| **Kansas City PD (Corrupt)** | Most of the force is on the take. You can pay them off or fight them. |

### Ranks

Reputation with each faction runs from 0 to 100. Your rank in a faction depends on your rep:

| Rep | Rank |
|---|---|
| 10+ | Street Runner |
| 25+ | Associate |
| 45+ | Soldier |
| 65+ | Capo |
| 85+ | **Boss** |

Higher ranks unlock faction perks. For example, reaching Soldier with the Pendergast Machine makes heat decay faster. Factions also have enemies, so gaining rep with one can lose you rep with another.

## Jobs

Jobs are the main way you make progress. Each faction posts jobs on the job board (`f`):

| Job | Goal |
|---|---|
| **Delivery** | Move contraband from A to B without getting caught |
| **Heist** | Rob a rival shipment or cash stash |
| **Intimidation** | Rough someone up. Expect a fight |
| **Protection** | Defend a location against waves of enemies for a number of turns |
| **Bribery** | Talk your way into paying off a cop or official |
| **Assassination** | Kill a named rival. High risk, high reward |
| **Intel** | Scout a rival location and get back out |

**Rewards:** cash, faction rep, rare items, crew unlocks, and territory.
**If you fail:** your heat goes up, you lose rep, crew can get hurt or killed, and rival factions get aggressive.

## Heat

Heat is your wanted level, from 0 to 100.

- **Raised by:** fighting, gunshots, failed jobs, and being loud.
- **Lowered by:** bribes, laying low, and passive decay at the end of each chapter.
- **At 50:** cop patrols start appearing.
- **At 80:** you get raided.

## Economy

Cash is the only currency. The contraband types are:

- **Whiskey**: worth the most
- **Beer**: bulky, sold in volume
- **Gin**: sells quickly
- **Medicinal alcohol**: low heat

Prices change over time and differ between districts. You make money by buying where it's cheap and selling where it's expensive.

## Combat

Combat is turn-based and happens on the map grid. Walk into an enemy to attack it. Ranged weapons need line of sight.

**Weapons:** fists, brass knuckles, blackjack, straight razor, .38 revolver, 1911 pistol, Winchester shotgun, sawed-off, and the Thompson (Tommy gun).

**Enemies:**
- **Beat cops**: walk patrols and call for backup
- **Detectives**: smarter, and they investigate
- **Rival goons**: aggressive
- **Made men**: tough, with high stats
- **Bosses**: fights with two phases. At half HP a boss like Big Jim Torrio changes tactics, calls in reinforcements, and fights harder

**Named NPCs** include Tom Pendergast, Big Jim Torrio, The Ox, Dutch Malone, Ward Captain Higgins, Detective Flynn, Captain Morrison, Mama Dolores, Sal the Driver, and others. Each has dialogue for meeting you, being attacked, and being close to death.

## Crew

You can hire up to **4** crew members. Each has a role, a loyalty score (0–100), skills, a weekly wage, and a status: available, injured, arrested, or dead.

| Role | What they bring |
|---|---|
| **Muscle** | Better in fights and intimidation jobs |
| **Driver** | Faster deliveries and better odds of getting away |
| **Lookout** | Less heat, and earlier warning of enemies |
| **Fixer** | Better bribes, less cop heat, and can break arrested crew out of jail |

Crew members take their turns with yours and fight alongside you.

## Stats and leveling

You have five stats: **STR, DEX, INT, CHA, LUCK**. Each one gives a D&D-style modifier of `(stat − 10) ÷ 2`.

- **Max HP** = 20 + 2 × STR
- **Attack** = 2 + STR modifier
- **Defense** = DEX modifier
- **Dodge** = 10 + DEX modifier

Your level comes from what you've done in the game, not from kills:

> **Level = 1 + (jobs completed ÷ 5) + (total rep across all factions ÷ 50)**

Each level-up lets you pick a perk. You spend skill points to raise stats in the skill menu (`s`).

## Perks

There are four perk categories, with six perks in each. Every class starts with one perk for free.

### Combat
| Perk | Effect |
|---|---|
| Iron Fists | Unarmed attacks +2 damage |
| Deadeye | Ranged attack rolls +2 |
| Streetfighter | You crit on a roll 2 lower than normal |
| Hard-Boiled | Max HP +15 |
| Sucker Punch | +3 damage on your first attack each fight |
| Blood Money | +$10 for each kill |

### Economy
| Perk | Effect |
|---|---|
| Black Market | Sell contraband for 15% more |
| Silk Tongue | Bribery +3 |
| Numbers Runner | Delivery job pay +20% |
| Bulk Buyer | Buy contraband for 15% less |
| Nest Egg | +$25 for each successful job |
| Protection Money | +$15 per turn from territory you control |

### Shadow
| Perk | Effect |
|---|---|
| Ghost | 25% less heat from combat |
| Friends in Low Places | Heat decays 5 more per chapter |
| Crooked Badge | Raids start at 95 heat instead of 80 |
| Light Fingers | Pick up items from adjacent tiles |
| Vanish | Once per run, press `v` to drop heat to 0 |
| Clean Hands | Successful bribery jobs never raise heat |

### Influence
| Perk | Effect |
|---|---|
| Natural Politician | All rep gains +10% |
| Street Rep | Lose half as much rep when you fail a job |
| Good Boss | Crew loyalty +10 after each job |
| Well Connected | 2 more candidates when hiring (6 total) |
| Word Gets Around | Every faction gains +2 rep when you level up |
| Made Man | Your rep with a faction can't be knocked below 25 |

## Meta-progression

Some stats carry over between runs, such as runs completed and your best cash total. They're stored in `data/meta_save.json`. Unlocks earned from past runs are tracked there too, but they don't change new runs yet.

## Saving

Saves are plain JSON files in `saves/`, so you can open and read them. The RNG state is saved too, which means a loaded game continues exactly where it left off.
