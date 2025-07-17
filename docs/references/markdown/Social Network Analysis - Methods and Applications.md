## SOCIAL NETWORK ANALYSIS : METHODS AND APPLICATIONS

STANLEY WASSERMAN University of Illinois KATHERINE FAUST University of South  Carolina

CAMBRIDGE

[Image]

## Contents

| List  of  Tables  List  of  illustrations                          | page  xxi  xxiv   |
|--------------------------------------------------------------------|-------------------|
| Part I:  Networks,  Relations,  and  Structure                     | 1                 |
| 1  Social Network Analysis in  the Social and Behavioral  Sciences | 3                 |
| 1.1  The Social Networks Perspective                               |                   |
| 1.2  Historical and Theoretical Foundations                        | 10                |
| 1.2.1  Empirical Motivations                                       | 11                |
| 1.2,2  Theoretical Motivations                                     | 13                |
| 1.2.3  Mathematical Motivations                                    | 15                |
| 1.2.4  In Summary                                                  | 16                |
| 1.3 Fundamental Concepts in Network Analysis                       | 17                |
| 1.4  Distinctive Features                                          | 21                |
| 1.5  Organization of the Book  and How to Read It                  | 22                |
| 1.5.1  Complexity                                                  | 23                |
| 1.5.2 Descriptive and Statistical Methods                          | 23                |
| 1.5.3 Theory Driven Methods                                        | 24                |
| 1.5.4 Chronology                                                   | 24                |
| 1.5.5  Levels of Analysis                                          | 25                |
| 1  S.6  Chapter Prerequisites                                      | 26                |
| 1.6  Summary                                                       | 27                |
| 2  Social Network Data                                             | 28                |
| 2.1  Introduction: What Are Network  Data?                         | 28                |

X

Contents

| 2.1.2  Modes                                                  | 29    |
|---------------------------------------------------------------|-------|
| 2.1.3  Affiliation Variables                                  | 30    |
| 2.2  Boundary Specification and Sampling                      | 30    |
| 2.2.1  What Is Your Population?                               | 31    |
| 2.2.2  Sampling                                               | 33    |
| 2.3  Types of Networks                                        | 35    |
| 2.3.1  One-Mode Networks                                      | 36    |
| 2.3.2  Two-Mode Networks                                      | 39    |
| 2.3.3  Ego-centered and Special Dyadic Networks               | 41    |
| 2.4  Network Data, Measurement and Collection                 | 43    |
| 2.4.1  Measurement                                            | 43    |
| 2.4.2  Collection                                             | 45    |
| 2.4.3  Longitudinal Data Collection                           | 55    |
| 2.4.4  Measurement Validity, Reliability, Accuracy, Error     | 56    |
| 2.5  Data Sets Found in These Pages                           | 59    |
| 2.5.1  Krackhardt's  High-tech Managers                       | 60    |
| 2.5.2  Padgett's Florentine Families                          | 61    |
| 2.5.3  Freeman's EIES  Network                                | 62    |
| 2.5.4  Countries Trade Data                                   | 64    |
| 2.5.5  Galaskiewicz's CEOs and Clubs Network                  | 65    |
| 2.5.6  Other Data                                             | 66    |
| Part  1 1 :   Mathematical Representations of Social Networks | 67    |
| 3  Notation for  Social Network  Data                         | 69    |
| 3.1  Graph Theoretic Notation                                 | 71    |
| 3.1.1  A Single Relation                                      | 71    |
| 3.1.2  OMultiple Relations                                    | 73    |
| 3.1.3  Summary                                                | 75    |
| 3.2  Sociometric Notation                                     | 77    |
| 3.2.1  Single Relation                                        | 79    |
| 3.2.2  Multiple Relations                                     | 81    |
| 3.2.3  Summary                                                | 83    |
| 3.3  OAlgebraic Notation                                      | 84    |
| 3.4  OTwo Sets of Actors                                      | 85    |
| 3.4.1  @Different Types of Pairs                              | 86    |
| 3.4.2  OSociometric Notation                                  |       |
| 3.5  Putting It All Together                                  | 87 89 |

