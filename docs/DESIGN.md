# Design notes

## Evidence contract

Each synthetic event has a unique `id`, `task_id`, `kind`, `skill`, `action`, `outcome`, `signals` and `outcome_basis`. Actions are Accept, Reject or Edit; outcomes are improved, not_improved or unknown. Outcome is a separate assessment after collaboration, not the action itself. A rejected AI proposal can lead to a successful human correction.

The fixture contains 47 judgment events (39 improved, 8 not improved), spread across 10 synthetic tasks, plus one excluded preference. Signal frequencies are 12 Camera height, 12 Lens choice, 12 Subject separation and 11 Lighting. They are tags, not automatically extracted facts. Unique events are not necessarily statistically independent.

The ratio uses all eligible evidence, including unknown outcomes in the denominator. With no evidence the ratio is null, shown as N/A. This is a conservative display rule, not a statistical estimator of skill. No threshold auto-registers a skill.

## Confirmation and roles

The demo makes a candidate, then applies a command-line human decision. Register permits a proposed role split; Observe and Reject keep it inactive. This process does not persist state. A production system would need reversible registration, expiration, removal of evidence and reconsideration across contexts.

The toy BALANCING rules use capability gap to suggest verification support, task frequency or stress to suggest repetitive variants, failure cost to require review of costly changes, and preference to retain the user's stated approval role. No tools are installed, agents trained or work executed. Team Coverage is a desired objective with no measured numeric score here.

## Evaluation before stronger claims

Compare with preference-only adaptation and static role allocation. Use held-out tasks, independent outcome raters and context-specific criteria; check whether revisions improve outcomes beyond the AI baseline. Track false candidates, correction burden, calibration, skill drift and user-rated usefulness. More accepted edits alone cannot establish ability or causality.

Prefer explicit consent and local processing. Let users inspect, correct, export and delete evidence. Do not infer protected attributes or use this toy model for hiring or other consequential ranking. Stress inputs should be voluntary and contextual.

## Public boundary

This repository contains only the concept and an illustrative aggregation/rule pipeline. It does not contain the private ELFCORE runtime, advanced allocation logic, proprietary training data or an automatic raw-conversation discovery model. No integration with Slime-core is required or implemented.
