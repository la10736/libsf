/*
 * libsf.c
 *
 *  Created on: 03/mar/2014
 *      Author: michele
 */

#include <math.h>
#include <string.h>

#include "structs.h"

#define MAX_SIZE_TYPEVAL DBL_MAX

ang_pt *simpleTree2ang_pt(STNode_queue_struct *stqueue);
STNode *STNode_dequeue(STNode_queue_struct *stqueue);
STNode *delete_STNode(STNode *nd);
void ins_ang_pt(ang_pt **, ang_pt *);
ang_pt *new_ang_pt(double x, double y);
STNode_queue_struct *SEGraph2STtree(SEGraph *H);
STNode *new_STNode(double phi);
STNode_queue_struct *new_STNode_queue_struct();
void STNode_queue(STNode_queue_struct *stqueue, STNode *to_queue);
void delSENode(SEGraph *G, SENode *node);
void freeSEList(SEList *toFree);

SEGraph *deltaStarRed(Graph *G);

void fixGraph(Graph *G, Node **orderArray);
SEGraph* newSEGraph();
void initset(djset *el, SENode *lbl);
SENode* addSENode(SEGraph *G, double phi);
djset *find(djset *el);
void addDjsetStack(djsetStack **top, djset* el);
void link(djset *s, djset *t);
djset *popDjsetStack(djsetStack **top);
void moveAdjList(SENode *from, SENode *to);
SEList *addSEedge(SENode *from, SENode *to);
int compar(Node **V, Node **W);

void write_ang_pt(ang_pt *ang, char *angout);
void destroy_all_ang_pt(ang_pt **first_id);
void del_ang_pt(ang_pt **id);

// FUNCTIONS

/* Create a Graph with max n nodes
 * @param n the max numbers of nodes
 * @return the graph pointer
 */
Graph *new_graph(int n) {
	Graph *G = (Graph *) malloc(sizeof(Graph));
	int i;

	if (!(G->first = (Node *) malloc(n * sizeof(Node)))) {
		fprintf(stdout, " in new_graph : can not allocate memory\n");
		exit(1);
	}

	G->n_nodes = 0;
	G->max_nodes = n;
	return G;
}

void loc_add_new_edge_graph(Node *from, Node *to) {
	L_node *new_edge;

	if (!(new_edge = (L_node *) malloc(sizeof(L_node)))) {
		fprintf(stdout, " in add_new_edge_graph : can not allocate memory\n");
		exit(1);
	}
	new_edge->p_node = to;
	new_edge->next = from->l_adj;
	from->l_adj = new_edge;
}

/* Add new edge to the graph G from the node n to the node m
 * @param G the Graph
 * @param n the node where the edge starts
 * @param m the node where the edge ends
 * @return 0 in case of success, <0 otherwise
 */
int add_new_edge_graph(Graph *G, int n, int m) {
	if (n>=0 && m>=0 && n < G->n_nodes && m< G->n_nodes){
		loc_add_new_edge_graph(&G->first[n], &G->first[m]);
		return 0;
	}
	return -1;
}

void erase_edge_graph(L_node **prev_id) {
	L_node *dead;

	if (*prev_id != NULL) {
		dead = *prev_id;
		*prev_id = (*prev_id)->next;
		free(dead);
	}

	return;
}

ang_pt *newDeltaStarReductionAlgorithm(Graph *G) {
	return (simpleTree2ang_pt(SEGraph2STtree(deltaStarRed(G))));
}

ang_pt *simpleTree2ang_pt(STNode_queue_struct *stqueue) {

	STNode *leaf, *node;
	ang_pt *ret = NULL;
	double x;

	while (stqueue->first) {
		while ((leaf = STNode_dequeue(stqueue))->n_children != 0)
			;
		x = leaf->phi;
		node = leaf;
		while ((node = delete_STNode(node)) && node->n_children == 0)
			;
		ins_ang_pt(&ret, new_ang_pt(x, (node) ? node->phi : MAX_SIZE_TYPEVAL));
	}
	free(stqueue);
	return (ret);
}

STNode *STNode_dequeue(STNode_queue_struct *stqueue) {
	STNode *ret = stqueue->first;

	if (stqueue->first) {
		stqueue->first = stqueue->first->next;
		if (!stqueue->first)
			stqueue->last = NULL;
	}
	return (ret);
}

STNode *delete_STNode(STNode *nd) {
	STNode *ret = nd->parent;
	if (nd->n_children != 0)
		return (ret);
	free(nd);
	if (ret)
		ret->n_children--;

	return (ret);
}