|                        | Contents                                          |   Xi |
|------------------------|---------------------------------------------------|------|
| 4  Graphs and Matrices | 4  Graphs and Matrices                            |   92 |
| 4.1                    | Why Graphs?                                       |   93 |
| 4.2                    | Graphs                                            |   94 |
|                        | 4.2.1  Subgraphs, Dyads, and Triads               |   97 |
|                        | 4.2.2  Nodal Degree                               |  100 |
|                        | 4.2.3  Density of  Graphs and Subgraphs           |  101 |
|                        | 4.2.4  Example: Padgett's Florentine Families     |  103 |
|                        | 4.2.5  Walks, Trails, and Paths                   |  105 |
|                        | 4.2.6  Connected Graphs and Components            |  109 |
|                        | 4.2.7  Geodesics, Distance, and Diameter          |  110 |
|                        | 4.2.8  Connectivity of  Graphs                    |  112 |
|                        | 4.2.9  Isomorphic Graphs and Subgraphs            |  117 |
|                        | 4.2.10  OSpecial Kinds of  Graphs                 |  119 |
| 4.3                    | Directed Graphs                                   |  121 |
|                        | 4.3.1  Subgraphs  -  Dyads                        |  124 |
|                        | 4.3.2  Nodal Indegree and Outdegree               |  125 |
|                        | 4.3.3  Density of  a Directed Graph               |  129 |
|                        | 4.3.4  An  Example                                |  129 |
|                        | 4.3.5  Directed Walks, Paths, Semipaths           |  129 |
|                        | 4.3.6  Reachability and Connectivity in  Digraphs |  132 |
|                        | 4.3.7  Geodesics, Distance and Diameter           |  134 |
|                        | 4.3.8  OSpecial Kinds of  Directed Graphs         |  134 |
|                        | 4.3.9  Summary                                    |  136 |
| 4.4                    | Signed Graphs and Signed Directed Graphs          |  136 |
|                        | 4.4.1  Signed Graph                               |  137 |
|                        | 4.4.2  Signed Directed Graphs                     |  138 |
| 4.5                    | Valued Graphs and Valued Directed Graphs          |  140 |
|                        | 4.5.1  Nodes and Dyads                            |  142 |
|                        | 4.5.2  Density in a Valued  Graph                 |  143 |
| 4.6                    | 4.5.3  OPaths in Valued Graphs                    |  143 |
|                        | Multigraphs                                       |  145 |
| 4.7                    | BHypergraphs                                      |  146 |
| 4.8                    | Relations                                         |  148 |
|                        | 4.8.1  Definition                                 |  148 |
|                        | 4.8.2  Properties of Relations                    |  149 |
| 4.9                    | Matrices                                          |  150 |
|                        | 4.9.1  Matrices for Graphs                        |  150 |
|                        | 4.9.2  Matrices for Digraphs                      |  152 |
|                        | 4.9.3  Matrices for Valued Graphs                 |  153 |
|                        | 4.9.4  Matrices for Two-Mode Networks             |  154 |

