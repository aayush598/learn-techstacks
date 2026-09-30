# General Aptitude — Part 4: Verbal Ability & Comprehension

> Part 4 of 5 of the GATE ECE General Aptitude question bank · Questions 1–234 of this file
> Read this file top to bottom, in order. The other four parts of this subject are Part 1
> (Quantitative aptitude, algebra and the number system), Part 2 (Geometry and mensuration),
> Part 3 (Data interpretation and logical reasoning) and Part 5 (Mixed timed drills). Nothing
> in those four files is needed to attempt this one.

**Covers:** Reading comprehension on technical and on general-science passages; vocabulary in
context; spotting errors; sentence improvement and para-jumble; fill-in-the-blank; idioms and
phrases; active–passive and direct–indirect speech; articles, prepositions and commonly confused
word pairs; precis writing; and a rapid-fire recall set. Every passage is written out inline
inside the question block, so no separate reading is required.

**Assumes:** Only the ability to read English and to attempt a GATE-style MCQ. No prior theory,
no formula, no external passage, no reading of any other file.

**Volume:** 234 questions across 12 sections. Roughly 25% recall/rule, 25% quick application,
25% medium reasoning, 15% GATE 1-mark MCQ (tagged `GATE-1`) and 10% GATE 2-mark MCQ
(tagged `GATE-2`).

---

## Section 1. Reading comprehension on technical passages

**Passage 1.** A bar of intrinsic germanium is doped uniformly with phosphorus to 10^16 cm⁻³ at 300 K. Under a weak field of 0.1 V/cm, the drift velocity of the majority carriers is directly proportional to the field, and the mobility read from that slope is about 3800 cm²/V·s. Under 10⁴ V/cm, the same bar's drift velocity flattens near 10⁷ cm/s and stops responding to more field. A carrier accelerated this hard does not stop moving; it reaches an average energy at which it hands back to the lattice as much energy between collisions as the field supplies. An engineer choosing a bias resistor must decide which regime the device is meant to live in.

### Q1. Which option best captures the main idea of Passage 1?

- (a) Doping germanium with phosphorus at 10^16 cm⁻³ produces a p-type material whose mobility is unusually high.
- (b) The drift velocity of majority carriers in doped germanium is constant in a weak field but rises steeply in a strong field.
- (c) Majority carriers in doped germanium move in proportion to the field at low field and saturate at high field, leaving the device two distinct transport regimes.
- (d) A mobility of 3800 cm²/V·s is a universal constant for all semiconductor materials at 300 K.

> **Type:** MCQ
> **Answer:** Majority carriers move proportionally to the field at low field and saturate at high field, leaving two distinct transport regimes (Option c).
> **Solution:** Sentences 2 and 3 report the two experiments, sentence 4 explains the mechanism, and sentence 5 says the choice matters for design. Option (a) is wrong on type: phosphorus is a donor, so the bar is n-type. Option (b) inverts the weak-field behaviour, and (d) over-generalises a number the passage attaches to one material in one regime.
> **Key point:** The main idea is the two regimes, not the doping or the mobility value.

### Q2. If the weak field is raised from 0.1 V/cm to 0.2 V/cm with everything else unchanged, the passage's own data predict that

- (a) the drift velocity roughly doubles while the mobility stays near 3800 cm²/V·s
- (b) the drift velocity and the mobility both roughly double
- (c) the drift velocity roughly doubles and the mobility roughly halves
- (d) the drift velocity saturates at about 10⁷ cm/s

> **Type:** MCQ
> **Answer:** The drift velocity roughly doubles while the mobility stays near 3800 cm²/V·s (Option a).
> **Solution:** Mobility is defined as μ = v_d/E, i.e. it is the *slope* of the drift-velocity-against-field plot, not the drift velocity itself. In the weak-field experiment that slope is linear and stated to be about 3800 cm²/V·s. Raising E therefore raises v_d in proportion and leaves the slope — the mobility — unchanged. Option (d) is the strong-field outcome, which 0.2 V/cm is nowhere near.
> **Key point:** Mobility is a ratio; it is invariant when the field–velocity relation is linear.

### Q3. In which sentence of Passage 1 does the author give the physical reason for the saturation of drift velocity?

- (a) The first sentence
- (b) The second sentence
- (c) The fourth sentence
- (d) The fifth sentence

> **Type:** MCQ
> **Answer:** The fourth sentence (Option c).
> **Solution:** Sentence 4 says a heavily accelerated carrier "reaches an average energy at which it hands back to the lattice as much energy between collisions as the field supplies" — that is an energy-balance explanation of saturation. Sentences 1, 2 and 3 only report the material and the two measurements, and sentence 5 states the design consequence, not the cause.
> **Key point:** Distinguish sentences that *report* a result from the sentence that *explains* it.

### Q4. Why does the author say a hard-accelerated carrier "does not stop moving"?

- (a) To remove the common wrong idea that saturation means the carriers have come to rest.
- (b) To suggest that the drift velocity is a poor measure of carrier speed at high field.
- (c) To claim that the lattice is unable to stop a carrier under any field.
- (d) To imply that saturation is a measurement artefact of the experiment.

> **Type:** Conceptual
> **Answer:** To remove the common wrong idea that saturation means the carriers have come to rest.
> **Solution:** Saturation means v_d stops *growing* with field, not that v_d becomes zero — the passage puts the value at 10⁷ cm/s, which is fast. The clause "it reaches an average energy at which…" is the corrective: the carrier still moves, it just no longer gains net energy per collision. (b), (c) and (d) go beyond anything the passage asserts.
> **Key point:** Saturation of a velocity means a ceiling, not a stop.

### Q5. The author's attitude towards the two regimes is best described as

- (a) openly enthusiastic about the saturated regime and dismissive of the linear one
- (b) cautious and informative, reporting measurements and flagging a design decision
- (c) strongly alarming, treating the high-field result as a hazard
- (d) openly sceptical, treating both measurements as unreliable

> **Type:** MCQ
> **Answer:** Cautious and informative, reporting measurements and flagging a design decision (Option b).
> **Solution:** The prose is neutral and quantitative: it gives concentrations, fields, a mobility and a saturated velocity, with no evaluative adjectives and no exclamation. The closing sentence turns the physics into a practical caution ("must decide"), which is informative caution, not alarm. (a) and (d) invent an attitude the wording does not carry, and (c) needs evaluative words that are absent.
> **Key point:** Tone is judged from the evaluative vocabulary, not from the topic's difficulty.

---

**Passage 2.** Orthogonal frequency division multiplexing does not send one wideband waveform and hope the channel is kind. It splits the data rate into hundreds of narrow subcarriers, each so narrow that its bandwidth is small beside the coherence time of the multipath channel, so a subcarrier arriving via a reflected path of 40 km does not smear into its neighbour. A cyclic prefix — a copy of the block's tail pasted in front of it — is what makes the channel look memoryless: provided the prefix is at least as long as the longest impulse-response delay, the convolution becomes a circular convolution, and every subcarrier can then be equalised with a single complex multiply. The price of that insensitivity to delay is a small, fixed overhead of symbols, paid on every block, whether or not the channel is hostile.

### Q6. [GATE-2] Which option states the main idea of Passage 2?

- (a) OFDM avoids multipath problems by transmitting each data stream on a wideband carrier that the channel distorts only mildly.
- (b) OFDM's resistance to multipath delay comes from narrow subcarriers plus a cyclic prefix, and it is bought at a fixed symbol overhead.
- (c) Cyclic prefix length must be chosen shorter than the longest impulse-response delay so that the channel remains frequency-selective.
- (d) OFDM reduces the transmitted data rate by discarding the subcarriers that the channel distorts most severely.

> **Type:** MCQ
> **Answer:** OFDM's resistance to multipath delay comes from narrow subcarriers plus a cyclic prefix, bought at a fixed symbol overhead (Option b).
> **Solution:** Sentence 2 gives the narrow-subcarrier argument and sentence 3 the cyclic-prefix argument; the last sentence names the cost. Option (a) contradicts the whole passage, (c) inverts the stated condition (the prefix must be *at least as long as* the delay), and (d) describes a technique the passage never mentions.
> **Key point:** Each mechanism sentence earns the right claimed in the cost sentence.

### Q7. Suppose a new channel is measured whose longest impulse-response delay is three times the cyclic prefix length used. Which claim in Passage 2 is the first to fail?

- (a) The claim that the data rate is split into many narrow subcarriers.
- (b) The claim that convolution with the channel becomes a circular convolution.
- (c) The claim that each subcarrier can be equalised with a single complex multiply.
- (d) The claim that the overhead is paid on every block.

> **Type:** MCQ
> **Answer:** The claim that convolution with the channel becomes a circular convolution (Option b).
> **Solution:** The circular-convolution result is stated as conditional: it holds "provided the prefix is at least as long as the longest impulse-response delay". Make the delay three times the prefix and that hypothesis is violated, so the channel no longer looks memoryless over the block. Option (c) is a consequence of (b) and fails at the same moment, but (b) is the first step to break. Options (a) and (d) are independent of the channel delay.
> **Key point:** Find the stated condition attached to a result, then test whether it still holds.

### Q8. The phrase "whether or not the channel is hostile" chiefly serves to

- (a) establish that the cyclic prefix makes the channel physically friendly.
- (b) show that the overhead is charged unconditionally, even when it is not needed.
- (c) warn that some channels destroy cyclic prefixes entirely.
- (d) suggest that hostile channels need no prefix at all.

> **Type:** Conceptual
> **Answer:** It shows that the overhead is charged unconditionally, even when it is not needed.
> **Solution:** The prefix is *paid on every block*, and the closing clause says the price does not depend on the channel being bad. So a clean line-of-sight link, which needs no delay protection, still carries the same reduced throughput. (a) contradicts the passage, (c) invents a failure mode, and (d) is the reverse of what the passage says.
> **Key point:** "whether or not" marks an unconditional cost.

### Q9. Why does the author describe the cyclic prefix as "a copy of the tail of the transmitted block pasted in front of it"?

- (a) To explain what a cyclic prefix is, for readers who may not know the term.
- (b) To show that the prefix carries new information for the receiver.
- (c) To prove that the prefix increases the effective bandwidth of the channel.
- (d) To argue that the prefix is shorter than the block it is attached to.

> **Type:** Conceptual
> **Answer:** It explains what a cyclic prefix is, for readers who may not know the term.
> **Solution:** The passage is written for an audience that has not met the concept, so it defines it by construction. "a copy of the block's tail" tells the reader it is redundant data, and "pasted in front" tells the reader where it goes. (b) is wrong because a copy carries no new information, (c) is never claimed, and (d) is a size fact the sentence does not make.
> **Key point:** An appositive built from "a copy of…" is a definition, not extra evidence.

### Q10. In "does not smear into its neighbour", the word *smear* is used to mean

- (a) to blur the amplitude of the received signal
- (b) to spread a subcarrier's energy in time so that it overlaps the neighbouring subcarrier's band
- (c) to reduce the subcarrier's carrier frequency
- (d) to distort the phase of the subcarrier

> **Type:** MCQ
> **Answer:** To spread a subcarrier's energy in time so that it overlaps the neighbouring subcarrier's band (Option b).
> **Solution:** The clause it explains is that each subcarrier is "its bandwidth is small beside the coherence time of the multipath channel". Multipath produces delayed copies, so a narrow signal spread by delay reaches into the adjacent subcarrier's band. "Smearing" is therefore a time-domain spreading into a neighbour. Phase distortion is real in OFDM but it is the cyclic prefix, not the narrowness, that removes it, so (d) is not what this word is doing.
> **Key point:** Read a figurative word through the technical clause that defines its scope.

---

**Passage 3.** An induction motor has no commutator and no brushes, which is why it is the workhorse of a factory and the largest load on a feeder. Its rotor turns close to, but never equal to, the synchronous speed set by the supply frequency and pole count. The gap between the two, as a fraction of synchronous speed, is the slip, and slip is not a defect: the very lag that makes the rotor fall behind is the lag that induces rotor current, and without it no torque would be produced at all. At standstill the slip is one and the starting current is several times the full-load current. As the rotor accelerates the current falls, the referred rotor resistance becomes a smaller term in the circuit, and the machine settles on a stable operating point that shifts with load.

### Q11. Which option best states the main idea of Passage 3?

- (a) Induction motors are preferred because their brushes and commutator never need maintenance.
- (b) The rotor of an induction motor must run slightly below synchronous speed, and this unavoidable lag is exactly what produces its torque.
- (c) An induction motor draws several times its full-load current at startup and is therefore unsuitable for direct-on-line starting.
- (d) The synchronous speed of an induction motor is fixed by the number of brushes on its rotor.

> **Type:** MCQ
> **Answer:** The rotor runs slightly below synchronous speed, and this lag is exactly what produces its torque (Option b).
> **Solution:** Sentences 3 and 4 make exactly this claim — "without it no torque would be produced at all". Option (a) is a true statement but it is a side remark, not the point of the passage. Option (c) is stated but the passage never draws the conclusion in (c). Option (d) is nonsense: the speed is set by supply frequency and pole count.
> **Key point:** A main idea must be the claim the passage builds its explanation around.

### Q12. [GATE-2] The passage says the rotor speed is "never equal to" synchronous speed. If a rotor did reach synchronous speed, the passage's own logic implies that

- (a) the rotor would draw a very large current and overheat
- (b) no current would be induced in the rotor and therefore no torque would be produced
- (c) the machine would immediately lose synchronism and stall
- (d) the stator current would fall to zero while the torque doubled

> **Type:** MCQ
> **Answer:** No current would be induced in the rotor and therefore no torque would be produced (Option b).
> **Solution:** Sentence 4 chains the argument: slip causes the lag, the lag induces rotor current, the rotor current produces the torque. Remove the slip and the whole chain breaks at its first link. Options (a) and (d) contradict the passage (a large current is attached to *high* slip, and no torque is produced with no slip), and (c) misuses "synchronism" for a machine whose problem is the opposite.
> **Key point:** Follow the causal chain in the passage; every link must survive the hypothetical.

### Q13. Why does the author call slip "not a defect"?

- (a) Because slip makes the machine less efficient than a synchronous motor.
- (b) Because the same lag that creates slip is the mechanism that creates torque.
- (c) Because slip disappears once the rotor reaches its stable operating point.
- (d) Because the brushes and commutator keep slip below one per cent.

> **Type:** Conceptual
> **Answer:** Because the same lag that creates slip is the mechanism that creates torque (Option b).
> **Solution:** The colon after "not a defect" introduces the justification: "the very lag that makes the rotor fall behind is the lag that induces rotor current". So the feature cannot be designed away without removing the function. Option (c) contradicts the passage (slip is one at standstill and persists at load), and (d) is irrelevant to the rotor at all.
> **Key point:** "Not a defect:" promises the reason in the text that follows.

### Q14. In "settles on a stable operating point that shifts with load", the phrase "stable operating point" means

- (a) a rated speed that the machine can never leave
- (b) the combination of slip and torque at which the machine's net accelerating torque is zero for a given load
- (c) the point at which the rotor reaches synchronous speed and the slip becomes zero
- (d) the voltage at which the stator current reaches its minimum

> **Type:** MCQ
> **Answer:** The combination of slip and torque at which the machine's net accelerating torque is zero for a given load (Option b).
> **Solution:** The sentence follows from "the referred rotor resistance becomes a smaller term in the circuit", which is a statement about the equivalent-circuit equation. A machine "settles" on an operating point when the accelerating torque has died away, and the point "shifts with load" because a heavier load demands more torque and therefore more slip. (a) and (c) deny the load dependence or the necessity of slip; (d) is a supply-side quantity, not an operating point.
> **Key point:** "Settles" in a rotating machine language means the acceleration has gone to zero.

### Q15. Why does the author mention that starting current is several times the full-load current?

- (a) To show that the motor is dangerously over-rated for its task.
- (b) To suggest that a direct-on-line start is easy on the supply.
- (c) To give a practical reason for soft starters, star-delta switching or reduced-voltage starting.
- (d) To show that the machine cannot be protected by a fuse.

> **Type:** Conceptual
> **Answer:** It gives a practical reason for soft starters, star-delta switching or reduced-voltage starting (Option c).
> **Solution:** The sentence is a factual datum whose only function is to flag that a direct start is a shock to the supply. Combined with sentence 1's mention of the motor being the largest load on the feeder, it points straight at reduced-voltage starting methods. (b) is the opposite of what "several times" implies, and (a) and (d) are not supported at all.
> **Key point:** Ask why the author included a fact; the answer reveals the passage's purpose.

---

**Passage 4.** A digitiser does not record a waveform; it records a list of numbers, and the price of turning an analogue voltage into a list is a promise about the highest frequency the signal may contain. Sample a 4 kHz sine every 125 microseconds and the sampler sees the same phase of that wave on every one of its 8000 samples per second, so an observer looking only at the samples would be equally happy to be told the signal was 4 kHz, or −4 kHz, or 7960 kHz, or anything congruent to 4 kHz modulo 8 kHz. Nothing in the samples breaks the tie. The cure is not cleverer arithmetic; it is a filter placed before the sampler that removes everything above half the sample rate, so the ambiguity is never given a chance to exist.

### Q16. Which option best expresses the main idea of Passage 4?

- (a) A sampled signal can be reconstructed exactly only if the input contains no frequency above half the sample rate.
- (b) Sampling a 4 kHz waveform at 8000 samples per second destroys the phase information in the signal.
- (c) Digital recorders must filter the input after sampling to remove frequencies above the sample rate.
- (d) The highest frequency a digitiser can handle is fixed by the number of samples it stores.

> **Type:** MCQ
> **Answer:** A sampled signal is recoverable only if the input contains no frequency above half the sample rate (Option a).
> **Solution:** The example shows that 4 kHz sampled at 8000/s is indistinguishable from −4 kHz or 7960 kHz, and the last sentence says the remedy is a *pre*-sampler filter that removes everything above half the sample rate. Option (b) is wrong because the phase is perfectly repeatable — that is exactly the problem. Option (c) reverses the order (the filter is before the sampler), and (d) confuses resolution with range.
> **Key point:** The ordering of filter and sampler is the whole content of the last sentence.

### Q17. [GATE-2] The sampling interval is instead 62.5 microseconds, and the same 4 kHz sine is applied. Given only the passage's reasoning, the correct conclusion is that

- (a) the 4 kHz signal now aliases and the tie can no longer be broken from the samples
- (b) the 4 kHz signal still lies below half the sample rate and is not aliased by this particular rule
- (c) the aliasing is doubled because the sample rate has been halved
- (d) the waveform must now be reconstructed at exactly 4 kHz with no filter at all

> **Type:** MCQ
> **Answer:** The 4 kHz signal still lies below half the sample rate and is not aliased by this particular rule (Option b).
> **Solution:** A 62.5 µs interval is a 16 kHz sample rate, so half the sample rate is 8 kHz, and 4 kHz is still under it. The ambiguity the passage describes appears when a component lands above half the sample rate, which 4 kHz does not. Option (a) has the condition backwards, (c) asserts a doubling the passage never states, and (d) drops the filter requirement the passage insists on.
> **Key point:** Aliasing is judged against half the sample rate, not against the sample rate.

### Q18. Why does the author write "Nothing in the samples breaks the tie"?

- (a) To show that the ambiguity is a property of the data itself, not of the equipment.
- (b) To argue that the digitiser is faulty.
- (c) To suggest that more storage would resolve the ambiguity.
- (d) To indicate that the arithmetic has been done incorrectly.

> **Type:** Conceptual
> **Answer:** It shows the ambiguity is a property of the data itself, not of the equipment (Option a).
> **Solution:** The clause after it — "The cure is not cleverer arithmetic" — makes the contrast explicit: no processing of a tie in the data can break it, because every candidate frequency predicts the samples identically. (b) and (d) are ruled out by that same clause, and (c) confuses resolution with range.
> **Key point:** "Nothing in the data X" marks an information-theoretic limit, not a hardware fault.

### Q19. The tone of Passage 4 is best described as

- (a) dismissive of the difficulty of the problem
- (b) corrective, gently correcting a natural misreading of what sampling does
- (c) promotional, encouraging wider use of digitisers
- (d) anxious, warning against the use of sampled data

> **Type:** MCQ
> **Answer:** Corrective, gently correcting a natural misreading of what sampling does (Option b).
> **Solution:** The passage opens by contradicting a common belief ("does not record a waveform; it records a list of numbers") and ends by replacing a false hope ("cleverer arithmetic") with the real cure. It never warns against sampling, and it never sells anything. The word "gently" is carried by the absence of alarmist vocabulary.
> **Key point:** "X; not Y" at the head of a passage signals a corrective purpose.

### Q20. [GATE-1] Which single term names the phenomenon that makes 4 kHz, −4 kHz and 7960 kHz indistinguishable in the samples described?

- (a) Quantisation
- (b) Aliasing
- (c) Windowing
- (d) Interpolation

> **Type:** MCQ
> **Answer:** Aliasing (Option b).
> **Solution:** Aliasing is the folding of frequencies that differ by an integer multiple of the sample frequency onto the same apparent frequency, which is exactly what "congruent to 4 kHz modulo 8 kHz" states. Quantisation is amplitude resolution and is not at issue; windowing shapes the spectrum before analysis; interpolation reconstructs between samples and cannot recover a folded component.
> **Key point:** Frequencies congruent modulo the sample frequency are the same signal after sampling.

---

**Passage 5.** The first thing that breaks when a transistor is shortened is not the current it can carry but the transistor's grip on its off state. A gate a few nanometres long, sitting that far above the channel, is a switch rather than a wall, and the electric field reaching the channel leaks around the edge of the gate contact and lowers the barrier a drain voltage had raised. The result is drain-induced barrier lowering: the subthreshold swing of the tail current grows beyond the ideal 60 mV per decade at 300 K, the off current rises, and a comfortably negative gate voltage turns out adequate to switch the device on. Designers answer with a higher dielectric constant, a longer effective gate, and a fin or a surrounding gate that increases electrostatic control without a longer drawn gate.

### Q21. Which option best captures the main idea of Passage 5?

- (a) Shorter transistors carry more current, so the current-carrying capability is the first quantity to be lost.
- (b) As transistors are shortened, electrostatic control of the channel weakens, the off state leaks, and geometries and materials must compensate.
- (c) The subthreshold swing of a short-channel transistor is limited to exactly 60 mV per decade.
- (d) A fin or a surrounding gate lets designers draw a physically longer gate at the same drawn length.

> **Type:** MCQ
> **Answer:** As transistors are shortened, electrostatic control of the channel weakens, the off state leaks, and geometries and materials must compensate (Option b).
> **Solution:** The first three sentences trace the failure (leakage around the gate, barrier lowering, rising off current) and the last sentence lists the three responses. Option (a) reverses the opening clause ("not the current it can carry"). Option (c) inverts the sentence that says the swing grows *beyond* 60 mV/decade. Option (d) misreads "without a longer drawn gate" as a licence to draw a longer gate.
> **Key point:** "X; not Y" at the head tells you which of two facts the passage is about.

### Q22. The qualifier "at 300 K" attached to the figure 60 mV per decade signals that

- (a) the figure is a definition that is only valid at 300 K and not a temperature-independent constant
- (b) the transistor must be operated at 300 K for correct switching
- (c) the off current is zero at 300 K
- (d) the figure was measured on a particular sample and is unreliable elsewhere

> **Type:** MCQ
> **Answer:** The figure is a definition valid only at 300 K, not a temperature-independent constant (Option a).
> **Solution:** An ideal subthreshold swing has a floor proportional to thermal voltage, and the thermal voltage itself scales with temperature; the author attaches the temperature precisely because the number is quoted *for* that temperature and calls it "ideal" as opposed to measured. (b) and (c) are not claimed, and (d) misreads a stated condition as a measurement caveat.
> **Key point:** When a figure carries a stated condition, the condition is part of the claim.