void ins_ang_pt(ang_pt **id, ang_pt *ang) {
	ang->next = *id;
	*id = ang;

	return;
}

ang_pt *new_ang_pt(double x, double y) {
	ang_pt *new_pt;

	if (!(new_pt = (ang_pt *) malloc(sizeof(ang_pt)))) {
		fprintf(stdout, " in new_ang_pt : can not allocate memory\n");
		exit(1);
	}
	new_pt->x = x;
	new_pt->y = y;
	new_pt->next = NULL;

	return (new_pt);
}

STNode_queue_struct *SEGraph2STtree(SEGraph *H) {
	STNode_queue_struct *Hnew = new_STNode_queue_struct();
	SENode *actualSENode = H->first;
	SEList *cur;

	while (actualSENode) {

		STNode_queue(Hnew,
				actualSENode->stlink = new_STNode(actualSENode->phi));
		actualSENode = actualSENode->next;
	}
	//Aggiusta i link nell'albero

	while (H->first) {
		cur = H->first->start;
		while (cur) {
			cur->to->stlink->parent = H->first->stlink;
			H->first->stlink->n_children++;
			cur = cur->next;
		}
		delSENode(H, H->first);
	}
	free(H);
	return Hnew;
}

STNode *new_STNode(double phi) {
	STNode *ret = (STNode *) malloc(sizeof(STNode));

	ret->phi = phi;
	ret->n_children = 0;
	ret->next = NULL;
	ret->parent = NULL;

	return (ret);
}

STNode_queue_struct *new_STNode_queue_struct() {
	STNode_queue_struct *ret = (STNode_queue_struct *) malloc(
			sizeof(STNode_queue_struct));
	ret->first = ret->last = NULL;
	return (ret);
}

void STNode_queue(STNode_queue_struct *stqueue, STNode *to_queue) {
	if (stqueue->last) {
		stqueue->last->next = to_queue;
	} else {
		stqueue->first = to_queue;
	}
	stqueue->last = to_queue;
	to_queue->next = NULL;
	return;
}
;

void delSENode(SEGraph *G, SENode *node) {

	if (node->next != NULL)
		node->next->prev = node->prev;
	if (node->prev != NULL) {
		node->prev->next = node->next;
	} else {
		G->first = node->next;
	}

	freeSEList(node->start);
	free(node);
	G->n_nodes--;

}