| 4.9.5  OMatrices for Hypergraphs                       |   154 |
|--------------------------------------------------------|-------|
| 4.9.6  Basic Matrix Operations                         |   154 |
| 4.9.7  Computing Simple Network Properties             |   159 |
| 4.9.8  Summary                                         |   164 |
| 4.10  Properties                                       |   164 |
| 4.10.1  Reflexivity                                    |   164 |
| 4.10.2  Symmetry                                       |   165 |
| 4.10.3  Transitivity                                   |   165 |
| 4.1  1  Summary                                        |   165 |
| Part  1 1 1 :   Structural and  Locational  Properties |   167 |
| 5  Centrality and  Prestige                            |   169 |
| 5.1  Prominence: Centrality and Prestige               |   172 |
| 5.1.1  Actor Centrality                                |   173 |
| 5.1.2  Actor Prestige                                  |   174 |
| 5.1.3  Group Centralization  and Group Prestige        |   175 |
| 5.2  Nondirectional Relations                          |   177 |
| 5.2.1  Degree Centrality                               |   178 |
| 5.2.2  Closeness Centrality                            |   183 |
| 5.2.3  Betweenness Centrality                          |   188 |
| 5.2.4  @Information  Centrality                        |   192 |
| 5.3  Directional Relations                             |   198 |
| 5.3.1  Centrality                                      |   199 |
| 5.3.2  Prestige                                        |   202 |
| 5.3.3 A Different  Example                             |   210 |
| 5.4  Comparisons and Extensions                        |   215 |
| 6  Structural Balance and Transitivity                 |   220 |
| 6.1  Structural Balance                                |   222 |
| 6.1.1  Signed Nondirectional  Relations                |   223 |
| 6.1.2  Signed Directional Relations                    |   228 |
| 6.1.3  OChecking for Balance                           |   230 |
| 6.1.4  An Index for Balance                            |   232 |
| 6.1.5  Summary                                         |   232 |
| 6.2  Clusterability                                    |   233 |
| 6.2.1  The Clustering Theorems                         |   235 |
| 6.2.2  Summary                                         |   238 |
| 6.3  Generalizations of Clusterability                 |   239 |

| Contents                                       | xiii   |
|------------------------------------------------|--------|
| 6.3.1  Empirical Evidence                      | 239    |
| 6.3.2  ORanked Clusterability                  | 240    |
| 6.3.3  Summary                                 | 242    |
| 6.4  Transitivity                              | 243    |
| 6.5  Conclusion                                | 247    |
|                                                | 249    |
| 7  Cohesive Subgroups  7.1  Background         | 250    |
| 7.1.1  Social Group and Subgroup               | 250    |
| 7.1.2  Notation                                | 252    |
| 7.2  Subgroups Based  on Complete Mutuality    | 253    |
| 7.2.1  Definition of a  Clique                 | 254    |
| 7.2.2  An Example                              | 254    |
| 7.2.3  Considerations                          | 256    |
| 7.3  Reachability and Diameter                 | 257    |
| 7.3.1  n-cliques                               | 258    |
| 7.3.2  An Example                              | 259    |
| 7.3.3  Considerations                          | 260    |
| 7.3.4  n-clans and n-clubs                     | 260    |
| 7.3.5  Summary                                 | 262    |
| 7.4  Subgroups Based on Nodal Degree           | 263    |
| 7.4.1  k-plexes                                | 265    |
| 7.4.2  k-cores                                 | 266    |
| 7.5  Comparing Within to Outside Subgroup Ties | 267    |
| 7.5.1  LS Sets                                 | 268    |
| 7.5.2  Lambda  Sets                            |        |
| 7.6  Measures of  Subgroup Cohesion            | 270    |
| 7.7  Directional  Relations                    | 273    |
| 7.7.1  Cliques Based on Reciprocated Ties      | 273    |
| 7.7.2  Connectivity in  Directional Relations  | 274    |
| 7.7.3  n-cliques in  Directional  Relations    | 275    |
| 7.8  Valued Relations                          | 277    |
| 7.8.1  Cliques, n-cliques, and k-plexes        | 278    |
| 7.8.2  Other Approaches for Valued Relations   | 282    |
| 7.9  Interpretation of Cohesive Subgroups      | 283    |
| 7.10  Other Approaches                         | 284    |
| 7.10.1  Matrix Permutation Approaches          | 284    |
| 7.10.2  Multidimensional Scaling               | 287    |
| 7.10.3  OFactor Analysis  7.11  Summary        | 290    |
|                                                | 290    |

xiv

Contents

