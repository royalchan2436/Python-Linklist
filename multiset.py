"""Implementation of the Multiset ADT.
c2yaozhi, c2shenfu, c2chenro

Modified By: Zhiyang Yao, Fujun Shen, Rongyao Chen
Original Author: Francois Pitt, February 2013.
"""

##from official_skiplist import SkipList
from skiplist import SkipList 
from skiplist import TailNode
from skiplist import HeadNode


class MultiSet(object):
    """A multiset is like a set where the number of repetitions of elements
    matters. This implementation uses SkipLists so it is limited to store
    elements that can be compared with each other.
    """
    
    def __init__(self):
        """(MultiSet) -> NoneType
        Initialize this MultiSet to be empty.
        """
        self.skiplist = SkipList()
    
    def __repr__(self):

        # Efficiency: O(n)
        
        """(MultiSet) -> str
        Return a string representation of this MultiSet.
        """
        r = ""
        head = self.travel_down()
            
        for e in head:
            if type(e) != TailNode:
                r += str(e.data) + ", "
            
        return "MultiSet([" + r[:-2] + "])"
    
    def insert(self, elem):
        """(MultiSet, object) -> NoneType
        Add one occurrence of element elem to this MultiSet.
        """
        # Call insert function form skiplist
        self.skiplist.insert(elem)
    
    def remove(self, elem):
        """(MultiSet, object) -> NoneType
        Remove one occurrence of element elem from this MultiSet.
        """
        # Efficiency: O(n)
        # Call remove function from skiplist
        self.skiplist.remove(elem)
    
    def clear(self):
        """(MultiSet) -> NoneType
        Remove all elements from this MultiSet.
        """
        # No need to actually "remove" anything: unused memory will be
        # reclaimed automatically.
        
        self.skiplist = SkipList()
    
    def __contains__(self, elem):
        """(MultiSet, object) -> bool
        Return True iff element elem belongs to this MultiSet.
        """
        # Orginial Code has Efficiency O(n)
        # With the new SkipList, the efficiency O(log(n))
        
        return elem in self.skiplist
    
    def __len__(self):
        """(MultiSet) -> int
        Return the number of elements in this MultiSet.
        """
        return len(self.skiplist)

    def travel_down(self):
        """(MultiSet) -> HeadNode
        A helper function which return the bottom level of skiplist
        """
        #going to the bottom of skiplist
        temp = self.skiplist.head
        while temp.down:
            temp = temp.down

        return temp
    
    def count(self, elem):
        """(MultiSet, object) -> int
        Return the number of occurrences of element elem in this MultiSet.
        """
        
        temp = self.travel_down()
        count = 0
        #if e is equal to elem, then count plus 1
        for e in temp:
            if type(e) != TailNode and e.data == elem:
                count += 1

        return count
    
    def __eq__(self, other):
        """(MultiSet, MultiSet) -> bool
        Return True iff this MultiSet is equal to other.
        """
        # Two sets are equal iff they are subsets of each other.
        # The Efficiency is O(n)

        head = self.travel_down()
        head_1 = other.travel_down()
        
        return str(head) == str(head_1)
    
    def __le__(self, other):
        """(MultiSet, MultiSet) -> bool
        Return True iff this MultiSet is a subset of other.
        """
        # Check that the count of each element in self is no larger than the
        # count of the element in other.
        
        for e in self.skiplist:
            if self.count(e) > other.count(e):
                return False
            
        return True
    
    def __sub__(self, other):
        """(MultiSet, MultiSet) -> MultiSet
        Return the multiset difference between this MultiSet and other.
        """
        # __isub__ should always be called indirectly through the '-=' operator
        # but this is acceptable in implementation code.
        return self.copy().__isub__(other)
    
    def __isub__(self, other):
        """(MultiSet, MultiSet) -> MultiSet
        Make this MultiSet equal to self - other, in-place.
        """
        # Remove every element of other from this MultiSet.
        temp = other.travel_down()

        for e in temp:
            if type(e) != TailNode:
                self.remove(e.data)
        return self
    
    def __add__(self, other):
        """(MultiSet, MultiSet) -> MultiSet
        Return the multiset union between this MultiSet and other.
        """
        # Efficiency: O(n)
        return self.copy().__iadd__(other)
    
    def __iadd__(self, other):
        """(MultiSet, MultiSet) -> MultiSet
        Make this MultiSet equal to self + other, in-place.
        """
        # Add any additional elements in other to self.
        temp2 = other.copy()
        temp = self - other
        
        for i in temp.travel_down():
            if type(i) != TailNode:
                temp2.insert(i.data)
                
        self.skiplist = temp2.skiplist
        return self
    
    def __and__(self, other):
        """(MultiSet, MultiSet) -> MultiSet
        Return the multiset intersection between this MultiSet and other.
        """
        #Efficiency: O(n)
        return self.copy().__iand__(other)
    
    def __iand__(self, other):
        """(MultiSet, MultiSet) -> MultiSet
        Make this MultiSet equal to self & other, in-place.
        """
        # Remove any elements in self that are not also in other.
        temp = self - other
        
        for i in temp.travel_down():
            if type(i) != TailNode:
                self.remove(i.data)

        return self 
    
    def isdisjoint(self, other):
        """(MultiSet, MultiSet) -> bool
        Return True iff this MultiSet has no element in common with other.
        """
        # if there difference is not equal to self, then false
        #Efficiency: O(n)
        return (self - other) == self
    
    def copy(self):
        """(MultiSet) -> MultiSet
        Return a (shallow) copy of this MultiSet.
        """
        new_set = MultiSet()
        temp = self.travel_down()

        #put all elements in old skiplist's bottom level into new multiset
        for e in temp:
            if type(e) != TailNode:
                new_set.insert(e.data)
            
        return new_set
