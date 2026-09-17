"""How Does It Know Where You Are? — Day 6 (The Global Positioning System).

Rendered by tools/build_quiz.py to docs/quizzes/gps/index.html. Everything here comes from
slides/day-06/gps-part-1.md; the extended deck (slides/day-07/gps-part-2.md) covers the same
ground one sphere at a time, so this works after either.
"""

SLUG = "gps"
TITLE = "How Does It Know Where You Are?"
DAY = 6
WEEK = 4
TOPIC = "The Global Positioning System"
DESCRIPTION = ("CCE 114 in-class self-check: how a receiver turns a coded time signal into a "
               "position, what the digits of a coordinate are worth, and where GPS error comes "
               "from.")

BLURB = """Twelve questions in three parts: how a receiver turns a radio signal into a
      <strong>position</strong>, what the digits of a <strong>coordinate</strong> are actually
      worth, and where the <strong>error</strong> comes from."""

CLOSING = """\
        <strong style="color: var(--text);">For Thursday:</strong><br>
        Record <strong>every digit</strong> your phone gives you &mdash; five decimals or more<br>
        Keep the <strong>minus sign</strong> on the longitude<br>
        Stand in the open, away from the building wall<br>
        <em>Degrees for storing and sharing; projected meters for measuring.</em>"""

MESSAGES = [
    "Every one. Now go collect points that deserve that.",
    "Solid. Read the explanations on the ones you missed — the coordinate questions are the ones that bite on Thursday.",
    "Worth a second run. The error you control is the last row of the budget, and it is the biggest.",
]

