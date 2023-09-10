# Maze Game with Pygame

![Gameplay Screenshot](screenshot.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Game Controls](#game-controls)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Welcome to the 'Ghost in the Maze' project. This project serves a dual purpose:
1. To provide a hands-on experience in implementing and using search algorithms to solve complex problems, and,
2. to illustrate the distinction between planning and execution in uncertain environments.

This is achieved in an environment resembling a maze, with different agents designed to navigate through it, and collect data to analyze the agent's performance as it strives to reach its goal.

## 1. Implementation

### 1.1 The Environment

The environment consists of a maze-like square grid, with some cells open (unblocked) and others obstructed (blocked). The agent can move through unblocked cells but cannot traverse blocked ones. To create varied test environments, mazes are generated randomly, with a 51x51 grid.

The challenge lies in ensuring these mazes are navigable. DFS algorithm is used to verify the existence of paths from the upper left to the lower right corners before finalizing the randomly created maze as a valid environment.

### 1.2 The Agent
The agent starts in the upper left corner and aims to reach the lower right corner. It can move in the cardinal directions (up, down, left, right) but only through unblocked squares. At any moment, the agent has complete knowledge of the entire maze, and hence can plan its path using it's strategy and updated maze information.

### 1.3 The Problem: Ghosts
The maze is inhabited by multiple randomly spawned ghosts in the maze which can travel in cardinal directions and can tranverse through all the cells in the maze environment. The agent dies if a ghost encounters it. Ghosts move each time the agent does, which necessitates dynamic path planning by the agent to avoid collisions. Ghost picks any one of its adjacent cells, with probability of each cell of 25%. If the selected cell block is blocked, then there is a 50% probability that the agent will move towards it.

### 1.4 The Strategies
Agent type and strategies implemented:

First Header | Second Header 
 ------------ | ------------- 
Content from cell 1 | Content from cell 2 
Content in the first column | content in the second column 

Agent Nr | Strategy Followed
 ------------ | ------------- 
Agent 1 | *Plan Once and Execute Blindly* : Possesses full knowledge of the blocked and unblocked cells in the maze and plans its entire path from source to destination at timestamp 0, completely disregarding the position of ghosts and their movements. This method results in a single, optimal plan executed without alterations and contigency plans in case ghost in encountered in between.
Agent 2 | *Plan at Every step* The Agent plans its path at the 0th timestamp and then continually evaluates the ghost's position at each timestamp. Thus the Agent adapts its course dynamically, ensuring it avoids encountering ghosts if the ghost appears in its path to the goal.
Agent 3 | *Forecasting on Agent 2’s knowledge* Relies on Agent 2's history data. When Agent 3 encounters a cell, it checks if Agent 2 has visited it before. If not, Agent 3 uses A* and mimics Agent 2's behavior. If the cell is unexplored, Agent 3 evaluates valid directions, selecting the one with maximum survivability. Explored cells prompt Agent 3 to mimic Agent 2 or stay put if no valid moves exist.
Agent 4 | *Plan only when needed* Equipped with a dynamic strategy that adapts to the presence of ghosts based on the parameters _visibility_ and _strike_. _Visibility parameter_ defines how far the ghost can see. Until the agent encounters a ghost within this visibility range, it remains steadfast on its current path, optimizing efficiency. _Strike parameter_ is set to 1 when a ghost enters the visibility range of the agent. This acts as an early warning, alerting Agent that a ghost is lurking nearby. If in the next turn too the ghost remains in the visibility range, the Agent immediately changes its path to avoid potential danger.
Agent 5 | *Plan with impaired sight* Agent 5 brings a unique twist. It operates under the constraint of losing sight of ghosts when they enter blocked cells. This agent primarily follows Agent 4's strategy with the unique constraint.



## Features

- Randomly generated mazes for a new challenge each time you play.
- Multiple ghosts with unique movement patterns.
- Simple and intuitive controls.
- Engaging gameplay with the thrill of evading ghosts.

## Getting Started

### Prerequisites

- Python 3.x: Make sure you have Python 3.x installed. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kunjanvaghela/GhostsInTheMaze.git
   ```

2. Navigate to the project directory:
    ```
    cd Maze
    ```

3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

### Usage

To start the game, run the following command:
```
python3 MazeVisualizer.py
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