| 8  Affiliations and  Overlapping Subgroups            |   291 |
|-------------------------------------------------------|-------|
| 8.1  Affiliation Networks                             |   291 |
| 8.2  Background                                       |   292 |
| 8.2.1  Theory                                         |   292 |
| 8.2.2  Concepts                                       |   294 |
| 8.2.3  Applications and Rationale                     |   295 |
| 8.3  Representing Affiliation Networks                |   298 |
| 8.3.1  The Affiliation Network  Matrix                |   298 |
| 8.3.2  Bipartite Graph                                |   299 |
| 8.3.3  Hypergraph                                     |   303 |
| 8.3.4  OSimplices and  Simplicial Complexes           |   306 |
| 8.3.5  Summary                                        |   306 |
| 8.3.6  An example: Galaskiewicz's CEOs and Clubs      |   307 |
| 8.4  One-mode Networks                                |   307 |
| 8.4.1  Definition                                     |   307 |
| 8.4.2  Examples                                       |   309 |
| 8.5  Properties of Affiliation Networks               |   312 |
| 8.5.1  Properties of Actors and Events                |   312 |
| 8.5.2  Properties of One-mode Networks                |   314 |
| 8.5.3  Taking Account of Subgroup Size                |   322 |
| 8.5.4  Interpretation                                 |   324 |
| 8.6  @Analysis of Actors and Events                   |   326 |
| 8.6.1  @Galois  Lattices                              |   326 |
| 8.6.2  @Correspondence  Analysis                      |   334 |
| 8.7  Summary                                          |   342 |
| Part  IV: Roles and  Positions                        |   345 |
| 9  Structural Equivalence                             |   347 |
| 9.1  Background                                       |   348 |
| 9.1.1  Social Roles and Positions                     |   348 |
| 9.1.2  An Overview of Positional and Role Analysis    |   351 |
| 9.1.3  A Brief History                                |   354 |
| 9.2  Definition of Structural Equivalence             |   356 |
| 9.2.1  Definition                                     |   356 |
| 9.2.2  An Example                                     |   357 |
| 9.2.3  Some Issues in Defining Structural Equivalence |   359 |
| 9.3  Positional Analysis                              |   361 |
| 9.3.1  Simplification of Multirelational Networks     |   361 |

Contents

XV

| 9.3.2  Tasks in a Positional Analysis                                                                                                               | 9.3.2  Tasks in a Positional Analysis                                                                                                               |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| 9.4  Measuring Structural Equivalence                                                                                                               | 9.4  Measuring Structural Equivalence                                                                                                               |
| 9.4.1  Euclidean  Distance  as  a  Measure  of  Structural                                                                                          | 9.4.1  Euclidean  Distance  as  a  Measure  of  Structural                                                                                          |
|                                                                                                                                                     | Equivalence  9.4.2  Correlation as a Measure of Structural Equivalence                                                                              |
|                                                                                                                                                     | 9.4.3  Some  Considerations  in  Measuring  Structural  Equivalence                                                                                 |
| 9.5  Representation  of Network  Positions                                                                                                          | 9.5  Representation  of Network  Positions                                                                                                          |
| 9.5.1  Partitioning  Actors                                                                                                                         | 9.5.1  Partitioning  Actors                                                                                                                         |
|                                                                                                                                                     | 9.5.2  Spatial Representations  of Actor Equivalences                                                                                               |
|                                                                                                                                                     | 9.5.3 Ties Between and Within Positions                                                                                                             |
|                                                                                                                                                     | 9.6  Summary                                                                                                                                        |
|                                                                                                                                                     |                                                                                                                                                     |
| 10  Blockmodels  10.1 Definition                                                                                                                    | 10  Blockmodels  10.1 Definition                                                                                                                    |
|                                                                                                                                                     |                                                                                                                                                     |
| 10.2 Building Blocks  10.2.1 Perfect Fit (Fat Fit)                                                                                                  | 10.2 Building Blocks  10.2.1 Perfect Fit (Fat Fit)                                                                                                  |
| 10.2.2  Zeroblock (Lean Fit) Criterion                                                                                                              | 10.2.2  Zeroblock (Lean Fit) Criterion                                                                                                              |
| 10.2.3  Oneblock Criterion                                                                                                                          | 10.2.3  Oneblock Criterion                                                                                                                          |
| 10.2.4 a Density Criterion                                                                                                                          | 10.2.4 a Density Criterion                                                                                                                          |
| 10.2.5  Comparison of Criteria                                                                                                                      | 10.2.5  Comparison of Criteria                                                                                                                      |
| 10.2.6  Examples                                                                                                                                    | 10.2.6  Examples                                                                                                                                    |
| 10.2.7  Valued Relations                                                                                                                            | 10.2.7  Valued Relations                                                                                                                            |
| 10.3  Interpretation                                                                                                                                | 10.3  Interpretation                                                                                                                                |
| 10.3.1 Actor Attributes                                                                                                                             | 10.3.1 Actor Attributes                                                                                                                             |
| 10.3.2  Describing Individual Positions                                                                                                             | 10.3.2  Describing Individual Positions                                                                                                             |
| 10.3.3  Image Matrices                                                                                                                              | 10.3.3  Image Matrices                                                                                                                              |
|                                                                                                                                                     |                                                                                                                                                     |
| 10.4 Summary                                                                                                                                        | 10.4 Summary                                                                                                                                        |
| 11  Relational  Algebras                                                                                                                            | 11  Relational  Algebras                                                                                                                            |
| 11.1  Background                                                                                                                                    | 11.1  Background                                                                                                                                    |
| 11.2  Notation and Algebraic Operations  1  1.2.1 Composition and Compound Relations  11.2.2  Properties  of  Composition  and  Compound  Relations | 11.2  Notation and Algebraic Operations  1  1.2.1 Composition and Compound Relations  11.2.2  Properties  of  Composition  and  Compound  Relations |
|                                                                                                                                                     |                                                                                                                                                     |
| 11.3  Multiplication  Tables for Relations                                                                                                          | 11.3  Multiplication  Tables for Relations                                                                                                          |
| 11.3.1 Multiplication Tables and Relational  Structures                                                                                             | 1  1.3.2 An Example                                                                                                                                 |
|                                                                                                                                                     |                                                                                                                                                     |
| 11.4  Simplification of  Role Tables                                                                                                                | 11.4  Simplification of  Role Tables                                                                                                                |
| 1  1.4.1  Simplification by  Comparing Images                                                                                                       | 1  1.4.1  Simplification by  Comparing Images                                                                                                       |

