/*
 * structs.h
 *
 *  Created on: 03/mar/2014
 *      Author: michele
 */

#ifndef STRUCTS_H_
#define STRUCTS_H_

#include <stdlib.h>
#include <stdio.h>
#include <float.h>

#include "libsf.h"

#define _HALVING
#define _MAX_RANK
#define label(a) a->lbl
#if defined(_MAX_RANK)
#define rank(a) a->rank
#elif defined(_MAX_DIMENSION)
#define size(a) a->size
#endif


/* STRUCTRES */
struct ang_pt{
	double	x;
	double y;
	struct ang_pt	*next;
};


/* GRAPH STRUCTURES */

struct Node{
	struct L_node	*l_adj;
	double	val;
	int	visit;
};

struct L_node{
	struct Node		*p_node;
	struct L_node	*next;
};

struct Graph{
	struct Node	*first;
	int		n_nodes;
	int 	max_nodes;
};

typedef struct Node Node;
typedef struct L_node L_node;

/* DGRAPH STRUCTURES */

struct Edge_links{
	struct D_node	*to;
	struct L_edge	*from_l;
};

struct Edge{
	struct Edge_links	low;
	struct Edge_links	high;
};

struct L_edge{
	struct L_edge	*next;
	struct L_edge	*prev;
	struct Edge		*edge;
};

struct D_node{
	struct L_edge	*l_adj_low;
	struct L_edge	*l_adj_high;
	double			val;
	struct D_node	*visit;
	struct D_node	**order_link;
};

struct D_graph{
	struct D_node	*first;
	int				n_nodes;
	struct D_node	**order_array;
};

typedef struct Edge_links Edge_links;
typedef struct Edge Edge;
typedef struct L_edge L_edge;
typedef struct D_node D_node;
typedef struct D_graph D_graph;

/* PGRAPH STRUCTURES */

struct P_node{
	struct P_node	*next;
	struct P_node	*prev;
	double	val;
};

struct P_graph{
	struct P_node	*first;
	int		n_nodes;
};

struct P_list{
	struct P_node	*node;
	struct P_list	*next;
};

typedef struct P_node P_node;
typedef struct P_graph P_graph;
typedef struct P_list P_list;


// OTHERS

typedef struct STNode{
  double phi;
  struct STNode *parent;
  struct STNode *next;
  int n_children;
}STNode;

typedef struct STNode_queue_struct{
   STNode *first;
   STNode *last;
}STNode_queue_struct;


typedef struct SENode{
    double phi;
    struct SEList *start;
    struct SEList *end;
    struct SENode *next;
    struct SENode *prev;
    STNode *stlink;
}SENode;

typedef struct SEList{
    struct SENode *to;
    struct SEList *next;
}SEList;

typedef struct SEGraph{
    struct SENode *first;
    int           n_nodes;
}SEGraph;


// DA UNIONFIND.h

typedef struct djset{
    struct djset  *parent;
#if defined(_MAX_RANK)
    int           rank;
#elif defined(_MAX_DIMENSION)
    int           size;
#endif
    SENode        *lbl;
    Node        *visFrom;
}djset;

typedef struct djsetStack{
    djset  *el;
    struct djsetStack *next;
}djsetStack;


#endif /* STRUCTS_H_ */
