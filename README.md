# GenerationLearning

This is a pet project I've worked on from Summer 2020 to Fall 2020 that tests evolution based learning on various systems. Each project uses a simlar framework but are run independently of eachother. Currently the following two projects have been finished:

foodsurvivor - Starting at the middle of a 2 dimensional grid, neural networks are given their location and the location of food and need to learn to collect the food as efficiently as possible to survive as long as possible. Fitness is defined by how much food each survivor has eaten plus the manhattan distance from the end location to the food location normalized. Each cycle, the worst 50% of the poulation are killed and the rest are led to asexually reproduce a child. This is where mutations are introduced as well as duplication of good genes.
