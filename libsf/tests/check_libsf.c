/*
 * check_libsf.c
 *
 *  Created on: 21/apr/2014
 *      Author: michele
 */

#include <check.h>
#include <libsf.h>
#include "structs.h"

START_TEST (test_new_graph)
	{
		Graph *g;
		g = new_graph(5);
		ck_assert_int_eq(g->max_nodes, 5);
		ck_assert_int_eq(g->n_nodes, 0);
		destroy_graph(g);
	}END_TEST

START_TEST (test_graph_add_node)
	{
		Graph *g;
		int i = 0;
		g = new_graph(3);
		ck_assert_int_eq(g->n_nodes, i);
		ck_assert_int_eq(graph_add_node(g, 2.3), 0);
		ck_assert(g->first[i].val == 2.3);
		ck_assert(!g->first[i].visit);
		ck_assert_ptr_eq(g->first[i].l_adj, NULL);
		i = 1;
		ck_assert_int_eq(g->n_nodes, i);
		ck_assert_int_eq(graph_add_node(g, 3.1), i);
		ck_assert(g->first[i].val == 3.1);
		ck_assert(!g->first[i].visit);
		ck_assert_ptr_eq(g->first[i].l_adj, NULL);
		i = 2;
		ck_assert_int_eq(g->n_nodes, i);
		ck_assert_int_eq(graph_add_node(g, -1.23), i);
		ck_assert(g->first[i].val == -1.23);
		ck_assert(!g->first[i].visit);
		ck_assert_ptr_eq(g->first[i].l_adj, NULL);
		i = 3;
		ck_assert_int_eq(g->n_nodes, i);

		ck_assert_int_le(graph_add_node(g, 1.0), 0);
		ck_assert_int_eq(g->n_nodes, i);
		ck_assert(g->first[2].val == -1.23);
		ck_assert(!g->first[2].visit);
		ck_assert_ptr_eq(g->first[2].l_adj, NULL);
		destroy_graph(g);
	}END_TEST

START_TEST (test_graph_set_node)
	{
		Graph *g;
		int i;
		g = new_graph(2);
		i = graph_add_node(g, 1.3);
		ck_assert_int_eq(graph_set_node(g, i, 1.0), 0);
		ck_assert(g->first[i].val == 1.0);
		ck_assert_int_lt(graph_set_node(g, i + 1, 1.0), 0);
		i = graph_add_node(g, 1.2);
		ck_assert_int_eq(graph_set_node(g, i, 1.1), 0);
		ck_assert(g->first[i].val == 1.1);
		ck_assert_int_lt(graph_set_node(g, -1, 1.0), 0);
		destroy_graph(g);
	}END_TEST

START_TEST (test_add_new_edge_graph)
	{
		Graph *g;
		int n, m;
		g = new_graph(2);
		n = graph_add_node(g, 1.3);
		m = graph_add_node(g, 2.2);
		ck_assert_int_eq(add_new_edge_graph(g, n, m), 0);
		ck_assert_ptr_eq(g->first[n].l_adj->p_node, &g->first[m]);
		ck_assert_int_lt(add_new_edge_graph(g, -1, m), 0);
		ck_assert_int_lt(add_new_edge_graph(g, n, -1), 0);
		ck_assert_int_lt(add_new_edge_graph(g, m + 1, m), 0);
		ck_assert_int_lt(add_new_edge_graph(g, n, m + 1), 0);
		destroy_graph(g);
	}END_TEST

Suite *graph_suite(void) {
	Suite * s = suite_create("Graph");
	/* Core test case */
	TCase * tc_core = tcase_create("Create Destroy");
	tcase_add_test(tc_core, test_new_graph);
	suite_add_tcase(s, tc_core);
	TCase * tc_nodes = tcase_create("Add and modify nodes");
	tcase_add_test(tc_nodes, test_graph_add_node);
	tcase_add_test(tc_nodes, test_graph_set_node);
	suite_add_tcase(s, tc_nodes);
	TCase * tc_edges = tcase_create("Add edges");
	tcase_add_test(tc_edges, test_add_new_edge_graph);
	suite_add_tcase(s, tc_edges);

	return s;
}