### Q23. According to the passage, as the subthreshold swing grows beyond 60 mV per decade, the off current

- (a) falls, because a faster turn-off needs less current
- (b) is unchanged, because swing and off current are unrelated
- (c) rises, because the passage chains rising swing to a rising off current
- (d) oscillates about 60 mV per decade

> **Type:** MCQ
> **Answer:** Rises, because the passage chains rising swing to a rising off current (Option c).
> **Solution:** The third sentence lists the consequences in sequence: "the subthreshold swing … grows beyond the ideal 60 mV per decade at 300 K, the off current rises, and a comfortably negative gate voltage turns out adequate". Option (a) inverts the sequence, and (b) contradicts the passage's own causal chain.
> **Key point:** When a passage lists consequences with commas, they form a chain; read them in order.

### Q24. Why does the author begin with "not the current it can carry"?

- (a) To prevent the reader from assuming that short-channel failure is a current-capacity problem
- (b) To claim that short transistors cannot carry much current
- (c) To introduce a second mechanism discussed later
- (d) To compare a short-channel transistor with a long-channel one

> **Type:** Conceptual
> **Answer:** It prevents the reader from assuming that short-channel failure is a current-capacity problem (Option b).
> **Solution:** The clause after the semicolon names what *does* break — the grip on the off state — and the rest of the passage develops only that. The construction exists to correct a plausible prior belief, which is the standard purpose of a "not X; it is Y" opening. Option (b) is contradicted by the passage's own opening clause, and (c) and (d) have no support.
> **Key point:** A "not X; it is Y" opening exists to kill a default assumption.

### Q25. In "increases electrostatic control", the term *electrostatic control* means

- (a) the ability of the gate to attract and repel carriers electrostatically
- (b) the ability of the gate terminal to resist electrostatic breakdown
- (c) the strength of the fringing field around the gate edge
- (d) the capacitance between the gate metal and the interconnect

> **Type:** MCQ
> **Answer:** The ability of the gate to attract and repel carriers electrostatically (Option a).
> **Solution:** The passage has already said that in a short gate "the electric field reaching the channel leaks around the edge of the gate contact", which is a loss of this ability. So electrostatic control is the gate's power to hold carriers in or push them out. (b), (c) and (d) each concern one side of the sentence rather than the quantity the contrast turns on.
> **Key point:** Define a term in context by what the passage says is being lost.

---

**Passage 6.** A signal reaching a receiver by two reflected paths is the same signal twice, a fraction of a microsecond apart, and the two copies add or cancel depending on where the receiver stands. Over one wavelength this looks like noise with no pattern, and a single antenna moving one centimetre may see its power fall by a factor of ten. A second receive antenna adds no information about what was sent, but it adds a delay difference whose sign changes reliably with position, enough to separate the two paths. Repeat this over several transmit antennas and the channel matrix, never measured but inferred from pilot symbols, sets the ceiling on data rate. The catch is that the inference must be refreshed: a receiver acting on a matrix from a millisecond ago is acting on a channel that no longer exists.

### Q26. [GATE-2] Which option best states the main idea of Passage 6?

- (a) Two receive antennas are needed so that the receiver can hear twice as much information as one.
- (b) A second receive antenna converts a flat, position-dependent fading pattern into a distinguishable delay difference, at the cost of having to keep re-estimating the channel.
- (c) Pilot symbols allow a receiver to measure the channel matrix directly and exactly.
- (d) Moving a single antenna by one centimetre usually causes a tenfold loss of received power.

> **Type:** MCQ
> **Answer:** A second receive antenna turns an indistinguishable fading pattern into a usable delay difference, at the cost of continual re-estimation (Option b).
> **Solution:** Sentences 2 and 3 make the separation argument and the last sentence gives the cost. Option (a) is explicitly denied ("adds no information about what was sent"). Option (c) is denied too ("never measured but inferred"). Option (d) turns a worst-case "may see" into a rule and drops the argument it supports.
> **Key point:** When a passage says "does not add information", look for what it adds instead.

### Q27. The passage says the channel matrix is "never measured but inferred from pilot symbols". The reason given is that

- (a) pilot symbols are transmitted more often than data symbols.
- (b) the channel cannot be probed directly, so known symbols are used to solve for it
- (c) pilot symbols are cheaper to generate than data symbols.
- (d) the channel matrix has too many elements to be sent.

> **Type:** MCQ
> **Answer:** The channel cannot be probed directly, so known symbols are used to solve for it (Option b).
> **Solution:** "Never measured" is the premise; "inferred from pilot symbols" is the consequence, and the only coherent reason for needing a special estimate is that no direct measurement is available. (a) and (c) are properties the passage does not mention, and (d) is contradicted by the passage's own account of estimating it.
> **Key point:** Read "never X but inferred from Y" as: X is impossible, so Y stands in for X.

### Q28. The phrase "fall by a factor of ten" is included mainly to

- (a) quantify the antenna gain available from a second receive element.
- (b) quantify how deep and how local the fades are in a single-antenna channel.
- (c) show that path loss dominates over fading at this distance.
- (d) show that a millisecond is long compared with a wavelength.

> **Type:** MCQ
> **Answer:** It quantifies how deep and how local the fades are in a single-antenna channel (Option b).
> **Solution:** The number is attached to "a single antenna moving one centimetre", so it measures the depth of the null and the distance over which it occurs — the two facts the next sentence needs in order to make the case for a second antenna. (a) is about a two-antenna system and appears only afterwards; (c) and (d) compare quantities the passage never puts side by side.
> **Key point:** A number plus a unit of change usually illustrates the property just described.

### Q29. "Acting on a channel that no longer exists" is best read as

- (a) a statement that channel matrices are stored in non-volatile memory and persist.
- (b) a warning that a stale channel estimate drives the wrong equaliser coefficients.
- (c) a claim that the channel changes sign every millisecond.
- (d) evidence that pilot symbols are transmitted too slowly.

> **Type:** MCQ
> **Answer:** A warning that a stale channel estimate produces the wrong equaliser coefficients (Option b).
> **Solution:** The sentence's logic is: the channel varies in time, the matrix is inferred, so an old inference describes a different channel and the equaliser built on it is wrong. (a) contradicts the sentence, (c) over-reads "no longer exists" as a sign change, and (d) confuses the two.
> **Key point:** "No longer exists" refers to validity over time, not to physical removal.

### Q30. The author closes with "The catch is that…". The word *catch* signals

- (a) that a technique has been described and now its cost must be stated
- (b) that a trick used by the author is about to be revealed
- (c) that the previous paragraphs were unreliable.
- (d) that the channel matrix cannot be estimated at all

> **Type:** Conceptual
> **Answer:** It signals that a technique has been described and its cost must now be stated (Option a).
> **Solution:** The passage first builds an argument in favour of multiple antennas and only then names a limitation, which is the standard "benefit, then catch" structure. (b) and (c) misread *catch* as secrecy or doubt, and (d) is contradicted by the passage's statement that the matrix is inferred.
> **Key point:** "The catch is" is a signpost for the counter-argument, not the conclusion.

---

**Passage 7.** A transform is a change of coordinates, and the theory of the Laplace transform says that one such change is legal only inside a strip. The transform F(s) of x(t) converges when the integral of x(t) times e^(−st) from 0 to infinity exists; the set of s for which it exists is the region of convergence. For a right-sided signal growing no faster than an exponential, the region is a half plane; for one existing only on a finite interval, it is the whole s-plane; for a two-sided signal whose left tail grows faster, a vertical strip whose two edges are fixed by the two tails. Two signals whose transforms are algebraically identical but whose regions differ are different signals, which is why an answer quoting a rational function without its region is not yet an answer.

### Q31. Which option best captures the main idea of Passage 7?

- (a) The Laplace transform is the only change of coordinates in which a signal can be analysed.
- (b) A Laplace transform is valid only where its integral converges, and the region of convergence is part of the transform's meaning, not an afterthought.
- (c) The region of convergence of a signal is fixed entirely by the number of poles in its rational transform.
- (d) A two-sided signal with a fast-growing left tail has a region of convergence that is the entire s-plane.

> **Type:** MCQ
> **Answer:** The transform is valid only where its integral converges, and the region of convergence is part of its meaning (Option b).
> **Solution:** Sentence 2 defines convergence, sentence 3 classifies the regions, and sentence 4 makes the region constitutive of the transform. Option (a) is contradicted by "a transform is a change of coordinates" as a general remark. Option (c) reverses the dependence — the region comes from the signal's tails, not from the pole count. Option (d) is the opposite of what the passage says for the two-sided case.
> **Key point:** "Which is it" is settled by what the text says defines the quantity.

### Q32. For the signal x(t) = e^(−2t) for t > 0 and x(t) = 0 otherwise, the passage's own classification gives the region of convergence as

- (a) the entire s-plane
- (b) a vertical strip with two finite edges
- (c) the half plane Re(s) > −2
- (d) the half plane Re(s) < −2

> **Type:** MCQ
> **Answer:** The half plane Re(s) > −2 (Option c).
> **Solution:** The signal is right-sided and decays, so it falls under "a right-sided signal growing no faster than an exponential", for which the region is a half plane. The integrand behaves like e^(−(s+2)t), which decays only when Re(s) > −2. Option (a) is the finite-duration case, (b) the two-sided strip, and (d) the wrong half plane.
> **Key point:** A right-sided decaying signal always gives Re(s) > (decay rate).

### Q33. Why does the author say an answer quoting "a rational function without its region is not yet an answer"?

- (a) Because rational functions are hard to evaluate.
- (b) Because the same rational function with a different region of convergence corresponds to a different signal.
- (c) Because the region of convergence determines the number of poles.
- (d) Because the region of convergence is normally given in the time domain.

> **Type:** MCQ
> **Answer:** Because the same rational function with a different region of convergence corresponds to a different signal (Option b).
> **Solution:** Sentence 4 states it directly: "Two signals whose transforms are algebraically identical but whose regions differ are different signals." So an answer that omits the region is not wrong, it is incomplete — the same formula plus a different region names a different time-domain signal. (a), (c) and (d) are each contradicted by the passage.
> **Key point:** An incomplete specification is not the same as a wrong one.

### Q34. [GATE-2] A signal is two-sided, with a left tail that decays as t → −∞ and a right tail that grows as e^(3|t|) as t → +∞. The passage's classification predicts that the region of convergence is

- (a) the entire s-plane, because both tails are integrable for some real s
- (b) a right half plane, because only the left tail matters for convergence from 0 to ∞
- (c) a vertical strip, with the right edge set by the left tail and the left edge set by the right tail
- (d) empty, because no single s makes both tails decay

> **Type:** MCQ
> **Answer:** A vertical strip, with the right edge set by the left tail and the left edge set by the right tail (Option c).
> **Solution:** The passage gives the two-sided strip explicitly, with the "two edges … fixed by the two tails", so a two-sided signal whose tails are shaped differently yields a strip rather than a half plane. A half plane (b) arises only when one tail is absent; the entire s-plane (a) only when both tails decay; and (d) ignores that between the two convergence thresholds both tails do decay, so the set of admissible s is non-empty.
> **Key point:** Strip edges come from the two tails; a half plane is the one-tail special case.

---

## Section 2. Reading comprehension on general-science and current-affairs passages

**Passage 8.** Seawater and fresh water refuse to mix until a pressure of roughly 70 atmospheres is applied, at which point the denser side pushes back through a membrane permeable to water but not to salt. That single fact is the whole of reverse-osmosis desalination, and the engineering that follows is entirely about damage. A municipal plant must feed seawater at 55 bar through a membrane with pores a tenth of a micron across, and must do so without letting the pressure collapse, without fouling the membrane with the growth that feeds on the brine, and without spending more energy than the alternative it was chosen over. The last is why recovery fractions reach the high tens of percent but never a hundred: pushing more product out concentrates the reject until its osmotic pressure opposes the very pump doing the pushing.

### Q35. Which option best captures the main idea of Passage 8?

- (a) Reverse-osmosis desalination is cheaper than thermal distillation but cannot achieve a recovery fraction of a hundred per cent.
- (b) Desalination by reverse osmosis rests on one pressure-driven fact, and the practical difficulties all come from damage and energy.
- (c) Membrane fouling by brine is the principal reason no desalination plant has ever reached a recovery fraction of a hundred per cent.
- (d) A membrane with pores a tenth of a micron across is required in order to keep the brine from passing through with the product.

> **Type:** MCQ
> **Answer:** Desalination rests on one pressure-driven fact, and the practical difficulties come from damage and energy (Option b).
> **Solution:** Sentence 2 says the engineering "is entirely about damage", sentence 3 lists the three hazards and the last sentence names energy as decisive. Option (a) is true but partial — the passage never compares costs with thermal distillation. Option (c) promotes one of three listed hazards to sole cause, and the last sentence actually names the osmotic back-pressure. Option (d) is invented: the passage says the pores are small, not why.
> **Key point:** A main idea must cover the whole passage, not its most vivid detail.

### Q36. [GATE-2] According to Passage 8, what would most directly allow a plant to raise its recovery fraction?

- (a) Widening the membrane pores so that more water passes per unit pressure.
- (b) Increasing the pressure fed to the membrane well beyond 55 bar.
- (c) Diluting the reject stream continuously with additional permeate.
- (d) Removing the biological growth that feeds on the brine.

> **Type:** MCQ
> **Answer:** Diluting the reject stream continuously with additional permeate (Option c).
> **Solution:** The final clause says the barrier is that concentrating the reject builds an osmotic pressure "its osmotic pressure opposes the very pump doing the pushing". The only option that keeps the reject from concentrating is (c). Option (a) would let salt through and destroy the separation. Option (b) faces exactly the same back-pressure, which is the point the passage makes. Option (d) removes a fouling hazard the passage lists separately but does not tie to recovery fraction.
> **Key point:** Identify the stated *barrier* before evaluating the proposed fixes.

### Q37. The words "The last of these" in the first sentence of the last paragraph refer to

- (a) the pressure collapsing
- (b) the membrane fouling with biological growth
- (c) spending more energy than the alternative method
- (d) feeding seawater at 55 bar through fine pores

> **Type:** MCQ
> **Answer:** Spending more energy than the alternative method (Option c).
> **Solution:** The preceding sentence lists three obligations joined by "without": letting the pressure collapse, fouling the membrane, and spending more energy. "The last" is the third. The next sentence then explains that it is the energy question that caps the recovery fraction, which confirms the referent.
> **Key point:** Pronoun reference in a list of three resolves to the final item, and context confirms it.

### Q38. Why does the author give both the figure "55 bar" and the figure "a tenth of a micron across"?

- (a) To show that high pressure and fine pores are the two independent causes of membrane damage.
- (b) To convey how thin the margin is between the pressure the membrane must see and the pressure it can survive.
- (c) To compare the membrane with the pumps that drive it.
- (d) To show that the plant's energy bill is dominated by pumping losses.

> **Type:** Conceptual
> **Answer:** They convey how thin the margin is between the pressure the membrane must see and the pressure it can survive (Option b).
> **Solution:** The two figures are attached to the same clause — what the plant "must" do — and the very next list is a set of things the plant must do *without*, including "letting the pressure collapse". Together they describe a component that is simultaneously loaded and fragile. Options (a), (c) and (d) attribute causation or comparison that the passage does not assert.
> **Key point:** Two figures in one clause usually characterise a single object, not two causes.

### Q39. The phrase "The last of these is why the literature keeps reporting…" shows the author

- (a) doubting that the recovery fraction can be raised further by any means
- (b) reporting an industry limitation with a stated physical cause, without polemics
- (c) arguing that reverse osmosis should be abandoned in favour of thermal methods.
- (d) complaining about the quality of the published literature.

> **Type:** MCQ
> **Answer:** Reporting an industry limitation with a stated physical cause, without polemics (Option b).
> **Solution:** The author neither endorses nor condemns: the limitation is attributed to a mechanism, and the colon expands it. Option (a) overstates the finality ("never a hundred" is about the literature, not about physics). Option (c) has no support — thermal methods are only named as "the alternative it was chosen over". Option (d) reads "the literature" as a complaint, which the neutral wording contradicts.
> **Key point:** "The literature keeps reporting X" is evidence of a settled empirical limit, not an opinion.

### Q40. [GATE-2] A plant raises its recovery fraction from 50% to 75%, rejecting the same mass of salt. Given only the arithmetic the passage makes explicit, the reject stream will

- (a) carry the same mass of salt in three-quarters of its former volume, so its concentration rises
- (b) carry three-quarters of the former mass of salt, so its concentration falls
- (c) carry the same concentration, because the salt load is unchanged
- (d) carry twice the mass of salt, because the pressure has doubled

> **Type:** MCQ
> **Answer:** The same mass of salt in three-quarters of its former volume, so its concentration rises (Option a).
> **Solution:** The passage's final clause states the mechanism: "pushing more product out concentrates the reject". Rejecting the same salt into a smaller remaining volume can only raise its concentration, which is what then opposes the pump. (b) would require the salt itself to be lost; (c) contradicts "concentrates the reject"; (d) invents a pressure change the passage never links to recovery.
> **Key point:** More product out at fixed salt load means a smaller, saltier reject.

---

**Passage 9.** Solar and wind generation are cheap enough to build, and neither is of any use at eleven at night. A grid balancing load minute by minute must move energy across hours, and for two decades the answer was pumped storage: push water uphill when the sun is out, and the round trip returns some three-quarters of what went in. Batteries broke the tie on speed — they respond in milliseconds and can be sited where the grid is congested, not where the water is — so they have displaced pumped storage in new-build almost everywhere, while it survives where there is a mountain and cheap water. The honest summary is that the two were never rivals for the same job: one is cheap and slow, the other expensive and fast, and a system needing both keeps both.

### Q41. Which option best captures the main idea of Passage 9?

- (a) Batteries have made pumped storage obsolete everywhere except where geography is favourable.
- (b) Intermittency of renewables creates a need for storage, and pumped storage and batteries serve different halves of that need.
- (c) Pumped storage is cheaper and batteries are faster, so a grid should choose between them on price.
- (d) Renewables are now cheap enough that the remaining cost of a grid is entirely its storage.

> **Type:** MCQ
> **Answer:** Intermittency of renewables creates a need for storage, and the two storage technologies serve different halves of that need (Option b).
> **Solution:** Sentence 2 names the need, sentence 3 contrasts the two technologies, and the last sentence states the summary. Option (a) inverts the final sentence ("a system needing both keeps both"). Option (c) makes it a price decision, which the passage's "never rivals" denies. Option (d) turns "cheap enough to build" into "cheap enough to build", which is not claimed.
> **Key point:** A summary sentence at the end of a passage is usually the main idea.

### Q42. The passage says pumped storage "survives where there is a mountain and cheap water". The most direct reading is that

- (a) such places have mountains because they store water
- (b) where a mountain and cheap water exist, the cost gap that batteries must overcome is largest, so pumped storage remains competitive
- (c) pumped storage requires cheap water in every country that has it.
- (d) batteries cannot be used in countries with mountains.

> **Type:** MCQ
> **Answer:** Where a mountain and cheap water exist, the cost gap that batteries must overcome is largest, so pumped storage remains competitive (Option b).
> **Solution:** The preceding clause has already established pumped storage as the cheap-and-slow option. A mountain plus cheap water is exactly the input that makes "cheap" achievable, so its presence closes the gap that displaces the technology elsewhere. Option (a) reverses cause and effect; (c) and (d) attach a "only/never" that the passage does not state.
> **Key point:** A survival clause explains why the option did not lose everywhere.

### Q43. Why does the author give the figure "some three-quarters of what went in"?

- (a) To show that a pumped-storage round trip loses a quarter of its energy and is therefore a poor candidate for long-duration duty.
- (b) To show that the round trip is nearly lossless.
- (c) To establish the price of water pumped uphill.
- (d) To compare the round trip with a battery's efficiency.

> **Type:** MCQ
> **Answer:** It shows that a pumped-storage round trip loses about a quarter of its energy and is therefore a poor candidate for loss-sensitive duty (Option a).
> **Solution:** "some three-quarters of what went in" is by definition a 25% loss, and the number is inserted where the author is crediting pumped storage — but the qualifier "some" keeps it from being exact. The efficiency figure is stated without being compared with any battery figure, so (b), (c) and (d) go beyond the text.
> **Key point:** A retained fraction is a loss figure stated indirectly.

### Q44. "Batteries broke the tie on speed" uses the idiom of a competition. Reading it in context, it means that

- (a) batteries won a public contest between the two technologies.
- (b) where the two were previously equal, speed is the dimension on which batteries established a decisive advantage
- (c) the two technologies were competing only over speed.
- (d) batteries are the only technology that can respond in milliseconds.

> **Type:** MCQ
> **Answer:** The two were previously equal, and speed is the dimension on which batteries established a decisive advantage (Option b).
> **Solution:** The dash that follows supplies the reason: "they respond in milliseconds and can be sited where the grid is congested, not where the water is". "Broke the tie" therefore names a tie-breaking dimension, and the closing sentence adds that the two were never on the same axis at all. Options (a) and (c) read a metaphor as a report, and (d) is an absolute claim the passage does not make.
> **Key point:** Competition idioms in technical prose usually name a dimension of difference.

### Q45. The last sentence is introduced by "The honest summary is that…". The word *honest* implies that the author regards

- (a) the earlier paragraphs as a promotional exaggeration
- (b) common descriptions of the storage market as oversimplified
- (c) the literature on pumped storage as unreliable
- (d) the cost of batteries as deliberately hidden
> **Type:** MCQ
> **Answer:** Common descriptions of the storage market as oversimplified (Option b).
> **Solution:** "Honest" contrasts with what is usually said, and what the passage has just said is that the "displaced pumped storage in new-build almost everywhere" story is a simplification. The corrective is the "never rivals for the same job" claim. Options (a), (c) and (d) each invent a target for the honesty, none of which the passage identifies.
> **Key point:** "The honest X" flags the preceding material as the accepted, not the true, version.

### Q46. [GATE-1] Which of the following statements is TRUE according to Passage 9?

- (a) Pumped storage has been completely replaced by batteries in every country.
- (b) A grid with both mountains and cheap water may keep building pumped storage because it remains the cheap option.
- (c) Batteries can only be sited where there is water.
- (d) Solar and wind output is highest at eleven at night.

> **Type:** MCQ
> **Answer:** A grid with both mountains and cheap water may keep building pumped storage because it remains the cheap option (Option b).
> **Solution:** The passage says pumped storage "survives where there is a mountain and cheap water" and calls it the cheap-and-slow option. (a) contradicts "survives"; (c) inverts the sentence about siting ("where the grid is congested, not where the water is"); (d) contradicts the opening line.
> **Key point:** Check each option against the sentence that most nearly contains it.

---

**Passage 10.** For three centuries everything known about other stars came from the faint arithmetic of their light: how bright, how red, how much it wobbles. Spectroscopy added a third dimension and turned starlight into a chemical inventory, but still required the light to arrive. That requirement broke in 1995, when a planet orbiting a star in Pegasus was found to tug that star by about a metre per second, and the story has been repeated with better instruments several thousand times since. It matters because the method does not merely detect a planet, it measures the star's velocity, and a periodic velocity curve can be distinguished from the single drift of a sunspot or a magnetic cycle. What it cannot do is see the planet, and for nine hundred confirmed planets the planet remains a point of mathematics.

### Q47. [GATE-2] Which option best captures the main idea of Passage 10?