xvi

Contents

| 11.4.2  @Homomorphic Reduction                             |   445 |
|------------------------------------------------------------|-------|
| 11.5  @Comparing Role Structures                           |   449 |
| 11.5.1 Joint  Homomorphic Reduction                        |   451 |
| 11.5.2 The Common Structure Semigroup                      |   452 |
| 11.5.3 An Example                                          |   453 |
| 11.5.4  Measuring the Similarity of Role Structures        |   457 |
| 11.6  Summary                                              |   460 |
| 12  Network  Positions and  Roles                          |   461 |
| 12.1  Background                                           |   462 |
| 12.1.1  Theoretical Definitions  of Roles and Positions    |   462 |
| 12.1.2 Levels of Role Analysis in Social Networks          |   464 |
| 12.1.3  Equivalences in Networks                           |   466 |
| 12.2  Structural Equivalence, Revisited                    |   468 |
| 12.3  Automorphic and Isomorphic Equivalence               |   469 |
| 12.3.1  Definition                                         |   470 |
| 12.3.2  Example                                            |   471 |
| 12.3.3 Measuring Automorphic Equivalence                   |   472 |
| 12.4  Regular Equivalence                                  |   473 |
| 12.4.1 Definition  of  Regular  Equivalence                |   474 |
| 12.4.2  Regular  Equivalence for Nondirectional  Relations |   475 |
| 12.4.3 Regular Equivalence Blockmodels                     |   476 |
| 12.4.4  O A   Measure of Regular  Equivalence              |   479 |
| 12.4.5 An Example                                          |   481 |
| 12.5  "Types"  of Ties                                     |   483 |
| 12.5.1 An Example                                          |   485 |
| 12.6  Local Role Equivalence                               |   487 |
| 12.6.1  Measuring Local Role Dissimilarity                 |   488 |
| 12.6.2  Examples                                           |   491 |
| 12.7  @Ego Algebras                                        |   494 |
| 12.7.1  Definition  of  Ego Algebras                       |   496 |
| 12.7.2  Equivalence of Ego Algebras                        |   497 |
| 12.7.3  Measuring Ego Algebra Similarity                   |   497 |
| 12.7.4  Examples                                           |   499 |
| 12.8  Discussion                                           |   502 |