START_TEST (test_create_sf)
	{
		sf *sf = sf_create();
		ck_assert_ptr_ne(sf, NULL);
		sf_destroy(sf);
	}END_TEST

START_TEST (test_create_ssf)
	{
		sf *sf = sf_create();
		ssf *ssf = ssf_create(sf, 0.1, 1.2);
		ck_assert_ptr_ne(ssf, NULL);
		ck_assert_ptr_eq(ssf_create(sf, 0.1, 0.0), NULL);
		ck_assert_ptr_ne(ssf_create(sf, 0.1, 0.1), NULL);
		sf_destroy(sf);
	}END_TEST

START_TEST (test_ssf_add_point)
	{
		sf *sf = sf_create();
		ssf *ssf = ssf_create(sf, 0.1, 1.2);
		ck_assert_int_eq(ssf_add_ang_pt(ssf, 0.1, 0.3), 0);
		/* x>y fail*/
		ck_assert_int_lt(ssf_add_ang_pt(ssf, 0.3, 0.2), 0);
		/* x==y fail*/
		ck_assert_int_lt(ssf_add_ang_pt(ssf, 0.3, 0.3), 0);
		/* x<cl fail*/
		ck_assert_int_lt(ssf_add_ang_pt(ssf, 0.0, 0.3), 0);
		/* x>max fail*/
		ck_assert_int_lt(ssf_add_ang_pt(ssf, 1.3, 1.4), 0);
		/* y>max fail*/
		ck_assert_int_lt(ssf_add_ang_pt(ssf, 0.3, 1.4), 0);
		sf_destroy(sf);
	}END_TEST

START_TEST(test_sf_get_n_ssf)
	{
		sf *sf = sf_create();
		ck_assert_int_eq(sf_get_n_ssf(NULL), 0);
		ck_assert_int_eq(sf_get_n_ssf(sf), 0);
		ssf_create(sf, 0.1, 1.2);
		ck_assert_int_eq(sf_get_n_ssf(sf), 1);
		ssf_create(sf, 0.1, 1.2);
		ck_assert_int_eq(sf_get_n_ssf(sf), 2);
		sf_destroy(sf);
	}END_TEST

static int arr_index(void **arr, int len, void *chk) {
	int i;
	for (i = 0; i < len; i++) {
		if (arr[i] == chk) {
			return i;
		}
	}
	return -1;
}

START_TEST(test_sf_get_ssf)
	{
		sf *sf = sf_create();
		ssf *ssf[3];
		int i;
		ck_assert_ptr_eq(sf_get_ssf(sf, -1), NULL);
		ck_assert_ptr_eq(sf_get_ssf(sf, 0), NULL);

		ssf[0] = ssf_create(sf, 0.1, 1);
		ssf[1] = ssf_create(sf, 0.1, 2);
		ssf[2] = ssf_create(sf, 0.1, 3);
		i = arr_index((void **) ssf, 3, sf_get_ssf(sf, 0));
		ck_assert_int_ge(i, 0);
		ssf[i] = NULL;
		i = arr_index((void **) ssf, 3, sf_get_ssf(sf, 1));
		ck_assert_int_ge(i, 0);
		ssf[i] = NULL;
		i = arr_index((void **) ssf, 3, sf_get_ssf(sf, 2));
		ck_assert_int_ge(i, 0);
		ssf[i] = NULL;

		ck_assert_ptr_eq(sf_get_ssf(sf, -1), NULL);
		ck_assert_ptr_eq(sf_get_ssf(sf, 4), NULL);
		ck_assert_ptr_eq(sf_get_ssf(NULL,0), NULL);
		sf_destroy(sf);

	}END_TEST