QUESTIONS = [
    dict(
        section="Part 1 — From a radio signal to a position",
        prompt="What is the difference between GPS and GNSS?",
        setup="",
        options=[
            "They are two names for the same American system",
            "GNSS is the family of satellite positioning systems; GPS is the United States one",
            "GPS is the satellites, GNSS is the receivers",
            "GNSS is the newer, more accurate replacement for GPS",
        ],
        correct=1,
        explanation="GNSS is Global Navigation Satellite System, the category. GPS is the U.S. "
                    "constellation, about 31 working satellites at 20,200 km. GLONASS is Russian, "
                    "Galileo European, BeiDou Chinese. Your phone listens to several at once, "
                    "which is why it locks on so quickly.",
    ),
    dict(
        section="Part 1 — From a radio signal to a position",
        prompt="Your receiver has no atomic clock. So how does it measure how long the signal took to arrive?",
        setup="",
        options=[
            "It reads a timestamp out of the message the satellite sends",
            "It measures the strength of the signal, which falls off with distance",
            "The satellite and the receiver generate the same code at the same time, and the receiver slides its own copy until the two line up",
            "It compares the signal against a second satellite and takes the difference",
        ],
        correct=2,
        explanation="This is the clever trick at the heart of GPS. How far the receiver had to "
                    "slide its copy is the travel time. It needs a code generator, not an atomic "
                    "clock — which is why the thing in your pocket costs what it costs.",
    ),
    dict(
        section="Part 1 — From a radio signal to a position",
        prompt="A satellite's code arrives 0.067 seconds after it was sent. How far away is the satellite?",
        setup="The speed of light is 299,792,458 m/s.",
        options=[
            "About 200 km",
            "About 2,000 km",
            "About 20,000 km",
            "About 200,000 km",
        ],
        correct=2,
        explanation="0.067 × 299,792,458 = 20,086,094 m, about 20,100 km, which is the real orbit "
                    "height. Notice how sharp that is: one microsecond of clock error is 300 m of "
                    "position error.",
    ),
    dict(
        section="Part 1 — From a radio signal to a position",
        prompt="Three satellites narrow your position to two points, one of them absurd. So why does a receiver need a fourth?",
        setup="",
        options=[
            "To rule out the absurd point",
            "To solve for the receiver's own clock error",
            "To improve the signal strength",
            "As a spare, in case one is blocked",
        ],
        correct=1,
        explanation="Four unknowns — latitude, longitude, height, and time — need four "
                    "measurements. The absurd point rules itself out; it is usually in space or "
                    "deep underground. Measuring distances like this is called trilateration; "
                    "triangulation, which people say instead, measures angles.",
    ),
    dict(
        section="Part 2 — What the digits are worth",
        prompt="You copy a phone fix into a spreadsheet as 40.25, -111.65. How far can that point have moved?",
        setup="",
        options=[
            "A few centimeters",
            "About 11 meters",
            "About 1.1 kilometers",
            "It has not moved; those are the same coordinates",
        ],
        correct=2,
        explanation="Two decimal places is about 1.1 km of latitude — it cannot resolve a city "
                    "block, never mind a building. Rounding is throwing away accuracy you already "
                    "paid for. A phone fix is good to a few meters, so it deserves five decimals "
                    "(about 1.1 m). Record every digit your phone gives you.",
    ),
    dict(
        section="Part 2 — What the digits are worth",
        prompt="You drop the minus sign from a Provo longitude and write 111.65 instead of -111.65. Where does your point land?",
        setup="",
        options=[
            "In the same place — the sign is a formatting convention",
            "On the other side of the world, at the same latitude",
            "At the equator",
            "It will not import at all",
        ],
        correct=1,
        explanation="Negative longitude is west, negative latitude is south. Dropping the minus "
                    "sign is the most common way to put Provo in China, and it imports perfectly "
                    "happily — nothing warns you, the dot is just in the wrong hemisphere.",
    ),
    dict(
        section="Part 2 — What the digits are worth",
        prompt="Your phone reports 40.2496612, -111.6493388 while sitting still on a desk. The desk is really 8 m away from that. Precise, accurate, both, or neither?",
        setup="",
        options=[
            "Precise and accurate",
            "Precise but not accurate",
            "Accurate but not precise",
            "Neither",
        ],
        correct=1,
        explanation="Seven decimal places is about a centimeter of precision; being 8 m from the "
                    "truth is poor accuracy. The receiver reports every digit it computed, not "
                    "the digits it can defend. The two words are not interchangeable and the "
                    "difference costs people money.",
    ),
    dict(
        section="Part 2 — What the digits are worth",
        prompt="Why can you not convert degrees to meters with a single multiplication?",
        setup="",
        options=[
            "Because the Earth is not a perfect sphere, so the number changes slightly",
            "Because a degree of longitude shrinks as you move away from the equator, down to zero at the pole",
            "Because latitude and longitude use different units",
            "You can — 111 km per degree works everywhere",
        ],
        correct=1,
        explanation="A degree of latitude is about 111 km anywhere. A degree of longitude is "
                    "111 km at the equator and nothing at all at the pole: at Provo, "
                    "111,320 × cos 40.25° ≈ 85 km. So never measure length or area in degrees — "
                    "project into meters first (UTM Zone 12N, EPSG:26912, for Utah), then measure. "
                    "QGIS will happily hand you a meaningless number in degrees if you ask it to.",
    ),
    dict(
        section="Part 3 — Where the error comes from",
        prompt="Which line of the GPS error budget is the biggest?",
        setup="",
        options=[
            "Satellite clocks and orbits, 1 to 4 m",
            "The ionosphere and troposphere, 5 to 8 m",
            "Multipath, 0.5 to 1 m",
            "User error, up to a kilometer or more",
        ],
        correct=3,
        explanation="The atmosphere is the largest instrument error, and user error dwarfs all of "
                    "it: wrong sign, wrong datum, wrong point, rounding. It is also the only row "
                    "on the table you control.",
    ),
    dict(
        section="Part 3 — Where the error comes from",
        prompt="You take your fix standing against the wall of the Clyde building. What has that done to your position?",
        setup="",
        options=[
            "Nothing — the wall blocks signals but does not distort them",
            "Signals bouncing off the building arrive late, so those satellites read as farther away than they are",
            "The building's mass bends the signal toward it",
            "It improves the fix, because the wall blocks noise from behind you",
        ],
        correct=1,
        explanation="That is multipath: a bounced signal took a longer path, so the range comes "
                    "out too long. Trees, urban canyons and deep valleys also cost you satellites "
                    "outright. On Thursday, the lawn will give you a better fix than the wall.",
    ),
    dict(
        section="Part 3 — Where the error comes from",
        prompt="Two fixes have the same range errors, but one was taken while the visible satellites were bunched in one part of the sky. Which is better, and what is the multiplier called?",
        setup="",
        options=[
            "The bunched one; PDOP, and higher is better",
            "The spread-out one; PDOP, and lower is better — under 3 is good",
            "They are identical; geometry does not affect the result",
            "The bunched one; multipath, and lower is better",
        ],
        correct=1,
        explanation="Satellites spread across the sky give a small area of uncertainty; bunched "
                    "together, a large one. The multiplier is dilution of precision. It changes "
                    "minute by minute as the constellation moves, which is why the same spot can "
                    "read differently an hour later.",
    ),
    dict(
        section="Part 3 — Where the error comes from",
        prompt="How does differential GPS get you a better position?",
        setup="",
        options=[
            "It averages many fixes taken at the same spot over a long time",
            "It uses two constellations at once instead of one",
            "A receiver on a known point measures the error happening right now, and a nearby receiver applies that correction",
            "It filters out the satellites with the weakest signal",
        ],
        correct=2,
        explanation="A base station knows where it is. Whatever error it sees at this moment, a "
                    "receiver a few kilometers away sees almost the same error at the same moment, "
                    "so the base's correction applies to the rover too. WAAS in your phone, RTK on "
                    "a survey rover, and the Utah reference network are all this one idea; "
                    "survey-grade receivers reach centimeters with it.",
    ),
]