- (a) The radial-velocity method found most known exoplanets by measuring a star's periodic velocity wobble, not by imaging the planet.
- (b) Spectroscopy is a more powerful planet-finding tool than any velocity measurement.
- (c) Planetary systems around other stars are rare, and only a few thousand are known.
- (d) Three centuries of astronomy produced almost no knowledge of stars other than the Sun.

> **Type:** MCQ
> **Answer:** The velocity-wobble method found most known exoplanets by measuring the star's periodic wobble, not by imaging (Option a).
> **Solution:** The 1995 episode, the reason the method "matters", and the closing sentence about nine hundred planets all support (a). Option (b) is contradicted — spectroscopy "still required the light to arrive". Option (c) inverts the number, and option (d) says "everything known about other stars", which the passage's first sentence denies.
> **Key point:** The method plus its limitation together usually form the main idea.

### Q48. Why does the passage insist that the velocity curve be "periodic rather than a single drift"?

- (a) Because a single drift cannot be measured accurately by any instrument.
- (b) Because only a repeating signature distinguishes a planet's pull from other causes of stellar wobble.
- (c) Because a planet's gravitational pull is periodic only when it is very close to its star.
- (d) Because stellar magnetic cycles are perfectly periodic.

> **Type:** MCQ
> **Answer:** Only a repeating signature distinguishes a planet's pull from other causes of stellar wobble (Option b).
> **Solution:** The sentence names the competing explanations — "a sunspot or a magnetic cycle" — and says the periodic curve can be told apart from them. So periodicity is the discriminator, not an accuracy issue. Option (c) is false physics and is not in the passage; option (d) would defeat the distinction the sentence exists to make.
> **Key point:** A contrast stated in the text is the reason the preceding clause is there.

### Q49. "The planet itself remains a point of mathematics" means that

- (a) the planet's orbit is described by an equation but the planet has never been detected by any means
- (b) the planet exists only as a theoretical prediction with no observational basis.
- (c) the planet's mathematical description is inaccurate.
- (d) the planet has been imaged but not measured.
> **Type:** MCQ
> **Answer:** The planet's orbit is described by an equation but the planet has never been detected by any means (Option a).
> **Solution:** The sentence before it says the method "cannot do" is see the planet, so the knowledge is entirely kinematic — an inferred position from a velocity curve. Option (b) is wrong because the detection is real; (c) and (d) have no basis in the passage.
> **Key point:** "Point of mathematics" = inferred quantity, never observed.

### Q50. "The faint arithmetic of their light" is a figure of speech. Its function is to

- (a) suggest that starlight is physically very weak.
- (b) present the extraction of stellar properties as the manipulation of measured quantities, and so as a source of information
- (c) imply that early astronomers made computational errors.
- (d) express the author's admiration for precision photometry.
> **Type:** MCQ
> **Answer:** It presents the extraction of stellar properties as manipulation of measured quantities, hence as a source of information (Option b).
> **Solution:** The colon expands it — "how bright, how red, how much it wobbles" — which are all measured quantities converted into properties. "Arithmetic" is being used for a small, careful calculation, not for a deficiency. Option (a) confuses faintness of signal with thinness of information, and (c) and (d) are unsupported.
> **Key point:** A colon after a metaphor defines the metaphor.

### Q51. Why does the author mention sunspots and magnetic cycles at all?

- (a) To show that stars have surface activity comparable to the Sun's.
- (b) To give the reader the competing explanations that a periodic curve must be distinguished from.
- (c) To argue that sunspots are the most common cause of known exoplanet detections.
- (d) To explain why the Pegasus planet was found in 1995.
> **Type:** Conceptual
> **Answer:** To give the reader the competing explanations that a periodic curve must be distinguished from (Option b).
> **Solution:** The phrase is attached by "can be distinguished from", so the two phenomena exist in the sentence solely as rivals to be ruled out. Option (c) reverses the logic — they are what must be excluded, not what is found. Options (a) and (d) are topics the passage never develops.
> **Key point:** Items named as "distinguished from" are alternatives, not results.

### Q52. [GATE-2] According to Passage 10, the decisive advantage of the velocity method over earlier methods is that it

- (a) provides a direct photograph of the planet in visible light
- (b) yields the planet's mass and its orbital period from the same velocity curve
- (c) works only for stars close to the Sun
- (d) requires no light from the star to reach the observer
> **Type:** MCQ
> **Answer:** The planet's mass and its orbital period come from the same measured velocity curve (Option b).
> **Solution:** Earlier methods, including spectroscopy, "still required the light to arrive"; the velocity method works from the star's motion, measured through its spectral lines. The measured curve's period gives the orbital period and its amplitude gives a minimum mass through Kepler's laws, so both come from one observable. (a) is excluded by the closing sentence; (c) is not discussed; (d) is wrong because the method still relies on the star's spectrum.
> **Key point:** Amplitude and period of a velocity curve give minimum mass and orbital period.

---

**Passage 11.** Every antibiotic ever put into a clinic was discovered by accident, by a mould or fungus that made a chemical hostile to a bacterium, and each was then copied chemically into look-alikes. The bacteria that survived the first copy did so by accident too, and passed the trick to their descendants on small circular DNA. Population pressure, meaning the sustained use of one drug over years, selects for that trick at the rate at which the drug is consumed. This is why resistance is not a mystery of evolution but an accounting problem: a hospital's total consumption of a drug, summed over years, predicts local resistance better than any property of the drug, and a programme banning only the worst offenders cannot see the drug used steadily, correctly and for good reasons, which is quietly making its patients resistant.

### Q53. Which option best captures the main idea of Passage 11?

- (a) Antibiotic resistance arises wherever a drug is used, and its local intensity is best predicted by cumulative consumption rather than by the drug's chemistry.
- (b) Bacteria that develop resistance are a natural consequence of evolution and cannot be controlled by prescribing policy.
- (c) New antibiotics should be discovered by screening fungi rather than by modifying existing molecules.
- (d) Hospitals that use antibiotics responsibly still generate resistance, so guidelines are ineffective.

> **Type:** MCQ
> **Answer:** Resistance arises wherever a drug is used, and its local intensity is best predicted by cumulative consumption, not by the drug's chemistry (Option a).
> **Solution:** Sentences 2 and 3 make both halves of (a) explicit. Option (b) is refused by "not a mystery of evolution"; option (c) inverts the historical order in sentence 1; option (d) accepts the premise but adds a conclusion the passage explicitly denies.
> **Key point:** "Not X but Y" in the middle of a passage states the author's real claim.

### Q54. The passage says a programme that "bans only the worst offenders has no way to see" a steadily used drug. The implied reason is that

- (a) steadily used drugs are not officially classified as antibiotics
- (b) steady, clinically justified use is exactly what produces resistance, and it is invisible to a policy aimed at extremes
- (c) regulators do not record consumption data at all
- (d) the bacteria responsible develop resistance only against banned drugs
> **Type:** MCQ
> **Answer:** Steady, clinically justified use is exactly what produces resistance, and it is invisible to a policy aimed at extremes (Option b).
> **Solution:** The final clause describes a drug "used steadily, correctly and for good reasons" as the one "quietly making its patients resistant". A policy that acts on the worst offenders therefore misses precisely this case. Options (a), (c) and (d) are not supported by anything in the passage.
> **Key point:** Ask what kind of case a stated policy cannot see.

### Q55. "A small piece of circular DNA that can be copied and passed on again" most plausibly denotes

- (a) a bacterial chromosome
- (b) an independently replicating plasmid that can be transferred between bacteria
- (c) a viral capsid
- (d) a bacterial ribosome
> **Type:** MCQ
> **Answer:** An independently replicating plasmid that can be transferred between bacteria (Option b).
> **Solution:** A chromosome is a single large non-circular molecule; a capsid is protein, not DNA; a ribosome is a ribonucleoprotein complex. A small circular self-replicating DNA element that carries a resistance trait and can be copied and passed on is the definition of a plasmid.
> **Key point:** Small + circular + self-replicating + transmissible ⇒ plasmid.

### Q56. "Resistance is not a mystery of evolution but an accounting problem" is best understood as saying that

- (a) resistance has an evolutionary mechanism and an economic one, and the passage is concerned with the second
- (b) resistance should not be studied by evolutionary biologists
- (c) the evolutionary account of resistance is false.
- (d) hospitals should keep better financial records.

> **Type:** Conceptual
> **Answer:** Resistance has both an evolutionary mechanism and a supply-and-demand one, and the passage is discussing the second (Option a).
> **Solution:** The passage has already described the mechanism (transfer of the trick, selection by pressure); the "but" then redirects attention to consumption as the predictive variable. "Accounting" here is bookkeeping of cumulative use, not finance, so (d) misreads the metaphor, and (c) contradicts the earlier sentences.
> **Key point:** "Not X but Y" redirects, it does not usually delete X.

### Q57. The tone of Passage 11 is best described as

- (a) alarmist, calling for an immediate halt on all antibiotic use
- (b) sober and corrective, using a familiar mechanism to make an unglamorous point
- (c) sarcastic about the pharmaceutical industry
- (d) nostalgic about the era before resistance
> **Type:** MCQ
> **Answer:** Sober and corrective, using a familiar mechanism to make an unglamorous point (Option b).
> **Solution:** The vocabulary is neutral-technical ("population pressure", "selects for", "predictor of"), and the closing clause is quiet — "quietly making its patients resistant". There is no imperative, no exclamation, and no attack on any party. Option (a) proposes a policy the passage would contradict, and (c) and (d) need evaluative words that are absent.
> **Key point:** Absence of imperative verbs is strong evidence against an alarmist tone.

### Q58. [GATE-1] Which conclusion follows from Passage 11?

- (a) A drug with a long history of safe use is less likely to select resistance than a newer drug.
- (b) Two hospitals that consume the same drug at similar total rates over similar periods are likely to face similar resistance pressure.
- (c) Banning the most over-prescribed drug will eliminate resistance in a country within a decade.
- (d) Resistance genes spread only between related species.
> **Type:** MCQ
> **Answer:** Two hospitals with similar total consumption over similar periods face similar resistance pressure (Option b).
> **Solution:** The passage's central claim is that "a hospital's total consumption of a drug, summed over years, predicts local resistance better than any property of the drug", so equal consumption implies equal pressure. (a) makes drug properties the predictor, which is the position the passage rejects; (c) is refuted by the last clause; (d) contradicts "passed on" between organisms.
> **Key point:** The passage's own predictive rule answers the question directly.

---

**Passage 12.** A river does not stop being a river at the sea; it stops when its speed drops below what its sediment can carry. That is why a delta forms at the Ganges and the Mississippi and not at the Congo, though all three carry comparable sediment loads, and why the Niger has built an inland fan that looks almost exactly like a coastal one. The variable is not sediment supply but its ratio to the water's capacity to move it. Increase the water without the sediment and the flow spreads its load thinly on the shelf; increase the sediment without the water and the mouth chokes, the channel switches course, and the delta shifts sideways in a few years. Between those failures sits a narrow band, and much of a delta's history is spent creeping back toward its middle.

### Q59. Which option best captures the main idea of Passage 12?

- (a) A delta exists where a river's sediment load is matched by the water's capacity to carry it, and departures in either direction destroy it.
- (b) Large rivers such as the Ganges and the Mississippi are the only rivers in the world that build deltas.
- (c) Inland deltas are geologically impossible and the Niger's feature has another explanation.
- (d) Deltas form wherever a river meets a standing body of water.

> **Type:** MCQ
> **Answer:** A delta exists where the sediment load is matched by the water's capacity to carry it, and either departure destroys it (Option a).
> **Solution:** The ratio sentence states the criterion, and the two following sentences test the two failure directions. Option (b) is refuted by the Niger. Option (c) is denied by "looks almost exactly like a coastal one". Option (d) repeats the opening line but stops before the actual condition.
> **Key point:** A "the variable is not X but the ratio of…" sentence is the passage's thesis.

### Q60. [GATE-2] The Congo's failure to build a coastal delta is attributed to its

- (a) unusually small sediment load
- (b) unusually large sediment load
- (c) unusually large discharge relative to its sediment load
- (d) unusually small discharge relative to its sediment load

> **Type:** MCQ
> **Answer:** Unusually large discharge relative to its sediment load (Option c).
> **Solution:** The passage states that all three rivers carry "comparable sediment loads", so the sediment supply is ruled out. The variable is the ratio of supply to carrying capacity, so the only remaining explanation is that the Congo has more water for the same sediment. That is precisely the first failure case: "it stops when its speed drops below what its sediment can carry".
> **Key point:** Eliminate the factor the passage has already held equal across the cases.

### Q61. The two failure cases described are best summarised as

- (a) too little water for the sediment, and too much water for the sediment
- (b) too little sediment, and too much sediment
- (c) a channel that is too deep, and a channel that is too shallow
- (d) a coastline that advances, and a coastline that retreats

> **Type:** MCQ
> **Answer:** Too little water for the sediment, and too much water for the sediment (Option a).
> **Solution:** "Increase the water without the sediment" is water in excess; "increase the sediment without the water" is water in deficit. Both are stated as failures, so the water is the variable that can be too big or too little. Options (b) and (c) hold water constant, and (d) is a consequence the passage never frames as a cause.
> **Key point:** Identify the held-constant variable before naming the two failure directions.

### Q62. In "the mouth chokes, the channel switches course", the clause about the switching describes

- (a) erosion of the delta's seaward edge
- (b) the sudden relocation of the main channel to a new course across the fan, which relocates the deposition
- (c) the tidal reopening of a blocked distributary
- (d) the drying of the river during drought
> **Type:** MCQ
> **Answer:** The sudden relocation of the main channel to a new course across the fan, which relocates the deposition (Option b).
> **Solution:** It follows from choking: with more sediment than the flow can move, the channel's gradient is reduced, and the flow re-enters a former course. The next clause — "the delta shifts sideways" — is the consequence the author attaches to it. Option (a) is a different, gradual process, and (c) and (d) are not described.
> **Key point:** Read a clause in sequence with the consequence that follows it.

### Q63. The author calls the band between the two failures "narrow" and says a delta "creeps back toward the middle of it". The rhetorical effect is to

- (a) present delta formation as a stable, self-correcting process rather than a fixed achievement
- (b) suggest that deltas are geologically transient and worthless.
- (c) claim that delta formation is unpredictable.
- (d) imply that rivers are unlikely to reach the sea.
> **Type:** MCQ
> **Answer:** It presents delta formation as a stable, self-correcting process rather than a fixed achievement (Option a).
> **Solution:** The word "creeping" is a deliberate contrast with the sudden switching described earlier, and "back toward its middle" implies repeated return to the balance point. That makes deltas look like a system with a restoring tendency. Options (b), (c) and (d) each contradict the balance the author keeps returning to.
> **Key point:** A metaphor for slow motion can be the argument, not decoration.

### Q64. [GATE-1] Which change would, by the passage's own rule, be most likely to build a coastal delta at the Congo's mouth?

- (a) Halving the Congo's water discharge while leaving its sediment load unchanged
- (b) Increasing the Congo's water discharge by a factor of two
- (c) Doubling the Congo's sediment load with no change in discharge
- (d) Building a dam on the Congo and trapping all its sediment

> **Type:** MCQ
> **Answer:** Halving the water discharge while leaving the sediment load unchanged (Option a).
> **Solution:** The variable is the ratio of sediment supply to carrying capacity, and the Congo is already on the "too much water" side. Reducing the water moves the ratio back toward the balance band. (b) and (c) both push it further out, and (d) removes the sediment supply entirely, which the passage's failure cases do not include but which plainly cannot build a delta.
> **Key point:** Determine which side of the band the case sits on, then move it toward the middle.

---

## Section 3. Vocabulary in context

Each item gives a short context in which the target word carries a definite sense. Choose the
option that matches that sense, not the word's most famous sense.

### Q65. "Harmonic distortion is **ubiquitous**: every site measured showed some, and the argument was never whether it existed but which orders dominated."

In the sense carried by the sentence, *ubiquitous* means

- (a) present only under special laboratory conditions
- (b) present essentially everywhere, so its mere presence is not remarkable
- (c) mandated by an applicable standard
- (d) growing steadily from one survey to the next

> **Type:** MCQ
> **Answer:** Present essentially everywhere, so its mere presence is not remarkable (Option b).
> **Solution:** The context supplies the definition itself: "every site measured showed some", and the consequence "never whether it existed" says the existence is not in dispute. Option (c) would need a reference to a standard, which is absent; (d) needs a time trend, which is absent; (a) contradicts "every site".
> **Key point:** "X: <gloss>" defines X in place; trust the gloss, not the memory.

### Q66. "Adding a series resistor at the gate is the standard way to **mitigate** the risk of electrostatic discharge during handling."

- (a) to make the risk more severe
- (b) to measure the risk accurately
- (c) to make the risk less severe without necessarily removing it
- (d) to delay the risk until the device reaches the customer

> **Type:** MCQ
> **Answer:** To make the risk less severe without necessarily removing it (Option c).
> **Solution:** A series resistor is a familiar partial remedy — it limits discharge current but does not abolish the possibility of damage — and that partial character is built into the word *mitigate*. Option (a) is the opposite direction; (b) and (d) describe different verbs.
> **Key point:** *Mitigate* reduces severity; it never means eliminate.

### Q67. "The measured drift velocity agreed with the model, and an independent Hall measurement was used to **corroborate** it."

- (a) to prove the model wrong by re-measuring
- (b) to support the model by evidence that is independent of the original measurement
- (c) to correct an arithmetic slip in the computation
- (d) to reproduce the method so that others can learn it

> **Type:** MCQ
> **Answer:** To support the model by evidence independent of the original measurement (Option b).
> **Solution:** "Independent" plus "corroborate" gives the definition: a second, unrelated line of evidence that agrees. Option (a) is the opposite of corroboration; (c) describes a different function entirely; (d) is teaching, not verification.
> **Key point:** *Corroborate* is support from a source independent of the original.

### Q68. "The **ostensible** reason for the guard band was component tolerance, though the design notes make clear that it was also there to absorb model error."

- (a) genuine, and the only reason on record
- (b) concealed, and forbidden to be written down
- (c) presented as the reason but not the whole or the real one
- (d) the reason recorded only in the private notes

> **Type:** MCQ
> **Answer:** Presented as the reason but not the whole or the real one (Option c).
> **Solution:** The word is set against the "though" clause, which supplies a second, larger purpose. So *ostensible* = outwardly stated, possibly not the operative one. Option (a) denies the gap that "though" creates; (b) and (d) misread it as secrecy.
> **Key point:** *Ostensible* flags the stated reason, which a contrast usually undercuts.

### Q69. "Running the junction above its rated temperature will **exacerbate** the leakage rather than cure it."

- (a) to relieve and reduce
- (b) to make an already bad condition worse
- (c) to correct by compensating elsewhere
- (d) to make public

> **Type:** MCQ
> **Answer:** To make an already bad condition worse (Option b).
> **Solution:** The object is "the leakage", a fault already present, and the "rather than cure it" clause marks the direction. That fixes the sense as aggravation. Options (a) and (c) invert the direction; (d) is the unrelated sense of publishing.
> **Key point:** *Exacerbate* needs a pre-existing negative; check the object word.

### Q70. "The review found the species harmless in the active region, but warned that the same species is not **innocuous** near the oxide interface."

- (a) harmless in the situation the context describes
- (b) harmful in every situation without exception
- (c) harmful only once a dose threshold is crossed
- (d) untested and therefore unassessed

> **Type:** MCQ
> **Answer:** Harmless in the situation the context describes (Option a).
> **Solution:** The sentence is explicitly location-dependent: harmless in the active region, not innocuous at the interface. So the word means "harmless", scoped to a stated context. Option (b) breaks that scoping, (c) introduces a dose notion the sentence has no use for, and (d) is refuted because the review *did* assess it.
> **Key point:** Context-sensitive harmlessness: read the "but" clause to find the limit.

### Q71. "The specification is notoriously **nebulous**: 'suitable response time' is quoted without saying whether it means settling time, rise time or delay."

- (a) so precisely worded that it admits only one reading
- (b) so loosely worded that careful engineers read different requirements out of it
- (c) obsolete, and no longer applied by anyone
- (d) deliberately obscure, in order to hold down the quoted price

> **Type:** MCQ
> **Answer:** So loosely worded that careful engineers read different requirements out of it (Option b).
> **Solution:** The colon lists three defensible readings of one phrase, which is exactly the situation *nebulous* names. Option (a) is the opposite; (c) needs a statement about age; (d) attributes a motive that the context never mentions.
> **Key point:** Vague wording is diagnosed by the number of defensible readings.

### Q72. "**Proponents** of software-defined networking argue that control loops in the data plane can react in microseconds, which no human operator can do."

- (a) people who hold and defend the position
- (b) people who oppose the position
- (c) people who report the position without endorsing it
- (d) people paid to promote the position

> **Type:** MCQ
> **Answer:** People who hold and defend the position (Option a).
> **Solution:** "Argue" is the giving-away verb: proponents are holders of a position who argue for it. Option (b) is the antonym; (c) describes a reporter; (d) adds a motive the sentence does not supply.
> **Key point:** Follow the verb — *proponents argue for*, *opponents argue against*.

### Q73. Context: "The committee's finding was **unequivocal**: no further investigation was required."

In which of the following sentences is the bolded word used in the sense carried by the context?

- (a) Her equivocal reply — agreeing on Monday, disagreeing on Tuesday — was the opposite of an unequivocal one.
- (b) The book is equivocal on free will, never having said anything whatever about it.
- (c) The two editions are equivocal, one printing 1911 and the other 1922.
- (d) The drug is equivocal in two patients, curing one and failing on the other.

> **Type:** MCQ
> **Answer:** The equivocal reply that agreed on Monday and disagreed on Tuesday (Option a).
> **Solution:** In the context, *unequivocal* means admitting only one interpretation, so *equivocal* must mean admitting more than one. (a) is exactly that. (b) is silence, not ambiguity; (c) is flat contradiction; (d) is inconsistent outcome, which is a different kind of indecision. Only (a) gives a single statement with two readings.
> **Key point:** Contradiction, silence and inconsistency are not ambiguity.

### Q74. "The paper **juxtaposes** a photograph of the prototype board with a plot of that board's measured noise floor, so the reader can see which layout feature is responsible."

- (a) places two things side by side so that they can be compared
- (b) substitutes a better object for an inferior one
- (c) demonstrates that the two things contradict each other
- (d) defers the second thing until the first is finished

> **Type:** MCQ
> **Answer:** Places two things side by side so that they can be compared (Option a).
> **Solution:** The purpose clause "so the reader can see which layout feature is responsible" is only achievable by comparison, and juxtaposition is the standard term for that juxtaposition of two displayed items. Option (c) confuses juxtaposition with contradiction, which requires a claim, not a placement.
> **Key point:** *Juxtapose* is a verb about placement; it asserts no relationship.

### Q75. "There is an **inherent** delay of one sample period in any loop that samples its error before acting on it."

- (a) introduced later by careless design
- (b) existing as a necessary part of the structure itself
- (c) present only while the loop is out of tune
- (d) removable simply by raising the loop gain

> **Type:** MCQ
> **Answer:** Existing as a necessary part of the structure itself (Option b).
> **Solution:** The delay is attached to the definition of the loop — "any loop that samples its error before acting" — so it cannot be designed out without changing what the loop is. Option (a) and (d) both claim it is removable; (c) needs a fault condition the sentence does not mention.
> **Key point:** *Inherent* = structural and not removable by tuning.

### Q76. "A finite word length **constrains** the representable set of values, so not every sinusoid expressible in theory can be produced by the accumulator."