START_TEST (test_ssf_info)
	{
		sf *sf = sf_create();
		ssf *ssf = ssf_create(sf, 0.1, 1.2);
		ck_assert(ssf_get_corner_line(ssf) == 0.1);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.2);
		ck_assert_ptr_eq(ssf_get_angular_points(ssf), NULL);
		ck_assert_int_eq(ssf_get_n_ang_pt(ssf), 0);
		ssf_add_ang_pt(ssf, 0.1, 0.3);
		ck_assert_ptr_ne(ssf_get_angular_points(ssf), NULL);
		ck_assert_int_eq(ssf_get_n_ang_pt(ssf), 1);
		ssf_add_ang_pt(ssf, 0.2, 0.4);
		ck_assert_int_eq(ssf_get_n_ang_pt(ssf), 2);
		sf_destroy(sf);
	}END_TEST

START_TEST (test_ssf_compare)
	{
		sf *sf = sf_create();
		ssf *a = ssf_create(sf, 0.1, 10);
		ck_assert_int_ne(0, ssf_compare(a, NULL));
		ck_assert_int_ne(0, ssf_compare(NULL,a));
		ck_assert_int_ne(0, ssf_compare(NULL,NULL));
		ssf *b = ssf_create(sf, 0.1, 10);
		ck_assert_int_eq(0, ssf_compare(a, b));
		ssf_add_ang_pt(a, 1, 2);
		ck_assert_int_ne(0, ssf_compare(a, b));
		ssf_add_ang_pt(b, 2, 3);
		ck_assert_int_ne(0, ssf_compare(a, b));
		ssf_add_ang_pt(a, 2, 3);
		ssf_add_ang_pt(b, 1, 2);
		ck_assert_int_eq(0, ssf_compare(a, b));
		ssf_add_ang_pt(a, 2, 3);
		ck_assert_int_ne(0, ssf_compare(a, b));
		ssf_add_ang_pt(b, 2, 3);
		ck_assert_int_eq(0, ssf_compare(a, b));
		sf_destroy(sf);
	}END_TEST

START_TEST (test_ssf_void)
	{
		sf *sf = sf_create();
		ssf *ssf = ssf_void(sf);
		ck_assert_ptr_ne(ssf, NULL);
		ck_assert_ptr_eq(ssf_void(NULL), NULL);
		ck_assert_int_eq(0,
				ssf_compare(ssf, ssf_create(sf,-MAX_SIZE_TYPEVAL,MAX_SIZE_TYPEVAL)));
		sf_destroy(sf);
	}END_TEST

START_TEST (test_ang_pt_x)
	{
		sf *sf = sf_create();
		ssf *ssf = ssf_create(sf, 0.1, 1.2);
		ssf_add_ang_pt(ssf, 0.1, 0.3);
		ck_assert(ang_pt_x(ssf_get_angular_points(ssf)) == 0.1);
		sf_destroy(sf);
	}END_TEST

START_TEST (test_ang_pt_y)
	{
		sf *sf = sf_create();
		ssf *ssf = ssf_create(sf, 0.1, 1.2);
		ssf_add_ang_pt(ssf, 0.1, 0.3);
		ck_assert(ang_pt_y(ssf_get_angular_points(ssf)) == 0.3);
		sf_destroy(sf);
	}END_TEST

START_TEST (test_ang_pt_next)
	{
		sf *sf = sf_create();
		ssf *ssf = ssf_create(sf, 0.1, 1.2);
		ssf_add_ang_pt(ssf, 0.1, 0.3);
		ck_assert_ptr_eq(ang_pt_next(ssf_get_angular_points(ssf)), NULL);
		sf_destroy(sf);
	}END_TEST