| Contents                                                                                                    | xvii    |
|-------------------------------------------------------------------------------------------------------------|---------|
| Part V:  Dyadic and  Triadic  Methods                                                                       | 503     |
|                                                                                                             | 505     |
| 13  Dyads  13.1 An Overview                                                                                 | 506     |
| 13.2 An Example and Some Definitions                                                                        | 508     |
| 13.3  Dyads                                                                                                 | 510     |
| 13.3.1  The Dyad Census                                                                                     | 512     |
| 13.3.2  The Example and Its Dyad Census                                                                     | 513     |
| 13.3.3 An Index for Mutuality                                                                               | 514     |
| 13.3.4 @A  Second Index for Mutuality                                                                       | 518     |
| 13.3.5  OSubgraph Analysis, in  General                                                                     | 520     |
| 13.4 Simple Distributions                                                                                   | 522     |
| 13.4.1  The Uniform Distribution  -  A Review                                                               | 524     |
| 13.4.2  Simple Distributions on Digraphs                                                                    | 526     |
| 13.5  Statistical Analysis of  the Number of Arcs                                                           | 528     |
| 13.5.1  Testing                                                                                             | 529     |
| 13.5.2 Estimation                                                                                           | 533     |
|                                                                                                             | 535     |
| 13.6 @Conditional  Uniform Distributions  13.6.1 Uniform Distribution, Conditional  on the Number           | 536     |
| of Arcs  13.6.2 Uniform Distribution, Conditional  on the                                                   | 537     |
| Outdegrees  13.7  Statistical Analysis of the Number of Mutuals                                             | 539     |
| 13.7.1  Estimation                                                                                          | 540     |
| 13.7.2 Testing                                                                                              | 542     |
| 13.7.3  Examples                                                                                            | 543     |
| 13.8  @Other  Conditional Uniform Distributions  13.8.1  Uniform Distribution, Conditional on the Indegrees | 544 545 |
|                                                                                                             | 547     |
| 13.8.2  The  UlMAN  Distribution                                                                            |         |
| 13.9  Other Research                                                                                        | 552     |
| 13.10  Conclusion                                                                                           | 555     |
| 14  Triads                                                                                                  | 556     |
| 14.1  Random Models and Substantive Hypotheses                                                              | 558     |
| 14.2.1  The Triad Census                                                                                    | 564     |
| 14.2.2  The Example and Its Triad Census                                                                    | 574     |
|                                                                                                             | 575     |
| 14.3 Distribution of a Triad Census                                                                         |         |

xviii

Contents

| 14.3.2  Mean and Variance of a Triad Census                           | 579   |
|-----------------------------------------------------------------------|-------|
| 14.3.3  Return to the Example                                         | 581   |
| 14.3.4  Mean and Variance of Linear  Combinations of  a  Triad Census | 582   |
| 14.3.5  A Brief Review                                                | 584   |
| 14.4  Testing Structural Hypotheses                                   | 585   |
| 14.4.1  Configurations                                                | 585   |
| 14.4.2  From Configurations to Weighting Vectors                      | 590   |
| 14.4.3  From Weighting Vectors to Test Statistics                     | 592   |
| 14.4.4  An  Example                                                   | 595   |
| 14.4.5  Another  Example  -  Testing for Transitivity                 | 596   |
| 14.5  Generalizations and Conclusions                                 | 598   |
| 14.6  Summary                                                         | 601   |
| Part VI: Statistical Dyadic Interaction Models                        | 603   |
| 15  Statistical Analysis of  Single Relational  Networks              | 605   |
| 15.1  Single Directional Relations                                    | 607   |
| 15.1.1  The Y-array                                                   | 608   |
| 15.1.2  Modeling the Y-array                                          | 612   |
| 15.1.3  Parameters                                                    | 619   |
| 15.1.4  @Is  p1  a  Random Directed Graph Distribution?               | 633   |
| 15.2  Attribute Variables                                             | 635   |
| 15.2.1  Introduction                                                  | 636   |
| 15.2.2  The W-array                                                   | 637   |
| 15.2.3  The Basic Model with Attribute Variables                      | 640   |
| 15.2.4  Examples: Using Attribute Variables                           | 646   |
| 15.3  Related Models for Further Aggregated Data                      | 649   |
| 15.3.1  Strict Relational Analysis  -  The V-array                    | 651   |
| 15.3.2  Ordinal Relational Data                                       | 654   |
| 15.4  ONondirectional  Relations                                      | 656   |
| 15.4.1  A Model                                                       | 656   |
| 15.4.2  An  Example                                                   | 657   |
| 15.5  @Recent  Generalizations of  p1                                 | 658   |
| 15.6                                                                  |       |
| @Single Relations and Two Sets of Actors                              | 662   |
| 15.6.1  Introduction                                                  | 662   |
| 15.6.2  The Basic Model                                               | 663   |