- (a) restricts the range or set of possibilities
- (b) widens the set of possibilities
- (c) assigns units to the quantities involved
- (d) physically builds the circuit

> **Type:** MCQ
> **Answer:** Restricts the range or set of possibilities (Option a).
> **Solution:** "Finite" and the contrast "not every … in theory" together define the effect: some theoretically valid values become unrepresentable. Option (b) is the opposite; (c) and (d) are senses of the verb used in completely different fields.
> **Key point:** A "finite X constrains Y" sentence fixes *constrain* to the restrictive sense.

### Q77. "The most **salient** feature of the report is not its length but its recommendation to scrap the existing fleet."

- (a) the most noticeable and most important
- (b) the saltiest in taste
- (c) the most recently added
- (d) the most likely to be challenged in court

> **Type:** MCQ
> **Answer:** The most noticeable and most important (Option a).
> **Solution:** "Not its length but its recommendation" is a comparison of importance, so the word carries the sense "standing out". The other three options attach to taste, chronology and litigation, none of which the sentence touches.
> **Key point:** *Salient* means standing out in importance, not standing out in size.

### Q78. "Duty cycling the transmitter between transmissions **alleviates** the average power drawn from the battery."

- (a) makes a burden or difficulty smaller
- (b) makes a burden more severe
- (c) conceals the true figure from the datasheet
- (d) transfers the burden to another party

> **Type:** MCQ
> **Answer:** Makes a burden or difficulty smaller (Option a).
> **Solution:** Duty cycling lowers the time-averaged current, so the battery's burden falls; the object is a burden, which is the setting the word is built for. Option (b) reverses it, and (c) and (d) are unrelated senses.
> **Key point:** *Alleviate* takes a burden, pain or hardship as its object.

### Q79. "The requirement that the tap be welded **precludes** any field replacement of the fuse holder."

- (a) makes impossible in advance
- (b) delays until a later date
- (c) actively encourages
- (d) predicts with high accuracy

> **Type:** MCQ
> **Answer:** Makes impossible in advance (Option a).
> **Solution:** "Any field replacement" is ruled out by the welding requirement, and "precludes" is the verb for ruling out by a prior condition. Option (b) would allow it later, which the sentence denies.
> **Key point:** *Preclude* is stronger than delay: it closes the possibility.

### Q80. "The test suite is **amenable** to automation because every case has a single expected numeric result."

- (a) readily adaptable to a particular treatment or approach
- (b) easily bored and in need of variety
- (c) legally obliged to be performed
- (d) answerable for the outcome of the test

> **Type:** MCQ
> **Answer:** Readily adaptable to a particular treatment or approach (Option a).
> **Solution:** "Amenable to X" is a fixed construction meaning "receptive to X", and the reason given — a single expected result — is a property that suits automation. Option (b) is the personality sense of a different word, and (d) is a homophone trap.
> **Key point:** "Amenable to" is the idiomatic form; it never means answerable.

### Q81. "The datasheet's **derivative** curve gives the probe's output change per degree, which is the number a designer needs for temperature compensation."

- (a) a quantity measuring how fast one quantity changes with respect to another
- (b) something removed from a larger whole
- (c) a legal claim against a supplier
- (d) a product made by copying an original design

> **Type:** MCQ
> **Answer:** A quantity measuring how fast one quantity changes with respect to another (Option a).
> **Solution:** "Change per degree" is the operational definition, and the context is a calibration curve, so the mathematical sense is fixed. Options (b), (c) and (d) are the commoner non-technical senses and none of them fits "per degree".
> **Key point:** The context selects the sense; a unit of "per" signals the calculus sense.

### Q82. "Once the guard band is added, the second checksum is **superfluous**: it can detect nothing the first has not already caught."

- (a) necessary, and difficult to replace
- (b) unnecessary, because something else already does the same job
- (c) placed physically beneath another component
- (d) extraordinarily expensive to implement

> **Type:** MCQ
> **Answer:** Unnecessary, because something else already does the same job (Option b).
> **Solution:** The justification clause "it can detect nothing the first has not already caught" is the definition of redundancy. Option (a) is the antonym; (c) and (d) are senses of other words.
> **Key point:** *Superfluous* is diagnosed by a stated redundancy.

### Q83. "The question about the vendor's subcontractor was designed to make the candidate **feign** surprise, and the candidate obliged."

- (a) pretend to feel a state that is not actually felt
- (b) feel genuine surprise
- (c) physically conceal an object from view
- (d) lose consciousness from shock

> **Type:** MCQ
> **Answer:** Pretend to feel a state that is not actually felt (Option a).
> **Solution:** "Make someone feign X" is a manipulation phrase, and "obliged" confirms that the candidate complied with the request. Option (b) removes the deception the sentence requires; (c) and (d) are different verbs.
> **Key point:** *Feign* requires the pretense to be false.

### Q84. "Interviewers were **reticent** about the score distribution, on the grounds that a candidate who knew it might negotiate."

- (a) reserved and slow to volunteer information
- (b) loud and insistent in their questioning
- (c) unable to retain what they are told
- (d) eager to spend what they have

> **Type:** MCQ
> **Answer:** Reserved and slow to volunteer information (Option a).
> **Solution:** The stated reason — withholding information for a reason — matches the reserved sense. Option (b) is the opposite temperament; (c) and (d) come from *retentive* and *liberal*, not *reticent*.
> **Key point:** *Reticent* is about disclosure; it says nothing about memory or spending.

### Q85. "The reviewer's argument was **cogent** — every step followed from the one before, and the conclusion was hard to dispute."

The word in the sentence is most nearly

- (a) forceful and logically persuasive
- (b) brief and easy to remember
- (c) pleasing in tone
- (d) subtly deceptive

> **Type:** MCQ
> **Answer:** Forceful and logically persuasive (Option a).
> **Solution:** "Every step followed from the one before" describes an unbreakable chain of reasoning, and "hard to dispute" describes the effect on a reader; that pair is the sense of *cogent*. Option (b) is about brevity, which is not praised; (c) is about manner, which is not mentioned; (d) reverses the verdict.
> **Key point:** *Cogent* is about the strength of a logical chain, not its tone.

### Q86. "The subsidy did not create the shortage; it **perpetuated** it by hiding the price signal for another decade."

The word in the sentence is most nearly the opposite of

- (a) bringing an end to
- (b) recording for the first time
- (c) spreading widely
- (d) predicting accurately

> **Type:** MCQ
> **Answer:** Bringing an end to (Option a).
> **Solution:** The context says the shortage existed before the subsidy and continued because of it, so *perpetuate* means "keep something bad going". Its opposite is therefore "end it". Options (b), (c) and (d) are not antonyms of the verb at all.
> **Key point:** Match the antonym to the sense *in the sentence*, not to the dictionary's first entry.

---

## Section 4. Spotting errors

Each sentence below contains exactly one grammatical or usage error. Find it and correct it.

### Q87. Correct the single error: "**A** engineer from the calibration lab presented the drift measurements at the monthly review."

- (a) A → An
- (b) A → The
- (c) engineer → engineers
- (d) presented → had presented

> **Type:** Common-mistake
> **Answer:** A → An
> **Solution:** The indefinite article takes *an* before a vowel **sound**, and the first sound of "engineer" is the /e/ of "engine", not the consonant /dʒ/ that the spelling might suggest. The verb agrees with the singular "engineer", so (c) and (d) introduce new errors, and (b) is not an article choice for an unspecified first mention.
> **Key point:** Article choice follows pronunciation, not spelling.

### Q88. Correct the single error: "The **list** of available part numbers **are** posted on the intranet every Monday."

> **Type:** Common-mistake
> **Answer:** are → is
> **Solution:** The true subject is "list", which is singular, and the prepositional phrase "of available part numbers" sits between it and the verb. Agreement is with the head noun of the subject, not with the nearest noun. Writing "are" agrees with "numbers", which is only the object of the preposition.
> **Key point:** With "the X of Y", the verb agrees with X, not with Y.

### Q89. [GATE-1] Correct the single error: "The **number of hours** the technician spent on the intermittent fault, which cost the plant a full day of output, **were** eventually found to be thirty."

- (a) were → was
- (b) number → numbers
- (c) spent → spends
- (d) remove the comma before "which"

> **Type:** MCQ
> **Answer:** were → was (Option a).
> **Solution:** Two things are at work. First, the head of the subject is "number", singular, so the verb must be "was". Second, a long non-defining clause beginning "which" separates the subject from the verb, which is the classic setting for this agreement error. (b) and (c) would each create a second error, and the comma before a non-defining "which" is correct.
> **Key point:** A long intervening relative clause is where subject–verb agreement slips.

### Q90. Correct the single error: "The transistor was manufactured in 2019, but it **fails** when the junction temperature exceeds 150 °C."

> **Type:** Common-mistake
> **Answer:** fails → failed
> **Solution:** The first verb fixes the time reference in the past, and a coordinated clause joined by "but" shares that reference; the observation about the junction belongs to the same reported time, not to the present. Any other time adverbial — "today", "now", "these days" — would be required to license the present tense.
> **Key point:** Two coordinated clauses share one time frame unless a new time marker appears.

### Q91. Correct the single error: "**One of the students**, together with two of her friends, **were** late for the viva."

> **Type:** Common-mistake
> **Answer:** were → was
> **Solution:** The subject is the singular "one", and a phrase introduced by "together with" is a supplement, not an addition to the subject, so it does not make the subject plural. The same rule governs "as well as", "along with" and "in addition to".
> **Key point:** "Together with", "as well as" and "along with" never pluralise the subject.

### Q92. Correct the single error: "The measurement was carried out **according** the procedure described in Annex B of the standard."

- (a) according → according to
- (b) procedure → procedures
- (c) carried out → carried
- (d) standard → standards

> **Type:** MCQ
> **Answer:** according → according to (Option a).
> **Solution:** "According" is a preposition only when it is followed by "to"; "according the procedure" is ungrammatical because the preposition slot is empty. The rest of the sentence is sound: "the procedure" is correctly singular in the source and "Annex B of the standard" requires no change.
> **Key point:** Some prepositions are inseparable; "according" must take "to".

### Q93. [GATE-1] Correct the single error: "The objectives of the project are **to reduce** the noise floor, **to improve** the isolation **and for lowering** the power consumption."

- (a) for lowering → to lower
- (b) to reduce → reducing
- (c) are → were
- (d) objectives → objective

> **Type:** MCQ
> **Answer:** for lowering → to lower (Option a).
> **Solution:** The three items in a list of objectives introduced by "are" must share one form, and the first two are bare infinitives, so the third must be one too. "for lowering" is the pattern of a preposition plus a gerund, which belongs in a sentence such as "the project is responsible for lowering …", not in this list. (b) would break the same parallelism, (c) has no time marker, and (d) is wrong because the three listed items are genuinely three.
> **Key point:** In a list governed by one verb form, every item takes that form.

### Q94. Correct the single error: "The committee decided **to postpone** the decision, **to ask** for more data **and to reconvene** in March."

> **Type:** Common-mistake
> **Answer:** to ask → asking
> **Solution:** When one item in a list is a plain to-infinitive, the others are normally gerunds or the whole list is rewritten as infinitives; a single "to ask" among "to postpone" and "to reconvene" is inconsistent. The clean fix is either "to postpone the decision, to ask for more data and to reconvene in March" or "postponing the decision, asking for more data and reconvening in March".
> **Key point:** Fix parallelism by making all three items match, not just one.

### Q95. Correct the single error: "The manager told the engineers that the schedule had slipped, and **it** did not inform them of the new deadline."

> **Type:** Common-mistake
> **Answer:** it → he
> **Solution:** "It" has no plausible antecedent: the only singular nouns available are "manager" and "schedule", and the clause's action is performed by a person. "Schedule had slipped" is a subordinate content clause, not a candidate referent, and "informing" a person is not something a schedule does. The pronoun must therefore be "he", referring to the manager.
> **Key point:** Pronouns must match a plausible antecedent, and people act on people.

### Q96. Correct the single error: "**Neither** of the two cables **were** long enough to reach the top of the rack."

> **Type:** Common-mistake
> **Answer:** were → was
> **Solution:** "Neither" is singular in modern standard English and normally takes a singular verb, even when the noun it refers to is plural ("neither of the cables **was** long enough"). "Either" behaves the same way, whereas "none of" normally takes a plural verb.
> **Key point:** *Neither of* and *either of* take a singular verb; *none of* usually takes a plural one.

### Q97. Correct the single error: "**Walking through the switchyard**, the frost on the insulators was clearly visible to the inspector."

> **Type:** Common-mistake
> **Answer:** "Walking through the switchyard" is a dangling participle; the subject must be a person — e.g. "Walking through the switchyard, the inspector could clearly see the frost on the insulators."
> **Solution:** A participial phrase at the start of a sentence must belong to the subject it is written next to. Here that subject is "the frost", which cannot walk through a switchyard, so the modifier is left dangling. The frost is then picked up as an object of a new verb, which is why the corrected version needs "could clearly see".
> **Key point:** Test the dangling participle by asking who performs the action.

### Q98. Correct the single error: "The authors **deny to have falsified** the data, and the raw logs have been archived."

> **Type:** Common-mistake
> **Answer:** deny to have falsified → deny having falsified (or deny that they falsified the data)
> **Solution:** The verb "deny", like "admit", "avoid" and "resist", is not followed by a to-infinitive. "Deny" either takes a that-clause or takes a gerund or a bare noun phrase: "deny having falsified", "deny falsification". "Deny to have" would need a different verb, such as "refuse".
> **Key point:** *Deny*, *admit* and *resist* take a gerund or a that-clause, never a to-infinitive.

### Q99. Correct the single error: "The report **recommends to install** the anti-aliasing filter before the sampler rather than after it."

> **Type:** Common-mistake
> **Answer:** recommends to install → recommends installing
> **Solution:** Verbs of advice and recommendation take a gerund, not a to-infinitive: "recommends installing", "suggests installing", "advises installing". A to-infinitive form appears only after a noun, as in "a recommendation to install", or after a different verb, as in "the committee decided to install".
> **Key point:** Suggest / recommend / advise / propose + gerund; a to-infinitive follows only the noun.

### Q100. Correct the single error: "The induction motor has been running at full load **since** three hours."

> **Type:** Common-mistake
> **Answer:** since → for
> **Solution:** "Since" introduces a point in time ("since nine o'clock", "since Monday", "since 2019"); "for" introduces a length of duration ("for three hours", "for a week"). Here the phrase gives a duration, so the preposition must be "for".
> **Key point:** *Since* takes a point, *for* takes a period.

### Q101. [GATE-1] Correct the single error: "The assembled unit **is comprised of** three sub-modules, a cooling plate and a shielded harness."

- (a) is comprised of → comprises
- (b) is comprised of → is comprised
- (c) three → three's
- (d) assembled → assembly

> **Type:** MCQ
> **Answer:** is comprised of → comprises (Option a).
> **Solution:** *Comprise* is normally a transitive verb, as in "the unit comprises three sub-modules", or the unit is used adjectivally in passive, as in "the unit is comprised of three sub-modules". The form "is comprised of" is widely regarded as a redundancy, because the passive already carries the "of". Options (c) and (d) are unrelated, and (b) leaves the sentence without a verb.
> **Key point:** Say "comprises" or "is composed of", not both at once.

### Q102. Correct the single error: "The new design employs **less** components than the old one, which is why the bill of materials is shorter."

> **Type:** Common-mistake
> **Answer:** less → fewer
> **Solution:** Components are countable, so they take "fewer"; "less" is for uncountable quantities such as time, water or noise. The correct comparison is "fewer components than the old one", parallel with "shorter" for the bill of materials, which is itself countable.
> **Key point:** Countable nouns take *fewer* and take an "s" on the comparative.

### Q103. Correct the single error: "The engineer **which** designed the low-noise amplifier told the technician that the offsets had been trimmed."

> **Type:** Common-mistake
> **Answer:** which → who
> **Solution:** A relative clause referring to a person takes "who" or "that", not "which"; "which" is reserved for things. Since the antecedent is "engineer", the pronoun must be "who". The "that" alternative would also be correct, but "which" is not.
> **Key point:** *Who* for people, *which* for things.

### Q104. Correct the single error: "**Despite of** the excellent noise figure of the front end, the receiver proved unusable in the presence of interference."

- (a) Despite of → Despite
- (b) excellent → excellently
- (c) the → a
- (d) proved → proves

> **Type:** MCQ
> **Answer:** Despite of → Despite (Option a).
> **Solution:** "Despite" is a preposition and needs no "of"; "in spite of" is the phrase that does take "of". Everything else is sound — "noise figure" is singular and the past tense is consistent with "proved unusable".
> **Key point:** *Despite* and *in spite of* are not interchangeable in form.

### Q105. Correct the single error: "The result obtained with the new etch is **more cheaper** than the one obtained with the previous process."

> **Type:** Common-mistake
> **Answer:** more cheaper → cheaper
> **Solution:** Adjectives of one syllable already inflect for degree — cheap, cheaper, cheapest — so "more" is redundant and ungrammatical here. Double comparison is only possible with comparatives of two or more syllables, as in "more expensive", and even then it is avoided in standard English.
> **Key point:** Short adjectives never take both -er and "more".

### Q106. Correct the single error: "Although the two circuits are electrically identical, they differ in **a** important respect: one of them is temperature-compensated and the other is not."

> **Type:** Common-mistake
> **Answer:** a → an
> **Solution:** "Important" begins with a vowel sound, so the indefinite article must be "an". Note that the following word "respect" would determine the choice if the adjective were absent — "a respect" — which is exactly why the article must be read with the word immediately following it.
> **Key point:** The article is decided by the next word, never by the word after that.

---

## Section 5. Sentence improvement and rearrangement

### Q107. Which sentence is grammatically correct and preserves the meaning?

- (a) The committee have decided that the proposal will be considered in the next meeting.
- (b) The committee has decided that the proposal will be considered in the next meeting.
- (c) The committee have decided that the proposal would be considered in the next meeting.
- (d) The committee has decided that the proposal were considered in the next meeting.

> **Type:** MCQ
> **Answer:** The committee has decided that the proposal will be considered in the next meeting (Option b).
> **Solution:** A collective noun acting as a single body takes a singular verb in British and in formal Indian usage, so "has" is the safe choice, and "the next meeting" points to a future event, which licenses "will be considered". Option (a) keeps the singular/plural error, (c) mixes a present decision with a past-in-the-future modal, and (d) has a subjunctive "were" that this complement does not call for.
> **Key point:** A collective noun with a singular meaning takes a singular verb; check the time adverbial before the modal.

### Q108. [GATE-1] Which sentence is correct?

- (a) Neither the manager nor his assistants was aware of the change in the schedule.
- (b) Neither the manager nor his assistants were aware of the change in the schedule.
- (c) Neither the manager nor the assistants was aware of the change in schedules.
- (d) Neither the manager nor his assistants are aware of the change in the schedule.

> **Type:** MCQ
> **Answer:** Neither the manager nor his assistants were aware of the change in the schedule (Option b).
> **Solution:** In a "neither … nor" construction the verb agrees with the subject nearest to it, which here is the plural "his assistants". "The change" is singular, so (c) is wrong twice over, and (d) has the wrong agreement plus a tense the context does not fix.
> **Key point:** With *neither … nor* and *either … or*, the verb agrees with the nearer subject.

### Q109. Which sentence correctly expresses the intended conditional?

- (a) If I would have known the datasheet was wrong, I would have ordered a different part.
- (b) If I had known the datasheet was wrong, I would have ordered a different part.
- (c) If I would have known the datasheet was wrong, I had ordered a different part.
- (d) If I had known the datasheet was wrong, I would order a different part.

> **Type:** MCQ
> **Answer:** If I had known the datasheet was wrong, I would have ordered a different part (Option b).
> **Solution:** The second conditional pairs the past perfect "had known" in the if-clause with "would have ordered" in the main clause. Options (a) and (c) misplace "would", and (d) mixes a third-conditional if-clause with a second-conditional main clause.
> **Key point:** If the if-clause is past ("had"), the main clause must be "would have".

### Q110. Correct the error and choose the best sentence: "**There is** many reasons why the measurement cannot be repeated on the same specimen."

- (a) There is many reasons why the measurement cannot be repeated on the same specimen.
- (b) There are many reasons why the measurement cannot be repeated on the same specimen.
- (c) There is many reasons why the measurement is cannot be repeated on the same specimen.
- (d) There are many reason why the measurement cannot be repeated on the same specimen.

> **Type:** MCQ
> **Answer:** There are many reasons why the measurement cannot be repeated on the same specimen (Option b).
> **Solution:** In "there is/are" the verb agrees with the notional subject that follows — here the plural "reasons" — so "are" is required and "many reasons" is plural. Option (c) inserts an extra modal that changes the meaning, and (d) makes the noun singular while leaving the verb plural.
> **Key point:** In *there is / there are*, agree with the noun that actually follows.

### Q111. Which rewrite removes the dangling participle without changing the meaning?

- (a) Having completed the calibration, the samples were then sent for analysis.
- (b) The calibration having completed, the samples were then sent for analysis.
- (c) After completing the calibration, the operator sent the samples for analysis.
- (d) The samples, having completed the calibration, were then sent for analysis.

> **Type:** MCQ
> **Answer:** After completing the calibration, the operator sent the samples for analysis (Option c).
> **Solution:** In (a), (b) and (d) the subject of "completed" is a calibration or a set of samples, none of which can complete a calibration. Only (c) supplies a human agent who can. (b) and (d) preserve the participle while failing to attach it to a person, so they keep the error.
> **Key point:** A dangling participle is fixed by giving the phrase a subject that can perform the action.

### Q112. [GATE-1] Which sentence avoids redundancy?

- (a) The experiment was repeated twice again with a fresh specimen.
- (b) The experiment was repeated once again with a fresh specimen.
- (c) The experiment was repeated again and again with a fresh specimen.
- (d) The experiment was repeated two times again with a fresh specimen.

> **Type:** MCQ
> **Answer:** The experiment was repeated once again with a fresh specimen (Option b).
> **Solution:** "Repeated" already reports the repetition, so any numeral attached to "again" counts it twice: "twice again" implies three repetitions, and "repeated again and again" is pleonastic. (b) pairs the single adverb "once again" with "repeated", which together report one further repetition. (d) keeps the double count.
> **Key point:** "Again" already means a further instance; a numeral before it double-counts.

### Q113. Which sentence is correct and idiomatic?

- (a) The reason why the amplifier is unstable is because the phase margin is too small.
- (b) The reason why the amplifier is unstable is that the phase margin is too small.
- (c) The reason the amplifier is unstable because the phase margin is too small.
- (d) The reason why the amplifier is unstable is because of the too small phase margin.

> **Type:** MCQ
> **Answer:** The reason why the amplifier is unstable is that the phase margin is too small (Option b).
> **Solution:** In formal English "the reason … is that" is the construction; "the reason … is because" is a fault of the "reason" clause. Option (c) leaves the "is" out entirely, and (d) piles up "because of" after "is" as well as misplacing the adjective in "the too small phase margin".
> **Key point:** Say "the reason is that", not "the reason is because".

### Q114. Which sentence is correct?

- (a) She is one of the only engineers who understand analogue design.
- (b) She is one of the only engineers who understands analogue design.
- (c) She is the only engineer who understand analogue design.
- (d) She is one of the few engineers who understand analogue design and is also the best at it.

> **Type:** MCQ
> **Answer:** She is one of the only engineers who understand analogue design (Option a).
> **Solution:** The antecedent of "who" is "engineers", plural, so the verb must be "understand"; the singular "understands" in (b) is the classic error. (c) is wrong for the same reason. (d) is a grammatical sentence, but it does not preserve the original meaning, which asserted no uniqueness.
> **Key point:** With *one of the*, the relative clause takes a plural verb.

