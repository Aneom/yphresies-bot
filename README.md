# yphresies-bot

This is a Python script that reads a duty roster and informs conscripts about their upcoming duties. It is (for now) simply informative and does not generate a schedule by itself.

Briefly, this script:
1. Reads an Excel file maintained by the Company's Administrative Office, using the Pandas library.
2. Extracts useful information relevant to upcoming conscript duties.
3. Provided a conscript's name, it prints out their scheduled duties.

## Prerequisites

* Pandas library (do `pip install pandas` in the command line if you don't have it installed)

## Future Plans

* Discord integration (using a bot)
