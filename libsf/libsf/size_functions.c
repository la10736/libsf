/*
 * size_functions.c
 *
 *  Created on: 21/apr/2014
 *      Author: michele
 */

#include <libsf.h>
#include <stdlib.h>
#include "structs.h"

struct ssf {
	double minx;
	double maxy;
	ang_pt *points;
};
typedef struct ssf_list {
	ssf *ssf;
	struct ssf_list *next;
} ssf_list;

struct sf {
	ssf_list *ssfs;
};

static void _sf_add_ssf(sf *sf, ssf *ssf) {
	ssf_list *ssfl = (ssf_list *) malloc(sizeof(ssf_list *));
	ssfl->next = sf->ssfs;
	ssfl->ssf = ssf;
	sf->ssfs = ssfl;
}

/* Create a new simple size function where the minimum (the corner line coordinate)
 * is min_x and max_y is the maximum of the measuring function on the graph.
 * @param sf the size function that containt that simple size function
 * @param min_x is the minimum of the measuring function
 * @param max_y is the maximum of the measuring function
 * @return a new simple size function of sf if all ok NULL otherwise (for instance min_x>max_y)
 */
ssf *ssf_create(sf *sf, double min_x, double max_y) {
	ssf *ssf = NULL;
	if (!sf) {
		return NULL;
	}
	if (max_y < min_x) {
		return NULL;
	}
	ssf = (struct ssf*) malloc(sizeof(ssf));
	if (ssf) {
		ssf->points = NULL;
		ssf->minx = min_x;
		ssf->maxy = max_y;
		_sf_add_ssf(sf, ssf);
	}
	return ssf;
}

static void _ang_pt_list_destroy(ang_pt *points) {
	while (points) {
		ang_pt *dead = points;
		points = points->next;
		free(dead);
	}
}

static void _ssf_destroy(ssf *ssf) {
	if (ssf) {
		if (ssf->points) {
			_ang_pt_list_destroy(ssf->points);
		}
		free(ssf);
	}
}

/* Create a size function */
sf *sf_create(void) {
	sf *sf = (struct sf *) malloc(sizeof(sf));
	if (sf) {
		sf->ssfs = NULL;
	}
	return sf;
}

/* Destroy a size function */
void sf_destroy(sf *sf) {
	if (sf) {
		while (sf->ssfs) {
			ssf_list *ssfs = sf->ssfs;
			sf->ssfs = sf->ssfs->next;
			_ssf_destroy(ssfs->ssf);
			free(ssfs);
		}
	}
}

/* Return the position of the corner line of a simple size function.
 * @return the value of the corner line
 */
double ssf_get_corner_line(ssf *ssf){
	return ssf->minx;
}
/* Return max of measuring function (should be MAX_SIZE_TYPEVAL in the legacy
 * implementation)
 * @return the value of the maximum of the measuring function
 */
double ssf_get_max_measuring_function(ssf *ssf){
	return ssf->maxy;
}
/* Return the list of angular points in the function.
 * @return the the list of angular points in the function.
 */
const ang_pt *ssf_get_angular_points(ssf *ssf){
	return ssf->points;
}

/* Add a angular point to the simple size function. y must be greater than x.
 * and lesser than the max of measuring function. x  must be greater equal than the corner line
 * of the simple size function.
 * @param ssf the simple size function
 * @param x the x value of the point
 * @param y the y value of the point
 * @return 0 if success <0 otherwise (for instance y is greather than the max of ssf)
 */
int ssf_add_ang_pt(ssf *ssf, double x, double y){
	if (!(x<y && x>=ssf->minx && y<=ssf->maxy)){
		return -1;
	}
	ang_pt *new_pt = (ang_pt *) malloc(sizeof(ang_pt));
	if (!new_pt) {
		fprintf(stdout, " in new_ang_pt : can not allocate memory\n");
		return -2;
	}
	new_pt->x = x;
	new_pt->y = y;
	new_pt->next = ssf->points;
	ssf->points = new_pt;
	return 0;
}

/* Return the number of angular points in the simple size function ssf.
 * @param ssf the simple size functition
 * @return the number of angular points simple size function of ssf.
 */
int ssf_get_n_ang_pt(ssf *ssf){
	ang_pt *a = ssf->points;
	int ret = 0;
	while(a){
		++ret;
		a = a->next;
	}
	return ret;
}
/* Return x of angular point */
double ang_pt_x(const ang_pt *p){
	return p->x;
}
/* Return y of angular point */
double ang_pt_y(const ang_pt *p){
	return p->y;
}
/* Return next angular point */
const ang_pt *ang_pt_next(const ang_pt *p){
	return p->next;
}