void freeSEList(SEList *toFree) {
	SEList *p, *last;
	p = toFree;
	while (p != NULL) {
		last = p;
		p = p->next;
		free(last);
	}
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//////////////////////// DELTASTARRED //////////////////////////////////////

SEGraph *deltaStarRed(Graph *G) {

	Node **orderArray;
	int i;
	SEGraph *H;
	SENode *w;
	L_node *cur;
	Node *v, *v_i;
	djset *t, *s;

	djset *djsetArray;

	djsetStack *C = NULL;

	int n_comp = 0;

#ifdef TIMECOMPUTING
	int n_times=10,j;
	clock_t start_t,end_t, partial, timeAlloc = 0, timeQS = 0, timeFix = 0;
#endif

#ifdef TIMECOMPUTING
	start_t = clock();
	partial = start_t;
	for(j=0;j<n_times;j++) {
#endif

	if (!(orderArray = (Node **) malloc(G->n_nodes * sizeof(Node *)))) {
		fprintf(stderr,
				"in deltaStarRed (orderArray) G->n_nodes = %d : Can not allocate memory\n",
				G->n_nodes);
		exit(1);
	}
	for (i = 0; i < G->n_nodes; i++) {
		orderArray[i] = G->first + i;
	}
#ifdef TIMECOMPUTING
	end_t = clock();
	timeAlloc += end_t - partial;
	partial = end_t;
#endif
	qsort(orderArray, G->n_nodes, sizeof(Node *),
			(int (*)(const void *, const void *)) compar);

//      quick_sortNode(orderArray,0, G->n_nodes - 1);
#ifdef TIMECOMPUTING
	end_t = clock();
	timeQS += end_t - partial;
	partial = end_t;
#endif
	fixGraph(G, orderArray);
#ifdef TIMECOMPUTING
	end_t = clock();
	timeFix += end_t - partial;
	partial = end_t;
}
end_t = clock();
fprintf(stdout,"\nTempo di Calcolo con  quick_sortNode(G),fixGraph(G,orderArray) (n_times = %d) = %ld (ms)\n",
		n_times,((end_t-start_t)*1000)/CLOCKS_PER_SEC );
fprintf(stdout,"\nRipartiti in Allocazione = %ld (ms) *** QuickSort = %ld (ms)  *** Fix = %ld\n",
		(timeAlloc*1000)/CLOCKS_PER_SEC,
		(timeQS*1000)/CLOCKS_PER_SEC,
		(timeFix*1000)/CLOCKS_PER_SEC );
#endif

//   n_comp = countConnectedComponents(G,orderArray);

#ifdef TIMECOMPUTING
	start_t = clock();
	for(j=0;j<n_times;j++) {
#endif
	H = newSEGraph();

	if (!(djsetArray = (djset *) malloc(G->n_nodes * sizeof(djset)))) {
		fprintf(stderr,
				"in deltaStarRed (djset) G->n_nodes = %d : Can not allocate memory\n",
				G->n_nodes);
		exit(1);
	}

	for (i = 0; i < G->n_nodes; i++) {
		v_i = orderArray[i];
		s = djsetArray + (v_i - G->first);
		initset(s, NULL);
		if (v_i->l_adj == NULL) {
			s->lbl = w = addSENode(H, v_i->val);
		} else {
			cur = v_i->l_adj;
			while (cur != NULL) {
				v = cur->p_node;
				t = find(djsetArray + (v - G->first));
				if (t->visFrom != v_i) {
					t->visFrom = v_i;
					addDjsetStack(&C, t);
				}
				cur = cur->next;
			}
			if (C->next == NULL) { // C contiene un solo elemento
				link(t = popDjsetStack(&C), s);
			} else {
				s->lbl = w = addSENode(H, v_i->val);
				while (C != NULL) {
					t = popDjsetStack(&C);
					if (t->lbl->phi == w->phi) {
						moveAdjList(t->lbl, w);
						delSENode(H, t->lbl);
					} else {
						addSEedge(w, t->lbl);
					}
					link(s, t);
				}
			}
		}
	}
#ifdef TIMECOMPUTING
}
end_t = clock();
fprintf(stdout,"\nTempo di Calcolo per la costruzione di H (n_times = %d) = %ld (ms)\n",
		n_times,((end_t-start_t)*1000)/CLOCKS_PER_SEC );
#endif
	free(orderArray);
	free(djsetArray);
	return (H);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void fixGraph(Graph *G, Node **orderArray) {
	int *nodeIndex;
	int i;
	L_node **cur;
	Node *from, *to;

	if (!(nodeIndex = (int *) malloc(G->n_nodes * sizeof(int)))) {
		fprintf(stderr,
				"in fixGraph (nodeIndex) G->n_nodes = %d : Can not allocate memory\n",
				G->n_nodes);
		exit(1);
	}

	for (i = 0; i < G->n_nodes; i++) {
		nodeIndex[orderArray[i] - G->first] = i;
	}

// Abbiamo l'ordine, dobbiamo aggiustare G:
// gli archi devono essere orientati solo verso il basso;

	for (i = 0; i < G->n_nodes; i++) {
		from = G->first + i;
		cur = &(from->l_adj);
		while (*cur != NULL) {
			to = (*cur)->p_node;
			if (nodeIndex[to - G->first] > nodeIndex[i]) {
				// Bisogna togliere l'arco e aggiungere quello inverso
				erase_edge_graph(cur);
				loc_add_new_edge_graph(to, from);
			} else {
				cur = &((*cur)->next);
			}
		}
	}

	free(nodeIndex);
	return;
}

SEGraph* newSEGraph() {
	SEGraph *ret = NULL;
	if (!(ret = (SEGraph *) malloc(sizeof(SEGraph))))
		return (NULL);
	ret->n_nodes = 0;
	ret->first = NULL;
	return (ret);
}

void initset(djset *el, SENode *lbl) {
	el->lbl = lbl;
	el->visFrom = NULL;
#if defined(_SPLITTING) ||  defined(_HALVING)
	el->parent = el;
#else
	el->parent=NULL;
#endif
#if defined(_MAX_RANK)
	el->rank = 0;
#elif defined(_MAX_DIMENSION)
	el->size = 1;
#endif
	return;
}

SENode* addSENode(SEGraph *G, double phi) {
	SENode *node;
	if (!(node = (SENode *) malloc(sizeof(SENode))))
		return (NULL);
	node->prev = NULL;
	node->next = G->first;
	if (G->first != NULL) {
		G->first->prev = node;
	}
	node->phi = phi;
	node->start = NULL;
	node->end = NULL;
	node->stlink = NULL;
	G->first = node;
	G->n_nodes++;
	return (node);
}

djset *find(djset *el) {
#if defined(_SIMPLE_NON_RECURSIVE_FIND)
	djset *set = el;
	djset *p = el,*tmp;

	while (set->parent) set=set->parent;
	while (p->parent) {
		tmp = p;
		p=p->parent;
		tmp->parent = set;
	}
	return(set);
#elif defined(_SIMPLE_RECURSIVE_FIND)
	return((el->parent)?el->parent = find(el->parent):el);
#elif defined(_SPLITTING)
	djset *set = el,*tmp;

	while (set->parent->parent != set->parent) {
		tmp = set->parent;
		set->parent = set->parent->parent;
		set = tmp;
	}
	return(set->parent);
#elif defined(_HALVING)
	while (el->parent->parent != el->parent)
		el = el->parent = el->parent->parent;
	return (el->parent);
#endif
}

void addDjsetStack(djsetStack **top, djset* el) {
	djsetStack *newEl = (djsetStack *) malloc(sizeof(djsetStack));
	newEl->el = el;
	newEl->next = *top;
	*top = newEl;
	return;
}

void link(djset *s, djset *t) {
	s = find(s);
	t = find(t);
#if defined(_MAX_RANK)
	if (s != t) {
		if (rank(s) > rank(t)) {
			t->parent = s;
		} else if (rank(s) < rank(t)) {
			s->parent = t;
			t->lbl = s->lbl;
		} else {
			t->parent = s;
			rank(s)++;
		}
	}
#elif defined(_MAX_DIMENSION)
	if (s!=t) {
		if (size(s)>=size(t)) {
			t->parent = s;
			size(s) += size(t);
		} else {
			s->parent = t;
			t->lbl = s->lbl;
			size(t) += size(s);
		}
	}
#endif
	return;
}

djset *popDjsetStack(djsetStack **top) {
	djset *ret;
	djsetStack *toFree = *top;
	if (toFree == NULL)
		return (NULL);
	ret = (*top)->el;

	*top = (*top)->next;

	free(toFree);
	return (ret);
}

void moveAdjList(SENode *from, SENode *to) {

	if (from->start) {
		from->end->next = to->start;
		to->start = from->start;
		if (!to->end) {
			to->end = from->end;
		}
		from->start = from->end = NULL;
	}
	return;
}

SEList *addSEedge(SENode *from, SENode *to) {
	SEList *edge;
	if (!(edge = (SEList *) malloc(sizeof(SEList))))
		return (NULL);
	edge->to = to;
	edge->next = from->start;
	from->start = edge;
	if (from->end == NULL)
		from->end = edge;
	return (edge);
}

int compar(Node **V, Node **W) {
	if ((*V)->val == (*W)->val)
		return (0);
	return (((*V)->val < (*W)->val) ? -1 : 1);
}

void destroy_graph(Graph *G) {
	int i;
	if (G){
		if (G->first){
			for (i = 0; i < G->n_nodes; i++) {
				while (G->first[i].l_adj != NULL)
					erase_edge_graph(&(G->first[i].l_adj));
			}
			free(G->first);
		}
		free(G);
	}
	return;
}

/* Add a node to Graph g with value val
 * @param g the Graph
 * @param val the value
 * @return the index of the node if >=0 and <0 if there aren't any space in the graph
 */
int graph_add_node(Graph *G, double val){
	if (G->n_nodes < G->max_nodes){
		int index = G->n_nodes++;
		G->first[index].val = val;
		G->first[index].visit = 0;
		G->first[index].l_adj = NULL;
		return index;
	}
	return -1;
}

/* Set the value of the node if the index is less of graph size
 * @param index the index of the node
 * @param val the value
 * @return 0 is success <0 othrewise
 */
int graph_set_node(Graph *G,int node, double val){
	if (node >=0 && node < G->n_nodes){
		G->first[node].val = val;
		return 0;
	}
	return -1;
}


void write_ang_pt(ang_pt *ang, char *angout) {
	FILE *pmf;
	int k, l;
	ang_pt *car;
	pmf = fopen(angout, "w");
	car = ang;
	k = l = 0;
	while (car != NULL) {
		if (car->y < MAX_SIZE_TYPEVAL)
			fprintf(pmf, "p %d %f %f\n", ++k, car->x, car->y);
		else
			fprintf(pmf, "l %d %f\n", ++l, car->x);
		car = car->next;
	}
	fclose(pmf);
	return;
}

void destroy_all_ang_pt(ang_pt **first_id) {

	while (*first_id != NULL)
		del_ang_pt(first_id);
	return;
}

void del_ang_pt(ang_pt **id) {
	ang_pt *dead;

	dead = *id;
	*id = dead->next;

	free(dead);
	return;
}
