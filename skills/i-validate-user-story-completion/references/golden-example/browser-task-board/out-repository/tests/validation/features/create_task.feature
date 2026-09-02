Feature: Create tasks

  Scenario: US-0001 - Create a task with a title
    Given the board is available
    When the user creates a task with a non-empty title
    Then the task is added to TODO with that title