START_TEST(test_ssf_set_min_x)
	{
		sf *sf = sf_create();
		ssf *ssf = ssf_create(sf, 0.1, 1.2);
		ck_assert_int_lt(ssf_set_min_x(NULL,1.0, 1), 0);
		ck_assert_int_eq(ssf_set_min_x(ssf, 0.3, 1), 0);
		ck_assert(ssf_get_corner_line(ssf) == 0.3);
		ck_assert_int_eq(ssf_set_min_x(ssf, 0.2, 1), 0);
		ck_assert(ssf_get_corner_line(ssf) == 0.2);
		ck_assert_int_eq(ssf_set_min_x(ssf, 0.4, 0), 0);
		ck_assert(ssf_get_corner_line(ssf) == 0.4);
		ck_assert_int_eq(ssf_set_min_x(ssf, 0.2, 0), 0);
		ck_assert(ssf_get_corner_line(ssf) == 0.2);
		ssf_add_ang_pt(ssf, 0.4, 1.0);
		ck_assert_int_eq(ssf_set_min_x(ssf, 0.3, 1), 0);
		ck_assert(ssf_get_corner_line(ssf) == 0.3);
		ck_assert_int_lt(ssf_set_min_x(ssf, 1.2, 1), 0);
		ck_assert(ssf_get_corner_line(ssf) == 0.3);
		ck_assert_int_lt(ssf_set_min_x(ssf, 0.5, 1), 0);
		ck_assert(ssf_get_corner_line(ssf) == 0.3);
		ck_assert_int_eq(ssf_set_min_x(ssf, 0.4, 1), 0);
		ck_assert(ssf_get_corner_line(ssf) == 0.4);
		ck_assert_int_eq(ssf_set_min_x(ssf, 1.4, 0), 0);
		ck_assert(ssf_get_corner_line(ssf) == 1.4);
		sf_destroy(sf);
	}END_TEST

START_TEST(test_ssf_set_max_y)
	{
		sf *sf = sf_create();
		ssf *ssf = ssf_create(sf, 0.1, 1.2);
		ck_assert_int_lt(ssf_set_max_y(NULL,1.0,1), 0);
		ck_assert_int_eq(ssf_set_max_y(ssf, 1.7, 1), 0);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.7);
		ck_assert_int_eq(ssf_set_max_y(ssf, 1.6, 1), 0);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.6);
		ck_assert_int_eq(ssf_set_max_y(ssf, 1.7, 0), 0);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.7);
		ck_assert_int_eq(ssf_set_max_y(ssf, 1.6, 0), 0);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.6);
		ssf_add_ang_pt(ssf, 1.44, 1.45);
		ck_assert_int_eq(ssf_set_max_y(ssf, 1.7, 1), 0);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.7);
		ck_assert_int_lt(ssf_set_max_y(ssf, 1.0, 1), 0);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.7);
		ck_assert_int_lt(ssf_set_max_y(ssf, 1.445, 1), 0);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.7);
		ck_assert_int_eq(ssf_set_max_y(ssf, 1.45, 1), 0);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.45);
		ck_assert_int_eq(ssf_set_max_y(ssf, 1.4, 0), 0);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.4);
		sf_destroy(sf);
	}END_TEST

START_TEST (test_sf_copy)
	{
		ck_assert_ptr_eq(NULL, sf_copy(NULL));
		sf *a = sf_create();
		ssf_create(a, 0.1, 10);
		sf *b = sf_copy(a);
		ck_assert_ptr_ne(NULL, b);
		ck_assert_int_eq(sf_get_n_ssf(a), sf_get_n_ssf(b));
		ck_assert_int_eq(0, ssf_compare(sf_get_ssf(a, 0), sf_get_ssf(b, 0)));
		sf_destroy(b);
		ssf_create(a, 0.2, 20);
		b = sf_copy(a);
		ck_assert_ptr_ne(NULL, b);
		ck_assert_int_eq(sf_get_n_ssf(a), sf_get_n_ssf(b));
		int i;
		int j;
		ck_assert_int_ne(0, ssf_compare(sf_get_ssf(b, 0), sf_get_ssf(b, 1)));
		for (i = 0; i < 2; i++) {
			int found = 0;
			for (j = 0; j < 2; j++) {
				if (!ssf_compare(sf_get_ssf(a, i), sf_get_ssf(b, j))) {
					found = 1;
					break;
				}
			}
			ck_assert(found);
		}
		sf_destroy(b);

	}END_TEST

