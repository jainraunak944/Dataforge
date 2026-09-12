# NAADI — Speaker notes (10-minute final-round script)

Target: ~9.5 min talk + buffer; 60–75 s per substantive slide. The same notes
are embedded in the PPTX (View → Notes). Suggested split: Raunak opens and
takes slides 1–2, 5, 7; Anushriya takes 3–4, 6, 8 (chemical-plant context,
pilot & way forward) — adjust to comfort. DRAFT for team rehearsal & rewrite.

---

**Slide 1 — Title (≈60 s)**
Good morning. We are Raunak Jain, mechanical engineering, and Anushriya
Bhattacharya, chemical engineering, from NIT Warangal. Our proposal is NAADI —
the Sanskrit word for pulse — a predictive-maintenance stack for the pumps
that keep a chemical plant alive. The one-line thesis: continuous vibration
monitoring with interpretable machine learning on a plant's 25 worst pumps
costs about ₹37 lakh, pays back in roughly eleven months, and — unlike
proprietary cloud offerings — leaves the data and the models with the plant.
The 35–45% downtime-reduction range is the US Department of Energy's published
band for functioning predictive-maintenance programmes, not our invention.
Everything you will see is either sourced, or computed by us in code we can
hand you.

**Slide 2 — Problem (≈70 s)**
Our use case is deliberately narrow: not "the chemical industry", but the 25
worst centrifugal pumps in one mid-size speciality-chemicals plant. Using our
assumption register — ₹500 crore revenue, 8,000 hours — each hour down costs
about ₹1.9 lakh in contribution margin. Sixty hours of pump-caused outage plus
twelve repairs a year is roughly ₹1.4 crore of annual exposure. These are
labelled estimates; phase zero of the pilot replaces them with the plant's own
24-month history. The root cause is structural: the classic
reliability-centred-maintenance finding is that 89% of failure modes show no
fixed wear-out age, so calendar-based maintenance is blind to them. Bearings
and seals — which dominate pump failures — degrade over weeks. That window is
our opportunity.

**Slide 3 — Benchmark & gap (≈70 s)**
We compared five realistic approaches on the six criteria that decide
adoption, weighting detection lead time and MSME scalability highest. Reactive
and calendar-based maintenance fail on lead time — and calendar PM is today's
Indian default. Monthly offline vibration rounds help, but leave four-week
blind windows and depend on scarce analysts. Global best practice — continuous
OEM cloud monitoring — is technically excellent but scores poorly for India:
high per-point cost, subscriptions, and the plant's own condition data locked
in a vendor silo. So the gap is not a sensing gap or an algorithm gap; it is
an architecture-and-affordability gap. That analysis produces five design
principles — continuous, interpretable, open, retrofit-friendly, human-in-loop
— and those principles, not a product preference, define NAADI.

**Slide 4 — Solution (≈75 s)**
The architecture is four layers, and we are explicit about what is ours and
what is not. Sensing is commodity and proven — Ex-certified wireless
accelerometers that magnet-mount during normal operation, no shutdown. The
edge layer computes sixteen interpretable condition indicators, and ISO 20816
velocity zones give usable alarm limits from day one, before any learning. The
learning layer is our contribution: an anomaly tier per pump plus a fault-type
classifier, whose honest benchmark results are on the next slide. The act
layer keeps a human in the loop — every alert becomes a drafted CMMS work
order that the reliability engineer accepts or rejects, and those decisions
retrain the system. Three defensible differences: openly validated metrics,
plant-owned data, and a cost architecture — about one and a half lakh per pump
— that a cluster of MSMEs can realistically share.

**Slide 5 — Technical feasibility (≈75 s)**
Why does this work? A defect in a bearing race strikes the rolling elements at
a defect-specific frequency — energy moves into characteristic bands and the
waveform turns impulsive. Sixteen classical indicators capture that; a random
forest classifies it. We did not take anyone's word for this: we trained the
prototype ourselves on Case Western's public bearing benchmark. Under the
strictest split — whole recordings held out, and an entire motor-load
condition never seen in training — fault-versus-healthy separation is perfect
on this benchmark, and fault-type accuracy is 97.9%. One honesty point: many
projects quote random window splits, which leak near-identical windows into
the test set and inflate accuracy. We refuse to. And the limits are printed on
the slide, not hidden: a test rig is not a plant, which is why our pilot
success threshold is seventy percent early detection, not ninety-seven.

**Slide 6 — Execution & pilot (≈75 s)**
Execution is a six-month pilot built around one principle: earn trust before
touching anyone's maintenance schedule. Phase zero builds the baseline from
the plant's own CMMS history and freezes the success criteria jointly with the
plant — the pass bar is agreed before we install anything. Installation takes
a month: wireless magnet-mount sensors fitted during routine access, no
shutdown, hazardous-area permits handled properly. Then the crucial part:
three months of shadow mode. Alerts are logged and adjudicated weekly against
what maintenance actually finds — but nobody acts on them. The system earns
its precision statistics in the open. The month-six gate is numeric: ≥70%
early detection, ≤2 false alerts per pump-month, every validated alert a work
order within 24 hours. Pass, and it goes live and scales. Fail, and we publish
the post-mortem. Either way the plant keeps the data.

**Slide 7 — Economics & risk (≈75 s)**
We show the calculation, not just the answer. Each avoided downtime hour is
worth about ₹1.9 lakh of contribution margin. Applying the DOE's effectiveness
ranges at the conservative end — 35% downtime reduction, 10% repair savings —
annual benefit is about ₹47 lakh against ₹6 lakh operating cost. Against ₹37
lakh of CapEx, that is an eleven-month payback and about ₹1.1 crore of
five-year NPV at twelve percent. We stress-tested it: if the programme
achieves only 20% reduction — below DOE's band — or CapEx overruns 30%,
payback stays under 24 months; both together, still under two years.
Environmentally, fewer seal blow-outs mean fewer releases, and the same data
stream exposes cavitation and off-BEP operation for energy savings. The risk
we respect most is false alarms destroying operator trust — which is exactly
why the pilot runs in shadow mode behind a hard false-alert gate.

**Slide 8 — Evidence & way forward (≈75 s)**
To close: what is proven, and what is not. Proven, with sources: the DOE
effectiveness band, the reliability-engineering failure logic, a standards
pathway, and our own prototype's detection numbers on a public benchmark —
reproducible from code we publish. Not yet proven, and we have said so on
every slide: real-plant lead times, false-alarm rates, and Indian cost points.
That is precisely what the six-month pilot measures. After the pilot:
plant-wide coverage within a year, and by month 24 a shared-service model for
MSME chemical clusters, aligned with the SAMARTH Udyog Industry 4.0 centres —
because one shared edge stack is how this reaches plants that could never buy
an OEM cloud contract. Our ask is one pilot partner: 25 pumps, their
maintenance history, six months of access; we bring everything else, and the
plant keeps the data, models and results, published either way. One line to
remember: listen to the machines before they stop the plant — ₹37 lakh,
eleven-month payback, and the plant keeps the brains. Thank you.

---
Total ≈ 9.4 minutes at a measured pace, leaving ~30 s buffer inside the
10-minute limit.