### Q115. Which sentence is entirely correct?

- (a) The equipment were damaged and the samples has been destroyed.
- (b) The equipment was damaged and the samples have been destroyed.
- (c) The equipment were damaged and the samples have been destroyed.
- (d) The equipment have been damaged and the samples has been destroyed.

> **Type:** MCQ
> **Answer:** The equipment was damaged and the samples have been destroyed (Option b).
> **Solution:** "Equipment" is uncountable and so takes the singular "was"; the two past events, damage and destruction, are not presented as a single completed time, so the natural pairing is simple past with present perfect, giving "have been destroyed". Every other option breaks one of those two agreements.
> **Key point:** Uncountable subjects take a singular verb, and different tenses can legitimately be paired.

### Q116. Which version of the sentence is unambiguous and idiomatic?

- (a) The engineer who inspected the wafer and the engineer who tested the samples left the building.
- (b) The engineer who inspected the wafer and the engineer who tested the samples have left the building.
- (c) After the engineer inspected the wafer, he tested the samples and left the building.
- (d) The engineer inspected the wafer, and he tested the samples that he left the building with.

> **Type:** MCQ
> **Answer:** The engineer who inspected the wafer and the engineer who tested the samples have left the building (Option b).
> **Solution:** (a) is ambiguous because the second "who" may be read as attaching to the first "the engineer", making it unclear whether one or two people left; the plural verb in (b) removes the ambiguity. (c) and (d) are grammatical but change the number of people involved, so they do not preserve the original meaning.
> **Key point:** Test repeated relative pronouns for attachment to the nearest noun, and fix with the verb number.

---

### Q117. Arrange the four statements P, Q, R and S into a coherent paragraph.

- **P.** Only after the prototype passed the thermal cycling test was the layout frozen.
- **Q.** The prototype itself was built from a hand-drawn layout that two engineers had produced in a weekend.
- **R.** The thermal cycling test took six weeks, during which two of the three boards had to be reworked.
- **S.** The schedule, however, allowed no time for a second cycle after the freezing.

- (a) Q P R S
- (b) P Q R S
- (c) Q R P S
- (d) S R Q P

> **Type:** MCQ
> **Answer:** Q P R S (Option a).
> **Solution:** P cannot open the paragraph, because "only after the prototype passed" presumes a prototype already mentioned, so Q must precede it. R then explains what the thermal cycling test involved, and its reference to "the freezing" looks back to P. S closes with "however", introducing a contrast that modifies the sequence just described. Option (c) breaks the P–R link by putting the test's duration before the freezing, and (b) and (d) both start with a sentence that depends on a later one.
> **Key point:** Start with the only sentence that has no forward or backward dependency.

### Q118. Arrange the four statements P, Q, R and S into a coherent paragraph.

- **P.** The signal therefore has to be regenerated, not merely amplified, at every repeater.
- **Q.** A digital signal travelling along a noisy cable accumulates jitter and attenuation at every metre.
- **R.** Regeneration is expensive, which is why engineers keep looking for cheaper ways to extend a link.
- **S.** The oldest attempt at those cheaper ways was to space repeaters very widely, an approach that gave up bandwidth in order to save hardware.

- (a) S R Q P
- (b) Q P R S
- (c) R Q P S
- (d) P Q R S

> **Type:** MCQ
> **Answer:** Q P R S (Option b).
> **Solution:** Q states the problem, and P's "therefore" must follow it. R depends on P, since it is *regeneration* that is expensive. S then refers back to "cheaper ways" and adds a historical example, so it closes the paragraph. Option (a) opens with a sentence that refers to something not yet mentioned, and (c) and (d) put a conclusion or a dependent clause before its antecedent.
> **Key point:** *Therefore*, *however* and *which is why* each need the preceding sentence in place.

### Q119. Arrange the four statements P, Q, R and S into a coherent paragraph.

- **P.** The balance was calibrated against a national standard traceable to the kilogram prototype before any weighing began.
- **Q.** The samples had to be dried at 105 °C for two hours, because moisture was suspected of affecting the mass readings.
- **R.** Each sample was then weighed three times and the mean recorded to four decimal places.
- **S.** A blind duplicate of every tenth sample was then submitted by a second operator, and the two results agreed to within the stated tolerance.

- (a) S R Q P
- (b) P Q R S
- (c) Q P R S
- (d) R Q P S

> **Type:** MCQ
> **Answer:** P Q R S (Option b).
> **Solution:** P is the only sentence with a fully independent subject and no forward reference, so it opens. Q then gives the sample preparation, and R's "then" refers to the drying just described. S's "then" in turn follows the weighing, and the clause about the second operator reads as a closing statement about the quality of the data. Options (a), (c) and (d) all place a "then" clause before the event it depends on.
> **Key point:** Count the *then*s and *therefore*s — each one points backwards.

### Q120. Arrange the four statements P, Q, R and S into a coherent paragraph.

- **P.** The measurement team set out to answer a narrow question: how much of the coupling came from the cable run rather than from the device.
- **Q.** Isolation between the two ports was not good, and the first figure obtained was thirty-two decibels.
- **R.** The test was then repeated with the antenna rotated by ninety degrees, which gave a figure seven decibels lower.
- **S.** Only the cable run, therefore, accounted for most of the coupling, and the shielding specification was rewritten to match.

- (a) P Q R S
- (b) P S R Q
- (c) R S P Q
- (d) R Q P S

> **Type:** MCQ
> **Answer:** P Q R S (Option a).
> **Solution:** P states the aim, which explains why the following sentences report figures at all. Q supplies the initial situation and the first measurement, and R's "then" refers back to that measurement. S's "therefore" draws the conclusion from the two figures and reports the action taken, so it must end. Options (b) and (d) put the conclusion before its evidence, and (c) opens with the repeat of a test that has not yet been described.
> **Key point:** A sentence reporting an action taken is nearly always the last sentence.

### Q121. Arrange the four statements P, Q, R and S into a coherent paragraph.

- **P.** It is the first of these that turns out to be decisive.
- **Q.** When a pipeline is deep, a register added at each stage costs both area and a clock cycle.
- **R.** There are two reasons why designers shrink those stages anyway.
- **S.** The second is that the logic can be made faster once the wire is no longer carrying the whole function.

- (a) P Q R S
- (b) R Q S P
- (c) R S Q P
- (d) S Q R P

> **Type:** MCQ
> **Answer:** R Q S P (Option b).
> **Solution:** R announces "two reasons", which obliges the paragraph to supply exactly two, and it must come before both of them. Q is the first reason and S, marked "The second", is the second. Only then can P, which refers back to "the first of these", be placed. Options (a) and (d) place the summary before the reasons, and (c) puts the "second" reason before the first.
> **Key point:** An announcement of a number commits the paragraph to that exact number of items.

### Q122. [GATE-1] Arrange the four statements P, Q, R and S into a coherent paragraph.

- **P.** The next morning the same two teachers were assigned to the same class.
- **Q.** A survey of schools in the district had found that the classes taught by the two best-trained teachers scored highest on the reading tests.
- **R.** On the day the report was published, the district shuffled its entire teaching schedule at random.
- **S.** When the results were re-analysed a year later, the advantage had vanished.

- (a) Q R P S
- (b) R Q P S
- (c) P Q R S
- (d) S Q R P

> **Type:** MCQ
> **Answer:** Q R P S (Option a).
> **Solution:** Q reports the survey finding, and R's "the report" and "on the day" refer to it, so R must come second. P's "next morning" fixes it immediately after the shuffle. S then reports the re-analysis a year later, which depends on the shuffle having happened. Option (c) puts "the next morning" before the day it follows, and (b) and (d) both start with a sentence whose reference is unestablished.
> **Key point:** Fix the time-marker chain first: yesterday, then, the next morning, a year later.

### Q123. Arrange the four statements P, Q, R and S into a coherent paragraph.

- **P.** Since the three-click action was replaced by a single shortcut and an undo was added, those who have used the interface for a month rarely go back.
- **Q.** An interface can be technically flawless and still be abandoned in a week.
- **R.** The first version had every feature that the specification asked for, and it was still widely disliked.
- **S.** The reasons turned out to be boring: three clicks for a routine action, and no way to undo the last one.

- (a) Q R S P
- (b) P Q R S
- (c) R Q P S
- (d) S P Q R

> **Type:** MCQ
> **Answer:** Q R S P (Option a).
> **Solution:** Q makes the general claim, R supplies the first instance, and S explains why the first instance was disliked. P's "Since" clause refers to the changes implied by S's complaints, so it must come last, and it also resolves the claim made in Q. Options (b) and (c) place the outcome before its cause, and (d) opens with a sentence whose referent has not yet been introduced.
> **Key point:** A *Since* clause states the reason, so it belongs with or after its main clause's effect.

### Q124. [GATE-2] Arrange the four statements P, Q, R and S into a coherent paragraph.

- **P.** Only after the margin was finally removed did the model prove able to predict the onset of oscillations that the full nonlinear solver missed.
- **Q.** The reduced model dropped the fast variable and kept the slow one.
- **R.** It was validated over four hundred operating points before anyone put it into the control loop.
- **S.** There, for a decade, its errors were absorbed by a deliberately oversized safety margin.

- (a) P Q R S
- (b) R Q S P
- (c) Q R S P
- (d) S Q P R

> **Type:** MCQ
> **Answer:** Q R S P (Option c).
> **Solution:** Q introduces the model with the pronoun "it" ready for use, so Q must be first. R's "before anyone put it into the control loop" then places validation ahead of use, and S's "There" refers to the control loop, so S follows R. P's "Only after the margin was finally removed" refers to the margin named in S, so P closes. Options (a), (b) and (d) all place P, R or S before the sentence that supplies their reference.
> **Key point:** Track pronouns — "it", "there" and "the margin" each fix a position in the sequence.

---

## Section 6. Fill in the blanks

### Q125. Choose the correct article: "___ 470 pF capacitor is placed across the output terminals of the op-amp."

- (a) A
- (b) An
- (c) The
- (d) No article

> **Type:** MCQ
> **Answer:** A (Option a).
> **Solution:** The sentence introduces a component for the first time, not one already identified, so the indefinite article is required. "470" is read "four hundred and seventy", which begins with a consonant sound, so "a" and not "an". "The" would point to a capacitor the reader already knows about, and omitting the article is not possible before a singular countable noun.
> **Key point:** The article is decided by the first sound of the next word — "four hundred" starts with /f/.

### Q126. Choose the correct preposition: "The measured bandwidth depends ___ the capacitance of the feedback network."

- (a) at
- (b) on
- (c) for
- (d) with

> **Type:** MCQ
> **Answer:** on (Option b).
> **Solution:** "Depend on" is the fixed verb–preposition combination for a quantity being determined by another. "Depend at" has no idiomatic use, "depend for" is not standard, and "depend with" would require a person or thing to depend upon. The grammar is otherwise sound.
> **Key point:** Learn verb–preposition pairs as single units.

### Q127. [GATE-1] Choose the word that completes the sentence with the intended meaning: "___ the amplifier is operated below 1 V, the gain remains close to unity."

- (a) Because
- (b) Provided that
- (c) In spite of
- (d) Due to

> **Type:** MCQ
> **Answer:** Provided that (Option b).
> **Solution:** The clause after the blank is a condition that guarantees the main clause, and "provided that" is the standard conditional conjunction for that. "Because" would make the gain the cause rather than the condition, "in spite of" reverses the logic entirely, and "due to" is a preposition that cannot open a subordinate clause here.
> **Key point:** *Provided that* and *as long as* state conditions; *because* states cause.

### Q128. Choose the option that fills both blanks: "___ the fault clears, the controller will keep re-initialising, ___ a watchdog timer is fitted."

- (a) Until / unless
- (b) Unless / until
- (c) While / unless
- (d) Since / since

> **Type:** MCQ
> **Answer:** Until / unless (Option a).
> **Solution:** "Until" is followed by a clause whose event has not yet happened, and the persistence of re-initialisation "until the fault clears" is exactly that. "Unless" introduces a negative condition, which is what the second clause needs before "a watchdog timer is fitted". Option (b) swaps the two and produces two negative conditions in a row, and (c) uses "while" for a limit that has not been reached.
> **Key point:** *Until* marks an unreached limit; *unless* marks a negative condition.

### Q129. [GATE-1] Choose the correct conjunction: "___ the fault was first reported, the line has been running at reduced capacity."

- (a) While
- (b) Since
- (c) During
- (d) For

> **Type:** MCQ
> **Answer:** Since (Option b).
> **Solution:** The main clause uses the present perfect ("has been running"), so the blank must name a starting point in the past, which is what "since" does. "While" and "during" name durations rather than starting points, and "for" would also need to be followed by a duration, not by a clause.
> **Key point:** A present perfect clause pairs with *since* plus a point, or *for* plus a period.

### Q130. [GATE-1] Choose the option that fills both blanks correctly: "Neither the filter ___ the pre-amplifier was fitted before the test began."

- (a) nor was
- (b) or was
- (c) nor were
- (d) nor has been

> **Type:** MCQ
> **Answer:** nor was (Option a).
> **Solution:** "Neither … nor" is a negative correlative, so the first clause already needs a negative element, which "nor" supplies. The verb agrees with the nearer subject, "the pre-amplifier", which is singular, so "was" is required. Option (b) removes the correlation, (c) misagrees with the nearer subject, and (d) introduces a tense the time frame does not support.
> **Key point:** *Neither … nor* takes the nearer subject's number on the verb.

### Q131. Choose the conjunction that preserves the intended meaning: "___ the junction temperature exceeds 150 °C, the device will fail within seconds."

- (a) Unless
- (b) If
- (c) Because
- (d) So that

> **Type:** MCQ
> **Answer:** If (Option b).
> **Solution:** The sentence asserts that exceeding 150 °C causes failure, so the blank introduces a positive condition, and "if" does that. "Unless" would assert the opposite — that the device fails whenever the temperature does *not* exceed 150 °C. "Because" would make the temperature the cause of the failure in a way the sentence does not claim, and "so that" introduces a purpose clause.
> **Key point:** *Unless* = "if not"; always test which meaning the sentence actually asserts.

### Q132. Choose the correct determiner: "___ number of samples that can be held in the shift register is fixed by the address bus width."

- (a) A
- (b) An
- (c) The
- (d) Few

> **Type:** MCQ
> **Answer:** The (Option c).
> **Solution:** The clause "is fixed by the address bus width" identifies one specific number, already determined, so the definite article is correct. "A number" would suggest one of several, and "few" is a quantifier for plural countable nouns, which "number" is not.
> **Key point:** With *number of*, use *the* when the quantity is already determined.

### Q133. Choose the verb that fits: "The regulator ___ the output voltage to within 1 % despite large changes in the load."

- (a) maintains
- (b) consist
- (c) comprises
- (d) consists

> **Type:** MCQ
> **Answer:** maintains (Option a).
> **Solution:** The object is a voltage and the prepositional phrase is "to within 1 %", the standard collocation for *maintain* used of a regulating stage. "Consist", "comprise" and "consist of" are linking verbs that take a subject and a complement, not a voltage as a direct object followed by a tolerance phrase.
> **Key point:** Linking verbs cannot take a direct object; look at what follows the blank.

### Q134. [GATE-1] Choose the correct relative pronoun: "The engineer ___ designed the layout retired at the end of March."

- (a) who
- (b) which
- (c) whose
- (d) whom

> **Type:** MCQ
> **Answer:** who (Option a).
> **Solution:** The relative pronoun must refer to a person and stand in for the subject of "designed", so "who" is correct. "Which" is for things, "whose" is for possession, and "whom" is for a person as the object of a verb — as in "the engineer whom the client thanked".
> **Key point:** Check the referent first (person or thing), then the role (subject or object).

### Q135. [GATE-2] Choose the option that fills both blanks: "The report, ___ nobody has read since 2019, still provides ___ only complete description of the calibration procedure."

- (a) who / a
- (b) which / an
- (c) which / the
- (d) whom / that

> **Type:** MCQ
> **Answer:** which / the (Option c).
> **Solution:** "The report" is a thing, so the relative pronoun must be "which"; "who" and "whom" refer to people. "Only" normally follows the determiner, so the determiner here is "the", giving "the only complete description". Option (a) fails on both counts, and (b) puts "an" before a vowel-initial noun phrase that is already fixed by "only".
> **Key point:** *Only* after a determiner: "the only", "one of the only", never "a only".

### Q136. Choose the option that fills the blank: "The technician was asked ___ the fuse before the power was restored."

- (a) to replace
- (b) replacing
- (c) replace
- (d) to replacing

> **Type:** MCQ
> **Answer:** to replace (Option a).
> **Solution:** With a passive subject ("was asked") the expected complement is a to-infinitive, so "to replace" is correct. A bare infinitive, as in (c), is not a complement of "asked" in the passive here, and both gerund options are ungrammatical. Note that "asked to" is fixed, unlike "suggested", which takes a gerund.
> **Key point:** *Asked to* takes an infinitive; *suggested* takes a gerund.

### Q137. [GATE-1] Choose the conjunction: "The gain is high, ___ the noise figure is also poor."

- (a) so
- (b) and
- (c) but
- (d) or

> **Type:** MCQ
> **Answer:** and (Option b).
> **Solution:** The two clauses simply add a second fact, and neither reverses nor contrasts with the other, so "and" is right. "But" would require the second clause to contradict or disappoint the expectation set up by the first, and "so" would claim a causal link that the sentence does not make.
> **Key point:** *And* adds, *but* contrasts, *so* concludes — read the relationship, not the position.

### Q138. Choose the word that completes the correlative pair: "The filter is not only cheap ___ also easy to tune over a wide range."

- (a) and
- (b) but
- (c) or
- (d) nor

> **Type:** MCQ
> **Answer:** but (Option b).
> **Solution:** "Not only" is obligatorily paired with "but also", in that order, and both halves must be positive here — "not only cheap" and "easy to tune". "And" would be wrong because "not only" requires "but", and neither "or" nor "nor" can complete the pair.
> **Key point:** *Not only … but also* must keep both halves positive and in that order.

### Q139. [GATE-2] Choose the option that fills both blanks: "The report was circulated ___ all members of the committee ___ Friday evening."

- (a) to / on
- (b) for / on
- (c) to / in
- (d) to / at

> **Type:** MCQ
> **Answer:** to / on (Option a).
> **Solution:** A document is circulated *to* a person or group, and an occasion is named with *on*: "on Friday evening". Option (b) has the wrong recipient preposition, (c) gives the wrong preposition for a single named day, and (d) pairs *at* with a day, which is only correct with a clock time.
> **Key point:** Days take *on*; clock times take *at*; documents go *to* their recipients.

### Q140. [GATE-1] Choose the option that completes the sentence: "___ of the twelve transistors failed the burn-in test, and those that failed all came from the same wafer lot."

- (a) Only two
- (b) Two only
- (c) Only
- (d) All

> **Type:** MCQ
> **Answer:** Only two (Option a).
> **Solution:** "Only" normally sits immediately before the word it restricts, so "only two of the twelve" restricts the number, and the rest of the sentence confirms that the number is small and significant. "Two only" places the restriction at the end, where it reads oddly and, in a long sentence, can be misread; "Only" alone cannot quantify; and "All" contradicts "those that failed", which presupposes some that passed.
> **Key point:** Place *only* immediately before the word it limits.

### Q141. [GATE-1] Choose the correct quantifier: "There is ___ water left in the tank, so the test will have to be postponed."

- (a) little
- (b) a little
- (c) few
- (d) a few

> **Type:** MCQ
> **Answer:** a little (Option b).
> **Solution:** "Water" is uncountable, which rules out "few" and "a few". Between the two uncountable options, "there is little water" is a negative statement close to zero, and the reason given — the test must be postponed — points to some water remaining, not none. "A little" is therefore the correct positive quantifier.
> **Key point:** Uncountable nouns take *little* (negative) or *a little* (positive); countable nouns take *few* and *a few*.

### Q142. [GATE-2] Choose the option that fills both blanks: "The technician insisted ___ replacing the capacitor rather than ___ the whole board."

- (a) on / on
- (b) in / in
- (c) at / on
- (d) for / at

> **Type:** MCQ
> **Answer:** on / on (Option a).
> **Solution:** "Insist on" is a fixed phrase and the second blank is governed by "rather than", which requires the same preposition before the second gerund in order for the contrast to be parallel. Options (c) and (d) break that parallelism, and "insist in" is not idiomatic in this sense.
> **Key point:** A *rather than* contrast must keep both sides structurally identical.

---

## Section 7. Idioms and phrases

### Q143. "The board had no choice but to **bite the bullet** and approve the extra testing cost."

The idiom means

- (a) to accept an unpleasant necessity that cannot be avoided
- (b) to speak bluntly and annoyingly
- (c) to fail at the last moment
- (d) to act with great caution

> **Type:** MCQ
> **Answer:** To accept an unpleasant necessity that cannot be avoided (Option a).
> **Solution:** The idiom is set up by "no choice but to", which is itself the literal content of the phrase, and the object — approving a cost nobody wants — is exactly the unpleasant necessity. Options (b), (c) and (d) are all things an idiom of this shape can be confused with, but the "no choice" context fixes the sense.
> **Key point:** Idioms are best pinned down by the words around them.

### Q144. "The extra grant came as **a shot in the arm** for the department, which had been struggling since the previous year."

The idiom means

- (a) a permanent cure for a chronic problem
- (b) a temporary boost or encouragement
- (c) a painful injection given in hospital
- (d) an injury suffered in an accident

> **Type:** MCQ
> **Answer:** A temporary boost or encouragement (Option b).
> **Solution:** The department is described as having been "struggling", so the grant relieves a difficulty for a time; the sense of the idiom is relief, not cure. Option (a) overstates it, and (c) and (d) are the literal readings the idiom's figurative use rules out.
> **Key point:** Figurative idioms need not borrow their words literally.

### Q145. "Take the claim that the design has been validated at full scale **with a pinch of salt** until the field data arrive."

The idiom means

- (a) to accept it completely and without question
- (b) to regard it as doubtful and not wholly reliable
- (c) to reject it outright as false
- (d) to add seasoning to it before circulating it

> **Type:** MCQ
> **Answer:** To regard it as doubtful and not wholly reliable (Option b).
> **Solution:** "Until the field data arrive" supplies the reason for the caution, and a pinch of salt is a small corrective, not a repudiation. Option (a) is the opposite, option (c) goes further than the sentence warrants, and (d) is the literal reading.
> **Key point:** Caution idioms sit between acceptance and rejection.

### Q146. "The technician **let the cat out of the bag** during the meeting and admitted that the calibration was overdue."

The idiom means

- (a) to make a mess that had to be cleaned up
- (b) to reveal a secret that was meant to be kept
- (c) to buy an item that was badly needed
- (d) to escape from an awkward situation

> **Type:** MCQ
> **Answer:** To reveal a secret that was meant to be kept (Option b).
> **Solution:** "Admitted that the calibration was overdue" is the disclosure, and the idiom covers an unintended or deliberate telling of something withheld. Option (a) uses the same animal imagery wrongly, and (c) and (d) are unrelated senses of other idioms.
> **Key point:** The clause after the idiom normally shows the thing revealed.

### Q147. "She **burned the midnight oil** for a fortnight, re-running the extraction and checking every alignment by hand."

The idiom means

- (a) to destroy something valuable by overheating it
- (b) to work late into the night, repeatedly
- (c) to waste fuel on an unnecessary process
- (d) to celebrate something at a late hour

