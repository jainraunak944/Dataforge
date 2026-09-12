# NAADI — Jury preparation: 18 hard questions with answer directions

DRAFT for team rehearsal. Answers are directions, not scripts — rewrite in
your own words. Where an answer depends on a team-owned number, the source is
the assumption register or the model results in this repo.

## Technical mechanism

**1. Why vibration and not motor-current signature analysis (MCSA), acoustic
emission, or oil analysis?**
Vibration is the most mature, standard-backed signal for bearing-dominated
pump failures (ISO 20816/13373 ecosystem), retrofits without touching the MCC,
and has decades of analyst practice to validate against. MCSA is a strong
complement (no sensor at the pump) and oil analysis catches different modes
(lubrication/wear debris); the architecture accepts them later — layer 2 is
signal-agnostic. We start with the highest information-per-rupee channel.

**2. Your prototype is 97.9% accurate — do you seriously expect that in a
plant?**
No, and we say so on slide 5. CWRU is a clean rig with seeded faults; it
proves the feature-classifier mechanism, not plant performance. Plant noise,
variable speed and unseen degradations will cut performance — that is why the
pilot's go/no-go KPI is ≥70% detection ≥14 days ahead, and why tier 1 is
per-pump anomaly detection (needs only that pump's healthy data), not
classification.

**3. Why classical features + random forest instead of deep learning?**
Three reasons: (a) auditability — a reliability engineer can check RMS,
kurtosis and band energies against known defect physics; a CNN's evidence is
harder to challenge on the shop floor; (b) data efficiency — deep models need
failure examples plants don't have at the start; (c) our logistic-regression
baseline scored 97.2% on the same features, showing the signal is in the
features, not model complexity. Deep models can be added once plant data
accumulates.

**4. How do you set alarm thresholds on day one with no training data?**
ISO 20816-3 velocity-severity zones give machine-class-based limits
immediately; each pump's own healthy baseline then tightens them (statistical
control limits on the 16 features). Learning augments, never replaces, the
standard.

**5. What is your false-alarm strategy? One bad month kills operator trust.**
Shadow mode for three months — alerts adjudicated weekly but never actioned;
a hard gate of ≤2 false alerts/pump-month before going live; every live alert
arrives as a drafted work order with the evidence plot, and a human decides.
On the benchmark the prototype misflagged 0 of 237 healthy windows — the
plant number will be worse, and the pilot exists to measure it honestly.

**6. Bearing defect frequencies depend on shaft speed — what about
variable-speed pumps?**
True: BPFO/BPFI scale with speed. Mitigations: most critical process pumps in
the archetype run near-constant speed; where VFDs exist we bin features by
speed band (edge layer reads speed from the historian) and normalise band
edges by running speed. This is a known limitation listed on slide 5 and a
pilot validation item.

## Safety & regulation

**7. Can you legally install wireless electronics in a hazardous area?**
Only certified equipment: intrinsically-safe (Ex ia) sensors with IECEx/ATEX
certification and PESO approval for India, installed under the plant's
permit-to-work and area-classification rules. This is budgeted (Ex-rated
sensor cost) and phase P1 includes the permits. No DIY electronics.

**8. Doesn't wireless + cloud create an OT cybersecurity hole?**
Data flows one way: sensors → gateway → plant historian; the analytics can run
fully on-premise. No control action path exists — the system writes work-order
drafts to the CMMS, never to the DCS. Network segregation per the plant's
OT policy; this is on the risk register.

## Economics & assumptions

**9. Your ₹1.4 Cr exposure is an assumption. What if the real number is much
smaller?**
Then the model tells us so before any scale-up: P0 rebuilds the baseline from
the plant's actual 24-month CMMS history, and the sensitivity sheet shows the
programme still pays back < 16 months with lost-margin one-third lower. If a
plant genuinely loses < ~20 h/yr to these pumps, it is the wrong pilot host —
criticality screening in P0 exists to pick the right one.

