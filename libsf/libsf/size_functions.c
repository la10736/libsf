/*
 * size_functions.c
 *
 *  Created on: 21/apr/2014
 *      Author: michele
 */

#include <libsf.h>
#include <stdlib.h>
#include <string.h>
#include "structs.h"

#define STACK_SF_CHECK_LEN 8

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

/* Create a new void simple size function where minimum (the corner line coordinate)
 * and maximum are respectively -MAX_SIZE_VAL and MAX_SIZE_VAL
 */
ssf *ssf_void(sf *sf) {
	return ssf_create(sf, -MAX_SIZE_TYPEVAL, MAX_SIZE_TYPEVAL);
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
double ssf_get_corner_line(ssf *ssf) {
	return ssf->minx;
}
/* Return max of measuring function (should be MAX_SIZE_TYPEVAL in the legacy
 * implementation)
 * @return the value of the maximum of the measuring function
 */
double ssf_get_max_measuring_function(ssf *ssf) {
	return ssf->maxy;
}
/* Return the list of angular points in the function.
 * @return the the list of angular points in the function.
 */
const ang_pt *ssf_get_angular_points(ssf *ssf) {
	return ssf->points;
}

static ang_pt *_new_ang_pt(double x, double y, ang_pt *next) {
	ang_pt *new_pt = (ang_pt *) malloc(sizeof(ang_pt));
	if (new_pt) {
		new_pt->x = x;
		new_pt->y = y;
		new_pt->next = next;
	}
	return new_pt;
}

/* Add a angular point to the simple size function. y must be greater than x.
 * and lesser than the max of measuring function. x  must be greater equal than the corner line
 * of the simple size function.
 * @param ssf the simple size function
 * @param x the x value of the point
 * @param y the y value of the point
 * @return 0 if success <0 otherwise (for instance y is greather than the max of ssf)
 */
int ssf_add_ang_pt(ssf *ssf, double x, double y) {
	if (!(x < y && x >= ssf->minx && y <= ssf->maxy)) {
		return -1;
	}
	ang_pt *new_pt = _new_ang_pt(x, y, ssf->points);
	if (!new_pt) {
		fprintf(stdout, " in new_ang_pt : can not allocate memory\n");
		return -2;
	}
	ssf->points = new_pt;
	return 0;
}

/* Return the number of angular points in the simple size function ssf.
 * @param ssf the simple size functition
 * @return the number of angular points simple size function of ssf.
 */
int ssf_get_n_ang_pt(const ssf *ssf) {
	ang_pt *a = ssf->points;
	int ret = 0;
	while (a) {
		++ret;
		a = a->next;
	}
	return ret;
}
/* Return x of angular point */
double ang_pt_x(const ang_pt *p) {
	return p->x;
}
/* Return y of angular point */
double ang_pt_y(const ang_pt *p) {
	return p->y;
}
/* Return next angular point */
const ang_pt *ang_pt_next(const ang_pt *p) {
	return p->next;
}

/* Change the minimum of ssf (AKA cornel line). If check is true check if all angular point are
 * greather than min_x and don't change the value if check fail.
 * @param ssf the simple size function to change
 * @param min_x the new value
 * @param check if true check if all angular points are greather than min_x before change
 * the value.
 * @return 0 if change the value < 0 otherwise.
 */
int ssf_set_min_x(ssf *ssf, double min_x, int check) {
	if (!ssf) {
		return -1;
	}
	if (check) {
		ang_pt *a = ssf->points;
		while (a) {
			if (a->x < min_x) {
				return -2;
			}
			a = a->next;
		}
	}
	ssf->minx = min_x;
	return 0;
}

/* Change the maximum of ssf. If check is true check if all angular point are less
 * than max_y and don't change the value if check fail.
 * @param ssf the simple size function to change
 * @param max_y the new value
 * @param check if true check if all angular points are less than max_y before change
 * the value.
 * @return 0 if change the value < 0 otherwise.
 */
int ssf_set_max_y(ssf *ssf, double max_y, int check) {
	if (!ssf) {
		return -1;
	}
	if (check) {
		ang_pt *a = ssf->points;
		while (a) {
			if (a->y > max_y) {
				return -2;
			}
			a = a->next;
		}
	}
	ssf->maxy = max_y;
	return 0;
}

/* Return a simple size function of the size function sf at given index.
 * @param sf the size functition
 * @param index the index
 * @return the index-nt simple size function of sf. NULL if not exists.
 */
ssf *sf_get_ssf(const sf *sf, int index) {
	int i = -1;
	ssf_list *sl = NULL;
	if (!sf || index < 0) {
		return NULL;
	}
	sl = sf->ssfs;
	while (++i < index && sl) {
		sl = sl->next;
	}
	return (i == index && sl) ? sl->ssf : NULL;
}
/* Return the number of simple size functions in the size function sf.
 * @param sf the size functition
 * @return the number of simple size function of sf.
 */
int sf_get_n_ssf(const sf *sf) {
	int ret = 0;
	if (sf) {
		ssf_list *sl = sf->ssfs;
		while (sl) {
			++ret;
			sl = sl->next;
		}
	}
	return ret;
}

static ang_pt * _copy_angpt(const ang_pt *src) {
	ang_pt *ret = NULL;
	while (src) {
		ret = _new_ang_pt(src->x, src->y, ret);
		if (!ret) {
			fprintf(stdout, " in _copy_angpt : can not allocate memory\n");
			return NULL;
		}
		src = src->next;
	}
	return ret;
}

int _ang_pt_is_equal(const ang_pt *a, const ang_pt *b) {
	return (a->x == b->x && a->y == b->y);
}

/* Return 0 if if the ssf a is the same of ssf b. !0 otherwise.
 * @param a first ssf
 * @paarm b second ssf
 * @return 0 if a==b !=0 othewise*/
int ssf_compare(const ssf *a, const ssf *b) {
	if (!a || !b) {
		return -1;
	}
	if (a->minx != b->minx || a->maxy != b->maxy) {
		return -2;
	}
	ang_pt *aa = _copy_angpt(a->points);
	ang_pt *bb = _copy_angpt(b->points);
	int cont = 1;
	while (aa && bb && cont) {
		cont = 0;
		ang_pt **pcc = &bb;
		while (*pcc) {
			ang_pt *cc = *pcc;
			if (_ang_pt_is_equal(aa, cc)) {
				ang_pt *t = aa;
				*pcc = cc->next;
				aa = aa->next;
				free(cc);
				free(t);
				cont = 1;
				break;
			} else {
				pcc = &cc->next;
			}
		}
	}
	if (aa || bb) {
		_ang_pt_list_destroy(aa);
		_ang_pt_list_destroy(bb);
		return -3;
	}
	return 0;
}

/* Copy the sf a .
 * @param a the sh to copy
 * @return a copy of a or NULL if some error occur*/
sf *sf_copy(const sf *a) {
	if (!a) {
		return NULL;
	}
	sf *b = sf_create();
	if (!b) {
		fprintf(stdout, " in %s : can not allocate memory\n", __FUNCTION__);
		goto error;
	}
	int i;
	int n = sf_get_n_ssf(a);
	for (i = 0; i < n; ++i) {
		ssf *a_ssf = sf_get_ssf(a, i);
		ssf *b_ssf = ssf_create(b, a_ssf->minx, a_ssf->maxy);
		if (!b_ssf) {
			goto error;
		}
		b_ssf->points = _copy_angpt(a_ssf->points);
		if (!b_ssf->points && a_ssf->points) {
			fprintf(stdout, " in %s : Error while copy angular points\n",
					__FUNCTION__);
			goto error;
		}
	}
	return b;
	error: if (b) {
		sf_destroy(b);
	}
	return NULL;

}

/* Return 0 if if the sf a is the same of sf b. !0 otherwise.
 * @param a first sf
 * @paarm b second sf
 * @return 0 if a==b !=0 othewise*/
int sf_compare(const sf *a, const sf *b) {
	char *check_b;
	char st_chk[STACK_SF_CHECK_LEN];
	int ret = 0;
	check_b = st_chk;
	if (!a && !b) {
		goto end;
	}
	if (!a || !b) {
		ret = -1;
		goto end;
	}
	size_t la = sf_get_n_ssf(a);
	size_t lb = sf_get_n_ssf(b);
	if (la != lb) {
		ret = -2;
		goto end;
	}
	if (la > sizeof(check_b) / sizeof(check_b[0])) {
		check_b = (char *) malloc(la * sizeof(char));
	}
	memset(check_b, 0, la * sizeof(check_b[0]));
	int i, j;
	for (i = 0; i < la; ++i) {
		ssf *ssfa = sf_get_ssf(a, i);
		int found = 0;
		for (j = 0; j < lb; ++j) {
			if (!check_b[j] && !ssf_compare(ssfa, sf_get_ssf(b, j))) {
				found = check_b[j] = 1;
				break;
			}
		}
		if (!found) {
			ret = -3;
			goto end;
		}
	}
	end: if (check_b != st_chk && check_b) {
		free(check_b);
	}
	return ret;
}

void dump_sf(sf *sf) {
	int i;
	int j = 0;
	int n = sf_get_n_ssf(sf);
	printf("#### dump sf [%d] ####\n", n);
	for (i = 0; i < n; i++) {
		ssf *ssf = sf_get_ssf(sf, i);
		const ang_pt *a = ssf_get_angular_points(ssf);
		double my = ssf_get_max_measuring_function(ssf);
		printf("l %d %lf", j++, ssf_get_corner_line(ssf));
		if (my < MAX_SIZE_TYPEVAL) {
			printf(" %lf", my);
		}
		printf("\n");
		while (a) {
			printf("p %d %lf %lf\n", j++, a->x, a->y);
			a = a->next;
		}
	}
}

/* Write the size function sf in the file at the path angout.
 * If legacy write the corner lines in the legacy format of
 * l <x value of the corner line>
 * Otherwise if not legacy mode the corner line will be write
 * as
 * l <x value of the corner line> <the max value of relative connected component of the graph>
 * In every case, the points after a corner line will be all part
 * of the same connected component until another corner line will be present.
 *
 * @param sf the size function to write
 * @param angout the path of the output file
 * @param legacy the flag that activate or not the old legacy output mode
 *
 */

void write_ang_pt(sf *sf, char *angout, int legacy) {
	FILE *pmf;
	int k;
	int i;
	int n;
	if (!sf){
		printf("%s: NULL sf ABORT\n",__FUNCTION__);
		return;
	}
	n = sf_get_n_ssf(sf);
	pmf = fopen(angout, "w");
	if (!pmf){
		printf("Cannot open the fine %s to write the size function\n",angout);
		return;
	}
	for (i = 0; i < n; ++i) {
		ssf *ssf = sf_get_ssf(sf,i);
		const ang_pt *a = ssf_get_angular_points(ssf);
		k = 0;
		fprintf(pmf, "l %d %f", i, ssf_get_corner_line(ssf));
		if (legacy){
			fprintf(pmf, "\n");
		}else{
			fprintf(pmf, "%f\n", ssf_get_max_measuring_function(ssf));
		}
		while (a) {
			fprintf(pmf, "p %d %f %f\n", ++k, ang_pt_x(a), ang_pt_y(a));
			a = ang_pt_next(a);
		}
	}
	fclose(pmf);
	return;
}