> **Type:** MCQ
> **Answer:** To work late into the night, repeatedly (Option b).
> **Solution:** "For a fortnight, re-running and checking" establishes duration and repetition, which the idiom also carries. Options (a) and (c) attach to the word "burn" wrongly, and (d) is not a sense of the phrase at all.
> **Key point:** Repetition in the surrounding text usually belongs to the idiom.

### Q148. "Two teams were **in the same boat** when the funding was withdrawn, and both had to re-plan their scope."

The idiom means

- (a) travelling together for a sporting event
- (b) facing the same difficulty, whatever else differs between them
- (c) owning the same equipment
- (d) being under the same supervisor

> **Type:** MCQ
> **Answer:** Facing the same difficulty, whatever else differs between them (Option b).
> **Solution:** The withdrawal is the shared problem and the consequence — having to re-plan — applies to both, which is what the idiom asserts. The "boat" is a metaphor for the situation, not for the two teams' relationship; options (a), (c) and (d) read it literally or over-specify it.
> **Key point:** *In the same boat* is about a shared predicament, not a shared identity.

### Q149. "The auditors found that two managers had been **cooking the books** for at least three years."

The idiom means

- (a) preparing the accounts in a hurry
- (b) falsifying financial records dishonestly
- (c) destroying old records to save space
- (d) keeping careful records that are hard to follow

> **Type:** MCQ
> **Answer:** Falsifying financial records dishonestly (Option b).
> **Solution:** The setting is an audit, and the duration — three years — marks the behaviour as deliberate and concealed. Option (a) attaches to the word "cooking" neutrally, and (c) and (d) are not senses of the idiom.
> **Key point:** The institutional setting in a sentence often disambiguates a crime idiom.

### Q150. [GATE-1] The report describes the regulator's decision as "**a storm in a teacup**". The idiom means that the fuss is

- (a) genuine but very large
- (b) wildly out of proportion to the matter that caused it
- (c) likely to bring real damage if it continues
- (d) confined to a single household

> **Type:** MCQ
> **Answer:** Wildly out of proportion to the matter that caused it (Option b).
> **Solution:** The literal image is a storm that fits in a teacup, so the phrase measures disproportion, not size. Option (a) inverts that, option (c) claims a consequence the idiom does not assert, and option (d) merely re-reads "teacup" literally.
> **Key point:** A "storm in a teacup" measures ratio, not scale.

### Q151. Choose the single word that replaces the underlined phrase without changing the meaning: "The committee **gave a nod to** the revised specification after a single afternoon's discussion."

- (a) approved
- (b) rejected
- (c) postponed
- (d) copied

> **Type:** MCQ
> **Answer:** approved (Option a).
> **Solution:** "Gave a nod to" is a phrase of assent, and "approved" is the single word that carries exactly that meaning with a committee as the subject. "Rejected" and "postponed" are the opposite and a delay respectively, and "copied" would change the act entirely.
> **Key point:** A one-word substitution must preserve both the sense and the strength.

### Q152. [GATE-1] Choose the single word that replaces the underlined phrase: "The manager **turned a deaf ear to** the warning about the single-supply component."

- (a) listened to
- (b) ignored
- (c) reported
- (d) answered

> **Type:** MCQ
> **Answer:** ignored (Option b).
> **Solution:** "Turned a deaf ear to" is deliberate non-response, and "ignored" is the single verb that matches it. "Listened to" is the opposite, while "reported" and "answer" describe different actions altogether. Note that the substitution must also work with the object "a warning", which "ignored" does.
> **Key point:** Test a proposed substitute against the actual object of the phrase.

### Q153. Choose the single word that replaces the underlined phrase: "The review **cast aspersions on** the earlier measurement campaign."

- (a) praised
- (b) questioned
- (c) ignored
- (d) extended

> **Type:** MCQ
> **Answer:** questioned (Option b).
> **Solution:** "Cast aspersions on" means to speak disparagingly of something, and "questioned" is the nearest single verb that keeps the sense of doubt. "Praised" is the antonym, and "ignored" and "extended" are not related senses of the phrase.
> **Key point:** *Cast aspersions on* is about damaging someone's opinion, not about a neutral query.

### Q154. Choose the single word that replaces the underlined phrase: "The two calibration records **are at variance with** one another by about 0.3 %."

- (a) agree
- (b) conflict
- (c) compare
- (d) resemble

> **Type:** MCQ
> **Answer:** conflict (Option b).
> **Solution:** "At variance with" means in disagreement, and "conflict" is the single verb that preserves both the sense and the fact that the disagreement is between the two records. "Agree" is the antonym, and "compare" and "resemble" do not express disagreement at all.
> **Key point:** Check the preposition: *at variance with X* = *conflict with X*.

### Q155. Choose the single word that replaces the underlined phrase: "The internal audit **laid bare** the discrepancies between the ledger and the bank statements."

- (a) concealed
- (b) exposed
- (c) summarised
- (d) corrected

> **Type:** MCQ
> **Answer:** exposed (Option b).
> **Solution:** "Laid bare" means to reveal fully, and "exposed" is the single verb that carries that meaning with "the discrepancies" as the object. "Concealed" is the opposite, "summarised" would reduce rather than reveal, and "corrected" claims a repair the sentence does not report.
> **Key point:** *Laid bare* reveals; it does not repair.

### Q156. Choose the single word that replaces the underlined phrase: "The panel **made light of** the objections raised at the design review."

- (a) emphasised
- (b) dismissed
- (c) documented
- (d) repeated

> **Type:** MCQ
> **Answer:** dismissed (Option b).
> **Solution:** "Made light of" means to treat as unimportant, and "dismissed" is the single verb that preserves that judgement of the objections. "Emphasised" is the opposite attitude, and "documented" and "repeated" describe recording rather than judging.
> **Key point:** *Make light of* = treat as trivial.

### Q157. [GATE-1] Choose the single word that replaces the underlined phrase: "The measured trend **bears out** the prediction made before the trial began."

- (a) supports
- (b) refutes
- (c) delays
- (d) conceals

> **Type:** MCQ
> **Answer:** supports (Option a).
> **Solution:** "Bears out" means to confirm by evidence, and "supports" is the single word that keeps the sense of confirmation without overstating it as proof. "Refutes" and "conceals" are the opposite in each case, and "delays" is unrelated.
> **Key point:** *Bear out* is confirmation by evidence, which is weaker than proof.

### Q158. Choose the single word that replaces the underlined phrase: "Two members of the committee **took issue with** the draft on the question of tolerances."

- (a) agreed with
- (b) objected to
- (c) commented on
- (d) voted on

> **Type:** MCQ
> **Answer:** objected to (Option b).
> **Solution:** "Took issue with" means to raise an objection, and "objected to" is the single verb that preserves both the sense and the prepositional pattern with "the draft". "Agreed with" is the antonym, while "commented on" and "voted on" describe neutral or procedural acts.
> **Key point:** *Take issue with* = object to; note that the substitute needs the same preposition.

---

## Section 8. Active and passive voice

### Q159. Convert to the passive voice: "The technician replaced the faulty capacitor."

- (a) The faulty capacitor was replaced by the technician.
- (b) The faulty capacitor was replaced by technician.
- (c) The technician was replaced by the faulty capacitor.
- (d) The faulty capacitor has replaced the technician.

> **Type:** MCQ
> **Answer:** The faulty capacitor was replaced by the technician (Option a).
> **Solution:** The object of the active sentence ("the faulty capacitor") becomes the subject of the passive, the verb changes from "replaced" to "was replaced", and the original subject becomes the agent introduced by "by". Option (b) omits the article, (c) swaps subject and object without changing the verb's sense, and (d) changes the tense.
> **Key point:** In the passive, the old object becomes the subject and the old subject becomes the agent.

### Q160. [GATE-1] Convert to the passive voice: "They have completed the calibration of the receiver."

- (a) The calibration of the receiver has been completed by them.
- (b) The calibration of the receiver is completed by them.
- (c) The receiver has been completed the calibration.
- (d) The calibration of the receiver had been complete.

> **Type:** MCQ
> **Answer:** The calibration of the receiver has been completed by them (Option a).
> **Solution:** The present perfect active "have completed" becomes "has been completed" with the plural "they" dropped, because the plural is now carried by the singular noun "calibration". The tense must be preserved exactly, so (b)'s simple present and (d)'s past perfect are both wrong, and (c) leaves the object in the subject position.
> **Key point:** Tense is preserved in conversion; the verb number follows the new subject.

### Q161. Convert to the passive voice: "The committee will announce the results tomorrow."

- (a) The results will be announced by the committee tomorrow.
- (b) The results will be announcing by the committee tomorrow.
- (c) The committee will be announced the results tomorrow.
- (d) The results will be announced tomorrow by the committee will.

> **Type:** MCQ
> **Answer:** The results will be announced by the committee tomorrow (Option a).
> **Solution:** "Will announce" becomes "will be announced" — the modal is kept, the tense is kept, and only the voice changes, so no "-ing" is added as in (b). Option (c) leaves the object as the object, and (d) duplicates the auxiliary.
> **Key point:** Modal + verb passes through a conversion unchanged: *will announce* → *will be announced*.

### Q162. Convert to the passive voice: "Someone must tighten the terminal screws before the test begins."

- (a) The terminal screws must be tightened before the test begins.
- (b) The terminal screws must be tightening before the test begins.
- (c) Someone must be tightened the terminal screws.
- (d) The terminal screws must tightening before the test begins.

> **Type:** MCQ
> **Answer:** The terminal screws must be tightened before the test begins (Option a).
> **Solution:** After a modal, the passive is formed with "be" plus the past participle: "must be tightened". Options (b) and (d) use the wrong participial form, and (c) attempts a conversion where the object is not a valid passive subject in this construction.
> **Key point:** Modal + passive = modal + *be* + past participle.

### Q163. Convert to the passive voice: "The supplier is repairing the power supply this week."

- (a) The power supply is being repaired by the supplier this week.
- (b) The power supply is repaired by the supplier this week.
- (c) The supplier is being repaired the power supply this week.
- (d) The power supply has been repaired by the supplier this week.

> **Type:** MCQ
> **Answer:** The power supply is being repaired by the supplier this week (Option a).
> **Solution:** The present continuous "is repairing" becomes "is being repaired" with the "-ing" retained, which is the mark of the progressive passive. Option (b) drops the progressive aspect, (c) has no passive at all, and (d) changes the tense.
> **Key point:** *Am/is/are being* + past participle is the progressive passive.

### Q164. [GATE-2] Convert to the passive voice: "The engineer should have isolated the supply before starting work."

- (a) The supply should have been isolating before starting work.
- (b) The supply should have been isolated before starting work.
- (c) The supply should being isolated before starting work.
- (d) The supply should have been isolate before starting work.

> **Type:** MCQ
> **Answer:** The supply should have been isolated before starting work (Option b).
> **Solution:** A modal perfect has the fixed form modal + *have* + *been* + past participle, so "should have isolated" becomes "should have been isolated". Option (a) uses a present participle, (c) drops "have", and (d) uses a bare verb form. The temporal interpretation — that the isolation should have happened earlier — must survive the conversion.
> **Key point:** Modal perfect passive = *should have been* + past participle.

### Q165. Convert to the active voice: "The defect was traced to a faulty connector by the senior engineer."

- (a) The senior engineer traced the defect to a faulty connector.
- (b) The defect traced the senior engineer to a faulty connector.
- (c) The senior engineer was traced to the defect by the connector.
- (d) A faulty connector traced the defect to the senior engineer.

> **Type:** MCQ
> **Answer:** The senior engineer traced the defect to a faulty connector (Option a).
> **Solution:** The passive subject "the defect" was the object of the active verb, and the agent "the senior engineer" becomes the subject. The prepositional phrase "to a faulty connector" is a complement of "traced" and stays with it. Option (b) makes the defect the doer, which reverses the meaning, and (c) leaves a passive form.
> **Key point:** Recovering the active form means finding what performed the action and making it the subject.

### Q166. Convert to the active voice: "The new filter has been installed by the maintenance team."

- (a) The maintenance team has installed the new filter.
- (b) The new filter has installed the maintenance team.
- (c) The maintenance team is installing the new filter.
- (d) The new filter has been installing the maintenance team.

> **Type:** MCQ
> **Answer:** The maintenance team has installed the new filter (Option a).
> **Solution:** The tense is preserved: "has been installed" becomes "has installed", with the team as subject and the filter as object. Option (c) changes the tense to the present continuous, and (b) and (d) make the filter the doer, which is impossible.
> **Key point:** A conversion changes voice only — never tense, number or meaning.

### Q167. Convert to the active voice: "A short circuit was caused by the loose terminal."

- (a) The loose terminal caused a short circuit.
- (b) The loose terminal was caused by a short circuit.
- (c) A short circuit caused the loose terminal.
- (d) The loose terminal is causing a short circuit.

> **Type:** MCQ
> **Answer:** The loose terminal caused a short circuit (Option a).
> **Solution:** The agent is "the loose terminal" and the thing affected is "a short circuit", so the active sentence has the terminal as subject and the short circuit as object, in the past simple. Option (c) reverses cause and effect, and (d) changes the tense.
> **Key point:** In "X was caused by Y", Y is the cause and X is the effect.

### Q168. Convert to the active voice: "The results will be presented by the chairman in the morning."

- (a) The chairman will present the results in the morning.
- (b) The chairman will be presented the results in the morning.
- (c) The results will present the chairman in the morning.
- (d) In the morning the chairman presented the results.

> **Type:** MCQ
> **Answer:** The chairman will present the results in the morning (Option a).
> **Solution:** "Will be presented" becomes "will present" with the chairman as subject and the results as object, while the time adverbial stays in place. Option (d) changes the tense to the past simple, and (b) and (c) reverse the two nouns.
> **Key point:** Adverbials of time and place are never affected by a voice change.

### Q169. [GATE-1] Convert to the active voice: "It is reported that the chip had been returned to the supplier."

- (a) Someone reported that the chip had been returned to the supplier.
- (b) The chip reported that it had returned to the supplier.
- (c) It was reported by someone that the chip returned.
- (d) Someone returned the chip to the supplier.

> **Type:** MCQ
> **Answer:** Someone reported that the chip had been returned to the supplier (Option a).
> **Solution:** "It is reported that…" is an impersonal passive, and the active form requires a doer — "someone" or an unnamed source. Crucially, the embedded clause "the chip had been returned" is itself passive and must stay passive, because the chip is not the reporter. Option (d) wrongly promotes the embedded passive to an active claim, and (c) keeps the original construction.
> **Key point:** An embedded clause has its own voice; only the matrix clause is converted.

### Q170. Convert to the active voice: "Were the components tested after the packing was completed?"

- (a) Did somebody test the components after the packing was completed?
- (b) Did somebody test the components after the packing was complete?
- (c) Tested somebody the components after the packing was completed?
- (d) Were the components tested after did somebody complete the packing?

> **Type:** MCQ
> **Answer:** Did somebody test the components after the packing was completed? (Option a).
> **Solution:** A passive question becomes active with "did" plus the base form, an invented subject such as "somebody", and the object restored. The second clause is still passive, because the packing was performed by the same unnamed people, and the tense of that clause must not change. Options (b) and (d) alter tense, and (c) is not a question form.
> **Key point:** Passive questions become active with *did* + base verb + invented subject.

### Q171. Which of the following sentences is in the passive voice?

- (a) He is a well-known cardiac surgeon.
- (b) The manuscript was rejected by three reviewers.
- (c) The committee were divided over the issue.
- (d) The task proved harder than expected.

> **Type:** MCQ
> **Answer:** The manuscript was rejected by three reviewers (Option b).
> **Solution:** Only (b) has the form be + past participle with the doer named. In (a) "is" is a linking verb, in (c) "were" is a copula, and in (d) "proved" is a linking verb; none of them makes the subject the object of an action.
> **Key point:** Be + participle is only passive when a form of *have* does not make it a perfect.

### Q172. Choose the active form of the passive sentence "The gate was driven by the driver circuit."

- (a) The driver circuit was driven by the gate.
- (b) The driver circuit drove the gate.
- (c) The gate drove the driver circuit.
- (d) The driver circuit is driving the gate.

> **Type:** MCQ
> **Answer:** The driver circuit drove the gate (Option b).
> **Solution:** The active subject is the agent, "the driver circuit", and the object is what was acted upon, "the gate", so the two nouns exchange positions and the tense is restored to the simple past. Option (a) merely reverses the two nouns inside a passive, (c) keeps the original subject as subject, and (d) changes the tense.
> **Key point:** Converting voice exchanges the roles of the two nouns, not just their positions.

### Q173. In the passive sentence "The bridge was designed by an engineer from another state", the phrase "by an engineer from another state" names

- (a) the agent, that is, the doer of the designing
- (b) the patient, that is, the thing designed
- (c) the instrument used
- (d) the place where the designing took place

> **Type:** MCQ
> **Answer:** The agent, that is, the doer of the designing (Option a).
> **Solution:** In a passive sentence, a "by" + noun phrase normally identifies who performed the action. "An engineer" is capable of designing; a bridge is not an engineer, nor an instrument, so the whole phrase names the doer even though it also contains a place phrase.
> **Key point:** A "by" + person phrase in the passive is the agent.

### Q174. [GATE-1] In the passive sentence "The capacitor was replaced by the technician", the word "technician" is

- (a) the subject
- (b) the object
- (c) the agent
- (d) the indirect object

> **Type:** MCQ
> **Answer:** The agent (Option c).
> **Solution:** The grammatical subject is "the capacitor", and the object of the corresponding active sentence is also "the capacitor". "Technician" is the doer of the replacing, which in the passive is the agent introduced by "by". It is never the subject in this construction.
> **Key point:** In a passive, the agent is introduced by *by* and is neither subject nor object.

### Q175. [GATE-1] Which sentence is NOT in the passive voice?

- (a) The letters were delivered by the postman.
- (b) The stadium is being repainted.
- (c) The report reads well.
- (d) The window has been broken.

> **Type:** MCQ
> **Answer:** The report reads well (Option c).
> **Solution:** "Reads" is an active verb of perception here and "well" is an adverb, so the sentence is active. Options (a), (b) and (d) all show be + past participle with the subject as the thing acted upon. The trap in such questions is the linking-verb use of *be*, which never forms a passive.
> **Key point:** "Be + adjective" is a link, not a passive; look for a past participle.

### Q176. [GATE-2] Choose the correct active rendering of "The technician had the capacitor replaced before the test."

- (a) The technician replaced the capacitor before the test.
- (b) The capacitor was replaced by the technician before the test.
- (c) Somebody replaced the capacitor for the technician before the test.
- (d) The technician had replaced the capacitor before the test.

> **Type:** MCQ
> **Answer:** Somebody replaced the capacitor for the technician before the test (Option c).
> **Solution:** "Have something done" is a causative construction: the first subject arranges for someone else to do the action. The active form therefore needs a new doer ("somebody") and must show that the technician arranged it rather than performed it. Options (a) and (d) make the technician the doer, and (b) is still passive.
> **Key point:** "Have something done" = arranged done by another; the doer is never the first subject.

---

## Section 9. Direct and indirect speech

### Q177. Report the speech: He said, "I am repairing the power supply."

- (a) He said that he is repairing the power supply.
- (b) He said that he was repairing the power supply.
- (c) He told that he was repairing the power supply.
- (d) He said that I was repairing the power supply.

> **Type:** MCQ
> **Answer:** He said that he was repairing the power supply (Option b).
> **Solution:** Two rules apply. The present simple backshifts to the past simple, and the pronoun "I" changes to "he" because the reporter is now the speaker. Option (a) omits the backshift, (c) drops the pronoun that must report the first person, and (d) leaves the pronoun as "I", which would make the speaker the reporter's own speaker.
> **Key point:** In reported speech, *is* becomes *was* and *I* becomes *he/she*.

### Q178. Report the speech: She said, "I have finished the report."

- (a) She said that she has finished the report.
- (b) She said that she had finished the report.
- (c) She said that she would finish the report.
- (d) She said that she has been finishing the report.

> **Type:** MCQ
> **Answer:** She said that she had finished the report (Option b).
> **Solution:** "Have" backshifts to "had", and "I" becomes "she". The reported speech describes a completed action that preceded the moment of speaking, which is exactly what the past perfect expresses. Option (a) omits the backshift, and (c) and (d) change the meaning rather than the form.
> **Key point:** *Have finished* → *had finished* in reported speech.

### Q179. [GATE-1] Report the speech: The manager said, "We are leaving tomorrow."

- (a) The manager said that we are leaving tomorrow.
- (b) The manager said that they were leaving the next day.
- (c) The manager said that he was leaving today.
- (d) The manager told that he would be leaving the following day.

> **Type:** MCQ
> **Answer:** The manager said that they were leaving the next day (Option b).
> **Solution:** Three changes are required. "We" becomes "they" or "he" because the reporter is not the speaker; "are" becomes "were" by backshift; and "tomorrow" becomes "the next day" because the point of reference has moved. Option (a) keeps the pronoun and tense of direct speech, (c) changes the meaning, and (d) uses "told" without an indirect object.
> **Key point:** *Say* takes *that* + clause; *tell* must be followed by a person.

### Q180. Report the speech: She told me, "I am not sure whether the test passed."

- (a) She told me that she was not sure if the test had passed.
- (b) She told me that she is not sure whether the test passed.
- (c) She told me that I was not sure whether the test had passed.
- (d) She told me whether she was not sure about the test.

> **Type:** MCQ
> **Answer:** She told me that she was not sure if the test had passed (Option a).
> **Solution:** The matrix clause backshifts to "she was not sure", and the embedded question backshifts independently to "the test had passed". Reporting verbs after "tell" require a named indirect object, which "me" supplies, and "that" introduces the whole clause. Option (b) backshifts nothing, and (d) converts a statement into a question.
> **Key point:** A reported question inside a statement still backshifts its own verb.

### Q181. Report the speech: He said to me, "Please close the window."

- (a) He asked me to close the window.
- (b) He told me that I should close the window.
- (c) He requested me closing the window.
- (d) He said to me that please you close the window.

> **Type:** MCQ
> **Answer:** He asked me to close the window (Option a).
> **Solution:** A request in direct speech is reported with "asked" followed by the person and a to-infinitive. Because "please" is a politeness marker rather than part of the message, it is dropped in the report. Option (b) changes the act of requesting into a statement of obligation, and (c) uses an ungrammatical gerund pattern.
> **Key point:** Reported requests become *asked somebody to do* something; *please* is dropped.

### Q182. [GATE-2] Report the speech: "Don't touch that," he said.

- (a) He told me not to touch that.
- (b) He said me not to touch that.
- (c) He told that I must not touch that.
- (d) He told me that not to touch that.

> **Type:** MCQ
> **Answer:** He told me not to touch that (Option a).
> **Solution:** A negative command is reported with "tell somebody not to do something"; "don't" becomes "not to", and an indirect object is required after "tell". Options (b) and (d) are ungrammatical, and (c) wrongly makes the prohibition a statement of necessity reported by a different verb.
> **Key point:** Negative commands report as *told somebody not to do* something.

### Q183. Convert to direct speech: She said that she was tired.

- (a) She said, "I am tired."
- (b) She said, "She was tired."
- (c) She said, "I was tired."
- (d) She said, "You are tired."

> **Type:** MCQ
> **Answer:** She said, "I am tired." (Option a).
> **Solution:** Converting back reverses the two changes that were made: "was" returns to "is" and "she" returns to "I", because the speaker is now the person being quoted. Option (c) reverses only the pronoun, and (b) and (d) change who is speaking.
> **Key point:** Reported → direct reverses the backshift and restores the first person.

