\# Centre Back Scouting Case Study

\## Finding a Replacement for Marc Guéhi Using Data Analytics



\## Project Objective



This project answers a football recruitment question:



\*\*"Who could replace Marc Guéhi based on statistical similarity?"\*\*



The objective was to identify centre backs with a similar performance profile to Marc Guéhi using event-level football data and statistical modelling.



The analysis combines defensive output and possession contribution to create a shortlist of potential replacement candidates.



\---



\# Data Source



\*\*StatsBomb Open Data\*\*



Competition analysed:



\*\*UEFA Euro 2024\*\*



Dataset:



\- 51 matches analysed

\- 187,924 events processed

\- 108 centre backs identified

\- 58 centre backs analysed after applying a minimum playing time threshold



\---



\# Methodology



\## 1. Data Collection



Match events and player lineups were collected using the StatsBomb open data package:



\- Match events

\- Player actions

\- Defensive actions

\- Passing events

\- Player positions



\---



\## 2. Player Filtering



Only centre backs were included.



Players were filtered using:



\- Centre-back position data

\- Minimum 270 minutes played



This reduces the impact of small sample sizes.



\---



\## 3. Performance Metrics



Players were evaluated using:



\### Defensive Metrics



\- Tackles won per 90

\- Interceptions per 90

\- Clearances per 90



\### Possession Metrics



\- Pass completion percentage

\- Progressive passes per 90



\---



\## 4. Similarity Model



A statistical similarity model was created to compare each defender against Marc Guéhi's profile.



The model ranks players based on the distance between their performance profiles.



Lower distance = more similar profile.



\---



\# Results



\## Closest Statistical Profiles to Marc Guéhi



| Rank | Player | Team |

|---|---|---|

| 1 | Robin Le Normand | Spain |

| 2 | Jan Vertonghen | Belgium |

| 3 | Riccardo Calafiori | Italy |

| 4 | Wout Faes | Belgium |

| 5 | Jonathan Tah | Germany |



\---



\# Key Finding



The model identified:



\## Robin Le Normand



as the closest statistical match to Marc Guéhi.



His profile showed similarities in:



\- Defensive reliability

\- Passing efficiency

\- Positional consistency

\- Ability to play in structured defensive systems



\## Riccardo Calafiori



was identified as a higher-upside alternative due to:



\- Progressive passing ability

\- Technical quality

\- Modern centre-back profile



\---



\# Visual Analysis



The project includes:



\- Player similarity ranking

\- Radar chart comparison

\- Scouting report PDF



\---



\# Tools Used



Programming:



\- Python



Libraries:



\- pandas

\- statsbombpy

\- scikit-learn

\- matplotlib



\---



\# Project Structure



centre-back-scouting-case-study



├── README.md

├── report/

│ └── scouting\_report.pdf

│

├── scripts/

│ ├── 01\_fetch\_data.py

│ ├── 02\_compute\_metrics\_v2.py

│ ├── 03\_find\_replacements.py

│ └── 04\_radar\_chart.py

│

├── data/

│ └── centre\_back\_metrics\_v2.csv

│

└── visuals/

└── radar\_chart.png





\---



\# Limitations



This model should be combined with traditional scouting.



Limitations:



\- Euro 2024 is a limited sample size

\- Players faced different opposition levels

\- Tactical roles vary between teams

\- Some qualities cannot be measured statistically:

&#x20; - Leadership

&#x20; - Communication

&#x20; - Positioning

&#x20; - Personality



The model identifies statistical similarity, not guaranteed future performance.



\---



\# Conclusion



This project demonstrates how football event data can support recruitment decisions.



By combining:



\- Data collection

\- Performance metrics

\- Statistical modelling

\- Visualisation

\- Scouting interpretation



it creates a repeatable framework for identifying potential player replacements.



\---



\# Author



Marlene Thiery

