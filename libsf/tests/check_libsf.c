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
	}END_TEST

START_TEST (test_ssf_info)
	{
		sf *sf = sf_create();
		ssf *ssf = ssf_create(sf, 0.1, 1.2);
		ck_assert(ssf_get_corner_line(ssf) == 0.1);
		ck_assert(ssf_get_max_measuring_function(ssf) == 1.2);
		ck_assert_ptr_eq(ssf_get_angular_points(ssf), NULL);
		ck_assert_int_eq(ssf_get_n_ang_pt(ssf),0);
		ssf_add_ang_pt(ssf, 0.1, 0.3);
		ck_assert_ptr_ne(ssf_get_angular_points(ssf), NULL);
		ck_assert_int_eq(ssf_get_n_ang_pt(ssf),1);
		ssf_add_ang_pt(ssf, 0.2, 0.4);
		ck_assert_int_eq(ssf_get_n_ang_pt(ssf),2);
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
	TCase * tc_cssf_info = tcase_create("ssf info");
	tcase_add_test(tc_cssf, test_ssf_info);
	suite_add_tcase(s, tc_cssf_info);
	TCase * tc_apt_info = tcase_create("ang_pt info");
	tcase_add_test(tc_apt_info, test_ang_pt_x);
	tcase_add_test(tc_apt_info , test_ang_pt_y);
	tcase_add_test(tc_apt_info , test_ang_pt_next);
	suite_add_tcase(s, tc_apt_info);
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
