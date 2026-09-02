# TDD Policy

## Meaningful RED

A RED result must demonstrate missing approved behavior or reproduce a confirmed defect. Syntax, import, fixture, configuration, and unrelated baseline failures do not count.

## Small cycles

Plan the complete issue, but execute one small behavior at a time:

1. test;
2. meaningful failure;
3. minimal clear implementation;
4. passing target and related tests;
5. refactor with tests green.

## User stories

Map acceptance criteria to observable tests. Use the lowest test level that proves the behavior correctly, then add broader integration coverage only when component collaboration matters.

## Bugs

Create a regression test that fails before the fix. When the defect cannot be reproduced, stop and report the missing evidence.

## Refactors

Start from a green baseline. Add characterization tests only when needed to preserve observable behavior. Do not invent a functional failure merely to label the work TDD.

## Documentation and configuration

Use executable examples, parsers, linters, link checks, or configuration validation when relevant. Do not force a fake product test.

## Prohibited shortcuts

Do not:

- weaken assertions;
- delete valid tests;
- add skip or xfail to hide failure;
- mock the behavior being proven;
- replace a real cheap integration with an unnecessary mock;
- implement additional behavior because it is convenient.
