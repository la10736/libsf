#ifndef libTest_H
#define libTest_H

typedef struct ang_pt ang_pt;
typedef struct Graph Graph;

Graph *new_graph(int n_nodes);
void destroy_graph(Graph *G);
void graph_set_node(Graph *G, int node, double val);
void add_new_edge_graph(Graph *G, int from, int to);
ang_pt *newDeltaStarReductionAlgorithm(Graph *G);


#endif
