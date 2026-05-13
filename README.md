. 20260513: Run ARR_Phase1_b_parallel_TL_phase1_phase2.py

.. Stopping criterion 1: Phase 1 by TL (Time Limit) 

.. Stopping criterion 2: Phase 2 by grandTime (Line 588)


.Previous:
.. lines_md_2012.csv and nodes_md_2012.csv came from the shape file at [ https://github.com/MQLib/MQLib ]

.. lines_md_2012_add.csv added 27 edges to make the adjacency graph and its subgraphs induced by the existing districts of 2012 Maryland congressional district map connected

.. ARR_Phase1_b.py generates random plans (i.e., fictitious 2012 Maryland congressional district maps) ensuring 2 black majority districts (Line 126: num_majority_black = 2)

.. ARR_Phase1_b_parallel.py performs ARR_Phase1_b.py (serial code) in parallel manner
