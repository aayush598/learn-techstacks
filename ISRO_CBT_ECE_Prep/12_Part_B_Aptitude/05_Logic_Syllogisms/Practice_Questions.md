# Logic Syllogisms - Practice Questions (ISRO CBT ECE Style)

> **Exam Pattern**: 15 questions, 20 marks, NO negative marking
> **Time Target**: 1.5 minutes per question
> **Instructions**: Attempt ALL questions. Use Venn diagrams for complex syllogisms.

---

## Question 1: Basic Syllogism

**Premises:**
1. All engineers are scientists
2. All ISRO employees are engineers

**Conclusion:** All ISRO employees are scientists.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
Chain rule:
- All ISRO employees are engineers (given)
- All engineers are scientists (given)
- Therefore: All ISRO employees are scientists ✓

This is a classic "Barbara" syllogism (AAA-1).

**Answer: (A)** — Definitely true.

---

## Question 2: Undistributed Middle

**Premises:**
1. All dogs are animals
2. All cats are animals

**Conclusion:** All cats are dogs.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
Venn diagram:
- "Dogs" circle is entirely inside "Animals"
- "Cats" circle is entirely inside "Animals"
- But Dogs and Cats could be separate circles within Animals

The middle term "animals" is never distributed (never refers to ALL animals).
This is the Fallacy of Undistributed Middle.

**Answer: (B)** — Definitely false (invalid syllogism).

---

## Question 3: Some + All

**Premises:**
1. Some students are engineers
2. All engineers are graduates

