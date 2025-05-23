# Backend EV Logic - 7-Step Corrected Methodology

## 🚨 Finalized Corrected Logic (May 23, 2025)

This document outlines the **exact** 7-step No-Vig & +EV calculation logic that replaces the previous overcomplicated approach.

## ✅ Step-by-Step No-Vig & +EV Logic

### Step 1: Determine Sharp Sportsbook Base Line
- **Objective**: Identify the best sportsbook odds available across all markets
- **Implementation**: 
  - Compare odds from all available bookmakers for the target outcome
  - Select the most favorable odds to the bettor (highest positive odds or least negative odds)
  - Example: Pinnacle +113 becomes our baseline reference

### Step 2: Calculate No-Vig (Fair Odds) for Each Sportsbook
- **Objective**: Remove the sportsbook margin (vig) to get fair odds
- **Process**:
  1. Convert two-sided odds to implied probabilities
  2. Calculate total probability (will be > 100% due to vig)
  3. Remove vig by normalizing probabilities to sum to 100%
  4. Convert back to American odds

**Example**:
```
Brewers (+113), Pirates (-123):
• Brewers Implied: 100 / (113 + 100) = 46.95%
• Pirates Implied: 123 / (123 + 100) = 55.16%
• Total = 102.11% (2.11% vig)
• Brewers Fair = 46.95% / 102.11% ≈ 45.98%
• No-vig odds Brewers: (100 / 45.98%) - 100 ≈ +117
```

### Step 3: Choose Best Available No-Vig Line
- **Objective**: Select the most favorable no-vig odds across all sportsbooks
- **Implementation**: Compare each sportsbook's no-vig odds and choose the highest value for the bettor
- **Result**: This becomes our "true no-vig line" baseline

### Step 4: Adjust for 2% P2P Exchange Fee
- **Objective**: Account for standard P2P platform fees
- **Process**: 
  - Adjust the true no-vig implied probability for 2% fee
  - Formula: `adjusted_probability = fair_probability / (1 - 0.02)`

**Example**:
```
True no-vig probability: 46.08%
Adjust for 2% fee: 46.08% / 0.98 ≈ 47.02%
Adjusted odds: (100 / 47.02%) - 100 ≈ +113
```

### Step 5: Add EV Buffer (2% for Main, 3% for Alternate Lines)
- **Objective**: Add conservative buffer to ensure positive EV
- **Implementation**:
  - **Main lines**: Add 2% buffer
  - **Alternate/prop lines**: Add 3% buffer
  - Simply subtract from probability: `final_probability = adjusted_probability - buffer`

**Example (main line, 2% buffer)**:
```
Probability after fee: 47.02%
Apply 2% buffer: 47.02% - 2% = 45.02%
Recommended minimum odds: (100 / 45.02%) - 100 ≈ +122
```

**Example (alternate/prop line, 3% buffer)**:
```
Probability after fee: 47.02%
Apply 3% buffer: 47.02% - 3% = 44.02%
Recommended minimum odds: (100 / 44.02%) - 100 ≈ +127
```

### Step 6: Compare to Current P2P Odds
- **Objective**: Determine if available odds exceed our minimum threshold
- **Process**:
  1. Compare market odds to recommended minimum odds
  2. If market odds exceed minimum = highlight as +EV
  3. If market odds do NOT exceed minimum = recommend users manually set odds at calculated threshold
  4. Calculate expected value for qualifying opportunities

### Step 7: Highlight Significant Book-to-Book Opportunities
- **Objective**: Identify monetizable odds differences across sportsbooks
- **Implementation**:
  - Look for probability differences >5% between bookmakers
  - Highlight these as potential arbitrage or line shopping opportunities
  - Independent of P2P odds analysis

## 🔖 MVP Implementation Details

### Core Configuration
- **P2P Exchange Fee**: 2% (standard across platforms)
- **EV Buffer for Main Lines**: 2%
- **EV Buffer for Alternate Lines**: 3%
- **Book-to-Book Opportunity Threshold**: 5% probability difference

### Database Storage
The calculations are stored in the `ev_calculations` table with:
- `standard_ev`: The expected value using our 7-step methodology
- `no_vig_ev`: Same as standard_ev for consistency
- `no_vig_fair_probability`: The fair probability after vig removal
- `no_vig_fair_odds`: The recommended minimum odds with fees and buffers
- `calculation_method_details`: Full JSON of the 7-step calculation breakdown

### API Integration
The `EVCalculationService` integrates with the odds polling workflow:
1. Polls odds from multiple bookmakers
2. Groups odds by bookmaker in required format: `{'bookmaker': {'odds_a': float, 'odds_b': float}}`
3. Runs 7-step calculation for each bookmaker as target
4. Stores results in database
5. Makes results available to frontend via API endpoints

### Frontend Display
Results should be displayed showing:
- Target bookmaker and odds
- Recommended minimum odds for +EV
- Expected value per $100 bet
- Whether the opportunity qualifies as +EV
- Book-to-book opportunities (>5% difference)

## 🚀 Key Advantages of This Approach

1. **Clear and Systematic**: Each step has a specific purpose and calculation
2. **Conservative**: Built-in buffers ensure genuine +EV opportunities
3. **Practical**: Accounts for real-world P2P fees and market dynamics  
4. **Transparent**: Every calculation step is documented and stored
5. **Scalable**: Works for any number of bookmakers and market types

## 📊 Example End-to-End Calculation

**Scenario**: Milwaukee Brewers @ Pittsburgh Pirates

**Available Odds**:
- Pinnacle: Brewers +113, Pirates -123
- DraftKings: Brewers +110, Pirates -125  
- FanDuel: Brewers +108, Pirates -120

**Step-by-Step for Brewers**:
1. **Sharp Baseline**: Pinnacle +113 (best available)
2. **No-Vig Calculations**:
   - Pinnacle: +117 (after removing 2.11% vig)
   - DraftKings: +114 (after removing 2.38% vig)
   - FanDuel: +112 (after removing 2.78% vig)
3. **Best No-Vig**: Pinnacle +117
4. **P2P Fee Adjustment**: +113 (46.08% → 47.02%)
5. **EV Buffer**: +122 (47.02% → 45.02% with 2% buffer)
6. **Evaluation**: Any odds better than +122 = +EV opportunity
7. **Book-to-Book**: DraftKings (+110) vs Pinnacle (+113) = 1.2% difference (below 5% threshold)

**Result**: Recommend minimum odds of +122 for positive EV on Brewers. 