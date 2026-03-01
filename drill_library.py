"""
Basketball Drill Library
Comprehensive collection of specific drills for player development
"""

from typing import Dict, List, Optional

class DrillLibrary:
    """
    Library of basketball drills organized by skill category
    """
    
    def __init__(self):
        self.drills = self._initialize_drills()
    
    def _initialize_drills(self) -> Dict[str, List[Dict[str, str]]]:
        """Initialize drill database"""
        return {
            "dribbling": [
                {
                    "name": "Right Hand Dribbling",
                    "difficulty": "Beginner",
                    "duration": "10-15 minutes",
                    "description": "Practice dribbling with only your right hand",
                    "instructions": [
                        "Stand in place, dribble 50 times with right hand",
                        "Walk while dribbling with right hand (down and back court)",
                        "Jog while dribbling with right hand",
                        "Sprint while maintaining control with right hand",
                        "Focus: Keep ball low, use fingertips, eyes up"
                    ],
                    "key_points": "Control the ball at waist level, use your fingertips not palm, keep your eyes up"
                },
                {
                    "name": "Left Hand Dribbling",
                    "difficulty": "Beginner",
                    "duration": "10-15 minutes",
                    "description": "Practice dribbling with only your left hand",
                    "instructions": [
                        "Stand in place, dribble 50 times with left hand",
                        "Walk while dribbling with left hand (down and back court)",
                        "Jog while dribbling with left hand",
                        "Sprint while maintaining control with left hand",
                        "Focus: Build muscle memory in non-dominant hand"
                    ],
                    "key_points": "Same technique as right hand, build coordination in weak hand"
                },
                {
                    "name": "Two-Ball Dribbling",
                    "difficulty": "Intermediate",
                    "duration": "10 minutes",
                    "description": "Dribble two basketballs simultaneously",
                    "instructions": [
                        "Start standing still, dribble both balls at same time",
                        "Progress to walking with both balls",
                        "Try alternating dribbles (one high, one low)",
                        "Practice crossovers with both balls",
                        "Focus: Independent hand control"
                    ],
                    "key_points": "Develops hand-eye coordination and ambidexterity"
                },
                {
                    "name": "Crossover Dribble Drill",
                    "difficulty": "Intermediate",
                    "duration": "10 minutes",
                    "description": "Practice crossing the ball between hands",
                    "instructions": [
                        "Dribble right hand, crossover to left (10 reps)",
                        "Dribble left hand, crossover to right (10 reps)",
                        "Figure-8 pattern between legs (20 reps)",
                        "Crossover while moving forward",
                        "Focus: Quick, low crossovers"
                    ],
                    "key_points": "Ball should be below knee, protect with body"
                },
                {
                    "name": "Between the Legs Dribble",
                    "difficulty": "Intermediate",
                    "duration": "10 minutes",
                    "description": "Practice dribbling between your legs",
                    "instructions": [
                        "Stand with legs shoulder-width apart",
                        "Dribble ball between legs from front to back (10 reps each direction)",
                        "Walk forward while dribbling between legs",
                        "Combine with crossover dribbles",
                        "Focus: Control and speed"
                    ],
                    "key_points": "Keep ball low, use fingertips, protect ball"
                },
                {
                    "name": "Behind the Back Dribble",
                    "difficulty": "Advanced",
                    "duration": "10 minutes",
                    "description": "Master behind-the-back dribbling",
                    "instructions": [
                        "Practice stationary behind-back dribbles (10 reps each hand)",
                        "Walk while doing behind-back dribbles",
                        "Combine with crossovers and between-legs",
                        "Use in game-like situations",
                        "Focus: Smooth, controlled motion"
                    ],
                    "key_points": "Advanced move for ball protection, practice slowly first"
                }
            ],
            "shooting": [
                {
                    "name": "Form Shooting",
                    "difficulty": "Beginner",
                    "duration": "15-20 minutes",
                    "description": "Perfect shooting form close to basket",
                    "instructions": [
                        "Stand 3 feet from basket",
                        "Shoot 25 shots focusing on form (BEEF: Balance, Eyes, Elbow, Follow-through)",
                        "Move to 5 feet, shoot 25 more",
                        "Move to 10 feet, shoot 25 more",
                        "Focus: Consistent shooting motion every time"
                    ],
                    "key_points": "BEEF principle: Balance, Eyes on target, Elbow in, Follow-through"
                },
                {
                    "name": "Catch and Shoot",
                    "difficulty": "Intermediate",
                    "duration": "15 minutes",
                    "description": "Practice shooting off the catch",
                    "instructions": [
                        "Partner passes you the ball from various spots",
                        "Catch and shoot immediately (20 shots from each spot)",
                        "Practice from three-point line",
                        "Add game-like movement: curl, fade, etc.",
                        "Focus: Quick release, square to basket"
                    ],
                    "key_points": "Catch in shooting position, quick release, follow through"
                },
                {
                    "name": "Pull-Up Jump Shot",
                    "difficulty": "Intermediate",
                    "duration": "15 minutes",
                    "description": "Shoot while moving and pulling up",
                    "instructions": [
                        "Dribble towards basket, pull up at free throw line (10 reps)",
                        "Pull up from different distances",
                        "Practice from both sides of court",
                        "Add hesitation moves before pull-up",
                        "Focus: Balance and elevation on jump"
                    ],
                    "key_points": "Stop on balance, elevate straight up, follow through"
                },
                {
                    "name": "Three-Point Shooting",
                    "difficulty": "Intermediate",
                    "duration": "20 minutes",
                    "description": "Improve three-point accuracy",
                    "instructions": [
                        "Shoot 25 shots from 5 spots around three-point line",
                        "Practice catch-and-shoot threes",
                        "Practice shooting off the dribble",
                        "Game situation: shoot with defender closing out",
                        "Focus: Consistent arc and follow-through"
                    ],
                    "key_points": "Generate power from legs, consistent arc, follow-through"
                },
                {
                    "name": "Free Throw Practice",
                    "difficulty": "Beginner",
                    "duration": "10 minutes",
                    "description": "Master free throw shooting",
                    "instructions": [
                        "Develop consistent routine: dribble, breathe, shoot",
                        "Shoot 20 free throws, track percentage",
                        "Practice under pressure: make 10 in a row",
                        "Visualize game situations",
                        "Focus: Same routine every time"
                    ],
                    "key_points": "Routine is key, relax, follow through"
                }
            ],
            "passing": [
                {
                    "name": "Chest Pass Drill",
                    "difficulty": "Beginner",
                    "duration": "10 minutes",
                    "description": "Perfect chest passing technique",
                    "instructions": [
                        "Partner stands 10 feet away",
                        "Chest pass 50 times, focus on form",
                        "Move to 15 feet, chest pass 30 times",
                        "Pass with defender closing out",
                        "Focus: Two hands, snap through, follow through"
                    ],
                    "key_points": "Two hands on ball, thumbs down on release, step into pass"
                },
                {
                    "name": "Bounce Pass Drill",
                    "difficulty": "Beginner",
                    "duration": "10 minutes",
                    "description": "Master the bounce pass",
                    "instructions": [
                        "Bounce pass to partner (50 reps)",
                        "Practice from different distances",
                        "Bounce point should be 2/3 distance to target",
                        "Use in game situations (passing around defender)",
                        "Focus: Right bounce point, proper angle"
                    ],
                    "key_points": "Bounce point is key - not too close, not too far"
                },
                {
                    "name": "Outlet Pass Drill",
                    "difficulty": "Intermediate",
                    "duration": "10 minutes",
                    "description": "Practice rebounding and outlet passing",
                    "instructions": [
                        "Grab rebound, pivot, outlet pass to teammate",
                        "Practice from both sides",
                        "Add pressure (defender closing out)",
                        "Focus on speed and accuracy",
                        "Repeat 30 times"
                    ],
                    "key_points": "Pivot quickly, pass to numbers on fast break"
                },
                {
                    "name": "Skip Pass Drill",
                    "difficulty": "Advanced",
                    "duration": "10 minutes",
                    "description": "Pass across court to open teammate",
                    "instructions": [
                        "Partner on opposite side of court",
                        "Practice skip passing over defense",
                        "Add game-like situations",
                        "Focus on accuracy and timing",
                        "20 reps each side"
                    ],
                    "key_points": "High arc to clear defense, lead your teammate"
                }
            ],
            "rebounding": [
                {
                    "name": "Box Out Drill",
                    "difficulty": "Intermediate",
                    "duration": "10 minutes",
                    "description": "Master the box out technique",
                    "instructions": [
                        "Partner shoots, you box out",
                        "Maintain contact, find ball",
                        "Practice from different angles",
                        "Focus: Butt to opponent, arms wide",
                        "Repeat 20 times"
                    ],
                    "key_points": "Butt to opponent, wide base, find the ball"
                },
                {
                    "name": "Reaction Rebound Drill",
                    "difficulty": "Intermediate",
                    "duration": "10 minutes",
                    "description": "Improve rebounding reaction time",
                    "instructions": [
                        "Coach shoots from various spots",
                        "Sprint to rebound (offensive and defensive)",
                        "Practice securing ball with two hands",
                        "Add outlet pass after rebound",
                        "Focus: Read trajectory, pursue aggressively"
                    ],
                    "key_points": "Read the shot, anticipate where ball will go, secure with two hands"
                },
                {
                    "name": "Tip Drill",
                    "difficulty": "Advanced",
                    "duration": "10 minutes",
                    "description": "Practice tipping rebounds",
                    "instructions": [
                        "Partner shoots, you tip ball to yourself",
                        "Practice tipping to teammate",
                        "Work on timing and elevation",
                        "Focus: Quick hands, multiple tips",
                        "20 reps"
                    ],
                    "key_points": "Quick hands, jump with purpose, control tips"
                }
            ],
            "defense": [
                {
                    "name": "Defensive Slide Drill",
                    "difficulty": "Beginner",
                    "duration": "10 minutes",
                    "description": "Improve lateral movement and defensive stance",
                    "instructions": [
                        "Start in defensive stance (knees bent, weight on balls of feet)",
                        "Slide right 10 steps, slide left 10 steps",
                        "Keep body low, don't cross feet",
                        "Add drop step on direction changes",
                        "Focus: Stay low, maintain stance"
                    ],
                    "key_points": "Low stance, wide base, slide don't cross, stay on balls of feet"
                },
                {
                    "name": "Close-Out Drill",
                    "difficulty": "Intermediate",
                    "duration": "10 minutes",
                    "description": "Practice closing out on shooters",
                    "instructions": [
                        "Start under basket, coach/partner at three-point line",
                        "Sprint to close out, stop in defensive stance",
                        "Contest shot with high hand",
                        "Practice closing out from different angles",
                        "Focus: Quick close, controlled stop"
                    ],
                    "key_points": "Sprint to 3 feet, then close out under control, high hand contest"
                },
                {
                    "name": "One-on-One Defense",
                    "difficulty": "Intermediate",
                    "duration": "15 minutes",
                    "description": "Defend live offensive player",
                    "instructions": [
                        "Defend offensive player for 10 seconds",
                        "Prevent drive, contest shot",
                        "Focus on staying in front",
                        "Practice different positions (guard, wing, post)",
                        "Focus: Anticipate, react, stay balanced"
                    ],
                    "key_points": "Stay in stance, keep ball in front, move feet not hands"
                }
            ],
            "footwork": [
                {
                    "name": "Pivot Drill",
                    "difficulty": "Beginner",
                    "duration": "10 minutes",
                    "description": "Master pivoting on both feet",
                    "instructions": [
                        "Hold ball, pivot on right foot (forward pivot 10x, reverse 10x)",
                        "Pivot on left foot (forward 10x, reverse 10x)",
                        "Add chair to pivot around",
                        "Practice with defender",
                        "Focus: Keep pivot foot down, protect ball"
                    ],
                    "key_points": "Keep pivot foot planted, pivot on ball of foot, protect ball"
                },
                {
                    "name": "Triple Threat Position",
                    "difficulty": "Beginner",
                    "duration": "10 minutes",
                    "description": "Practice triple threat stance",
                    "instructions": [
                        "Catch ball, get into triple threat (shot, pass, dribble)",
                        "Practice jab steps from triple threat",
                        "Pivot from triple threat",
                        "Focus on balance and readiness",
                        "50 reps"
                    ],
                    "key_points": "Knees bent, ball at shooting pocket, ready to act"
                }
            ],
            "conditioning": [
                {
                    "name": "Suicide Runs",
                    "difficulty": "Intermediate",
                    "duration": "10 minutes",
                    "description": "Build speed and endurance",
                    "instructions": [
                        "Run to free throw line and back",
                        "Run to half court and back",
                        "Run to opposite free throw and back",
                        "Run full court and back",
                        "Rest 2 minutes, repeat 3 times"
                    ],
                    "key_points": "Maintain form, touch each line, push through fatigue"
                },
                {
                    "name": "Defensive Slide Conditioning",
                    "difficulty": "Intermediate",
                    "duration": "10 minutes",
                    "description": "Combine defense and conditioning",
                    "instructions": [
                        "Defensive slide full court width 5 times",
                        "Sprint back, repeat",
                        "Maintain defensive stance throughout",
                        "Focus: Don't sacrifice form for speed",
                        "Rest 1 minute between sets (3 sets)"
                    ],
                    "key_points": "Stay low, maintain form, build game-like endurance"
                }
            ]
        }
    
    def get_drills_for_category(self, category: str) -> List[Dict[str, str]]:
        """Get all drills for a specific category"""
        return self.drills.get(category.lower(), [])
    
    def get_drill_by_name(self, name: str) -> Optional[Dict[str, str]]:
        """Find a specific drill by name"""
        for category_drills in self.drills.values():
            for drill in category_drills:
                if drill["name"].lower() == name.lower():
                    return drill
        return None
    
    def get_drills_for_weakness(self, weakness: str) -> List[Dict[str, str]]:
        """Get recommended drills based on identified weakness"""
        weakness_lower = weakness.lower()
        recommended = []
        
        # Map weaknesses to drill categories
        if "dribble" in weakness_lower or "turnover" in weakness_lower or "ball control" in weakness_lower:
            recommended.extend(self.get_drills_for_category("dribbling"))
        
        if "shoot" in weakness_lower or "percentage" in weakness_lower:
            recommended.extend(self.get_drills_for_category("shooting"))
        
        if "rebound" in weakness_lower:
            recommended.extend(self.get_drills_for_category("rebounding"))
        
        if "pass" in weakness_lower or "playmaking" in weakness_lower or "assist" in weakness_lower:
            recommended.extend(self.get_drills_for_category("passing"))
        
        if "defense" in weakness_lower:
            recommended.extend(self.get_drills_for_category("defense"))
        
        return recommended
    
    def format_drill(self, drill: Dict[str, str]) -> str:
        """Format a drill for display"""
        lines = [
            f"### {drill['name']}",
            f"**Difficulty:** {drill['difficulty']} | **Duration:** {drill['duration']}",
            "",
            f"**Description:** {drill['description']}",
            "",
            "**Instructions:**"
        ]
        
        for i, instruction in enumerate(drill['instructions'], 1):
            lines.append(f"{i}. {instruction}")
        
        lines.append("")
        lines.append(f"**Key Points:** {drill['key_points']}")
        
        return "\n".join(lines)

# Global instance
drill_library = DrillLibrary()