### Q184. Convert to direct speech: The engineer said that he had lost the key.

- (a) The engineer said, "I have lost the key."
- (b) The engineer said, "I had lost the key."
- (c) The engineer said, "I lose the key."
- (d) The engineer said, "I will lose the key."

> **Type:** MCQ
> **Answer:** The engineer said, "I have lost the key." (Option a).
> **Solution:** "Had lost" is the backshifted form of "have lost", so the direct speech must use the present perfect. Option (b) would place the loss before the loss, and (c) and (d) change the tense class of the claim.
> **Key point:** The past perfect in reported speech came from the present perfect, not the past simple.

### Q185. [GATE-1] Convert to direct speech: Ram told me that he would call me the next day.

- (a) Ram told me, "I will call you tomorrow."
- (b) Ram told me, "He will call me tomorrow."
- (c) Ram told me, "I would call you the next day."
- (d) Ram told me, "I will call you the next day."

> **Type:** MCQ
> **Answer:** Ram told me, "I will call you tomorrow." (Option a).
> **Solution:** Three reversals are needed: "he" becomes "I" and "me" becomes "you" because Ram is the speaker; "would" becomes "will"; and "the next day" becomes "tomorrow". Option (b) keeps the wrong speaker, while (c) and (d) leave one change unreversed each.
> **Key point:** Reverse pronouns, time and modal together, or not at all.

### Q186. Convert to direct speech: The manager said that the meeting had been cancelled.

- (a) The manager said, "The meeting will be cancelled."
- (b) The manager said, "The meeting has been cancelled."
- (c) The manager said, "The meeting is cancelling."
- (d) The manager said, "The meeting had been cancelled."

> **Type:** MCQ
> **Answer:** The manager said, "The meeting has been cancelled." (Option b).
> **Solution:** "Had been cancelled" is the backshifted form of "has been cancelled", so the present perfect passive is restored. Option (a) changes the modality, (c) uses a non-existent continuous form for a passive, and (d) merely reproduces the reported form.
> **Key point:** Passive forms backshift too: *has been* + participle becomes *had been* + participle.

### Q187. Report the sentence with a reporting modifier: The technician said, "The delay was caused by a faulty sensor."

- (a) The technician told that the delay was caused by a faulty sensor.
- (b) According to the technician, the delay was caused by a faulty sensor.
- (c) The technician said to be caused by a faulty sensor.
- (d) According to the technician, the delay was caused by a faulty sensor yesterday.

> **Type:** MCQ
> **Answer:** According to the technician, the delay was caused by a faulty sensor (Option b).
> **Solution:** "According to" can replace "said" and requires no "that" clause. The verb "was caused" is already in the past, and a past verb is not backshifted, so it stays unchanged. Option (a) drops the pronoun "that" the reporting verb needs, and (d) adds a time reference that the original does not contain.
> **Key point:** *According to* replaces the reporting verb, and past verbs are not backshifted.

### Q188. Convert to direct speech: He said that the machine needed servicing.

- (a) He said, "The machine needs servicing."
- (b) He said, "The machine needed servicing."
- (c) He said, "The machine will need servicing."
- (d) He said, "The machine has needed servicing."

> **Type:** MCQ
> **Answer:** He said, "The machine needs servicing." (Option a).
> **Solution:** "Needed" is the backshifted form of the present simple "needs", and there is no subject or object pronoun to restore, so only the verb changes. Option (b) leaves the reported form unreversed, and (c) and (d) change the tense class.
> **Key point:** *Needed* in reported speech came from *needs*.

### Q189. Report the question: He asked me, "Are you coming to the seminar?"

- (a) He asked me if I was coming to the seminar.
- (b) He asked me that I was coming to the seminar.
- (c) He asked me if I am coming to the seminar.
- (d) He asked me whether you were coming to the seminar.

> **Type:** MCQ
> **Answer:** He asked me if I was coming to the seminar (Option a).
> **Solution:** A yes/no question is reported with "if" or "whether", the subject and auxiliary are inverted to statement order, and the verb backshifts: "Are you coming" becomes "if I was coming". Option (b) drops the conjunction, (c) keeps the un-backshifted tense, and (d) keeps the wrong pronoun.
> **Key point:** Reported yes/no questions use *if/whether* plus statement word order and a backshifted verb.

### Q190. Report the question: She asked, "Where is the transformer room?"

- (a) She asked where is the transformer room.
- (b) She asked where the transformer room was.
- (c) She asked where was the transformer room.
- (d) She asked that where the transformer room was.

> **Type:** MCQ
> **Answer:** She asked where the transformer room was (Option b).
> **Solution:** A wh-question keeps its question word but loses the interrogative inversion: "is the transformer room" becomes "the transformer room was". No conjunction such as "if" or "that" is used with a wh-word. Options (a) and (c) retain question order, and (d) adds a conjunction that wh-questions do not take.
> **Key point:** Wh-questions report without *if*, *that* or question order.

### Q191. [GATE-1] Report the question: The student asked the teacher, "How do I calibrate the probe?"

- (a) The student asked the teacher how he calibrated the probe.
- (b) The student asked the teacher how to calibrate the probe.
- (c) The student asked the teacher how did I calibrate the probe.
- (d) The student asked the teacher that how to calibrate the probe.

> **Type:** MCQ
> **Answer:** The student asked the teacher how to calibrate the probe (Option b).
> **Solution:** A question whose subject is the reporting speaker converts to a to-infinitive, because the implied subject of the action becomes the reporter's own "I" — here hidden in "how to". Option (a) changes the meaning by shifting the doer to the teacher, and (c) and (d) keep question order or add a conjunction.
> **Key point:** "How do I …?" reports as "how to …"; "How does he …?" keeps a pronoun.

### Q192. Report the question: He asked me, "Have you finished the calibration?"

- (a) He asked me if I have finished the calibration.
- (b) He asked me whether I had finished the calibration.
- (c) He asked me that I have finished the calibration.
- (d) He asked me if I had been finishing the calibration.

> **Type:** MCQ
> **Answer:** He asked me whether I had finished the calibration (Option b).
> **Solution:** The auxiliary "have" must both backshift to "had" and move behind the subject "I" to form statement order. Option (a) leaves the tense un-backshifted, and (d) uses a progressive form that the original does not contain.
> **Key point:** In a reported question, the auxiliary backshifts and the word order is inverted back.

### Q193. [GATE-2] Report the question: "Why did the test fail?" the director asked.

- (a) The director asked why did the test fail.
- (b) The director asked why the test had failed.
- (c) The director asked that why the test had failed.
- (d) The director asked why the test has failed.

> **Type:** MCQ
> **Answer:** The director asked why the test had failed (Option b).
> **Solution:** The past simple "did fail" backshifts to "had failed", and the question order is replaced by statement order after "why". No "that" or "if" is used with a wh-word. Option (a) keeps question order, (c) adds an impossible conjunction, and (d) leaves the tense un-backshifted.
> **Key point:** *Did* + verb backshifts to *had* + past participle.

### Q194. Convert to direct speech: The officer ordered the technicians to leave the building.

- (a) "Leave the building," the officer ordered the technicians.
- (b) The officer ordered the technicians, "I leave the building."
- (c) "You leave the building," ordered the officer to the technicians.
- (d) "I will leave the building," the officer ordered the technicians.

> **Type:** MCQ
> **Answer:** "Leave the building," the officer ordered the technicians (Option a).
> **Solution:** An indirect command built on "ordered somebody to do" becomes a direct command in the imperative, and the pronoun that stood for the commanded party becomes "you". Options (b) and (d) wrongly put the officer in the command, and (c) misplaces the reporting verb.
> **Key point:** Reported commands come back as imperatives, with *you* for the person commanded.

---

## Section 10. Articles, prepositions, and commonly confused word pairs

### Q195. [GATE-1] Choose the correct article: "She is ___ best engineer in the department and the only one who has worked on the switching supply."

- (a) a
- (b) an
- (c) the
- (d) no article

> **Type:** MCQ
> **Answer:** the (Option c).
> **Solution:** A superlative adjective takes the definite article, because it singles out one member of a definite set and compares it with all the rest. "A best engineer" is impossible and "an best" is impossible on sound as well as on form, so "the" is the only option that fits.
> **Key point:** Superlatives and ordinals take *the*; comparatives take no article.

### Q196. [GATE-2] Choose the correct article: "___ useful information about the failure was obtained from the calibration log."

- (a) A
- (b) An
- (c) The
- (d) no article at all

> **Type:** MCQ
> **Answer:** no article at all (Option d).
> **Solution:** "Information" is uncountable, so it takes neither "a" nor "an" in the ordinary singular sense; a singular countable article would require a countable noun. Options (a) and (b) are therefore unavailable, and "the" is reserved for a specific item already identified, which the sentence does not presuppose. Note that "an" is doubly wrong, since "information" begins with a consonant sound anyway.
> **Key point:** Uncountable nouns take no article, or *some*, *much* or *little*.

### Q197. Choose the correct article: "___ unit of capacitance is the farad, named after Michael Faraday."

- (a) A
- (b) An
- (c) The
- (d) No article at all

> **Type:** MCQ
> **Answer:** A (Option a).
> **Solution:** "Unit" is a countable singular noun with no article in a first, generic mention, so "a" is required; it begins with the consonant sound /j/ of "unit", so "an" is wrong. "The" would imply the reader already knows which unit is meant.
> **Key point:** A first generic mention of a countable singular takes *a* or *an*.

### Q198. Choose the option that fills both blanks correctly: "___ European Space Agency and ___ Indian Space Research Organisation both launch satellites."

- (a) the / no article
- (b) a / an
- (c) the / an
- (d) no article / the

> **Type:** MCQ
> **Answer:** the / no article (Option a).
> **Solution:** A proper organisation name takes "the" in this construction, which is option (a)'s first half. The second organisation is named by its full name and takes no article of its own, so the single "the" is shared across the compound subject joined by "and". Options (c) and (d) would put two articles in front of two co-ordinate proper names, and (b) is wrong for both.
> **Key point:** One *the* can govern two co-ordinate proper names joined by *and*.

### Q199. Choose the correct preposition: "The device was designed ___ low power consumption rather than high speed."

- (a) for
- (b) to
- (c) with
- (d) by

> **Type:** MCQ
> **Answer:** for (Option a).
> **Solution:** "Designed for" is the fixed combination when a purpose or goal is named. "Designed to" would need a to-infinitive, "designed with" would need a named material or feature, and "designed by" would need an agent.
> **Key point:** Learn verb–preposition pairs as single units, and check what kind of noun follows.

### Q200. Choose the correct preposition: "The measured values ___ from the simulated ones by less than 2 %."

- (a) from
- (b) to
- (c) with
- (d) of

> **Type:** MCQ
> **Answer:** from (Option a).
> **Solution:** "Differ from" is the fixed combination; "differ with" is not standard in this sense, and "differ to" and "differ of" do not exist. The clause "by less than 2 %" then correctly reports the size of the difference.
> **Key point:** "Differ" takes *from*; "vary" takes *with*.

### Q201. [GATE-1] Choose the correct preposition: "The board was divided ___ three factions, and only two of them voted for the proposal."

- (a) between
- (b) among
- (c) of
- (d) in

> **Type:** MCQ
> **Answer:** among (Option b).
> **Solution:** The established distinction is that *between* is used for two items and *among* for more than two, and the sentence says "three factions". Option (a) is the classic trap, and "divided of" and "divided in" are not the standard forms for this meaning.
> **Key point:** *Between two, among three or more* — but *between* the members of a group is also correct.

### Q202. Choose the correct preposition: "The failure was ___ a loose connection at the terminal block, not a defective component."

- (a) because
- (b) owing
- (c) due to
- (d) caused

> **Type:** MCQ
> **Answer:** due to (Option c).
> **Solution:** "Due to" is a preposition phrase and can stand alone in a sentence like this. "Because" is a conjunction and needs a clause, not a noun phrase; "owing" is an adjective and requires "to" after it; and "caused" is a past participle, so it would need "by" and would not fit a "was" construction.
> **Key point:** *Due to* takes a noun phrase; *because* takes a clause; *owing* is an adjective that needs *to*.

### Q203. [GATE-1] Choose the option that fills both blanks correctly: "The committee will ___ the revised drawing but ___ it from the earlier issue."

- (a) accept / except
- (b) except / accept
- (c) accept / accept
- (d) except / except

> **Type:** MCQ
> **Answer:** accept / except (Option a).
> **Solution:** "Accept" is a verb meaning to agree to receive, which is what the committee does with a drawing. "Except" is a preposition or conjunction meaning "other than", and the structure "except it from the earlier issue" is the standard use meaning "leaving it out". Options (c) and (d) fail on the second blank, and (b) fails on the first.
> **Key point:** *Accept* = take; *except* = leave out.

### Q204. Choose the option that fills both blanks correctly: "The filter must be ___ to the bandwidth of the channel, and the same component can be ___ unchanged in two different receivers."

- (a) adapted / adopted
- (b) adopted / adapted
- (c) adapted / adapted
- (d) adopted / adopted

> **Type:** MCQ
> **Answer:** adapted / adopted (Option a).
> **Solution:** *Adapt* means to modify something to fit new conditions, and "adapted to" is also the fixed phrase for being suited to a specification. *Adopt* means to take up a practice, a policy or a plan without necessarily changing it, which is what "adopted unchanged" requires. Option (b) exchanges the two, and (c) and (d) collapse the contrast the sentence is built on.
> **Key point:** *Adapt* = modify to fit; *adopt* = take up as it stands.

### Q205. Choose the option that fills both blanks correctly: "The stray capacitance will ___ the resonant frequency, and the ___ of the change was a shift of 40 kHz."

- (a) affect / effect
- (b) effect / affect
- (c) affect / affect
- (d) effect / effect

> **Type:** MCQ
> **Answer:** affect / effect (Option a).
> **Solution:** *Affect* is the verb meaning to influence, and it takes a direct object — here "the resonant frequency". *Effect* is the noun meaning the result, and it belongs before the prepositional phrase "of the change". Because the second blank requires a noun, only (a) is possible on grammatical grounds alone.
> **Key point:** *Affect* (v) = influence; *effect* (n) = result.

### Q206. Choose the option that fills both blanks correctly: "The ___ of superposition is that the total response is the sum of the individual responses; the ___ component in the circuit is the resistor."

- (a) principle / principal
- (b) principal / principle
- (c) principle / principle
- (d) principal / principal

> **Type:** MCQ
> **Answer:** principle / principal (Option a).
> **Solution:** *Principle* is a noun meaning a general law or rule, which is what the statement about superposition is. *Principal* is an adjective meaning chief or most important, and it modifies "component" as a rank. Option (b) reverses the two, and (c) and (d) cannot both be adjectives or both be nouns in these slots.
> **Key point:** *Principle* = rule; *principal* = chief (and also the head of a school).

### Q207. Choose the option that fills both blanks correctly: "The two stages are ___ to one another, and their output voltages ___ to a constant sum."

- (a) complementary / complement
- (b) complement / complementary
- (c) complementary / complementary
- (d) complement / complement

> **Type:** MCQ
> **Answer:** complementary / complement (Option a).
> **Solution:** The first blank is an adjective describing the stages, and only "complementary" ends in -ary and takes that role; "complement" is a noun. The second blank is a verb, and "complement" is the verb meaning to supply what is missing. Option (b) puts the noun in the adjective slot, and (c) supplies an adjective where a verb is required.
> **Key point:** *Complement* can be noun, verb or adjective; *compliment* is always about praise.

### Q208. Choose the option that fills both blanks correctly: "The interviewer was careful not to ___ an answer the witness did not wish to give; the recording of the conversation was plainly ___, and the case was dropped."

- (a) elicit / illicit
- (b) illicit / elicit
- (c) elicit / elicit
- (d) illicit / illicit

> **Type:** MCQ
> **Answer:** elicit / illicit (Option a).
> **Solution:** *Elicit* is a verb meaning to draw out a response, which fits "not to elicit an answer". *Illicit* is an adjective meaning unlawful, which fits "the recording was plainly illicit" and requires the vowel sound at the start. Option (b) exchanges them, and (c) and (d) fail the part of speech of the second blank.
> **Key point:** *Elicit* = draw out (v); *illicit* = unlawful (adj), with two l's and two i's.

### Q209. Choose the option that fills both blanks correctly: "The ___ solution was to reuse the existing cable rather than lay a new one; the account sounded ___, and nobody believed it."

- (a) ingenious / ingenuous
- (b) ingenuous / ingenious
- (c) ingenious / ingenious
- (d) ingenuous / ingenuous

> **Type:** MCQ
> **Answer:** ingenious / ingenuous (Option a).
> **Solution:** *Ingenious* is a positive adjective meaning cleverly inventive, which describes a solution that reuses an existing asset. *Ingenuous* is a negative adjective meaning artless and innocent, which is exactly the verdict on an account nobody believed. Option (b) reverses them, and (c) and (d) apply one word where the contrast is between two.
> **Key point:** *Ingenious* = inventive; *ingenuous* = artlessly honest.

### Q210. [GATE-1] Choose the option that fills both blanks correctly: "A referee must remain ___ from the two clubs; the ___ spectators left before the second half."

- (a) disinterested / uninterested
- (b) uninterested / disinterested
- (c) disinterested / disinterested
- (d) uninterested / uninterested

> **Type:** MCQ
> **Answer:** disinterested / uninterested (Option a).
> **Solution:** *Disinterested* means impartial — the referee's required quality — and it is a distinct word from *uninterested*, which merely means bored. *Uninterested* describes the spectators who left early, who are bored rather than impartial. Option (b) puts the wrong word in the referee's slot, and (c) and (d) erase the contrast.
> **Key point:** *Disinterested* = impartial; *uninterested* = not interested.

### Q211. Choose the option that fills both blanks correctly: "Nobody realised how ___ a catastrophic failure was until the root cause was identified; the investigation was led by an ___ engineer with forty years of experience."

- (a) imminent / eminent
- (b) eminent / imminent
- (c) imminent / imminent
- (d) eminent / eminent

> **Type:** MCQ
> **Answer:** imminent / eminent (Option a).
> **Solution:** *Imminent* means about to happen, which describes the approaching failure. *Eminent* means distinguished and famous, which describes the engineer's standing and is a compliment to her record. Option (b) exchanges them, and (c) and (d) lose the deliberate near-homophone contrast.
> **Key point:** *Imminent* = about to occur; *eminent* = distinguished, with an *e* after the *m*.

### Q212. [GATE-2] Choose the option that fills both blanks correctly: "The commissioning procedure must ___ that the earth continuity is tested, and the manager ___ the customer that the delay was outside the company's control."

- (a) ensure / assured
- (b) assured / ensured
- (c) ensure / ensured
- (d) assured / assured

> **Type:** MCQ
> **Answer:** ensure / assured (Option a).
> **Solution:** *Ensure* is a verb meaning to make certain that something is done, and it takes a that-clause — here that a test is carried out. *Assure* is a verb meaning to tell someone confidently, and it takes a person as its object. The two words are easily confused because *insurance* derives from *insure*, a third verb meaning to cover by policy; only two of the three are needed here.
> **Key point:** *Ensure* = make sure; *assure* = reassure a person; *insure* = cover by policy.

---

## Section 11. Precis and abstract summary

A precis states the core of a passage in one or two sentences. It drops examples, figures and
rhetoric, and it keeps the claim, the reason and any limit the author explicitly states.

**Passage 13.** Two desalination plants on the same coast produce identical water at very different prices, and the difference is not engineering. The first takes its feed from a deep offshore well where the water needs only a light polish; the second takes shallow surface water carrying a heavy load of silt and boron, and must be pushed harder and cleaned twice. Both meet the same quality specification and both were built within a decade of each other. The residents, asked which plant the council should approve, split almost evenly, and the council has postponed the decision twice. An engineer asked to advise says the choice is not technical at all, but a choice about how much of the household budget to spend on water the district already receives free from a river forty kilometres away.

### Q213. Which of the following is the best one-sentence precis of Passage 13?

- (a) Two desalination plants serving one district differ in price because of the quality of their feed water, so the council's real choice is how much of the household budget to spend on water the district already receives free from a river.
- (b) Desalination is always more expensive than river water, and councils should stop building desalination plants entirely.
- (c) The residents of the district are almost evenly divided on which of the two plants the council should approve.
- (d) An engineer has advised the council that the choice between the two plants is a technical question rather than a budgetary one.

> **Type:** MCQ
> **Answer:** The price difference comes from feed-water quality, so the council's real choice is a budget question (Option a).
> **Solution:** A precis must keep the cause the passage identifies (feed-water quality) and the point the passage ends on (a budget choice, not a technical one). Option (c) is a single detail, and option (d) reverses the engineer's statement, which says the opposite. Option (b) adds a recommendation the passage never makes.
> **Key point:** A precis keeps the passage's cause and its conclusion, not its most quotable detail.

---

**Passage 14.** When a six-month project ends four weeks late, the temptation is to blame a supplier who was three weeks late on a part not even on the critical path. The measurement that actually matters is shorter. Count the weeks of delay inside the work the team controlled, and there were only one; the rest was waiting for hardware, for a building inspection, and for a single signature that took eleven days. Of that one week, nine days went into a design approved without a thermal check. The project did not fail: it arrived late, cost eleven per cent more than planned, and the specific cause was nine days of a simulation nobody ran. The useful lesson is neither about suppliers nor about planning; it is that a delay must be attributed first to whoever could have prevented it.

### Q214. Write a precis of Passage 14 in one sentence of about 30 words, keeping the claim, one figure, and the generalisation, and dropping the list of excuses.

> **Type:** Theory
> **Answer:** A six-month project ran four weeks late, but only one week of the delay was the team's own — nine days of an unrun thermal check — showing that delay must be blamed first on whoever could have prevented it.
> **Solution:** The passage's structure is claim, then evidence, then a refusal of two obvious conclusions ("neither about suppliers nor about planning"), then a transferable rule. A precis keeps one figure (nine days), the claim (the project's specific cause), and the rule. The signature that took eleven days, the eleven per cent overspend, the building inspection and the supplier are all instances, and instances are the first thing a precis drops.
> **Key point:** In a post-mortem, keep the generalisation at the end and delete the parade of excuses.

---

**Passage 15.** Every battery at the end of its life must be collected, because a lithium cell left in household waste can ignite in a truck and destroy the load around it. Collection, however, is only the beginning. A cell must be discharged to a safe voltage, dismantled and its metals separated, and the dismantling done by a licensed facility; a household that opens a cell in the kitchen has not recycled it, it has redistributed the risk. The economics are unforgiving. Disassembly recovers a few per cent of the value of a new cell, so processing a battery costs more than the metal inside it, and no recycler earns a margin on material alone. Only two things have ever made collection pay: a producer-responsibility rule, which pays for collection, and a high cobalt price, which pays for the metal.

### Q215. Which of the following is the best one-sentence precis of Passage 15?

- (a) End-of-life lithium cells must be collected for safety, but because recovery yields only a few per cent of a new cell's value, collection only pays when a producer-responsibility rule or a high metal price covers it.
- (b) Lithium batteries are a fire risk in household waste and must be handed to a licensed facility rather than opened at home.
- (c) The economics of battery recycling are decided entirely by the price of cobalt.
- (d) Disassembling a battery recovers only a few per cent of the value of a new cell.

> **Type:** MCQ
> **Answer:** Collection is necessary for safety, but it only pays when a rule or a metal price covers it (Option a).
> **Solution:** The passage has two claims, and a precis needs both: the safety imperative and the economic impossibility. Option (b) keeps only the safety claim, option (c) drops one of the two paying conditions by making the other exclusive, and option (d) is a figure with no consequence attached.
> **Key point:** When a passage ends on "the only two things", the precis must name both.