START_TEST (test_sf_compare)
	{
		ck_assert_int_eq(0, sf_compare(NULL, NULL));
		sf *a = sf_create();
		ck_assert_int_ne(0, sf_compare(a, NULL));
		ck_assert_int_ne(0, sf_compare(NULL, a));
		sf *b = sf_copy(a);
		ck_assert_int_eq(0, sf_compare(a, b));
		ssf_create(a, .2, 3);
		ck_assert_int_ne(0, sf_compare(a, b));
		ssf_create(b, .2, 3);
		ck_assert_int_eq(0, sf_compare(a, b));
		ssf_create(a, .1, 4);
		ssf_create(a, .1, 4);
		ssf_create(a, 32, 43.2);
		ssf_create(a, 12.2, 13.1);
		ssf_create(a, -23.1, -2.1);
		ck_assert_int_ne(0, sf_compare(a, b));
		ssf_create(b, 12.2, 13.1);
		ck_assert_int_ne(0, sf_compare(a, b));
		ssf_create(b, 32, 43.2);
		ck_assert_int_ne(0, sf_compare(a, b));
		ssf_create(b, .1, 4);
		ck_assert_int_ne(0, sf_compare(a, b));
		ssf_create(b, -23.1, -2.1);
		ck_assert_int_ne(0, sf_compare(a, b));
		ssf_create(b, .1, 4);
		ck_assert_int_eq(0, sf_compare(a, b));

		int i;
		for (i = 0; i < 200; ++i) {
			ssf_create(a, i, i + 1);
		}
		for (i = 0; i < 200; ++i) {
			ck_assert_int_ne(0, sf_compare(a, b));
			ssf_create(b, i, i + 1);
		}
		ck_assert_int_eq(0, sf_compare(a, b));

		sf_destroy(a);
		sf_destroy(b);

	}END_TEST

START_TEST(test_sf_dot)
	{
		/* Case just one point */
		Graph *G = new_graph(3);
		graph_add_node(G, 0);
		sf *a = sf_create();
		ssf_create(a, 0, 0);
		sf *b = newDeltaStarReductionAlgorithm(G);
		ck_assert_int_eq(0, sf_compare(a, b));

	}END_TEST

	START_TEST(test_sf_I)
		{
			/* case line */
			Graph *G = new_graph(10);
			int i;
			for(i=0;i<10;++i){
				graph_add_node(G, i);
				if (i>0){
					add_new_edge_graph(G,i-1,i);
				}
			}
			graph_add_node(G, 0);
			sf *a = sf_create();
			ssf_create(a, 0, 9);
			sf *b = newDeltaStarReductionAlgorithm(G);
			dump_sf(a);
			dump_sf(b);
			ck_assert_int_eq(0, sf_compare(a, b));
		}END_TEST

START_TEST(test_sf_V)
	{
		/* Reversed V case */
		Graph *G = new_graph(3);
		graph_add_node(G, 0);
		graph_add_node(G, 1);
		graph_add_node(G, 0.2);
		add_new_edge_graph(G, 0, 1);
		add_new_edge_graph(G, 1, 2);
		sf *a = sf_create();
		ssf_add_ang_pt(ssf_create(a, 0, 1), 0.2, 1);
		sf *b = newDeltaStarReductionAlgorithm(G);
		dump_sf(a);
		dump_sf(b);
		ck_assert_int_eq(0, sf_compare(a, b));

	}END_TEST

	START_TEST(test_sf_branches)
		{
			/* case: a Tree with a lot of branches */
			Graph *G = new_graph(10);
			graph_add_node(G, -30);
			graph_add_node(G, 30);
			graph_add_node(G, 29);
			graph_add_node(G, 28);
			graph_add_node(G, 28);
			graph_add_node(G, 27);
			graph_add_node(G, 27);
			graph_add_node(G, 26);
			graph_add_node(G, 26);
			graph_add_node(G, 25);
			add_new_edge_graph(G, 0, 1);
			add_new_edge_graph(G, 1, 2);
			add_new_edge_graph(G, 2, 3);
			add_new_edge_graph(G, 2, 4);
			add_new_edge_graph(G, 4, 5);
			add_new_edge_graph(G, 4, 6);
			add_new_edge_graph(G, 6, 7);
			add_new_edge_graph(G, 6, 8);
			add_new_edge_graph(G, 8, 9);
			sf *a = sf_create();
			ssf *ssf = ssf_create(a, -30, 30);
			ssf_add_ang_pt(ssf, 28, 29);
			ssf_add_ang_pt(ssf, 27, 28);
			ssf_add_ang_pt(ssf, 26, 27);
			ssf_add_ang_pt(ssf, 25, 30);
			sf *b = newDeltaStarReductionAlgorithm(G);
			dump_sf(a);
			dump_sf(b);
			ck_assert_int_eq(0, sf_compare(a, b));

		}END_TEST

