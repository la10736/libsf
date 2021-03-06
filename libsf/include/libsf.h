#ifndef libTest_H
#define libTest_H

#define MAX_SIZE_TYPEVAL DBL_MAX

typedef struct sf sf; /**> Size function set: a collection of simple size function*/
typedef struct ssf ssf; /**> Simple Size function a size function of a connected graph.
 	 	 	 	 	 	 	 That means just one corner line*/
typedef struct ang_pt ang_pt; /**> A angular point of a simple size funtion */
typedef struct Graph Graph; /**> A Graph with measuring function */

/* Create a Graph with max n nodes
 * @param n the max numbers of nodes
 * @return the graph pointer
 */
Graph *new_graph(int n);
/* Destroy the graph G
 */
void destroy_graph(Graph *G);
/* Add a node to Graph G with value val
 * @param g the Graph
 * @param val the value
 * @return the index of the node if >=0 and <0 if there aren't any space in the graph
 */
int graph_add_node(Graph *G, double val);
/* Set the value of the node if the index is less of graph size
 * @param index the index of the node
 * @param val the value
 * @return 0 is success <0 othrewise
 */
int graph_set_node(Graph *G, int index, double val);
/* Add new edge to the graph G from the node n to the node m
 * @param G the Graph
 * @param n the node where the edge starts
 * @param m the node where the edge ends
 * @return 0 in case of success, <0 otherwise
 */
int add_new_edge_graph(Graph *G, int n, int m);
sf *newDeltaStarReductionAlgorithm(Graph *G);

/* Create a size function */
sf *sf_create(void);
/* Destroy a size function */
void sf_destroy(sf *sf);
/* Create a new simple size function where the minimum (the corner line coordinate)
 * is min_x and max_y is the maximum of the measuring function on the graph.
 * @param sf the size function that containt that simple size function
 * @param min_x is the minimum of the measuring function
 * @param max_y is the maximum of the measuring function
 * @return a new simple size function of sf if all ok NULL otherwise (for instance min_x>max_y)
 */
ssf *ssf_create(sf *sf, double min_x, double max_y);
/* Create a new void simple size function where minimum (the corner line coordinate)
 * and maximum are respectively -MAX_SIZE_VAL and MAX_SIZE_VAL
 */
ssf *ssf_void(sf *sf);
/* Change the minimum of ssf (AKA cornel line). If check is true check if all angular point are
 * greather than min_x and don't change the value if check fail.
 * @param ssf the simple size function to change
 * @param min_x the new value
 * @param check if true check if all angular points are greather than min_x before change
 * the value.
 * @return 0 if change the value < 0 otherwise.
 */
int ssf_set_min_x(ssf *ssf, double min_x, int check);
/* Change the maximum of ssf. If check is true check if all angular point are less
 * than max_y and don't change the value if check fail.
 * @param ssf the simple size function to change
 * @param max_y the new value
 * @param check if true check if all angular points are less than max_y before change
 * the value.
 * @return 0 if change the value < 0 otherwise.
 */
int ssf_set_max_y(ssf *ssf, double max_y, int check);
/* Add a angular point to the simple size function. y must be greater than x.
 * and lesser than the max of measuring function. x  must be greater equal than the corner line
 * of the simple size function.
 * @param ssf the simple size function
 * @param x the x value of the point
 * @param y the y value of the point
 * @return 0 if success <0 otherwise (for instance y is greather than the max of ssf)
 */
int ssf_add_ang_pt(ssf *ssf, double x, double y);
/* Return the position of the corner line of a simple size function.
 * @return the value of the corner line
 */
double ssf_get_corner_line(ssf *ssf);
/* Return max of measuring function (should be MAX_SIZE_TYPEVAL in the legacy
 * implementation)
 * @return the value of the maximum of the measuring function
 */
double ssf_get_max_measuring_function(ssf *ssf);
/* Return the list of angular points in the function.
 * @return the the list of angular points in the function.
 */
const ang_pt *ssf_get_angular_points(ssf *ssf);
/* Return a simple size function of the size function sf at given index.
 * @param sf the size functition
 * @param index the index
 * @return the index-nt simple size function of sf. NULL if not exists.
 */
ssf *sf_get_ssf(const sf *sf, int index);
/* Return the number of simple size functions in the size function sf.
 * @param sf the size functition
 * @return the number of simple size function of sf.
 */
int sf_get_n_ssf(const sf *sf);
/* Return the number of angular points in the simple size function ssf.
 * @param ssf the simple size functition
 * @return the number of angular points simple size function of ssf.
 */
int ssf_get_n_ang_pt(const ssf *ssf);
/* Return x of angular point */
double ang_pt_x(const ang_pt *p);
/* Return y of angular point */
double ang_pt_y(const ang_pt *p);
/* Return next angular point */
const ang_pt *ang_pt_next(const ang_pt *p);
/* Return 0 if if the ssf a is the same of ssf b. !0 otherwise.
 * @param a first ssf
 * @paarm b second ssf
 * @return 0 if a==b !=0 othewise*/
int ssf_compare(const ssf *a,const ssf *b);
/* Copy the sf a .
 * @param a the sh to copy
 * @return a copy of a or NULL if some error occur*/
sf *sf_copy(const sf *a);
/* Return 0 if if the sf a is the same of sf b. !0 otherwise.
 * @param a first sf
 * @paarm b second sf
 * @return 0 if a==b !=0 othewise*/
int sf_compare(const sf *a,const sf *b);

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
void write_ang_pt(sf *sf, char *angout, int legacy);


/*Dump size function on std out. JUST for debugging */
void dump_sf(sf *sf);

#endif