|                                                         | Contents                                                         |   xix |
|---------------------------------------------------------|------------------------------------------------------------------|-------|
|                                                         | 15.7  Computing for Log-linear Models                            |   665 |
|                                                         | 15.7.1 Computing Packages                                        |   666 |
|                                                         | 15.7.2  From Printouts to Parameters                             |   671 |
|                                                         | 15.8  Summary                                                    |   673 |
| 16  Stochastic Blockmodels and Goodness-of-Fit  Indices |                                                                  |   675 |
|                                                         | 16.1  Evaluating Blockmodels                                     |   678 |
|                                                         | 16.1.1  Goodness-of-Fit Statistics for Blockmodels               |   679 |
|                                                         | 16.1.2  Structurally  Based  Blockmodels and  Permutation  Tests |   688 |
|                                                         | 16.1.3 An Example                                                |   689 |
|                                                         | 16.2  Stochastic Blockmodels                                     |   692 |
|                                                         | 16.2.1  Definition of  a Stochastic Blockmodel                   |   694 |
|                                                         | 16.2.2  Definition of  Stochastic Equivalence                    |   696 |
|                                                         | 16.2.3  Application to Special Probability Functions             |   697 |
|                                                         | 16.2.4  Goodness-of-Fit Indices for Stochastic Blockmodels       |   703 |
|                                                         | 16.2.5  OStochastic a posteriori Blockmodels                     |   706 |
|                                                         | 16.2.6  Measures of Stochastic Equivalence                       |   708 |
|                                                         | 16.2.7  Stochastic Blockmodel Representations                    |   709 |
|                                                         | 16.2.8  The Example Continued                                    |   712 |
|                                                         | 16.3  Summary: Generalizations and Extensions                    |   719 |
|                                                         | 16.3.1  Statistical Analysis of Multiple Relational Networks     |   719 |
|                                                         | 16.3.2  Statistical Analysis of Longitudinal Relations           |   721 |
| Part VII:  Epilogue                                     | Part VII:  Epilogue                                              |   725 |
| L 7   Future Directions                                 |                                                                  |   727 |
|                                                         | 17.1  Statistical Models                                         |   727 |
|                                                         | 17.2  Generalizing to New Kinds of Data                          |   729 |
|                                                         | 17.2.1  Multiple Relations                                       |   730 |
|                                                         | 17.2.2 Dynamic and  Longitudinal Network Models                  |   730 |
|                                                         | 17.2.3  Ego-centered Networks                                    |   731 |
|                                                         | 17.3  Data Collection                                            |   731 |
|                                                         | 17.4  Sampling                                                   |   732 |
|                                                         | 17.5  General Propositions about Structure                       |   732 |
|                                                         | 17.6  Computer Technology                                        |   733 |
|                                                         | 17.7  Networks and Standard Social and Behavioral Science        |   733 |

| xx                | Contents                      |     |
|-------------------|-------------------------------|-----|
|                   | Appendix A  Computer Programs | 735 |
| Appendix  B       | Data                          | 738 |
| References        | References                    | 756 |
| Name  Index       | Name  Index                   | 802 |
| Subject  Index    | Subject  Index                | 811 |
| List  of Notation | List  of Notation             | 819 |