Suite *sf_suite(void) {
	Suite * s = suite_create("SizeFunction");
	/* Core test case */
	TCase * tc_csf = tcase_create("Create Destroy sf");
	tcase_add_test(tc_csf, test_create_sf);
	suite_add_tcase(s, tc_csf);
	TCase * tc_cssf = tcase_create("Create ssf");
	tcase_add_test(tc_cssf, test_create_ssf);
	tcase_add_test(tc_cssf, test_ssf_add_point);
	suite_add_tcase(s, tc_cssf);
	TCase * tc_cpssf = tcase_create("Create count and point ssf");
	tcase_add_test(tc_cpssf, test_sf_get_n_ssf);
	tcase_add_test(tc_cpssf, test_sf_get_ssf);
	suite_add_tcase(s, tc_cpssf);
	TCase * tc_cssf_info = tcase_create("ssf info");
	tcase_add_test(tc_cssf, test_ssf_info);
	suite_add_tcase(s, tc_cssf_info);
	TCase * tc_apt_info = tcase_create("ang_pt info");
	tcase_add_test(tc_apt_info, test_ang_pt_x);
	tcase_add_test(tc_apt_info, test_ang_pt_y);
	tcase_add_test(tc_apt_info, test_ang_pt_next);
	suite_add_tcase(s, tc_apt_info);
	TCase * tc_ssf_set_min_x = tcase_create("ssf set min x");
	tcase_add_test(tc_ssf_set_min_x, test_ssf_set_min_x);
	suite_add_tcase(s, tc_ssf_set_min_x);
	TCase * tc_ssf_set_max = tcase_create("ssf set max");
	tcase_add_test(tc_ssf_set_max, test_ssf_set_max_y);
	suite_add_tcase(s, tc_ssf_set_max);
	TCase * tc_ssf_compare = tcase_create("ssf compare");
	tcase_add_test(tc_ssf_compare, test_ssf_compare);
	suite_add_tcase(s, tc_ssf_compare);
	TCase * tc_ssf_void = tcase_create("");
	tcase_add_test(tc_ssf_void, test_ssf_void);
	suite_add_tcase(s, tc_ssf_void);

	TCase * tc_sf_copy = tcase_create("sf copy");
	tcase_add_test(tc_sf_copy, test_sf_copy);
	suite_add_tcase(s, tc_sf_copy);
	TCase * tc_sf_compare = tcase_create("sf compare");
	tcase_add_test(tc_sf_compare, test_sf_compare);
	suite_add_tcase(s, tc_sf_compare);
	TCase * tc_sf_dot = tcase_create("sf dot");
	tcase_add_test(tc_sf_dot, test_sf_dot);
	suite_add_tcase(s, tc_sf_dot);
	TCase * tc_sf_I = tcase_create("sf I");
	tcase_add_test(tc_sf_I, test_sf_I);
	suite_add_tcase(s, tc_sf_I);
	TCase * tc_sf_V = tcase_create("compute sf V");
	tcase_add_test(tc_sf_V, test_sf_V);
	suite_add_tcase(s, tc_sf_V);
	TCase * tc_sf_branches = tcase_create("sf branches");
	tcase_add_test(tc_sf_branches, test_sf_branches);
	suite_add_tcase(s, tc_sf_branches);


	return s;
}

int main(void) {
	int number_failed;
	Suite * s = graph_suite();
	SRunner * sr = srunner_create(s);
	srunner_add_suite(sr, sf_suite());
	srunner_run_all(sr, CK_NORMAL);
	number_failed = srunner_ntests_failed(sr);
	srunner_free(sr);
	return (number_failed == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}
