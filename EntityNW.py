import networkx


class EntityNW(networkx.classes.DiGraph):

      
   def add_node(self, n, weight=1, attr_dict=None, **attr):
      'adds a node n to the graph with weight weight'
      if attr_dict == None:
          attr_dict = {}
      super(EntityNW, self).add_node(n, weight=weight, **attr)

   def add_nodes_from(self, nodes, weights):
      """
      add a list of nodes to the graph with corresponding weights(also a list)s.
      """
      assert len(nodes) == len(weights), 'you should have weights list as large as nodes list'
      index = 0
      while index < len(nodes):
         self.add_node(nodes[index], weights[index])
         index += 1
      
      
   
   def add_edge(self, u, v, attr_dict=None, **attr):
        """Add an edge between u and v.

        The nodes u and v will be automatically added if they are
        not already in the graph.

        Edge attributes can be specified with keywords or by providing
        a dictionary with key/value pairs.  See examples below.

        Ensures no cycle are introduced in the graph.
        
        Parameters
        ----------
        u,v : nodes
            Nodes can be, for example, strings or numbers.
            Nodes must be hashable (and not None) Python objects.
        attr_dict : dictionary, optional (default= no attributes)
            Dictionary of edge attributes.  Key/value pairs will
            update existing data associated with the edge.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        """
        # set up attribute dict
        if attr_dict is None:
            attr_dict=attr
        else:
            try:
                attr_dict.update(attr)
            except AttributeError:
                raise NetworkXError(\
                    "The attr_dict argument must be a dictionary.")
        # add nodes
        if u not in self.succ:
            self.succ[u]={}
            self.pred[u]={}
            self.node[u] = {}
        if v not in self.succ:
            self.succ[v]={}
            self.pred[v]={}
            self.node[v] = {}
        # add the edge
        datadict=self.adj[u].get(v,{})
        datadict.update(attr_dict)
        self.succ[u][v]=datadict
        self.pred[v][u]=datadict
        
        # make sure it's a DAG        
        try:
            networkx.topological_sort(self)         
        except networkx.NetworkXUnfeasible:
            self.remove_edge(u,v)
            raise networkx.NetworkXUnfeasible("Graph contains a cycle! DAG is acyclic!")


   def add_edges_from(self, ebunch, attr_dict=None, **attr):
        """Add all the edges in ebunch.
        Parameters
        ----------
        ebunch : container of edges
            Each edge given in the container will be added to the
            graph. The edges must be given as as 2-tuples (u,v) or
            3-tuples (u,v,d) where d is a dictionary containing edge
            data.
        attr_dict : dictionary, optional (default= no attributes)
            Dictionary of edge attributes.  Key/value pairs will
            update existing data associated with each edge.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.

        Enusres No cycles are in this directed graph (DAG)
      
        """
        # set up attribute dict
        if attr_dict is None:
            attr_dict=attr
        else:
            try:
                attr_dict.update(attr)
            except AttributeError:
                raise NetworkXError(\
                    "The attr_dict argument must be a dict.")
        # process ebunch
        for e in ebunch:
            ne = len(e)
            if ne==3:
                u,v,dd = e
                assert hasattr(dd,"update")
            elif ne==2:
                u,v = e
                dd = {}
            else:
                raise NetworkXError(\
                    "Edge tuple %s must be a 2-tuple or 3-tuple."%(e,))
            if u not in self.succ:
                self.succ[u] = {}
                self.pred[u] = {}
                self.node[u] = {}
            if v not in self.succ:
                self.succ[v] = {}
                self.pred[v] = {}
                self.node[v] = {}
            datadict=self.adj[u].get(v,{})
            datadict.update(attr_dict)
            datadict.update(dd)
            self.succ[u][v] = datadict
            self.pred[v][u] = datadict

             # make sure it's a DAG        
            try:
               networkx.topological_sort(self)         
            except networkx.NetworkXUnfeasible:
               self.remove_edge(u,v)
               raise networkx.NetworkXUnfeasible("Graph contains a cycle! DAG is acyclic! Edge " + u + "-" + v +" cannot be added.")

  
              
   def lcs(self, node1, node2):

      def get_common(set1, set2):
         totalList1 = set1[0] + set1[1]
         totalList2 = set2[0] + set2[1]
         for e1 in totalList1:
            for e2 in totalList2:
               if e1 == e2:
                  return e1
         return None

      def process_get_pred(my_set):
         pred_list = []
         for e in my_set[1]:
            pred_list += self.pred[e].keys()
         return [my_set[0] + my_set[1], pred_list]

      def get_initial_pred(init_set):
         s = []
         for e in init_set:
            s += self.pred[e].keys()
         return s
            
            

      ## make node1 and node2 a list of nodes for base case for algorithm to work properly
      if(type(node1) and type(node2))!= list:
         node1 = [node1]
         node2 = [node2]
         node1 = [node1, get_initial_pred(node1)]  ## Make sure this works for multiple nodes
         node2 = [node2, get_initial_pred(node2)]  ## make sure this works for multiple nodes as well!
      ## algorithm actually starts here!
      predecessor_list = (node1, node2)
      print predecessor_list
      common = get_common(predecessor_list[0], predecessor_list[1])
      if(common != None): ## actuatlly found the common subsumer!, reveal it!
         return common
      else:
         if (node1[1] == [] and node2[1] == []):
            return None
         else:
            return self.lcs(process_get_pred(node1), process_get_pred(node2))
         


      
      
   def distance_metric(node1, node2):
       """Compute Distance Metric between two nodes in the network"""
       pass

   

  
        
if __name__ == "__main__":

   ## Test 1 
   g =  EntityNW()
   g.add_edges_from([('a','b'), ('a', 'c'), ('a','r'), ('x', 'c'), ('x', 'i'), ('b', 'd'), ('b', 'c'), ('d', 'f'), ('d', 'g') , ('d', 'e'), ('r', 'h'), ('r', 'i')\
                     ,('h', 'l'), ('l', 'm'), ('l', 'n'), ('i', 'k'), ('i', 'j')])

   ## Test 2
   net = EntityNW()
   net.add_edges_from([('entity', 'play'), ('entity', 'run'), ('entity', 'watch'), ('run', 'command'), ('run', 'marathon'), ('run', 'company')\
                       , ('watch', 'game'), ('game', 'PC game'), ('game', 'board game'), ('play', 'game'), ('play', 'PC game'), ('play', 'sport'), ('sport', 'marathon')\
                       , ('play', 'music'), ('play', 'instrument'), ('instrument', 'piano'), ('instrument', 'cello'), ('watch', 'sport'),('watch', 'tv'), ('tv', 'sport')])   
   
                       

