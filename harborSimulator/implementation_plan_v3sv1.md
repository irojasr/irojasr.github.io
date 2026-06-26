# Harbor Simulator V3.1 — Polish & Deep Systems Update

Comprehensive implementation plan addressing all 18 feedback items from playtesting (~150 months of gameplay). The focus is on polishing V3.0 before adding major new systems, but several items require substantial new mechanics (morale escalation, crane system, criminal expansion, exploitation system).

## User Review Required

> [!IMPORTANT]
> **Scope Warning**: This is a massive update touching nearly every system. The full file will grow from ~2300 lines to ~3500+ lines. I recommend implementing in **3 phases** to keep changes reviewable:
> - **Phase 1** (UI/QoL/Bugs): Items 2, 4, 6, 7, 8, 9, 10, 14 — quick wins
> - **Phase 2** (Balance/Systems): Items 1, 5, 11, 12, 13, 17 — gameplay systems
> - **Phase 3** (Deep Content): Items 15, 16, 18 — major new content

> [!WARNING]
> **Item 15 (Criminal Organizations)** includes sensitive content (human trafficking, organ trafficking). These are presented as morally repugnant in-game activities with severe consequences. Should I include all suggested organizations, or tone down certain ones?

## Open Questions

> [!IMPORTANT]
> 1. **Phase approach**: Should I implement all 3 phases in one go, or deliver them sequentially for testing between phases?
> 2. **Criminal content**: All 6 criminal organizations as listed, or should some be excluded/renamed?
> 3. **Strike cost formula**: You mention scaling with revenue/infrastructure — should a late-game strike potentially cost $5,000+? What's a reasonable ceiling?
> 4. **Crane automation**: Should cranes fully replace workers on a dock, or only reduce the number needed? (I'm leaning toward reducing workers needed by ~50%, not full automation.)
> 5. **Morale death spiral**: The escalation system (demonstrations → strikes → sabotage → takeover) — should there be a point of no return, or should the player always be able to recover?

---

## Proposed Changes

### Phase 1 — UI, QoL, and Bug Fixes

---

#### Item 2: Celebrity Cruise Dramatic Notification

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current behavior**: Celebrity cruises are pushed directly to `G.incoming` with only a log message (line 1648-1649). The Mothership gets a dramatic banner in the preview panel (lines 1992-2001).

**Changes**:
- Add a new CSS class `.celebrity-banner` with gold/star-themed gradient animation (similar to `.mothership-banner`)
- Add a `<div id="celebrityArrival">` inside the preview panel (next to `mothershipArrival`)
- Modify `eventCelebrity()` to add the ship to `G.previewShips` instead of `G.incoming`, so it appears in the Ships Approaching interface
- Add a new state flag `G.celebrityActive` to track display
- Render the celebrity banner in `renderPreview()` when a celebrity ship is in the preview list

---

#### Item 4: Forecast Panel — Always Show Projected Change

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current behavior** (lines 342-350): The entire forecast panel is a collapsible `<details>` element. The player must expand it to see anything.

**Changes**:
- Restructure the forecast panel: the outer panel is no longer collapsible
- Always display the **Projected Change** summary line (the total net) outside any `<details>`
- Move the detailed breakdown (Ship Revenue, Worker Wages, Contract Fees, Infrastructure Upkeep, Other) into an inner `<details>` collapsible
- The Morale Breakdown remains a second inner collapsible
- New HTML structure:
  ```html
  <div class="panel" id="forecastPanel">
    <h2>📊 Monthly Forecast</h2>
    <div id="forecastSummary"><!-- always visible: projected change --></div>
    <details class="collapsible">
      <summary><h3>📋 Detailed Breakdown</h3></summary>
      <div id="forecastBody"><!-- ship revenue, wages, etc --></div>
    </details>
    <details class="collapsible">
      <summary><h3>😊 Morale Breakdown</h3></summary>
      <div id="moraleBreakdown"></div>
    </details>
  </div>
  ```

---

#### Item 6: Storm Auto-Confirm

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current behavior** (line 831): When `G._stormNext` is true, `generatePreviewShips()` returns an empty array. The player still must manually confirm arrivals.

**Changes**:
- In `nextMonth()`, after generating preview ships (line 1452), if the preview list is empty (storm or no ships), automatically call `confirmArrivals()` logic inline
- This skips the preview phase entirely, going straight to docking phase
- Log message: "🌊 Storm has passed. No ships arrived."

---

#### Item 7: Smart Assignment Bug Fix

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current bug** (lines 935-945): Smart mode iterates through docks in order and breaks when workers run out. If early docks are already full (workDone >= workNeeded), they're filtered out at line 924, but the remaining ships are sorted by array order, not by priority.

**Root cause**: The algorithm doesn't **prioritize ships that still need workers**. If a ship has `workDone + (assigned * eff) >= workNeeded` already from a previous month's partial assignment, it may get skipped while another ship that genuinely needs workers gets 0.

**Fix**:
- Sort `docksWithShips` by `(workNeeded - workDone)` ascending in smart mode (finish ships closest to completion first)
- After first pass: if workers remain, do a second pass assigning to any ship that can still use more workers (up to maxCrew)
- This two-pass approach ensures no ship is left empty when workers are available

---

#### Item 8: Decline All Free Market Ships Button

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Changes**:
- Add a new button `Decline All Free Market ❌` in the preview panel batch actions area (line 358-361)
- New function `declineFreeMarketShips()` that sets `accepted = false` for all ships where `s.companyId === null`
- Positioned between "Accept All" and "Decline All"

---

#### Item 9: Larger Click Targets for Ship Selection

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current behavior** (line 2013): Ship acceptance uses a small checkbox `<input type="checkbox">`.

**Changes**:
- Make the entire `<tr>` row clickable by adding `onclick="togglePreviewShip(${i})"` to the row
- Add `cursor: pointer` styling to preview rows
- Keep the checkbox for visual feedback but make the row the primary click target
- Add a subtle hover highlight effect on preview rows

---

#### Item 10: Dock Occupancy in Header

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current behavior** (line 388): Dock header reads `🏗️ Your Docks`.

**Changes**:
- Change the dock header to dynamically show occupied count: `🏗️ Your Docks (X / Y)` where X = docks with ships or blocked, Y = total docks
- Update in `renderDocks()` to calculate and display this
- Add an `id` to the dock header `<h2>` for dynamic updates

---

#### Item 14: Harbor Log Grammar Polish

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current problematic messages** (sampling):
- Line 1713: `"Mafia attempted Dock #${d.id} — SECURITY BLOCKED IT!"`
- Line 1717: `"MAFIA TAKEOVER! Dock #${d.id} seized!"`
- Line 1628: `"DOCK STRIKE! Workers demand a $100 bonus."`
- Various other terse/robotic messages

**Changes**: Rewrite ~30 log messages throughout the game with more natural, narrative prose:
- `"The mafia attempted to seize Dock #7, but private security successfully repelled the attack."`
- `"The mafia has forcefully taken control of Dock #7. Your operations are compromised."`
- `"Dock workers have declared a strike, demanding a bonus payment before returning to work."`
- Review and rewrite all `log()` calls for consistent narrative tone

---

### Phase 2 — Balance, Systems, and New Mechanics

---

#### Item 1: Company Balancing

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current issue**: 3-star company ships feel identical to Free Market ships because the only difference is the contract fee — the ships generated by `makeShip()` use the same `SHIP_TYPES` ranges regardless of company.

**Root cause analysis**:
- Free Market fish ships: revenue $75-130, work 2-3, maxCrew 2
- Ocean Bounty (3-star fish): same ships, same revenue range, but you pay $20/mo for the contract
- The only benefit: trust ≥4 has 8% chance of +40% revenue, trust ≥2 has slight reliability

**Changes**:
- Add company-specific modifiers to COMPANIES: `revBonus`, `freqBonus`, `workReduction`, `crewBonus`
- **1-star companies**: Revenue penalty (×0.85), unreliable frequency (−15% chance of ship loss), higher spoilage risk. Advantage: cheap contracts, low rep requirement
- **3-star companies**: Revenue bonus (×1.15), consistent frequency, occasional premium cargo. Advantage: reliability + modest revenue boost
- **5-star companies**: Revenue bonus (×1.35), guaranteed minimum frequency, frequent premium cargo, reputation boost per delivery. Advantage: significant revenue premium
- Modify `makeShip()` to apply company `revBonus` when `companyId` is present
- Modify `getFreqCount()` to apply per-company `freqBonus`
- Free Market ships should get a slight revenue penalty (×0.9) to make them strictly the weakest option
- Add `permDockChance` field to companies (probability of requesting permanent dock assignment)

---

#### Item 5: Company Statistics Reference Table

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Changes**:
- Add a new `<details>` section inside the How to Play panel (lines 240-255) titled "📊 Company Reference"
- Generate a comprehensive table from COMPANIES and SHIP_TYPES data showing:
  - Company name, emoji, trust level
  - Cargo type
  - Average arrival frequency (derived from SHIP_TYPES freq + company modifiers)
  - Average work required (midpoint of wMin-wMax)
  - Max workers per ship
  - Dock slots occupied (1, or 2 for special ships)
  - Contract duration range
  - Typical revenue range
  - Reputation requirement
  - Permanent dock probability
  - Cargo volatility (based on seasonal behavior)
  - Seasonal behavior (peak months)
  - Government sensitivity
  - Mafia sensitivity
  - Special events
- This table is generated dynamically from game constants so it stays accurate

---

#### Item 11: Low Morale Escalation System

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current behavior**: Morale can reach 0 with no consequences beyond −15% efficiency.

**New escalation system** — tracked by `G.lowMoraleMonths` (consecutive months at morale < threshold):

| Months at Low Morale | Threshold | Event |
|---|---|---|
| 3+ months at <30 | **Demonstrations** — Workers protest, −2 reputation, no work for 1 month |
| 6+ months at <25 | **Slowdowns** — All work efficiency halved for 2 months |
| 9+ months at <20 | **Wildcat Strikes** — Automatic strikes that can't be paid off |
| 12+ months at <15 | **Sabotage** — Random dock/crane destroyed, $500-2000 damage |
| 15+ months at <10 | **Housing Destruction** — Worker settlement downgraded one level |
| 18+ months at <10 | **Infrastructure Destruction** — Random sub-facility destroyed |
| 21+ months at <5 | **Dock Occupation** — Workers seize 1-3 docks, require negotiation to free |
| 24+ months at <5 | **Worker Cooperative** — Workers demand ownership share, permanent wage increase |
| 30+ months at <5 | **Complete Takeover** — Game over variant: workers seize the harbor |

**State additions**: `G.lowMoraleMonths`, `G.moraleEscalationLevel`

**New function**: `tickMoraleEscalation()` — called in `nextMonth()` after morale calculation

---

#### Item 12: High Morale Rewards

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**New progression system** for sustained high morale (tracked by `G.highMoraleMonths`):

| Months at High Morale | Threshold | Reward |
|---|---|---|
| 6+ months at >70 | **Families Form** — Flavor event, +2 morale |
| 12+ months at >70 | **Children Born** — Population growth begins |
| 24+ months at >75 | **Apprentices** — Children become apprentice workers (free, half efficiency) |
| 36+ months at >75 | **Experienced Workers** — +5% global efficiency permanently |
| 48+ months at >80 | **Town Reputation** — +1 reputation/month passive, attracts better contracts |
| 60+ months at >80 | **Settlement Growth** — Worker cap +5, new families arrive |
| 72+ months at >85 | **Regional Hub** — Unlocks premium company contracts, +20% revenue from all ships |

**State additions**: `G.highMoraleMonths`, `G.workerFamilies`, `G.apprentices`, `G.permanentEffBonus`, `G.settlementGrowthLevel`

---

#### Item 13: Cargo Cranes

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**New system**: Cranes are purchased per-dock and increase unloading efficiency.

**Data structure**:
```javascript
// Added to each dock object
crane: { level: 0, health: 100, sabotaged: false }

const CRANE_LEVELS = [
  { name: 'None', effBonus: 0, cost: 0, upkeep: 0 },
  { name: 'Basic Crane', effBonus: 0.3, cost: 800, upkeep: 15 },
  { name: 'Heavy Crane', effBonus: 0.6, cost: 2000, upkeep: 35 },
  { name: 'Auto Crane', effBonus: 1.0, cost: 5000, upkeep: 60 },
];
```

**Mechanics**:
- Each crane level adds an efficiency bonus applied as additional "virtual workers" worth `effBonus * workNeeded` progress per month
- Cranes require upkeep (added to `infraUpkeep()`)
- Purchase via a new "Install Crane" button per dock in the docks table
- Crane column added to docks table showing crane level and health
- Workers dislike automation: each crane reduces morale by 2
- Low morale risks: sabotage (crane destroyed), vandalism (crane damaged, reduced efficiency)
- New `tickCranes()` function in `nextMonth()` for degradation and sabotage events

---

#### Item 17: Strike Cost Scaling

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current behavior** (line 1054): Strike cost is always $100.

**New formula**:
```javascript
function calcStrikeCost() {
    let base = 50;
    base += G.totalWorkers * 5;           // Worker count
    base += infraUpkeep() * 0.5;          // Infrastructure scale
    base += contractUpkeep() * 0.3;       // Contract scale
    if (G.unionActive) base *= 1.5;       // Union leverage
    if (G.workerMorale < 20) base *= 1.3; // Desperation
    base *= (1 + G.workerProgression * 0.2); // Town size
    return Math.round(Math.max(100, base));
}
```

**Expected late-game cost**: With 25 workers, full infrastructure, and union → ~$1,500-$3,000

**Changes**:
- Replace hardcoded `$100` in `payStrike()` and the strike panel button
- Update the strike panel to dynamically show the calculated cost
- Update `eventStrike()` log message

---

### Phase 3 — Deep Content Expansion

---

#### Item 15: Criminal Organizations

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**New constant**: `CRIMINAL_ORGS`
```javascript
const CRIMINAL_ORGS = [
    { id: 'human_traffic', name: 'Shadow Network', emoji: '👤',
      cargo: 'People', revenue: [2000,4000], risk: 'extreme',
      repPenalty: -20, govResponse: 'international', desc: 'Trafficking ring' },
    { id: 'organ_trade', name: 'Red Market', emoji: '🫀',
      cargo: 'Organs', revenue: [3000,6000], risk: 'extreme',
      repPenalty: -25, govResponse: 'taskforce', desc: 'Black market organ trade' },
    { id: 'arms_smuggle', name: 'Iron Curtain Co.', emoji: '🔫',
      cargo: 'Weapons', revenue: [1500,3000], risk: 'high',
      repPenalty: -15, govResponse: 'military', desc: 'Weapons pipeline' },
    { id: 'counterfeit', name: 'Mirror Image Ltd.', emoji: '💵',
      cargo: 'Counterfeits', revenue: [800,1500], risk: 'medium',
      repPenalty: -5, govResponse: 'customs', desc: 'Counterfeit goods' },
    { id: 'wildlife', name: 'Exotic Cargo Inc.', emoji: '🐆',
      cargo: 'Wildlife', revenue: [1200,2500], risk: 'high',
      repPenalty: -10, govResponse: 'interpol', desc: 'Illegal wildlife trade' },
    { id: 'pharma', name: 'Back Door Pharma', emoji: '💊',
      cargo: 'Pharmaceuticals', revenue: [1000,2000], risk: 'medium',
      repPenalty: -8, govResponse: 'fda_raid', desc: 'Black-market drugs' },
];
```

**Mechanics**:
- Criminal organizations become available after becoming a Smuggler (existing gate)
- Each has a unique reward/risk profile and triggers different government responses
- New contracts panel section: "🤵 Underground Contracts" — visible only when `G.isSmuggler`
- Each criminal contract has a `heatLevel` that increases with activity and triggers escalating responses
- New `SHIP_TYPES` entries for each criminal cargo type
- New state: `G.criminalContracts`, `G.heatLevel`, `G.activeOrgs`

---

#### Item 16: Late-Game Criminal Dynamics

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**New late-game event system** for smugglers, activated after month 100+ or 50+ months as smuggler:

**New events** (added to `rollEvent()` smuggler branch):
- **Rival Cartel** — Competing organization demands territory; fight or negotiate
- **Gang War** — Multiple docks blocked, worker casualties, $1000-3000 damage
- **Government Crackdown** — All criminal operations paused for 3-6 months, massive fines
- **International Investigation** — Heat increases dramatically, all criminal revenue reduced 50%
- **Corruption Scandal** — If gov is Corrupt, forced election; if Lawful, increased raids
- **Money Laundering** — New system: criminal revenue must be laundered (costs 20-40% of revenue)
- **Informant** — Random worker becomes informant; evidence accumulates automatically
- **Betrayal** — Criminal partner turns, massive fine + dock seizure
- **Assassination Attempt** — Security required to survive; without it, game consequences
- **International Sanctions** — All foreign companies suspend contracts for 6 months

**State additions**: `G.smugglerMonths`, `G.rivalCartels`, `G.launderingRate`, `G.informantActive`, `G.sanctioned`

**New function**: `tickCriminalDynamics()` — called monthly for smugglers

---

#### Item 18: Exploitation Management System

#### [MODIFY] [indexHarborSimulator.html](file:///Users/factoryimage/Documents/irojasr.github.io/harborSimulator/indexHarborSimulator.html)

**Current behavior**: Exploitation is 2 toggles — Token Economy and Gates Closed.

**New system**: Full labor policy management with 14 policies, each with tradeoffs.

**Data structure**:
```javascript
const LABOR_POLICIES = {
    // Exploitative
    mandatoryOvertime:    { name: 'Mandatory Overtime',     cost: 0,   eff: +0.20, morale: -8,  rep: -3,  upkeep: 0,   req: 2 },
    childLabor:           { name: 'Child Labor',            cost: 0,   eff: +0.15, morale: -15, rep: -20, upkeep: 0,   req: 3 },
    reducedSafety:        { name: 'Reduced Safety',         cost: 0,   eff: +0.10, morale: -5,  rep: -5,  upkeep: -20, req: 1 },
    productionQuotas:     { name: 'Production Quotas',      cost: 0,   eff: +0.15, morale: -10, rep: 0,   upkeep: 0,   req: 2 },
    wageSuppression:      { name: 'Wage Suppression',       cost: 0,   eff: 0,     morale: -12, rep: -5,  upkeep: 0,   req: 1, wageReduction: 0.25 },
    surveillance:         { name: 'Surveillance',           cost: 400, eff: 0,     morale: -8,  rep: -3,  upkeep: 15,  req: 3, unionPenalty: -5 },
    antiUnion:            { name: 'Anti-Union Campaign',    cost: 300, eff: 0,     morale: -5,  rep: -8,  upkeep: 10,  req: 2, unionPenalty: -8 },
    prisonLabor:          { name: 'Prison Labor Contracts', cost: 200, eff: +0.10, morale: -10, rep: -15, upkeep: 5,   req: 4, extraWorkers: 5 },
    // Benevolent
    performanceBonuses:   { name: 'Performance Bonuses',    cost: 0,   eff: +0.10, morale: +8,  rep: +3,  upkeep: 0,   req: 2, wageCost: 3 },
    retirementBenefits:   { name: 'Retirement Benefits',    cost: 500, eff: 0,     morale: +10, rep: +5,  upkeep: 25,  req: 3 },
    paidLeave:            { name: 'Paid Leave',             cost: 0,   eff: -0.05, morale: +12, rep: +5,  upkeep: 0,   req: 2, wageCost: 2 },
    healthcare:           { name: 'Healthcare Investment',  cost: 800, eff: +0.05, morale: +15, rep: +8,  upkeep: 40,  req: 3, accidentReduction: 0.7 },
    education:            { name: 'Education Programs',     cost: 600, eff: +0.15, morale: +10, rep: +5,  upkeep: 30,  req: 3 },
};
```

**New UI**: New section in the Infrastructure panel — "📜 Labor Policies"
- Toggle-based interface for each policy
- Clear display of effects (efficiency, morale, reputation, cost)
- Policies interact with each other (e.g., mandatory overtime + performance bonuses partially offset morale loss)
- Some policies are mutually exclusive (child labor + education programs)

**State addition**: `G.laborPolicies` — object mapping policy IDs to boolean

**Integration**: 
- `workerEff()` reads active policies for efficiency modifiers
- `calcMoraleDelta()` reads policies for morale modifiers
- `effectiveWage()` reads policies for wage modifiers
- `tickUnion()` reads anti-union policies
- Worker events check policy states for accident rates, riot chances, etc.

---

## Verification Plan

### Automated Tests
- No automated test framework exists for this single-file game. Verification will be manual.

### Manual Verification
1. **Phase 1**: Open the game in browser, verify:
   - Celebrity cruise shows dramatic banner in preview panel
   - Forecast shows projected change without expanding
   - Storm automatically skips to docking phase
   - Smart Assignment correctly distributes workers to unfinished ships
   - "Decline All Free Market" button works
   - Clicking ship rows toggles accept/decline
   - Dock header shows "(X / Y)" occupancy
   - Log messages read naturally

2. **Phase 2**: Use Debug Mode to fast-forward through game phases:
   - Verify company contracts provide meaningful advantages over free market
   - Check company reference table in Instructions
   - Test low morale escalation by forcing morale to 0 and advancing months
   - Test high morale rewards by keeping morale >80 for extended periods
   - Test crane purchase, upgrade, and sabotage
   - Verify strike costs scale with game state

3. **Phase 3**: Test criminal gameplay:
   - Become smuggler, verify new criminal organizations appear
   - Test each criminal contract type
   - Advance to month 150+ and verify late-game criminal events
   - Test exploitation policies individually and in combination
   - Verify mutual exclusivity and interaction effects
