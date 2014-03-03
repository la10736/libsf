/*
 ============================================================================
 Name        : exampleProgram.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Uses shared library to print greeting
 To run the resulting executable the LD_LIBRARY_PATH must be
 set to ${project_loc}/libTest/.libs
 Alternatively, libtool creates a wrapper shell script in the
 build directory of this program which can be used to run it.
 Here the script will be called exampleProgram.
 ============================================================================
 */

#include <stdlib.h>
#include <stdio.h>

#include "libsf.h"

int main(int argc, char *argv[]) {

	int nv, ne, i, ind1, ind2, len;
	double mf;
	FILE *fp, *fp_meas;
	int tt;

	char str1[256] = "";

	ang_pt *sf;

	if (argc < 4) {
		printf(
				"Usage: sizefunctions.exe nameSizeGraph nameFileValues outputFile \n");
		exit(-1);
	}
	if ((fp = fopen(argv[1], "r")) == NULL) {
		printf("Error (Reading): unable to open .size!\n");
		return (0);
	}
	if ((fp_meas = fopen(argv[2], "r")) == NULL) {
		printf("Error (Reading): unable to open measuring function file!\n");
		return (0);
	}

	tt = fscanf(fp, "%d\n %d\n", &nv, &ne);

	Graph *G = new_graph(nv);

	for (i = 0; i < nv; i++) {
		tt = fscanf(fp_meas, "%lf", &mf);
		graph_set_node(G,i,mf);
	}

	printf("Done\n");

	int x, y;
	for (i = 0; i < ne; i++) {
		tt = fscanf(fp, "%d %d \n", &ind1, &ind2);
		x = ind1;
		y = ind2;
		add_new_edge_graph(G,x,y);
	}

	fclose(fp);
	fclose(fp_meas);

	sf = newDeltaStarReductionAlgorithm(G);

	printf("Delta star reduction: done\n");

	destroy_graph(G);

	write_ang_pt(sf, argv[3]);

	printf("Sf printed\n");

	destroy_all_ang_pt(&sf);

	return 0;

}