**Conclusion:** Some students are graduates.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
- Some students are engineers (there's overlap between Students and Engineers)
- All engineers are graduates (Engineers ⊂ Graduates)
- The students who are engineers MUST also be graduates

Therefore: Some students are graduates ✓

**Answer: (A)** — Definitely true.

---

## Question 4: Negative Premise

**Premises:**
1. No politicians are honest
2. Some teachers are politicians

**Conclusion:** Some teachers are not honest.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
- No politicians are honest (Politicians and Honest don't overlap)
- Some teachers are politicians (some Teachers are in Politicians)
- Those teachers who are politicians CANNOT be honest

Therefore: Some teachers are not honest ✓

**Answer: (A)** — Definitely true.

---

## Question 5: Two Negatives

**Premises:**
1. No A are B
2. No B are C

**Conclusion:** No A are C.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
Two negative premises → no valid conclusion can be drawn.

Example to show invalidity:
- A = cats, B = dogs, C = pets
- No cats are dogs ✓
- No dogs are cats ✓ (but wait, B=C here doesn't work)

Let me try:
- A = cats, B = dogs, C = animals
- No cats are dogs ✓
- No dogs are animals? NO (dogs ARE animals)

This premise setup is self-contradictory in many cases. The rule is: two negative premises yield NO valid conclusion.

**Answer: (C)** — Possibly true, possibly false (two negative premises = invalid).

---

## Question 6: "Only" Statement

**Premises:**
1. Only graduates can be engineers
2. Ram is an engineer

**Conclusion:** Ram is a graduate.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
"Only graduates can be engineers" = "All engineers are graduates"
Ram is an engineer → Ram must be a graduate.

**Answer: (A)** — Definitely true.

---

## Question 7: Particular Conclusion Invalid

**Premises:**
1. Some doctors are rich
2. Some rich people are happy

**Conclusion:** Some doctors are happy.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
Two particular premises ("Some...Some") cannot yield a valid conclusion.

Example:
- Doctors = {A, B}, Rich = {B, C}, Happy = {C, D}
- Some doctors are rich: A=Doctor, B=Rich ✓
- Some rich are happy: B=Rich, C=Happy ✓
- But no doctor is happy (A, B not in {C, D})

**Answer: (C)** — Possibly true, possibly false.

---

## Question 8: Chain with Negative

**Premises:**
1. All cats are animals
2. No animals are plants

**Conclusion:** No cats are plants.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
- All cats are animals (Cats ⊂ Animals)
- No animals are plants (Animals ∩ Plants = ∅)
- Cats, being inside Animals, cannot overlap with Plants

Therefore: No cats are plants ✓

**Answer: (A)** — Definitely true.

---

## Question 9: Illicit Major

**Premises:**
1. All birds are animals
2. No cats are birds

**Conclusion:** No cats are animals.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
- All birds are animals
- No cats are birds
- Cats are NOT in Birds, but cats COULD still be in Animals (outside Birds)

"Animals" is distributed in the conclusion (No cats are animals → ALL animals are considered) but not distributed in Premise 1 (All birds are animals → we only know about birds, not all animals).

**Answer: (C)** — Possibly true, possibly false.

---

## Question 10: Universal from Particular

**Premises:**
1. Some students are smart
2. All smart people work hard

**Conclusion:** All students work hard.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
- "Some students are smart" → not ALL students are smart
- Only the smart students must work hard
- Non-smart students may or may not work hard

Can't conclude "All students work hard" from "Some students are smart."

**Answer: (C)** — Possibly true, possibly false.

---

## Question 11: Double Negative

**Premises:**
1. No peace is war
2. All war is destruction

**Conclusion:** No peace is destruction.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
- No peace is war (Peace ∩ War = ∅)
- All war is destruction (War ⊂ Destruction)
- Peace is outside War. War is inside Destruction.
- Peace COULD be inside Destruction (outside War) or outside Destruction

Not necessarily valid.

**Answer: (C)** — Possibly true, possibly false.

Actually, let me reconsider:
- Peace ∩ War = ∅
- War ⊂ Destruction
- Peace is disjoint from War, but War is a subset of Destruction
- Peace could overlap with Destruction (the part of Destruction that's not War)

So conclusion is NOT necessarily true.

**Answer: (C)** — Possibly true, possibly false.

---

## Question 12: Symmetric Relation

**Premises:**
1. Some A are B

**Conclusion:** Some B are A.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
"Some A are B" is logically equivalent to "Some B are A."
The relationship is symmetric for particular affirmative propositions.

**Answer: (A)** — Definitely true.

---

## Question 13: Complex Syllogism

**Premises:**
1. All parks are beautiful
2. Some beautiful places are crowded
3. No crowded place is peaceful

**Conclusion:** Some parks are not peaceful.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
- All parks are beautiful (Parks ⊂ Beautiful)
- Some beautiful places are crowded (Beautiful ∩ Crowded ≠ ∅)
- No crowded place is peaceful (Crowded ∩ Peaceful = ∅)

The crowded beautiful places are NOT peaceful.
But are any parks among those crowded beautiful places? We don't know.
Parks are beautiful, and some beautiful places are crowded, but parks specifically might not be the crowded ones.

**Answer: (C)** — Possibly true, possibly false.

---

## Question 14: Valid Syllogism Check

**Premises:**
1. All metals are conductors
2. All copper is a metal

**Conclusion:** All copper is a conductor.

(A) Definitely true
(B) Definitely false
(C) Possibly true, possibly false
(D) Neither true nor false

**Solution:**
Chain rule:
- All copper is a metal (Copper ⊂ Metals)
- All metals are conductors (Metals ⊂ Conductors)
- Therefore: Copper ⊂ Conductors ✓

**Answer: (A)** — Definitely true.

---

## Question 15: Contradictory Propositions

If "All students are intelligent" is TRUE, then which must be FALSE?

(A) Some students are intelligent
(B) Some students are not intelligent
(C) No students are intelligent
(D) Some intelligent people are students

**Solution:**
- "All A are B" (A proposition) and "Some A are not B" (O proposition) are contradictory
- One MUST be true and the other MUST be false
- If "All students are intelligent" is TRUE, then "Some students are not intelligent" is FALSE

**Answer: (B)** — "Some students are not intelligent" must be FALSE.

---

## Self-Assessment

| Metric | Target |
|--------|--------|
| Questions attempted | 15/15 |
| Correct answers | 12+/15 (80%+) |
| Average time per question | < 1.5 minutes |
| Questions needing review | Note them below |

**Questions I need to review**: _______________

**Key takeaways**:
1. Chain rule (All A→B, All B→C → All A→C) is the most common valid pattern
2. Two particular premises = no valid conclusion
3. Two negative premises = no valid conclusion
4. "Only A are B" = "All B are A"
5. Use Venn diagrams for complex cases involving "Some"
6. Contradictory pairs: A↔O, E↔I (one true, one false, always)
