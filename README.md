# poors_man_pce
Working on a small prototype for PCE Code for learning purposes.Right now it uses BGP-LS as an input and parses the topology.Then it allows to compute shortest path based on following constraints:

1) No Constraint ( Simple Heap based Dijkstra)

2) Avoid or Include a certain Link as a Constraint.

3) Available BW as a Constraint.

4) Available BW + (Avoid or Include a certain Link as constraint).

5) Avoid a Node