**10. Why should we trust DOE's 35–45% from 2010?**
It is the most-cited official range, published by a neutral government body,
and we applied the low end. Nothing newer and equally official contradicts it.
More importantly, we do not ask the plant to trust it: the pilot measures the
plant's own number in shadow mode before any maintenance decision changes.

**11. ₹35,000 per installed Ex-rated wireless point looks optimistic.**
It is a labelled estimate without vendor quotes — we say so in the register.
The sensitivity case with CapEx +30% (payback ~14 months) covers quote risk;
the pilot's first procurement step is three competitive quotes. If real cost
doubles, payback ~22 months — still inside a 24-month bar.

**12. Who pays for the pilot?**
Proposed: host plant funds CapEx (it keeps the hardware and data);
institutional/mission support (e.g., NM-ICPS TIH ecosystem, SAMARTH Udyog
centres) can subsidise the analytics development; our team contributes the
models and dashboards as open code. Structure to be negotiated — the ask on
slide 8 is deliberately specific about what we need and what the plant keeps.

## Novelty & alternatives

**13. OEMs like SKF/Emerson/Honeywell already sell this. What is new here?**
The components are not new — we mark them "proven" on slide 4 ourselves. The
contribution is architectural and contextual: open protocols and plant-owned
models instead of subscription silos; benchmark-published, reproducible
detection metrics instead of brochure claims; and a cost/deployment design
(shared cluster model) aimed at mid-size Indian plants and MSME clusters that
current offerings do not reach. Our comparison matrix scores the OEM route
2.9/5 for this segment — not because it fails technically, but on TCO, lock-in
and scalability.

**14. What stops an OEM from undercutting you?**
Nothing — and for India that would be a win; the proposal is a sector solution,
not a startup pitch. But structurally, an OEM's incentive is per-point
subscription revenue; a plant-owned open stack removes that margin, which is
exactly why it is unlikely to come from an OEM.

**15. Is this not just condition monitoring, which is 40 years old?**
Condition monitoring is the sensing practice; predictive maintenance is the
closed loop from detection to a planned work order and a measured downtime
outcome. The failure of adoption in mid-size Indian plants is not the physics
— it is cost, lock-in, analyst scarcity and trust. Those are the four things
the design principles on slide 3 target.

## Indian applicability & scalability

**16. Will this work for MSMEs who cannot afford ₹37 lakh?**
Not as a single-plant purchase — hence the month-12–24 shared-service model:
one edge/analytics stack, cluster-level monitoring service, per-pump
subscription priced off our cost model (~₹1.5 L/pump hardware, shared
gateways/compute). SAMARTH Udyog demo centres are the natural anchor tenants.
This is a roadmap proposal, clearly marked as unproven.

**17. Chemical plants in India often lack historians and digital CMMS. Then
what?**
The stack degrades gracefully: gateways buffer data locally and the dashboard
runs standalone; work orders can be issued via the plant's existing paper/
spreadsheet workflow in the worst case. P0 includes a data-infrastructure
audit; a plant with zero digital maintenance records would score low in host
selection.

## Environmental trade-offs & implementation risks

**18. Batteries, sensors and gateways are themselves e-waste — is the
environmental story honest?**
Order-of-magnitude honest: ~55 small devices with 3–5-year battery lives
against avoided seal-failure releases, avoided emergency flaring, avoided
premature replacement of shafts/impellers (embodied steel), and pump-energy
findings on a load class that is ~20% of global motor electricity. We commit
to vendor take-back for batteries in procurement. We do not claim a full LCA;
if the jury wants one, it is a fair pilot-phase addition.

---
Also rehearse: (a) walk through `train_fault_model.py` line-by-line — you must
be able to explain windowing, features, GroupKFold and the load-holdout; (b)
recompute payback live on a whiteboard from the slide-7 formula; (c) the
one-sentence answer to "what is NAADI?" — see slide 8 takeaway.