---

**Passage 16.** The usual argument for building sensors into a city is measurement. A city that
cannot see its own air cannot manage it, and the standard response to a pollution complaint is to
argue that the complaint is unsupported by data. For a decade that argument was accepted, and
instruments were bought accordingly. Then a study compared the official monitors with a hundred
low-cost sensors placed on balconies, and the two sets of numbers disagreed so badly that a third
of the officially reported exceedance days turned out not to have exceeded anything at all. The
programme that followed did not buy more official monitors. It bought more low-cost sensors, and it
used them to find the official monitors that were badly sited. The pivot, in other words, was not
from ignorance to knowledge, but from one instrument to many.

### Q216. Passage 16 turns on a single reversal. State that reversal in one sentence, naming which side the author treats as the error.

> **Type:** Theory
> **Answer:** The city blamed too little official data, when the real fault was badly sited official monitors, so the fix was more low-cost sensors rather than more official ones.
> **Solution:** A passage that pivots has two positions, and a precis of it must contain both, otherwise the reader is left with the position the author rejects. Here the rejected position is the first four sentences — that measurement was inadequate — and the retained one is the last two, that the instruments were in the wrong places. The hundred balcony sensors and the third of exceedance days are evidence for the turn and are dropped.
> **Key point:** In a pivoting passage, the rejected position is as indispensable to the precis as the accepted one.

---

**Passage 17.** A city is warmer in the middle than at its edges, because the middle has less bare ground. A park does not only cool the person under the tree; it moves water from the soil into the air, and that water takes heat from everything nearby, including the brick across the street. Planting therefore behaves unlike almost every other civic investment. A new road is used once or twice a day and its benefits accrue to whoever is on it; a tree costs money for years before it casts usable shade, and its effect is felt by whole streets, including people who never go near it. This is why cities that have planted heavily still measure little change in summer temperature at the regional scale, while planted streets are measurably cooler at pedestrian height.

### Q217. Which of the following is the best one-sentence precis of Passage 17?

- (a) Street-level planting cools local areas measurably even where it barely moves city-wide temperature, because trees release water vapour and their benefits accrue over years to people who never visit them.
- (b) Cities should plant trees more heavily, because summer temperatures at regional scale are already falling.
- (c) A park cools only the people who sit under its trees, not the surrounding buildings.
- (d) A new road delivers more benefit per rupee spent than a street tree does.

> **Type:** MCQ
> **Answer:** Planting cools streets measurably without moving city-wide figures, because trees release water vapour and benefit bystanders over years (Option a).
> **Solution:** The passage's puzzle is the apparent conflict between a null result at city scale and a real one at street scale, and the precis must resolve it by keeping the mechanism. Option (b) states the opposite of the last sentence, option (c) denies what the second sentence asserts, and option (d) reverses the comparison made in the fourth sentence.
> **Key point:** When a passage poses an apparent conflict, the precis must carry the explanation that dissolves it.

---

**Passage 18.** A workshop that replaced all its machine tools in a single year spent more and got less production. The same workshop that replaced one tool every second year, for the same total, ran at ninety-four per cent of capacity. A hospital that rebuilt its entire imaging department at once lost scanning capacity for eleven months; the same hospital rebuilding one scanner a year never lost any. A university that changed its whole curriculum in one step spent two years on committees and produced no better results. Four stories, and they say the same thing: a capability that must be continuously available is the one you cannot afford to replace in a single window. Replacing a whole system is not one large improvement; it is a long interval in which nothing is available.

### Q218. Write a precis of Passage 18 in about 30 words, omitting all four examples and retaining only the generalisation.

> **Type:** Theory
> **Answer:** A capability that must be continuously available cannot be replaced all at once, because replacing a whole system is a long interval in which nothing is available.
> **Solution:** Four instances support one generalisation, and the generalisation arrives in the penultimate sentence and is restated in the last. A precis of this shape is the generalisation alone: the ninety-four per cent, the eleven months and the two years of committees are the evidence, not the point. Keeping any instance is the commonest failure in a precis question, because the instances are memorable and the rule is not.
> **Key point:** When a passage piles up examples, the one sentence they all support is the entire precis.

---

**Passage 19.** Open hardware is often described as free, and the description is the source of most disappointment. The design may cost nothing, but a board still has to be laid out, routed, made in small quantities, tested and brought up in firmware, and none of that cost falls when the design is published. A design open for a decade and never built has not failed; it has simply never been paid for. What openness does change is the second cost. When a design is available a dozen organisations can build it, and the twelfth pays almost nothing for the eleven before, because the errors have already been found and documented. The result is a market in which the first build is expensive and every build after it is cheap, the reverse of the usual curve.

### Q219. Which of the following is the best one-sentence precis of Passage 19?

- (a) Open hardware is free in design but not in manufacture, so the first build is expensive and every later build is cheap because other builders have already paid to find the errors.
- (b) Open hardware is cheaper than proprietary hardware in every respect, from design through manufacture.
- (c) Publishing a design under an open licence guarantees that somebody will eventually build it.
- (d) The cost of writing and debugging firmware falls to zero once a design is published.

> **Type:** MCQ
> **Answer:** The design is free but the build is not, so the first builder pays and later ones benefit (Option a).
> **Solution:** The passage's structure is a correction of a common description, an explanation of why it is wrong, and a statement of what is actually true instead. Options (b) and (d) both claim costs fall to zero, which the passage explicitly denies, and (c) contradicts the sentence about a design that has been open for a decade and never built.
> **Key point:** A precis of a corrective passage must contain the correction, not the thing corrected.

---

**Passage 20.** For thirty years the standard explanation of why a class of early digital machines failed was that their engineers knew the hardware and not the software. The explanation was tidy, widely taught and largely untested, because the failed machines were gone and their programs lost with them. When a warehouse was opened last year, three of the machines were found working, with a card deck that computed something nobody had claimed it could. The programs were legible, written in the same languages and conventions; what they lacked was any way to express a loop whose trip count was not known in advance. The lost decades of hardware redesign were an attempt, in hardware, to supply a feature the language had never had. The engineers had known the software perfectly. The software had been the limitation.

### Q220. Write a precis of Passage 20 in about 30 words, stating the claim that the recovered evidence overturned and the claim that replaces it.

> **Type:** Theory
> **Answer:** The received explanation — that the engineers' weakness was software — was wrong; the language lacked any way to express a loop with an unknown trip count, and the hardware redesigns were attempts to supply it.
> **Solution:** The passage is a single reversal sustained from the first sentence to the last, and the two last sentences are deliberately parallel, one withdrawing the old claim and one stating the new. A precis of a reversal must keep both halves, because either alone misrepresents the passage. The warehouse, the card deck and the notations are the route to the conclusion and belong in the reading, not in the summary.
> **Key point:** Parallel closing sentences are usually the passage's verdict; quote their structure in the precis.

---

**Passage 21.** Hospitals are treated as quiet places, and the noise in them is mostly mechanical: air
handling, bed alarms, infusion pumps and the corridors of trolleys. Two measurements are usually
reported, and both of them mislead. The first is the average sound level over twenty-four hours,
a number that rewards a building that is silent at three in the morning and deafening at three in
the afternoon. The second is compliance with a peak limit, which a hospital can satisfy with alarms
set to their maximum, because the peaks are what get measured. The measurement that actually
predicts a patient's sleep is the number of events above a threshold between ten at night and six
in the morning; in two hospitals with similar average levels, that number differed by a factor of
three, and the sleep complaints differed with it.

### Q221. Which of the following is the best one-sentence precis of Passage 21?

- (a) The standard hospital noise metrics — the twenty-four-hour average and compliance with a peak limit — can look acceptable in two hospitals whose night-time event counts differ threefold and whose sleep complaints differ accordingly.
- (b) Hospitals are noisier at night than during the daytime.
- (c) Bed alarms are the single largest source of noise in a hospital.
- (d) Patients sleep badly in hospitals because of the noise made by trolleys in the corridors.

> **Type:** MCQ
> **Answer:** Standard noise metrics can look acceptable in hospitals that differ threefold in night-time noise events and in sleep complaints (Option a).
> **Solution:** The passage's argument is that two widely used metrics mislead, and its proof is the pair of hospitals that match on the average and differ on the event count. Option (a) is the only choice that carries the metric, the comparison and the consequence together. Options (b) and (d) are claims the passage never makes, and (c) promotes one of four listed sources to sole cause.
> **Key point:** A precis must carry the passage's method of proof, not merely its conclusion.

---

**Passage 22.** A survey of four hundred firms asked how much of their annual expenditure on
instrumentation went into calibration as against replacement. The answers were collected over
eighteen months by email, and the response rate was thirty-one per cent, which the authors state
plainly. The headline finding is that firms reporting any calibration spend also report lower
unscheduled downtime, and that the relationship is stronger where the instrumentation is older
than eight years. The authors are careful about what they do not claim. They do not claim that
calibration reduces downtime, because the firms that calibrate more may simply be the firms that
were already better managed. What they do claim is that the association is strong enough to justify
a trial in which calibration expenditure is set as an independent variable.

### Q222. Write a precis of Passage 22 in two clauses: what the survey establishes, and what it explicitly does not establish.

> **Type:** Theory
> **Answer:** Firms that spend on calibration report less unscheduled downtime, more strongly when the instrumentation is older; the survey does not establish that calibration causes this, only that the association justifies a controlled trial.
> **Solution:** The passage devotes more space to what the authors refuse to claim than to what they claim, so a precis that omits the refusal misrepresents it. The response rate of thirty-one per cent and the sample of four hundred are methodological detail, and the older-than-eight-years refinement narrows the finding without becoming the finding. Two clauses, one for each half, is the right shape here.
> **Key point:** When a passage states what it does *not* prove, that limitation belongs in the precis.

---

## Section 12. Reasoning traps in reading and rapid-fire recall

**Context for Q223–Q228.** Each item gives a short passage and an exam-style question about it.
Exactly one option is defensible; the others fail for the reason named in its solution.

### Q223. [GATE-1] "The audit was carried out by a team that had no prior relationship with the department, and its report recommended a full redesign of the logging system."

Question: *What is the author's opinion of the auditors' independence?*

- (a) The author considers it a strength of the audit.
- (b) The author considers it a weakness of the audit.
- (c) The author's opinion cannot be determined from the passage.
- (d) The author believes the audit should have been carried out by the department itself.

> **Type:** MCQ
> **Answer:** The author's opinion cannot be determined from the passage (Option c).
> **Solution:** The passage reports a fact — the auditors had no prior relationship — and the word "independent" is doing descriptive work, not evaluative work. There is no evaluative adjective and no sentence praising or criticising the arrangement. Options (a) and (b) supply an attitude the text does not carry, and (d) supplies a recommendation the text does not make. In GATE-style comprehension, an opinion question on a purely descriptive passage is a trap with the answer "not stated".
> **Key point:** If the passage only reports, the author's opinion is not stated — do not supply one.

### Q224. [GATE-1] "A study found that a periodic velocity curve can be distinguished from a stellar wobble caused by a sunspot or a magnetic cycle."

Question: *According to the passage, does the method always succeed in identifying a planet?*

- (a) Yes, because a periodic curve is unique to an orbiting body.
- (b) Yes, provided the observations span several cycles.
- (c) No; the passage does not claim the method always succeeds.
- (d) No, because the method measures only the star's brightness.

> **Type:** MCQ
> **Answer:** No; the passage does not claim the method always succeeds (Option c).
> **Solution:** The sentence says a periodic curve "can be distinguished" from certain alternatives, which is a claim of discrimination, not a guarantee. Options (a) and (b) add an absolute condition the passage does not state, and (d) misstates the method, which measures velocity. A question containing "always" is almost always false, because passages are written in terms of tendencies.
> **Key point:** Treat "always", "never" and "only" in a question as claims requiring explicit support.

### Q225. "The report notes that the transformer was replaced in 2018 and that the new unit has run without an oil leak since."

Question: *Which of the following voltage levels was available for that transformer in the market at the time?*

- (a) 33 kV
- (b) 110 kV
- (c) 220 kV
- (d) none of these can be determined from the passage

> **Type:** MCQ
> **Answer:** None of these can be determined from the passage (Option d).
> **Solution:** The question asks about external facts, and no amount of careful reading of this passage can produce them; that is what makes (d) the answer rather than a failure of comprehension. The three numbers are offered precisely because a reader who has read the passage will be tempted to supply one from background knowledge. In an exam, a question that the passage plainly cannot answer is testing whether you will invent an answer.
> **Key point:** When the passage lacks the information entirely, the correct response is that it cannot be determined.

### Q226. "The paper does not claim that the low-cost sensor network is more accurate than the official monitors; it claims only that the two sets of numbers disagreed."

Question: *Which claim is presupposed by the question "How much more accurate is the official monitor?"*

- (a) That the official monitors are more accurate.
- (b) That the low-cost sensors are more accurate.
- (c) That the two are equally accurate.
- (d) That both kinds of monitor were badly sited.

> **Type:** MCQ
> **Answer:** That the official monitors are more accurate (Option a).
> **Solution:** The phrase "how much more" presupposes that the official monitor *is* more accurate, and it is that presupposition the question is testing. The passage explicitly declines to make that claim, so the question cannot be answered from the passage. Options (b), (c) and (d) are not presupposed by the wording. Asking what a question *presupposes* is a different skill from asking what it *asks*.
> **Key point:** Separating what a question asks from what it presupposes is a standard reading trap.

### Q227. "Two hospitals reported the same average sound level and the same proportion of excursions above the daytime limit, but the first had three times as many night-time events and correspondingly more sleep complaints."

Question: *Which of the following best explains the difference in sleep complaints between the two hospitals?*

- (a) The first hospital had poorer sound insulation in the wards.
- (b) The first hospital's air handling was mechanically noisier.
- (c) The first hospital's noise events were concentrated in the hours when patients were trying to sleep.
- (d) The first hospital had fewer beds and therefore a lower average.

> **Type:** MCQ
> **Answer:** The first hospital's noise events were concentrated in the hours when patients were trying to sleep (Option c).
> **Solution:** The passage reports two hospitals that match on the average and on the daytime limit but differ on night-time events, and the complaint difference follows that variable. Option (c) is the only one that names the variable the passage itself identifies. Options (a), (b) and (d) each introduce a cause the passage has already excluded by making the hospitals equal on other measures.
> **Key point:** The right explanation is the one that accounts for what the passage made equal and what it made different.

### Q228. "The author's opening sentence is: 'A transform is a change of coordinates, and the whole of the theory of the Laplace transform is the claim that one particular change of coordinates is legal only inside a strip.'"

Question: *In the second paragraph, the author says the region of convergence is the whole s-plane. Which of the signals described there does this refer to?*

- (a) A right-sided signal that grows no faster than an exponential
- (b) A signal that exists only on a finite interval
- (c) A two-sided signal whose left tail grows faster than its right tail
- (d) A signal that is zero for all t except one point

> **Type:** MCQ
> **Answer:** A signal that exists only on a finite interval (Option b).
> **Solution:** The sentence in question classifies three cases: a right-sided signal gives a half plane, a finite-duration signal gives the whole s-plane, and a two-sided signal with mismatched tails gives a vertical strip. Only (b) is assigned the whole plane, so it is the only option the passage supports. Options (a) and (c) are explicitly given other regions, and (d) is not described at all.
> **Key point:** With several cases listed in one sentence, match the attribute to the correct case directly.

### Q229. In converting an active sentence to the passive voice, what happens to the original object and the original subject?

> **Type:** Theory
> **Answer:** The original object becomes the subject of the passive sentence, and the original subject becomes the agent, usually introduced by "by".
> **Solution:** "The technician replaced the capacitor" becomes "The capacitor was replaced by the technician". The verb changes from active to the appropriate be + participle form, the tense is otherwise unchanged, and the two noun phrases exchange grammatical roles. An agentless passive simply omits the "by" phrase.
> **Key point:** Active → passive swaps the roles of the two noun phrases; it does not change the tense.

### Q230. In reported speech, what happens to a present perfect tense and to the pronoun "I"?

> **Type:** Theory
> **Answer:** A present perfect backshifts to the past perfect, and "I" changes to "he" or "she" and "me" to "him" or "her".
> **Solution:** "I have finished" is reported as "he said that he had finished", and "have" backshifts to "had". The pronoun change occurs because the speaker is no longer the speaker: the reported clause is now observed from outside. Verbs already in the past are not backshifted a second time.
> **Key point:** In reported speech, *have* → *had* and *I/me* → *he/she*, *him/her*.

### Q231. Name the four error types most often found in subject–verb agreement questions, with one test for each.

> **Type:** Theory
> **Answer:** (1) Intervening phrase: in "the list of parts **are**", agree with the head noun "list". (2) Long relative clause: "the number of hours, which cost a day, **were**" still takes "was". (3) "Together with", "as well as", "along with": these supplement the subject and do not pluralise it. (4) Distance in time or words: "The committee have decided" is a judgement about dialect, but "neither … nor" and "either … or" always take the nearer subject's number.
> **Solution:** Every agreement error is a case of the verb latching on to the wrong noun. The four tests above are just four ways of finding the true head noun: look past the preposition, look past the relative clause, look past a supplement, and look for the nearest of a pair. The "each", "every" and "one of" family takes a singular verb because the quantifier itself is singular.
> **Key point:** Find the true head of the subject, then agree — the verb follows the head, not the nearest noun.

### Q232. Give the one-line distinctions for four commonly confused pairs.

> **Type:** Theory
> **Answer:** *accept* = take, *except* = leave out; *adapt* = modify to fit, *adopt* = take up unchanged; *affect* (v) = influence, *effect* (n) = result; *principle* = rule, *principal* = chief.
> **Solution:** Each pair differs either in part of speech or in the plain-English sense. Accepting a drawing is taking it; excepting it from a list is leaving it out. Adapting a filter changes it; adopting one takes it as it stands. A stray capacitance affects the resonant frequency; the effect of that is a shift. A principle is a general law, as in the principle of superposition; a principal component is the chief one, or a school's head.
> **Key point:** Distinguish confused pairs by part of speech first, by plain English second.

### Q233. What is the most reliable first move when a main-idea question gives four options?

> **Type:** Theory
> **Answer:** Decide which option the passage would still be worth reading for, and check it against the sentence that the passage builds its explanation around.
> **Solution:** A correct main-idea option survives the test of the whole passage, not of one vivid sentence. Typical wrong options are a true detail lifted from one sentence, a claim drawn from outside the passage, and an absolute statement. Reducing the passage to a single proposition and matching it against the options is faster and more reliable than reading the options first.
> **Key point:** A main idea must cover the whole passage; check it against the explanatory sentence, not the most striking one.

### Q234. [GATE-2] Give the three rules a reader applies to a question whose answer must be located in the passage, and state the trap in each.

> **Type:** Theory
> **Answer:** (1) Match the exact noun the question uses, because a paraphrase of the question's word may be a different concept in the passage. (2) Check the scope of the match, because a fact stated for one case is often wrongly generalised to all cases. (3) Check for an exception, because a passage that lists cases usually attaches a qualifying phrase to one of them.
> **Solution:** Each rule corresponds to a standard failure. Rule one is defeated by synonyms that change meaning, as when "cost" and "time" are interchanged. Rule two is defeated by a sentence that says "for a right-sided signal … it is a half plane", which must not be read as applying to two-sided signals. Rule three is defeated by ignoring "for a signal that exists only on a finite interval", which is precisely the phrase that makes option one of a set correct.
> **Key point:** Locate by exact match, then verify scope, then look for the qualifying exception.

---

## Quick revision — Verbal Ability & Comprehension

- Active → passive makes the old object the subject and the old subject the agent after "by"; passive → active reverses that and restores the tense. Neither conversion ever changes the tense.
- Modal → passive is modal + *be* + participle ("must tighten" → "must be tightened"); the progressive adds *being* ("is repairing" → "is being repaired"); the modal perfect is modal + *have been* + participle.
- "Have something done" is causative — the first subject arranges the work, so the active form needs a *different* doer.
- Be + adjective ("he is a surgeon") is a link, not a passive; a passive needs a past participle and no *have*.
- A yes/no question becomes active with "did" + base verb + an invented subject: "Were you tested?" → "Did somebody test you?"
- Reported speech: *is/am/are* → *was/were*, *have* → *had*, *will* → *would*, *can* → *could*.
- Reported speech: *I/me* → *he, she/him, her*; *today/now* → *that day/then*; *tomorrow* → *the next day*.
- Past-tense verbs are **not** backshifted again: "said, 'The delay was caused…'" reports with "was caused" unchanged.
- *Say* takes *that* + clause; *tell* must be followed by a person, and confusing them is an automatic error.
- Reported requests become *asked somebody to do*; reported commands become *warned/ordered somebody not to do*.
- A reported yes/no question uses *if* or *whether* with statement word order, and backshifts even when it sits inside a statement; a wh-question uses neither, and "How do I …?" becomes "how to …".
- Subject–verb agreement follows the head noun: "the list of parts **is**", "the number of hours, which cost a day, **was**".
- "Together with", "as well as" and "along with" supplement the subject — they never pluralise it.
- *Neither … nor* and *either … or* take the verb of the **nearer** subject; *each*, *every* and *one of the* take a singular verb.
- A dangling participle is repaired by giving the phrase a subject that can perform the action: "Walking …, the frost was visible" → "… the inspector could see".
- *Since* takes a point in time, *for* takes a period; "has been running **since** three hours" is wrong.
- *Deny*, *admit* and *resist* take a gerund or a that-clause, never a to-infinitive; *suggest*, *recommend* and *advise* likewise take a gerund, while *ask someone to* takes an infinitive.
- Parallelism: one list, one form — in "to postpone …, to ask … and to reconvene", a single "to ask" among gerunds must be regularised.
- Articles follow sound, not spelling: *a* engineer (the /e/ of "engine"), *an* important respect, *a* unit.
- Superlatives and ordinals take *the*; comparatives take no article; one *the* can govern "the ESA and the ISRO".
- Uncountable nouns take no article: no "a/an information"; they pair with *some*, *much* and *little*, not *few*/*a few*.
- *Between* is for two, *among* for more than two; *due to* takes a noun phrase, *because* a clause, *owing* needs *to*.
- Confused pairs: *accept* = take, *except* = leave out; *adapt* = modify to fit, *adopt* = take up unchanged.
- Confused pairs: *affect* (verb) = influence, *effect* (noun) = result; *principle* = rule, *principal* = chief.
- Confused pairs: *complement* = complete, *compliment* = praise; *elicit* = draw out, *illicit* = unlawful.
- Confused pairs: *ingenious* = inventive, *ingenuous* = artless; *disinterested* = impartial, *uninterested* = bored.
- Confused pairs: *imminent* = about to happen, *eminent* = distinguished; *ensure* = make sure, *assure* = reassure a person, *insure* = cover by policy.
- *Less* counts, *fewer* counts the countable: "fewer components", "less gain".
- A main-idea option must survive the whole passage, not one vivid sentence; the trap options are a lifted detail, an outside claim and an absolute.
- A question containing "always", "never" or "only" is almost always false, because a passage states tendencies, not guarantees.
- If the passage only reports, the author's opinion is not stated — do not supply one.
- A question the passage plainly cannot answer has one correct response: it cannot be determined.
- Locate a detail by exact noun match, then check the scope, then hunt the qualifying exception.
- A precis drops every example and keeps the claim, the reason and any limit the author explicitly states; a passage ending in "the only two things" needs both named.
- A passage that pivots needs **both** positions in the summary; the rejected one is what tells the reader what the author corrected.
