import unittest
import random
import types
import pickle

from zen import *

class DiGraphPickleTestCase(unittest.TestCase):
	
	def test_basic(self):
		G = DiGraph()
		G.add_edge(1,2)
		G.add_edge(2,3)
		G.add_edge(3,1)
		
		pstr = pickle.dumps(G)
		
		G2 = pickle.loads(pstr)
		assert G2.has_edge(1,2)
		assert G2.has_edge(2,3)
		assert G2.has_edge(3,1)
		assert not G2.has_edge(1,3)
		
	def test_removal(self):
		G = DiGraph()
		G.add_edge(1,2)
		G.add_edge(2,3)
		G.add_edge(3,4)
		G.add_edge(4,5)
		G.rm_node(3)
		
		idx2 = G.node_idx(2)
		eidx45 = G.edge_idx(4,5)
		
		pstr = pickle.dumps(G)
		
		G2 = pickle.loads(pstr)
		assert len(G2) == 4
		assert G2.size() == 2
		assert G.node_idx(2) == idx2
		assert G.edge_idx(4,5) == eidx45
		
		# make sure things don't crash when we add a new node - are internal structures valid?
		G2.add_edge(5,6)
		
class DiGraphTestCase(unittest.TestCase):

	def test_add_nodes(self):
		G = DiGraph()
		G.add_nodes(10)
		
		self.assertEquals(len(G),10)
		
	def test_add_nodes_w_objects(self):
		G = DiGraph()
		G.add_nodes(10,lambda x:str(x))
		
		self.assertEquals(len(G),10)
		
		for n_,n in G.nodes_iter_(obj=True):
			self.assertEquals(str(n_),n)

	def test_compact2(self):
		G = DiGraph()
		G.add_edge(1,2)
		G.add_edge(2,1)
		G.add_edge(1,4)
		G.add_edge(4,4)
		
		G.rm_node(2)
		
		G.compact()
		
		self.assertEquals(G.in_degree(4),2)
		self.assertEquals(G.out_degree(4),1)
		self.assertTrue(G.has_edge(4,4))
		self.assertTrue(G.has_edge(1,4))
		self.assertEquals(G.edge_idx(4,4),1)
		self.assertEquals(G.edge_idx(1,4),0)

	def test_compact_nodes(self):
		G = DiGraph()
		G.add_edge(1,2)
		G.add_edge(2,3)
		G.rm_node(2)
		
		self.assertEquals(G.max_node_idx,2)
		G.compact()
		self.assertEquals(G.max_node_idx,1)
		
	def test_compact_edges(self):
		G = DiGraph()
		G.add_edge(1,2)
		G.add_edge(2,3)
		G.rm_edge(1,2)

		self.assertEquals(G.max_edge_idx,1)
		G.compact()
		self.assertEquals(G.max_edge_idx,0)
		
	def test_is_compact(self):
		G = DiGraph()
		G.add_edge(1,2)
		G.add_edge(2,3)
		G.add_edge(3,2)
		
		self.assertTrue(G.is_compact())
		
		G.rm_node(2)
		
		self.assertFalse(G.is_compact())
		
		G.add_edge(3,4)
		G.add_edge(1,4)
		
		self.assertFalse(G.is_compact())
		
		G.add_edge(4,1)
		
		self.assertTrue(G.is_compact())
		
	def test_selfloop(self):
		G = DiGraph()
		G.add_edge(1,1)
		G.add_edge(2,2)
		G.add_edge(3,3)
			
	def test_adj_matrix(self):
		G = DiGraph()
		G.add_edge(0,1)
		G.add_edge(1,2)
		G.add_edge(2,2)
		
		M = G.matrix()
		
		self.assertEquals(M[0,0],0)
		self.assertEquals(M[0,1],1)
		self.assertEquals(M[0,2],0)
		self.assertEquals(M[1,0],0)
		self.assertEquals(M[1,1],0)
		self.assertEquals(M[1,2],1)
		self.assertEquals(M[2,0],0)
		self.assertEquals(M[2,1],0)
		self.assertEquals(M[2,2],1)
		
	def test_node_removal_nodes_(self):
		
		graph = DiGraph()
		graph.add_edge(1,2)
		graph.add_edge(3,2)
		graph.add_edge(3,4)
		graph.add_edge(3,6)
		nset1 = set(graph.nodes_())
		graph.rm_node_(2)
		nset2 = set(graph.nodes_())
		
		nset1.remove(2)
		
		self.assertTrue(4 in nset2)
		self.assertEqual(nset1,nset2)
		
	def test_max_indices(self):
		G = DiGraph()
		n1 = G.add_node()
		n2 = G.add_node()
		n3 = G.add_node()
		
		G.add_edge_(n1,n2)
		G.add_edge_(n2,n3)
		
		self.assertEqual(G.max_node_idx,2)
		self.assertEqual(G.max_edge_idx,1)
		
	def test_recycle_node_indices(self):
		G = DiGraph(node_capacity=5)
		for i in range(5):
			G.add_node(i)
			
		for i in range(5):
			G.rm_node(i)
			
		for i in range(5):
			G.add_node(i)
		
		self.assertEqual(G.node_capacity,5)
	
	def test_recycle_edge_indices(self):
		G = DiGraph(edge_capacity=5)

		G.add_edge(1,2)
		G.add_edge(1,3)
		G.add_edge(1,4)
		G.add_edge(1,5)
		G.add_edge(1,6)

		G.rm_edge(1,2)
		G.rm_edge(1,3)
		G.rm_edge(1,4)
		G.rm_edge(1,5)
		G.rm_edge(1,6)

		G.add_edge(1,2)
		G.add_edge(1,3)
		G.add_edge(1,4)
		G.add_edge(1,5)
		G.add_edge(1,6)

		self.assertEqual(G.edge_capacity,5)
		
	def test_reverse(self):
		G = DiGraph()
		G.add_edge(1,2)
		G.add_edge(2,3)
		G.add_node(4)
		
		G = G.reverse()
		
		self.assertTrue(4 in G)
		self.assertTrue(G.has_edge(2,1))
		self.assertFalse(G.has_edge(1,2))
		self.assertTrue(G.has_edge(3,2))
	
	def test_basicadding(self):
		G = DiGraph()
		n1 = G.add_node('hello')
		n2 = G.add_node('there')
		n3 = G.add_node('world')
		
		self.assertEqual(len(G),3)
		self.assertEqual(G.node_object(n1),'hello')
		self.assertEqual(G.node_object(n2),'there')
		self.assertEqual(G.node_object(n3),'world')
		self.assertEqual(G.node_data_(n3),None)
		
		# add by ids
		e1 = G.add_edge_(n1,n2)
		
		self.assertTrue(G.has_edge_(n1,n2))
		self.assertEqual(G.edge_idx_(n1,n2),e1)
		self.assertFalse(G.has_edge_(n1,n3))
		self.assertEqual(G.edge_data_(n1,n2),None)
		
		# check containment
		self.assertTrue('hello' in G)
		self.assertFalse('haloo' in G)
		
		# add by names
		e2 = G.add_edge('there','world')
		x,y = G.endpoints_(e2)
		
		self.assertEqual(x,n2)
		self.assertEqual(y,n3)
		self.assertTrue(G.has_edge_(n2,n3))
		self.assertEqual(G.edge_idx_(n2,n3),e2)
		self.assertEqual(G.edge_idx_(n2,n3),G.edge_idx('there','world'))
		
		# test degree
		self.assertEqual(G.degree_(n1),1)
		self.assertEqual(G.degree_(n2),2)
		self.assertEqual(G.in_degree_(n2),1)
		self.assertEqual(G.out_degree_(n2),1)
	
	def test_nodes(self):
		G = DiGraph()
		n1 = G.add_node('hello')
		G.add_edge('hello','there')
		G.add_edge('there','hello')
		
		self.assertEqual(type(G.nodes()),types.ListType)
		self.assertEqual(type(G.neighbors('hello')),types.ListType)
		self.assertEqual(len(G.neighbors('hello')),1)
	
	def test_nodes_(self):
		G = DiGraph()
		n1 = G.add_node('hello')
		G.add_edge('hello','there')
		G.add_edge('there','hello')
	
		self.assertEqual(len(G.neighbors_(n1)),1)
	
	def test_edge_removal(self):
		G = DiGraph()
		G.add_edge(1,2)
		G.add_edge(2,3)
		G.add_edge(3,4)
		
		self.assertEqual(G.size(),3)
		G.rm_edge(2,3)
		self.assertEqual(G.size(),2)
	
	def test_duplicate_edges(self):
		G = DiGraph()
		G.add_edge('1','2')
		success = False
		try:
			G.add_edge('1','2')
			success = True
		except Exception,e:
			if not str(e).startswith('Duplicate edges'):
				self.fail('Incorrect exception: %s' % str(e))
			
		self.assertFalse(success,'This call should have thrown an exception')
		
	def test_neighbors2(self):
		G = DiGraph()
		G.add_edge('hello','there')
		
		self.assertTrue('hello' in set(G.neighbors_iter('there')))
		
	def test_small_edge_insertion(self):
		G = DiGraph()
		
		for i in range(10):
			G.add_node()
		
		order = range(10)	
		order.remove(5)
		random.shuffle(order)
		
		for x in order:
			G.add_edge_(5,x)
			self.assertTrue(G.has_edge_(5,x))
			
		random.shuffle(order)
		for x in range(10):
			if x != 5:
				pass
			
		random.shuffle(order)
		for x in order:
			G.add_edge_(x,5)
	
		for x in range(10):
			if x != 5:
				self.assertTrue(G.has_edge_(x,5))
		
	def test_growing_nodearray(self):
		G = DiGraph(node_capacity=1)
		for i in range(10000):
			n = G.add_node(i)
			
	def test_growing_edgelistarray(self):
		G = DiGraph(edge_list_capacity=1)
		n0 = G.add_node('hello')
	
		for i in range(1000):
			n = G.add_node(i)
			G.add_edge_(n0,n)
			G.add_edge_(n,n0)
		
	def test_rm_node_edge(self):
		G = DiGraph()
		n1 = G.add_node()
		n2 = G.add_node('hello')
		n3 = G.add_node('foobar')
		
		e1 = G.add_edge_(n1,n2)
		e2 = G.add_edge_(n2,n3)
		e3 = G.add_edge_(n3,n1)
		
		G.rm_edge_(e3)
		
		self.assertFalse(G.has_edge_(n3,n1))
		self.assertTrue(G.has_edge_(n1,n2))
		self.assertTrue(G.has_edge_(n2,n3))
		self.assertFalse(G.has_edge_(n3,n2))
		
		self.assertEqual(G.degree_(n1),1)
		self.assertEqual(G.degree_(n2),2)
		
		G.rm_node_(n1)
		
		self.assertEqual(G.degree_(n2),1)
		self.assertEqual(G.degree_(n3),1)
		
	def test_node_iterator(self):
		G = DiGraph()
		for i in range(1000):
			G.add_node(i)
		
		count = 0
		for i,d in G.nodes_iter(data=True):
			count += 1
			
		self.assertEqual(count,1000)
		
	def test_edge_iterator(self):
		G = DiGraph()
		n1 = G.add_node()
		for i in range(1000):
			n = G.add_node()
			G.add_edge(n1,n)
			
		count = 0
		for x,y,d in G.edges_iter(data=True):
			count += 1
			
		self.assertEqual(count,1000)
		
	def test_edges(self):
		G = DiGraph()
		
		G.add_edge('x','y')
		E = G.edges()
		e1 = E[0]
		
		self.assertTrue('x' in set(e1))
	
	def test_grp_edge_iterators(self):
		G = DiGraph()
		n1 = G.add_node('n1')
		n2 = G.add_node()
		G.add_edge_(n1,n2)
		for i in range(10):
			n = G.add_node(i)
			G.add_edge_(n,n1)
			G.add_edge_(n2,n)
		
		# test total group iterators
		count = 0
		for eid in G.grp_edges_iter_([n1,n2]):
			count += 1
		
		self.assertEqual(count,21)
		
		# test the return of endpoints
		for x,y in G.grp_in_edges_iter(['n1']):
			self.assertEqual(y,'n1')
		
		# test the return of endpoints
		error_thrown = False
		try:
			for x,y in G.grp_out_edges_iter(['n1']):
				self.assertEqual(y,'n1')
		except:
			error_thrown = True
			
		self.assertTrue(error_thrown)
		
		# test indegree
		count = 0
		for eid in G.grp_in_edges_iter_([n1,n2]):
			count += 1
			
		self.assertEqual(count,11)
		
		# test outdegree
		count = 0
		for eid in G.grp_out_edges_iter_([n1,n2]):
			count += 1
			
		self.assertEqual(count,11)
		
	def test_grp_neighbor_iterators(self):
		G = DiGraph()
		n1 = G.add_node()
		n2 = G.add_node()
		G.add_edge_(n1,n2)
		for i in range(10):
			n = G.add_node()
			G.add_edge_(n,n1)
			G.add_edge_(n2,n)
	
		# test total group iterators
		count = 0
		for eid in G.grp_neighbors_iter_([n1,n2]):
			count += 1
	
		self.assertEqual(count,12)
	
		# test indegree
		count = 0
		for eid in G.grp_in_neighbors_iter_([n1,n2]):
			count += 1
	
		self.assertEqual(count,11)
	
		# test outdegree
		count = 0
		for eid in G.grp_out_neighbors_iter_([n1,n2]):
			count += 1
	
		self.assertEqual(count,11)
			
	def test_in_edge_iterator(self):
		G = DiGraph()
		n1 = G.add_node()
		for i in range(1000):
			n = G.add_node()
			G.add_edge_(n,n1)
			
		count = 0
		for i,d in G.in_edges_iter_(n1,data=True):
			count += 1
	
		self.assertEqual(count,1000)
		
	def test_out_edge_iterator(self):
		G = DiGraph()
		n1 = G.add_node()
		for i in range(1000):
			n = G.add_node()
			G.add_edge_(n1,n)
			
		count = 0
		for i,d in G.out_edges_iter_(n1,data=True):
			count += 1
			
		self.assertEqual(count,1000)
		
	def test_neighbor_iters(self):
		G = DiGraph()
		n1 = G.add_node('n1')
		n2 = G.add_node('n2')
		n3 = G.add_node('n3')
		n4 = G.add_node('n4')
		
		G.add_edge_(n1,n2)
		G.add_edge_(n1,n3)
		G.add_edge_(n4,n1)
		G.add_edge_(n2,n1)
		
		n1_in = set(G.in_neighbors_iter_(n1))
		n1_out = set(G.out_neighbors_iter_(n1))
		n1_all_raw = list(G.neighbors_iter_(n1))
		n1_all = set(n1_all_raw)
		
		self.assertEquals(n1_in,set([n4,n2]))
		self.assertEquals(n1_out,set([n2,n3]))
		self.assertEquals(n1_all,set([n2,n3,n4]))
		self.assertEquals(len(n1_all_raw),3)
		
	def test_neighbor_iter_recursionlimit(self):
		"""
		This tests an incorrect way that neighbor iter was implemented initially.
		"""
		G = DiGraph()
		n1 = G.add_node()
		for i in range(1100):
			n = G.add_node()
			G.add_edge_(n,n1)
			G.add_edge_(n1,n)
			
		count = 0
		for n in G.neighbors_iter_(n1):
			count += 1
			
		self.assertEquals(count,1100)
		
	def test_node_iterator_with_obj_and_data(self):
		G = DiGraph()
		G.add_node()
		G.add_node('there')

		for idx,nobj,data in G.nodes_iter_(obj=True,data=True):
			self.assertEqual(data,None)

	def test_edge_iterator_with_obj_and_data(self):
		G = DiGraph()
		G.add_edge(1,2)
		G.add_edge(2,3)

		for eidx,data in G.edges_iter_(data=True):
			self.assertEqual(data,None)

	def test_neighbor_iterator_with_obj_and_data(self):
		G = DiGraph()
		G.add_edge(1,2)
		G.add_edge(1,3)

		for x,nobj,data in G.neighbors_iter_(G.node_idx(1),obj=True,data=True):
			self.assertEqual(data,None)

	def test_neighbor_iterator_with_data(self):
		G = DiGraph()
		n1 = G.add_node('1')
		n2 = G.add_node()
		n3 = G.add_node('2')
		G.add_edge_(n1,n2)
		G.add_edge(n1,n3)

		success = True
		try:
			for nobj,data in G.neighbors_iter('1',data=True):
				self.assertEqual(data,None)
		except Exception, e:
			success = False
			self.assertTrue('does not have a node object' in str(e))

		self.assertFalse(success)
		
	def test_set_data(self):
		G = DiGraph()
		G.add_node(1,'hello')
		G.add_edge(1,2,'x')
		
		G.set_node_data(1,'there')
		G.set_edge_data(1,2,'y')
		
		self.assertEqual(G.node_data(1),'there')
		self.assertEqual(G.edge_data(1,2),'y')
		
	def test_weights(self):
		G = DiGraph()
		G.add_edge(1,2,weight=2)
		G.add_edge(1,3)
		G.set_weight(1,3,5)

		self.assertEqual(G.weight(1,2),2)
		self.assertEqual(G.weight(1,3),5)
		
	def test_edge_data(self):
		G = DiGraph()
		G.add_edge(1,2,1)
		G.add_edge(2,3)

		for e,data in G.edges_(data=True):
			pass
			
		for x,y,data in G.edges(data=True):
			pass
			
		n1 = G.add_node()
		n2 = G.add_node(3)
		G.add_edge_(n1,n2)

		success = True
		try:
			for x,y,data in G.edges(data=True):
				pass
		except Exception, e:
			if str(e).startswith('Edge'):
				success = False
				
		self.assertFalse(success)
		
		
	def test_modify_node_iterator(self):
		G = DiGraph()
		G.add_node(0)
		for i in range(1,100):
			G.add_node(i)
			G.add_edge(i,i-1)

		error = False
		try:	
			for n in G.nodes_iter():
				G.rm_node(n)
		except GraphChangedException:
			error = True

		self.assertTrue(error)

	def test_modify_edge_iterator(self):
		G = DiGraph()
		G.add_node(0)
		for i in range(1,100):
			G.add_node(i)
			G.add_edge(i,i-1)

		error = False
		try:	
			for n1,n2 in G.edges_iter():
				G.rm_edge(n1,n2)
		except GraphChangedException:
			error = True

		self.assertTrue(error)

	def test_modify_neighbor_iterator(self):
		G = DiGraph()
		G.add_node(0)
		for i in range(1,100):
			G.add_node(i)
			G.add_edge(0,i)

		error = False
		try:	
			for n in G.neighbors_iter(0):
				G.rm_node(n)
		except GraphChangedException:
			error = True

		self.assertTrue(error)
		
	def test_invalid_nidx(self):
		G = DiGraph()
		n1 = G.add_node(0)
		
		error = False
		try:
			G.node_data_(n1+1)
		except ZenException:
			error = True
			
		self.assertTrue(error)
		
	def test_edge_idx(self):
		G = DiGraph()
		n1 = G.add_node()
		n2 = G.add_node()
		e1 = G.add_edge_(n1,n2,'blah')
		
		self.assertEquals((e1,'blah'),G.edge_idx_(n1,n2,True))
		
	def test_has_edge(self):
		G = DiGraph()
		
		try:
			r = G.has_edge(1,2)
			self.assertFalse(r)
		except:
			self.fail('No error should be thrown')