# NAADI, speaker notes for the v2 deck (10-minute final-round script)

Matches India_Chem_2026_NITW_Raunak_Anushriya_v2.pptx (the same notes are
embedded in the file under View, Notes). Target about 9.5 minutes plus buffer.
Suggested split: Raunak opens and takes slides 1, 2, 5 and 7; Anushriya takes
slides 3, 4, 6 and 8. Adjust to comfort. DRAFT for team rehearsal and rewrite.
House rule for this deck: no em dashes or en dashes, including in these notes.

---

**Slide 1, title (about 60 s)**
Good morning. We are Raunak Jain, mechanical engineering, and Anushriya
Bhattacharya, chemical engineering, from NIT Warangal. Our proposal is NAADI,
a predictive maintenance system for the critical pumps of a chemical plant.
The idea in one sentence: continuous vibration sensing on a plant's 25 most
failure-prone pumps, with interpretable machine learning that drafts work
orders for the reliability engineer, while all data and models stay on the
plant's own network. We are proposing a six-month pilot. The base-case
economics, a public benchmark validation of our prototype, and the pilot
design follow in the next seven slides.

**Slide 2, existing problem (about 70 s)**
The use case is one representative mid-sized speciality chemicals plant, and
inside it the 25 pumps whose trips actually stop production. The funnel on
the left shows the filtering: about 200 pumps, 25 critical ones, an estimated
60 outage hours a year, and roughly 1.4 crore of annual exposure once lost
margin and repairs are added. These plant figures are labelled estimates, and
the pilot's first phase replaces them with the plant's own 24-month history.
The middle shows why this keeps happening: monthly inspection rounds leave
long blind windows, and the foundational reliability study found 89 percent
of failure modes have no predictable wear-out age, so calendar-based
maintenance misses them. Bearing and seal problems develop over days to
weeks. That is the window NAADI is designed to use.

**Slide 3, global practices and the gap (about 65 s)**
We compared five realistic approaches on the six criteria that decide
adoption, weighting detection lead time and fit for mid-sized plants highest.
Run to failure and calendar-based maintenance give no lead time for random
faults, and calendar maintenance is still the common practice in Indian
plants. Monthly offline vibration rounds help but leave blind windows of
several weeks and depend on scarce analysts. OEM cloud monitoring is the
global best practice and it works, but it scores poorly here on total cost
and on data control, because the plant's condition history ends up in a
vendor system. So the gap is architectural rather than technical. That
analysis gives the five design choices at the bottom, and those choices
define NAADI. The scores are our judgement and are labelled as such.

**Slide 4, proposed solution (about 70 s)**
This is the whole system on one picture. Wireless vibration and temperature
sensors sit on both bearing housings of each pump, using hardware that meets
the applicable PESO and IECEx requirements for hazardous areas. An area
gateway extracts sixteen standard vibration indicators per measurement
window, following ISO 13374, and ISO 20816-3 alarm zones give usable limits
from day one. The model layer produces a per-pump anomaly score and a fault
type. Results feed a reliability dashboard, and each alert arrives as a
drafted work order inside the plant's existing CMMS. The reliability engineer
approves or rejects every action, and confirmed findings feed back to retrain
the model. Everything inside the dashed boundary runs on the plant network,
so the condition history stays with the plant. What is genuinely ours is the
model layer and the workflow integration; sensors and gateways are mature
industrial products.

**Slide 5, technical feasibility (about 75 s)**
How the detection works: a bearing defect makes the vibration signal
impulsive and shifts energy into characteristic frequency bands. We compute
sixteen standard indicators per window, things like RMS, kurtosis, crest
factor and band energies, and a random forest classifies them. We trained and
tested this ourselves on the public Case Western bearing dataset. Under a
strict protocol, with whole recordings held out and one motor load never seen
in training, four-class accuracy is 97.9 percent, and none of the 237 healthy
benchmark windows was misclassified. The confusion matrix shows the only
errors are between fault types, not between faulty and healthy. The caveat is
printed on the slide: this is a controlled test rig with seeded faults, not a
chemical plant. Sensors, gateways and integration standards are mature; what
still needs proof is plant noise, lead time and false-alert rate, which is
exactly what the pilot measures.

**Slide 6, pilot and scale-up (about 75 s)**
Execution is a six-month pilot with one principle: the system must earn trust
before anyone relies on it. Months zero to one build the baseline from the
plant's own maintenance records and fix the success criteria together with
the plant, so the pass bar is agreed before installation. Month two is
installation: wireless sensors magnet-mounted during routine access, no
shutdown, permits handled through the plant's normal process. Month three
commissions healthy baselines, and months three to six run in shadow mode:
alerts are logged and compared weekly with what maintenance actually finds,
but no decision depends on them yet. The month-six gate is numeric and is on
the slide: seventy percent of confirmed developing faults caught at least
fourteen days ahead, at most two false alerts per pump per month, and
ninety-five percent data availability. Pass the gate and the system goes
live, then scales to other rotating assets and, between months twelve and
twenty-four, to a shared deployment across chemical clusters. What we need is
one plant partner, the pumps, their history and six months of access.

**Slide 7, economics and risk (about 75 s)**
The economics, with the calculation visible. Each avoided downtime hour is
worth about 1.9 lakh of contribution margin. Taking the US Department of
Energy's published effectiveness range at its low end, 35 percent downtime
reduction and 10 percent repair savings, the waterfall builds to 47.4 lakh of
annual benefit, less 6 lakh of operating cost, so 41.4 lakh net. Against an
estimated 37 lakh of CapEx that is roughly an 11-month base-case payback and
about 1.1 crore of five-year NPV at a 12 percent discount rate. The
sensitivity chart stress-tests it: even if the programme delivers only 20
percent reduction, below the DOE band, or CapEx overruns by 30 percent,
payback stays under 24 months in the stacked downside. The risks we take most
seriously are false-alert fatigue, hazardous-area compliance, OT security and
the shortage of early failure examples; each has a specific mitigation on the
slide. Environmentally, earlier seal-fault detection reduces leak risk, and
the same data helps find cavitation and off-design operation. Our
recommendation is deliberately conditional: proceed with the pilot, subject
to plant-data validation and vendor quotations.

**Slide 8, sources (about 30 s)**
The reference slide groups everything we relied on: government guidance
including the Department of Energy maintenance ranges, the engineering
standards for vibration evaluation and reliability data, the technical
literature behind the failure statistics, and our own dataset work and
economics files. Numbers in square brackets throughout the deck point here.
The basis-of-preparation note states plainly what is estimated, what is
judgement and what has not yet been proven. We are happy to take questions.

---
Total about 9.4 minutes at a measured pace, leaving buffer inside the
10-minute limit.
