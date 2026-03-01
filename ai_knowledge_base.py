"""
AI Knowledge Base
Contains all basketball coaching knowledge from our rule-based assistant
This is fed to OpenAI as context
"""

def get_drill_library_summary() -> str:
    """Get summary of available drills for OpenAI context"""
    return """
AVAILABLE BASKETBALL DRILLS:

DRIBBLING DRILLS:
- Right Hand Dribbling (Beginner, 10-15 min): Practice dribbling with only right hand. Stand in place (50 reps), walk, jog, then sprint while maintaining control. Focus: Keep ball low, use fingertips, eyes up.
- Left Hand Dribbling (Beginner, 10-15 min): Same as right hand but for non-dominant hand. Builds muscle memory and coordination.
- Two-Ball Dribbling (Intermediate, 10 min): Dribble two basketballs simultaneously. Develops hand-eye coordination and ambidexterity.
- Crossover Dribble Drill (Intermediate, 10 min): Practice crossing ball between hands. Figure-8 pattern between legs. Focus: Quick, low crossovers.
- Between the Legs Dribble (Intermediate, 10 min): Dribble ball between legs from front to back. Walk forward while dribbling between legs.
- Behind the Back Dribble (Advanced, 10 min): Master behind-the-back dribbling. Advanced move for ball protection.

SHOOTING DRILLS:
- Form Shooting (Beginner, 15-20 min): Perfect shooting form close to basket. BEEF principle: Balance, Eyes on target, Elbow in, Follow-through. Start 3 feet, move to 5 feet, then 10 feet.
- Catch and Shoot (Intermediate, 15 min): Practice shooting off the catch. Partner passes from various spots. Quick release, square to basket.
- Pull-Up Jump Shot (Intermediate, 15 min): Shoot while moving and pulling up. Practice from different distances. Focus: Balance and elevation.
- Three-Point Shooting (Intermediate, 20 min): Improve three-point accuracy. Shoot from 5 spots around three-point line. Practice catch-and-shoot and off dribble.
- Free Throw Practice (Beginner, 10 min): Master free throw shooting. Develop consistent routine. Practice under pressure.

PASSING DRILLS:
- Chest Pass Drill (Beginner, 10 min): Perfect chest passing technique. Two hands, snap through, follow through.
- Bounce Pass Drill (Beginner, 10 min): Master the bounce pass. Bounce point should be 2/3 distance to target.
- Outlet Pass Drill (Intermediate, 10 min): Practice rebounding and outlet passing. Pivot quickly, pass to numbers on fast break.
- Skip Pass Drill (Advanced, 10 min): Pass across court to open teammate. High arc to clear defense.

REBOUNDING DRILLS:
- Box Out Drill (Intermediate, 10 min): Master box out technique. Butt to opponent, wide base, find the ball.
- Reaction Rebound Drill (Intermediate, 10 min): Improve rebounding reaction time. Read trajectory, pursue aggressively, secure with two hands.
- Tip Drill (Advanced, 10 min): Practice tipping rebounds. Quick hands, jump with purpose.

DEFENSE DRILLS:
- Defensive Slide Drill (Beginner, 10 min): Improve lateral movement. Stay low, wide base, slide don't cross.
- Close-Out Drill (Intermediate, 10 min): Practice closing out on shooters. Sprint to 3 feet, then close out under control, high hand contest.
- One-on-One Defense (Intermediate, 15 min): Defend live offensive player. Stay in stance, keep ball in front, move feet not hands.

FOOTWORK DRILLS:
- Pivot Drill (Beginner, 10 min): Master pivoting on both feet. Keep pivot foot planted, protect ball.
- Triple Threat Position (Beginner, 10 min): Practice triple threat stance. Knees bent, ball at shooting pocket, ready to act.

CONDITIONING:
- Suicide Runs (Intermediate, 10 min): Build speed and endurance. Run to free throw line, half court, opposite free throw, full court and back.
- Defensive Slide Conditioning (Intermediate, 10 min): Combine defense and conditioning. Stay low, maintain form.
"""

def get_stat_definitions() -> str:
    """Get statistical definitions for OpenAI context"""
    return """
STATISTICAL DEFINITIONS:

- Points Per Game (PPG) = total points ÷ games played
- Rebounds Per Game (RPG) = total rebounds ÷ games played
- Assists Per Game (APG) = total assists ÷ games played
- Field Goal % (FG%) = field goals made ÷ field goals attempted
- Three-Point % (3P%) = three-pointers made ÷ three-pointers attempted
- Free Throw % (FT%) = free throws made ÷ free throws attempted
- 3PT Made (3PTM) = total three-pointers made
- Efficiency (EFF) = a summary stat that rewards points/rebounds/assists/steals/blocks and penalizes missed shots and turnovers (per game)
- Assist/Turnover Ratio = assists ÷ turnovers (higher is better)
- True Shooting % = accounts for 2PT, 3PT, and FT shooting efficiency
- Rebound % = percentage of available rebounds a player secured
- Win Shares = estimate of wins contributed by player
- VORP = Value Over Replacement Player

STRENGTHS IDENTIFICATION:
- Scoring ability: 15+ PPG = strong, 10+ PPG = solid
- Rebounding: 8+ RPG = strong, 5+ RPG = good
- Playmaking: 5+ APG = strong, 3+ APG = good
- Shooting: 45%+ FG% = efficient, 35%+ 3P% = good three-point shooter
- Defense: 2+ SPG = strong steals, 1+ BPG = shot blocking

WEAKNESSES IDENTIFICATION:
- Turnovers: 4+ TPG = high turnover rate, 2.5+ TPG = needs improvement
- Shooting: <35% FG% = needs improvement, <25% 3P% = three-point accuracy needs work
- Rebounding: <3 RPG = needs improvement
- Playmaking: <2 APG = needs improvement
"""

def get_coaching_guidelines() -> str:
    """Get coaching guidelines for OpenAI"""
    return """
COACHING GUIDELINES:

1. Always leverage player strengths while addressing weaknesses
2. Provide specific, actionable drills from the drill library
3. Use basketball terminology appropriately
4. Be encouraging and practical
5. Focus on measurable improvement goals
6. Consider game strategy based on playing style
7. For team questions: analyze team strengths/weaknesses vs league averages
8. For leaderboard questions: provide top performers with definitions
9. Always include stat definitions when showing leaderboards
10. For team scouting: identify offensive strengths, defensive strengths, and areas for improvement
"""

def get_full_knowledge_base() -> str:
    """Get complete knowledge base for OpenAI system prompt"""
    return f"""
{get_drill_library_summary()}

{get_stat_definitions()}

{get_coaching_guidelines()}
"""
