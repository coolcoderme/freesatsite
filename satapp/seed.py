"""Original demo and practice questions. Not official College Board or ACT items."""

QUESTIONS = [
    {
        "id": "demo-01",
        "exam": "SAT",
        "section": "Reading and Writing",
        "topic": "Craft and Structure",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": True,
        "stimulus": (
            "For decades, city planners treated vacant lots as leftover space. "
            "A newer approach treats them as a kind of civic infrastructure: "
            "places that can cool neighborhoods, store stormwater, and give "
            "residents a reason to linger outdoors. The shift is less about "
            "decorating empty land than about asking what a city needs from "
            "the ground it already owns."
        ),
        "question": "As used in the passage, “infrastructure” most nearly means",
        "choices": {
            "A": "ornamental landscaping used to hide unused property",
            "B": "a system of public assets that perform useful work",
            "C": "private real estate reserved for future construction",
            "D": "a temporary exhibit meant to attract tourists",
        },
        "answer": "B",
        "explanation": (
            "The passage defines vacant lots as assets that cool streets, "
            "manage water, and serve residents. That public-utility sense "
            "matches “a system of public assets that perform useful work.”"
        ),
    },
    {
        "id": "demo-02",
        "exam": "SAT",
        "section": "Reading and Writing",
        "topic": "Standard English Conventions",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": True,
        "stimulus": (
            "The archive’s earliest maps, drawn on fragile linen, ______ "
            "now stored in climate-controlled drawers."
        ),
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "choices": {
            "A": "is",
            "B": "has been",
            "C": "are",
            "D": "was",
        },
        "answer": "C",
        "explanation": (
            "The subject is “maps,” a plural noun, so the verb must be "
            "plural: “are now stored.”"
        ),
    },
    {
        "id": "demo-03",
        "exam": "SAT",
        "section": "Math",
        "topic": "Algebra",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": True,
        "stimulus": None,
        "question": (
            "A tutoring center charges a one-time registration fee of $25 "
            "plus $18 per hour of tutoring. If a family paid $133 in total, "
            "how many hours of tutoring did they purchase?"
        ),
        "choices": {"A": "4", "B": "5", "C": "6", "D": "7"},
        "answer": "C",
        "explanation": (
            "Solve 25 + 18h = 133. Then 18h = 108, so h = 6."
        ),
    },
    {
        "id": "demo-04",
        "exam": "SAT",
        "section": "Math",
        "topic": "Problem-Solving and Data Analysis",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": True,
        "stimulus": (
            "A school surveyed 200 students about weekend study time. "
            "45% studied less than 2 hours, 30% studied 2 to 4 hours, "
            "and the rest studied more than 4 hours."
        ),
        "question": "How many students studied more than 4 hours?",
        "choices": {"A": "40", "B": "50", "C": "55", "D": "60"},
        "answer": "B",
        "explanation": (
            "45% + 30% = 75%, so 25% studied more than 4 hours. "
            "0.25 × 200 = 50."
        ),
    },
    {
        "id": "demo-05",
        "exam": "PSAT",
        "section": "Reading and Writing",
        "topic": "Information and Ideas",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": True,
        "stimulus": (
            "Honeybees are famous for dancing, but the “waggle dance” is "
            "not a celebration. A worker returning from a good patch of "
            "flowers walks a figure-eight on the comb. The angle of her "
            "waggle run, relative to vertical, tells other bees the "
            "direction of the flowers compared with the sun. The length "
            "of the run reports the distance."
        ),
        "question": "The passage is primarily concerned with",
        "choices": {
            "A": "explaining how one bee signal conveys useful information",
            "B": "arguing that honeybees enjoy dancing more than working",
            "C": "comparing honeybees with other insects that use the sun",
            "D": "warning beekeepers about a decline in flower patches",
        },
        "answer": "A",
        "explanation": (
            "The passage explains what the waggle dance communicates: "
            "direction and distance. That is the main purpose."
        ),
    },
    {
        "id": "demo-06",
        "exam": "PSAT",
        "section": "Math",
        "topic": "Problem-Solving and Data Analysis",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": True,
        "stimulus": None,
        "question": (
            "A recipe uses 3 cups of flour for every 2 cups of milk. "
            "If a baker uses 12 cups of flour, how many cups of milk "
            "are needed to keep the same ratio?"
        ),
        "choices": {"A": "6", "B": "8", "C": "9", "D": "18"},
        "answer": "B",
        "explanation": "3/2 = 12/m, so 3m = 24 and m = 8.",
    },
    {
        "id": "demo-07",
        "exam": "ACT",
        "section": "English",
        "topic": "Punctuation",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": True,
        "stimulus": (
            "The chemist labeled each vial carefully, she knew that a "
            "single mix-up could ruin the trial."
        ),
        "question": "Which is the best version of the underlined sentence?",
        "choices": {
            "A": "NO CHANGE",
            "B": "The chemist labeled each vial carefully she knew that a single mix-up could ruin the trial.",
            "C": "The chemist labeled each vial carefully; she knew that a single mix-up could ruin the trial.",
            "D": "The chemist labeled each vial carefully: and she knew that a single mix-up could ruin the trial.",
        },
        "answer": "C",
        "explanation": (
            "The original is a comma splice. A semicolon correctly joins "
            "two independent clauses. B is a run-on, and D misuses a colon."
        ),
    },
    {
        "id": "demo-08",
        "exam": "ACT",
        "section": "Math",
        "topic": "Geometry",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": True,
        "stimulus": None,
        "question": (
            "A right triangle has legs of length 5 and 12. What is the "
            "length of the hypotenuse?"
        ),
        "choices": {"A": "13", "B": "15", "C": "17", "D": "60"},
        "answer": "A",
        "explanation": "5² + 12² = 25 + 144 = 169 = 13², so the hypotenuse is 13.",
    },
    {
        "id": "demo-09",
        "exam": "ACT",
        "section": "Reading",
        "topic": "Humanities",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": True,
        "stimulus": (
            "When the mural was first unveiled, critics called it unfinished. "
            "The painter had left wide fields of plaster uncolored, and the "
            "faces of the factory workers were only sketched. Years later, "
            "those same gaps are what people stand in front of longest. "
            "The empty plaster reads as heat, dust, and the hours that never "
            "made it into the official history of the mill."
        ),
        "question": "The narrator suggests that the mural’s unfinished areas now",
        "choices": {
            "A": "prove that the painter lacked formal training",
            "B": "distract viewers from the factory workers’ faces",
            "C": "help viewers sense the mill’s overlooked labor and atmosphere",
            "D": "were added later to satisfy the original critics",
        },
        "answer": "C",
        "explanation": (
            "The last sentences say the gaps now read as heat, dust, and "
            "hours left out of official history. Viewers linger there."
        ),
    },
    {
        "id": "demo-10",
        "exam": "ACT",
        "section": "Science",
        "topic": "Data Representation",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": True,
        "stimulus": (
            "Table 1. Average germination rate of bean seeds after 7 days\n"
            "Soil mix | Light | Dark\n"
            "Sand     | 18%   | 12%\n"
            "Compost  | 64%   | 41%\n"
            "Garden   | 51%   | 33%"
        ),
        "question": "According to the table, which condition produced the highest germination rate?",
        "choices": {
            "A": "Sand in the light",
            "B": "Compost in the light",
            "C": "Garden in the dark",
            "D": "Compost in the dark",
        },
        "answer": "B",
        "explanation": "Compost in the light is 64%, the largest value in the table.",
    },
    {
        "id": "sat-rw-03",
        "exam": "SAT",
        "section": "Reading and Writing",
        "topic": "Expression of Ideas",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "Many small libraries now lend tools, seeds, and musical "
            "instruments. ______ they still buy books; they have simply "
            "decided that a public collection can include more than paper."
        ),
        "question": "Which transition best completes the text?",
        "choices": {
            "A": "Nevertheless,",
            "B": "Specifically,",
            "C": "For example,",
            "D": "In conclusion,",
        },
        "answer": "A",
        "explanation": (
            "The second sentence contrasts with the first: libraries added "
            "new loans but still buy books. “Nevertheless” marks that contrast."
        ),
    },
    {
        "id": "sat-rw-04",
        "exam": "SAT",
        "section": "Reading and Writing",
        "topic": "Standard English Conventions",
        "difficulty": "Hard",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "The committee praised the intern who had organized the files, "
            "rewritten the guide, and ______ the volunteers."
        ),
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "choices": {
            "A": "she trained",
            "B": "training",
            "C": "trained",
            "D": "to train",
        },
        "answer": "C",
        "explanation": (
            "The list needs parallel past participles: organized, rewritten, "
            "and trained."
        ),
    },
    {
        "id": "sat-rw-05",
        "exam": "SAT",
        "section": "Reading and Writing",
        "topic": "Information and Ideas",
        "difficulty": "Hard",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "Study A found that students who took handwritten notes scored "
            "higher on conceptual questions than students who typed. Study B, "
            "using the same lectures but a shorter delay before the test, "
            "found no significant difference. Both studies used the same "
            "note-taking instructions."
        ),
        "question": "Which finding, if true, would most help explain the difference between the two studies?",
        "choices": {
            "A": "Handwriting is slower than typing for most students.",
            "B": "The advantage of handwriting appears mainly after students have had time to forget surface details.",
            "C": "Both groups of students were allowed to review their notes.",
            "D": "The lectures included diagrams as well as spoken explanations.",
        },
        "answer": "B",
        "explanation": (
            "Study B used a shorter delay and saw no difference. If the "
            "handwriting benefit shows up after forgetting, that would "
            "explain why only Study A found an effect."
        ),
    },
    {
        "id": "sat-ma-03",
        "exam": "SAT",
        "section": "Math",
        "topic": "Advanced Math",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": None,
        "question": (
            "The function f is defined by f(x) = x² − 6x + 5. What is the "
            "minimum value of f(x)?"
        ),
        "choices": {"A": "−4", "B": "−1", "C": "5", "D": "8"},
        "answer": "A",
        "explanation": (
            "Vertex at x = −b/(2a) = 6/2 = 3. f(3) = 9 − 18 + 5 = −4."
        ),
    },
    {
        "id": "sat-ma-04",
        "exam": "SAT",
        "section": "Math",
        "topic": "Algebra",
        "difficulty": "Medium",
        "type": "grid_in",
        "is_demo": False,
        "stimulus": None,
        "question": (
            "A line passes through (0, 4) and (6, 13). What is the y-value "
            "when x = 2?"
        ),
        "choices": None,
        "answer": "7",
        "explanation": (
            "Slope = (13 − 4)/6 = 9/6 = 3/2. So y = 4 + (3/2)x. "
            "When x = 2, y = 4 + 3 = 7."
        ),
    },
    {
        "id": "sat-ma-05",
        "exam": "SAT",
        "section": "Math",
        "topic": "Geometry and Trigonometry",
        "difficulty": "Hard",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": None,
        "question": (
            "A circle has equation (x − 3)² + (y + 1)² = 25. Which point "
            "lies on the circle?"
        ),
        "choices": {
            "A": "(3, 4)",
            "B": "(8, −1)",
            "C": "(0, 0)",
            "D": "(3, −7)",
        },
        "answer": "B",
        "explanation": (
            "Center (3, −1), radius 5. Distance from center to (8, −1) is 5, "
            "so that point is on the circle."
        ),
    },
    {
        "id": "sat-ma-06",
        "exam": "SAT",
        "section": "Math",
        "topic": "Problem-Solving and Data Analysis",
        "difficulty": "Hard",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "A store discounts a jacket by 20%, then adds 8% sales tax to "
            "the discounted price. The original price is $80."
        ),
        "question": "What is the final price, to the nearest dollar?",
        "choices": {"A": "$64", "B": "$69", "C": "$70", "D": "$86"},
        "answer": "B",
        "explanation": "Discounted price is 0.8 × 80 = 64. Tax: 64 × 1.08 = 69.12 ≈ $69.",
    },
    {
        "id": "psat-rw-02",
        "exam": "PSAT",
        "section": "Reading and Writing",
        "topic": "Standard English Conventions",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "After the storm, the ranger closed the trail ______ fallen "
            "branches blocked the only safe path."
        ),
        "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "choices": {
            "A": "because",
            "B": "because of",
            "C": "although",
            "D": "and because",
        },
        "answer": "A",
        "explanation": (
            "“Because” correctly introduces a full clause that explains why "
            "the trail was closed."
        ),
    },
    {
        "id": "psat-rw-03",
        "exam": "PSAT",
        "section": "Reading and Writing",
        "topic": "Craft and Structure",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "The review does not say the novel is bad. It says the novel is "
            "crowded: too many subplots tug at the same sleeve, and none of "
            "them is allowed to finish a sentence."
        ),
        "question": "The reviewer’s tone is best described as",
        "choices": {
            "A": "amused and admiring",
            "B": "neutral and statistical",
            "C": "critical but precise",
            "D": "angry and personal",
        },
        "answer": "C",
        "explanation": (
            "The reviewer names a specific flaw—overcrowding—without insults "
            "or praise. That is precise criticism."
        ),
    },
    {
        "id": "psat-ma-02",
        "exam": "PSAT",
        "section": "Math",
        "topic": "Algebra",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": None,
        "question": "If 4x − 7 = 21, what is the value of x?",
        "choices": {"A": "3.5", "B": "7", "C": "14", "D": "28"},
        "answer": "B",
        "explanation": "4x = 28, so x = 7.",
    },
    {
        "id": "psat-ma-03",
        "exam": "PSAT",
        "section": "Math",
        "topic": "Geometry and Trigonometry",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": None,
        "question": (
            "A rectangular garden is 12 feet long and 5 feet wide. What is "
            "the length of a diagonal path from one corner to the opposite corner?"
        ),
        "choices": {"A": "7", "B": "13", "C": "17", "D": "60"},
        "answer": "B",
        "explanation": "12² + 5² = 144 + 25 = 169 = 13².",
    },
    {
        "id": "psat-ma-04",
        "exam": "PSAT",
        "section": "Math",
        "topic": "Advanced Math",
        "difficulty": "Medium",
        "type": "grid_in",
        "is_demo": False,
        "stimulus": None,
        "question": (
            "A population of bacteria doubles every 3 hours. If there are "
            "40 bacteria at 8:00 a.m., how many are there at 2:00 p.m. the "
            "same day?"
        ),
        "choices": None,
        "answer": "160",
        "explanation": (
            "From 8:00 to 2:00 is 6 hours, so the population doubles twice: "
            "40 → 80 → 160."
        ),
    },
    {
        "id": "act-en-02",
        "exam": "ACT",
        "section": "English",
        "topic": "Grammar and Usage",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "Neither the drummer nor the guitarists ______ willing to skip sound check."
        ),
        "question": "Which choice best completes the sentence?",
        "choices": {
            "A": "is",
            "B": "are",
            "C": "was",
            "D": "has been",
        },
        "answer": "B",
        "explanation": (
            "With “neither…nor,” the verb agrees with the nearer subject. "
            "“Guitarists” is plural, so “are” is correct."
        ),
    },
    {
        "id": "act-en-03",
        "exam": "ACT",
        "section": "English",
        "topic": "Rhetoric",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "I woke up. I ate toast. I missed the bus. I ran to school anyway."
        ),
        "question": "Which revision most improves the flow without changing the meaning?",
        "choices": {
            "A": "I woke up and ate toast, missed the bus, but ran to school anyway.",
            "B": "Waking up, toast was eaten, the bus was missed, and school was run to.",
            "C": "I woke up; toast; bus; school.",
            "D": "NO CHANGE",
        },
        "answer": "A",
        "explanation": (
            "A combines the choppy sentences into one clear sequence. B is "
            "dangling and passive; C is incomplete."
        ),
    },
    {
        "id": "act-ma-02",
        "exam": "ACT",
        "section": "Math",
        "topic": "Algebra",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": None,
        "question": (
            "If 2(x + 4) = 3x − 5, what is the value of x?"
        ),
        "choices": {"A": "3", "B": "8", "C": "13", "D": "−3"},
        "answer": "C",
        "explanation": "2x + 8 = 3x − 5, so 8 + 5 = 3x − 2x, and x = 13.",
    },
    {
        "id": "act-ma-03",
        "exam": "ACT",
        "section": "Math",
        "topic": "Pre-Algebra",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": None,
        "question": (
            "A bag contains 4 red marbles, 3 blue marbles, and 5 green marbles. "
            "One marble is drawn at random. What is the probability it is blue?"
        ),
        "choices": {"A": "1/4", "B": "1/3", "C": "3/12", "D": "3/4"},
        "answer": "A",
        "explanation": "There are 12 marbles and 3 blue, so 3/12 = 1/4.",
    },
    {
        "id": "act-ma-04",
        "exam": "ACT",
        "section": "Math",
        "topic": "Trigonometry",
        "difficulty": "Hard",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": None,
        "question": (
            "In a right triangle, sin θ = 5/13. What is cos θ if θ is acute?"
        ),
        "choices": {"A": "5/12", "B": "12/13", "C": "13/12", "D": "12/5"},
        "answer": "B",
        "explanation": (
            "Opposite 5, hypotenuse 13, so adjacent is 12 (5-12-13 triangle). "
            "cos θ = 12/13."
        ),
    },
    {
        "id": "act-re-02",
        "exam": "ACT",
        "section": "Reading",
        "topic": "Natural Science",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "Permafrost is ground that stays frozen for at least two years. "
            "When it thaws, microbes wake up and digest old plant matter, "
            "releasing carbon dioxide and methane. Those gases trap heat, "
            "which can thaw still more permafrost. Researchers argue that "
            "this loop is not a distant risk; it is already visible in "
            "slumping hillsides and sudden lakes across the Arctic."
        ),
        "question": "The researchers mentioned in the passage would most likely agree that",
        "choices": {
            "A": "permafrost thaw is mainly a problem for future centuries",
            "B": "microbes in frozen soil are inactive forever",
            "C": "signs of the thaw-and-gas cycle can already be observed",
            "D": "methane is unrelated to trapped heat",
        },
        "answer": "C",
        "explanation": (
            "They say the loop is not distant and is already visible in "
            "slumping hillsides and sudden lakes."
        ),
    },
    {
        "id": "act-sc-02",
        "exam": "ACT",
        "section": "Science",
        "topic": "Research Summaries",
        "difficulty": "Medium",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "Experiment. Students grew identical basil plants under three "
            "conditions for 14 days.\n"
            "Group 1: 6 hours of light daily, 20 mL water\n"
            "Group 2: 12 hours of light daily, 20 mL water\n"
            "Group 3: 12 hours of light daily, 40 mL water\n"
            "Average height: Group 1 = 6.2 cm, Group 2 = 9.8 cm, Group 3 = 9.5 cm."
        ),
        "question": "Which conclusion is best supported by the results?",
        "choices": {
            "A": "Extra water was more important than extra light.",
            "B": "Increasing light from 6 to 12 hours raised height more than doubling the water.",
            "C": "Group 3 plants were unhealthy.",
            "D": "Basil cannot grow with only 6 hours of light.",
        },
        "answer": "B",
        "explanation": (
            "Groups 1 and 2 differ only in light, and height jumped from "
            "6.2 to 9.8 cm. Groups 2 and 3 differ only in water, and height "
            "was nearly the same."
        ),
    },
    {
        "id": "act-sc-03",
        "exam": "ACT",
        "section": "Science",
        "topic": "Conflicting Viewpoints",
        "difficulty": "Hard",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "Scientist 1: The crater lake is mostly rainwater. The water’s "
            "mineral profile matches nearby rain gauges, and the lake level "
            "rises within hours of storms.\n"
            "Scientist 2: The lake is fed by an underground spring. Temperature "
            "stays nearly constant year-round, which is typical of deep "
            "groundwater, not of rain-fed ponds."
        ),
        "question": "Which observation would most weaken Scientist 1’s explanation?",
        "choices": {
            "A": "A nearby rain gauge overflowed last June.",
            "B": "The lake is popular with hikers after storms.",
            "C": "During a two-week drought, the lake level kept rising.",
            "D": "Rainwater can contain dissolved minerals.",
        },
        "answer": "C",
        "explanation": (
            "If the lake rises with no rain, rainwater cannot be the main "
            "source. That undercuts Scientist 1."
        ),
    },
    {
        "id": "sat-rw-06",
        "exam": "SAT",
        "section": "Reading and Writing",
        "topic": "Craft and Structure",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "The biologist’s prose is deliberately plain. She refuses "
            "metaphor the way a lab refuses perfume: extra scent would "
            "only hide the thing she wants you to notice."
        ),
        "question": "The comparison to a lab most nearly emphasizes the writer’s",
        "choices": {
            "A": "preference for decorative language",
            "B": "belief that style should not obscure evidence",
            "C": "distrust of scientific laboratories",
            "D": "interest in perfume chemistry",
        },
        "answer": "B",
        "explanation": (
            "Plain prose, like an unscented lab, keeps attention on the "
            "actual subject rather than on extra fragrance."
        ),
    },
    {
        "id": "sat-ma-07",
        "exam": "SAT",
        "section": "Math",
        "topic": "Advanced Math",
        "difficulty": "Hard",
        "type": "grid_in",
        "is_demo": False,
        "stimulus": None,
        "question": (
            "The system below has exactly one solution (x, y).\n"
            "  y = 2x + 1\n"
            "  y = x² − 3x + k\n"
            "If x = 4 is the x-coordinate of that solution, what is k?"
        ),
        "choices": None,
        "answer": "5",
        "explanation": (
            "At x = 4, 2(4)+1 = 9 and 16 − 12 + k = 9, so 4 + k = 9 and k = 5. "
            "The graphs then touch at one point for this value."
        ),
    },
    {
        "id": "psat-rw-04",
        "exam": "PSAT",
        "section": "Reading and Writing",
        "topic": "Expression of Ideas",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "The museum’s night hours were a success. Attendance rose, "
            "gift-shop sales rose, and security overtime also rose. The "
            "director wants one sentence that keeps the first two gains "
            "and treats overtime as a cost."
        ),
        "question": "Which sentence best does what the director wants?",
        "choices": {
            "A": "Attendance, sales, and overtime all rose, which was perfect.",
            "B": "Attendance and sales rose, although security overtime increased as well.",
            "C": "Overtime rose, so attendance and sales must have fallen.",
            "D": "The museum should stay closed at night.",
        },
        "answer": "B",
        "explanation": (
            "B reports the two gains and uses “although” to mark overtime "
            "as a downside."
        ),
    },
    {
        "id": "act-re-03",
        "exam": "ACT",
        "section": "Reading",
        "topic": "Literary Narrative",
        "difficulty": "Easy",
        "type": "multiple_choice",
        "is_demo": False,
        "stimulus": (
            "Lina kept the concert ticket in a cookbook she never opened. "
            "Not because she meant to go—the date had passed—but because "
            "the ticket still smelled faintly of rain from the night she "
            "bought it, standing under the awning with her brother, both "
            "of them pretending they were the kind of people who always "
            "had plans."
        ),
        "question": "Lina keeps the ticket mainly because it",
        "choices": {
            "A": "will still admit her to the concert",
            "B": "reminds her of a shared moment with her brother",
            "C": "proves she is organized about future plans",
            "D": "belongs in a cookbook she uses every week",
        },
        "answer": "B",
        "explanation": (
            "The ticket’s value is memory: rain, the awning, and her "
            "brother. The concert date has already passed."
        ),
    },
]
