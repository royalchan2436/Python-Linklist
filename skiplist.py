"""An implementation of the Multiset ADT using a Skip List.
c2yaozhi, c2shenfu, c2chenro

Authors: Zhiyang Yao, Fujun Shen, Rongyao Chen
"""
import random


class TailNode(object):
    """ A TailNode object.
    """
    
    def __init__(self, down=None):
        """(TailNode) -> NoneType
        Initialize a TailNode object.
        """
        
        self.down = down
        self.skip = 0
        self.index = None  # initialize tailnode's index, which is only for
                           # the bottom level

    def __repr__(self):
        """(TailNode) -> str
        Return a string representation of this TailNode.
        """
        
        return ("TailNode({0})".format(repr(self.down)))
    
    
class HeadNode(TailNode):
    """ A HeadNode object used in SkipList.
    """
    
    def __init__(self, link=None, down=None):
        """(HeadNode) -> NoneType
        Initializes a HeadNode object.
        """
        
        TailNode.__init__(self, down)
        self.link = TailNode()
        self.skip = None 
        self.index = None
        
    def __repr__(self):
        """(HeadNode) -> str
        Return a string representation of this HeadNode object.
        """
        
        return ("HeadNode({0}, {1})".format(repr(self.link), repr(self.down)))
    
    def __str__(self):
        """(HeadNode) -> str
        Return the string representation of HeadNode.
        """
        arrow = '> '
        dash = ' -'
        s = ''
        temp = self
        
        while temp.link and type(temp.link) != TailNode:  
            x = temp.skip - 1  # skip num is 1, so theres no space btw next
                               # node so need skip num minus 1
            #skip each node needs 5 spaces
            s += dash + 5 * x * ' ' + arrow + str(temp.link.data) 
            temp = temp.link 
        #return elementnodes plus the arrow at the end
        return s + ' -' + (5 * (temp.skip - 1)) * ' ' + arrow
    
    def add(self, item):
        """(HeadNode, object) -> NoneType
        Add one occurence of item linked with this HeadNode.
        """
        
        #find the node before item
        temp = self._predecessor_head(item)
        
        #link item into this headnode
        temp.link = ElementNode(item, temp.link)
        
    def add_down(self, head):
        """(HeadNode, object) -> NoneType
        Connect this HeadNode with a Node downwards.
        """
        
        self.down = head
        
    def search(self, item):
        """(HeadNode, object) -> bool
        Return True if item is linked with this HeadNode.
        """

        if self.link and type(self.link) != TailNode:
            temp = self.link
        
            while temp.data != item:
                  
                if temp.link and type(temp.link) != TailNode:
                    temp = temp.link

                #if there no link or current node is tailnodefor current
                    #node, which means checked allnodes.
                else:
                    return False
            #if current node is equal to item
            return True
        
        return False
        
    def delete(self, item):
        """(HeadNode, object) -> NoneType
        Remove the item linked with this HeadNode, if the item exists.
        """
        #check whether it contains the node we are deleting
        if self.search(item) is True:
            temp = self
            #while it is not the item, then move to the next node
            while temp.link.data != item:
                temp = temp.link 

            temp.link = temp.link.link
        
    def _predecessor_head(self, item):
        
        # Helper method taken from official_skiplist.py by Francois Pitt
        # Modified to accomodate the HeadNode class.
        
        """(SkipList, object) -> _SkipNode
        Return a node p in this skip list such that:
         .  either p == self.head or p.data < item;
         .  either p.link == None, or p.link.data >= item.
        """
        
        p = self
        if type(p.link) == TailNode:
            return p
          
        #return the node before the item, else return headnode
        else:
            while p.link and p.link.data < item:
                if type(p.link.link) == TailNode:
                    return p.link
                else:
                    p = p.link
                
            return p

    def __iter__(self):
        """(HeadNode) -> NoneType
        Return an iterator for this HeadNode object. 
        """
        
        return _SkipIterHead(self)
        
    
class ElementNode(object):
    """ An Element Node in SkipList
    """
    
    def __init__(self, data, link=None, down=None):
        """(ElementNode, object, ElementNode, ElementNode) -> NoneType
        Initialize this node to store data and have next node link.
        """
        
        self.data = data
        self.link = link
        self.down = down
        self.skip = None  # The Initial Skip value is None
        self.index = None  # initialize tailnode's index, which is only for
                           # the bottom level
        
    def __repr__(self):
        """(ElementNode) -> str
        Return a string representation of this ElementNode, 
        for debugging purposes.     
        """
        
        return ("ElementNode({0}, \
{1}, {2})".format(repr(self.data), repr(self.link), repr(self.down)))
    
    def __lt__(self, other):
        """(ElementNode, ElementNode) -> bool
        Return True if the value of the data in this ElementNode is less than 
        the value of the data in the other ElementNode.
        """
        
        return self.data < other.data
    
    def __eq__(self, other):
        """(ElementNode, ElementNode) -> bool
        Return True if the value store in the other ElementNode equals to the 
        value store in this ElementNode.
        """
        
        return self.data == other.data


class SkipList(object):
    """ A Skiplist object
    """
    
    def __init__(self):
        """(SkipList) -> NoneType
        Initialize a skip list.
        """
        
        self.head = HeadNode()
        self.head.link = None  # The HeadNode at the top of the SkipList has 
                               # no TailNode.
        self.size = 0
        
    def insert(self, item):
        """(SkipList, object) -> NoneType
        Insert the item into this skip list. 
        """
            
        new_node = ElementNode(item)
        level = random_level()
        
        # First time of inserting item into the SkipList.
        
        if self.head.down is None:
            self.head.down = make_head(HeadNode(), level)
            for head in self:
                head.add(item)
            
        else:
        # Case 1 
        # The newly inserted node has levels less or equal to the number 
        # of original levels
            
            if level <= self.get_level():
                differ = self.get_level() - level 
                count = 0
                
                if differ == 0:  # If levels are the same.
                    temp = self.head
                    for head in self:
                        head.add(item)
                        
                elif differ != 0:
                    temp = self.head.down
                    while count < differ:
                        count += 1
                        temp = temp.down
                    i = 0
                    while i < level:
                        i += 1
                        temp.add(item)
                        temp = temp.down
                        
            # Case 2
            elif level > self.get_level():
                differ = level - self.get_level()  # of levels need to create.
                old = self.head.down
                self.head.down = make_head(HeadNode(), differ)  # Make levels.
                temp = self.head 
                while temp.down is not None:
                    temp = temp.down 
                    
                temp.add_down(old)  # Connect the old HeadNode 
                                    # to the new HeadNode.
                
                for head in self:
                    head.add(item)
            
        self.connect_down()
        self.fix_skip()
        set_index(self.head.down)
        self.size += 1

    def connect_down(self):
        """(SkipList) -> NoneType
        Connects all the elements in this SkipList together.
        """
        
        temp_down = self.head.down
        c = True
        #set 2 temps into current level and next level
        while temp_down.down and c:
            temp_1_right = temp_down.link
            temp_2_right = temp_down.down.link
            
            b = True
            #go through every node in upper level
            while temp_1_right and b:
                
                a = True

                #if equal to tailnode, then looking for tailnode in lower level
                #connct them
                if type(temp_1_right) == TailNode:
                    while temp_2_right and a:
                        if type(temp_2_right) == TailNode:
                            temp_1_right.down = temp_2_right
                            a = False
                        else:
                            temp_2_right = temp_2_right.link

                #connct other nodes except tailnodes                        
                else:
                    while temp_2_right and a:
                        if type(temp_2_right) != TailNode:
                            if temp_2_right == temp_1_right:
                                temp_1_right.down = temp_2_right
                                a = False  # exit while loop
                            else:
                                temp_2_right = temp_2_right.link
                                
                    #when connected one node, then move to the next node in
                    #lower level
                    temp_2_right = temp_2_right.link

                #stoped the upper level while loop, or move one node forward
                if type(temp_1_right) != TailNode:    
                    temp_1_right = temp_1_right.link
                else:
                    b = False
                    
            #stpped the headnode while loop, or move one headnode downward
            if temp_down.down.down: 
                temp_down = temp_down.down
                
            else:
                c = False

    def remove(self, item):
        """(SKipList, object) -> NoneType
        Remove the item from this SkipList, if it exists. 
        """
        
        for head in self:
            head.delete(item)
            
        self.fix_skip() 
        set_index(self.head.down)  # reset skip number and index number after
                                   # removing one node
        self.size -= 1

    def fix_skip(self):
        """(SkipList) -> NoneType
        Modify the skip value for all the nodes in this SkipList.
        """
        
        temp = self.head.down
        
        while temp and temp is not None:
            if type(temp.link) == TailNode:
                temp.skip = set_skip_helper(temp, TailNode())

            else:
                temp2 = temp  # Travel through the levels.
                while temp2 and type(temp2) != TailNode:
                    if type(temp2.link) != TailNode:
                        data = temp2.link.data
                        temp2.skip = set_skip_helper(temp2, data)

                    else:
                        temp2.skip = set_skip_helper(temp2, TailNode())

                    temp2 = temp2.link

            temp = temp.down  # Travel down the levels.

    def search(self, item):
        """(SkipList, object) -> bool
        Return True if the item is in this SkipList.
        """
        
        temp = self.head.down
        
        if not temp:  # Return False if the SkipList is empty
            return False
        
        while type(temp.link) == TailNode:  # Travel down the SkipList until 
                                            # reaches a non-empty level.
            if not temp.down: 
                return False
            
            else:
                temp = temp.down
        
        if temp.link.data == item: 
            return True
        
        else:
            # Go down each level if the value in the first element node in 
            # each level is greater than the item.
            
            while temp.link.data > item:                
                if temp.down:
                    temp = temp.down
                    
                else:
                    return False
            
            pre = find(temp, item)  # The predecessor of the item.
            
            while type(pre) != bool:
                if pre.down:
                    pre = find(pre.down, item)
                
                # The following is the situation where the predecessor is at 
                # the bottom level of the skiplist, where the predecessor node
                # has no other ElementNode connected down.
                
                elif pre.link and pre.down is None:
                    temp = pre
                    
                    while type(temp) != TailNode:
                        if temp.data == item:
                            return True
                        temp = temp.link
                            
                    return False
                
            return True
          
    def __len__(self):
        """(SkipList) -> int
        Return the length of the bottom level of this SkipList.
        """
        
        return self.size
      
    def get_level(self):
        """(SkipList) -> int
        Return the number of levels this skiplist currently has.
        """
        
        return get_level_helper(self.head)
    
    def __getitem__(self, item):
        """(SkipList, object) -> object or NoneType
        Return the item in this SkipList given its index. 
        """
        
        temp = self.head.down
        max_index = get_max_index(self)

        #if item's index is not in range of skiplist's index, then do nothing
        if item >= max_index or item <= -1:
            return None
    
        while temp:
            index = get_index(temp)
            #if sum of index and skip greater than item, then going down
            if index + (temp.skip) > item:
                temp = temp.down

            #if sum of index and skip smaller than item, then going right
            elif index + (temp.skip) < item:
                temp = temp.link

            #if sum of index and skip equal to item, then return next node
            elif index + (temp.skip) == item:
                
                return temp.link.data
   
    def __contains__(self, item):
        """(SkipList, item) -> bool
        Return True if this skiplist contains the item.
        """
        
        return self.search(item) 

    def __str__(self):
        """(SkipList) -> str
        Print the SkipList
        """
        
        s = '' 
        temp = self.head.down
        while temp:
            if not temp.down:  # If at the bottom level, no new line is made.
                s += str(temp)  

            else:
                s += str(temp) + '\n'

            temp = temp.down

        return s               
            
    def __iter__(self):
        """(SkipList) -> _SkipIter
        Return an iterator object over this skip list. 
        The iterator iterate through the HeadNodes.
        """
        
        return _SkipIter(self.head)

    
def make_head(root, count):
    """ (HeadNode, int) -> HeadNode
    Return number "count" of HeadNodes linked together. 
    """
    
    # Return a series of HeadNodes linked together.
    # Use of Recursion
    
    if root and count == 1:
        return root 
    
    if not root and count == 1:
        root = HeadNode()
        
    else:
        root = HeadNode()
        root.down = make_head(root.down, count - 1)
        
    return root 
        

def random_level():
    """(NoneType) -> int
    Keep generating a new number between 0 and 1, until the number is strictly
    greater than 0.5. Return the number of times the number generated is less 
    than 0.5.
    """
    
    p = 0.5
    count = 1
    r = random.random()  # Generate a radom number between 0 and 1.
    while r < p:
        count += 1
        r = random.random()
        
    return count  # Return number of times which the random number is strictly 
                  # less than 0.5, which becomes the levels. 

                  
def set_skip_helper(root, item):
    """(object, object or int) -> int
    Return the distance between root and the item, which is a node within 
    the SkipList.
    """
    
    count = 1
    temp = root

    #going to the bottom level
    while temp.down:
        temp = temp.down

    #if item's link is tailnode, then return 1
    if type(temp.link) == TailNode:
        return count

    #find root and item distance in bottom level
    elif type(item) == TailNode:
        while type(temp.link) != TailNode:
            count += 1
            temp = temp.link
            
        return count

    else:
        while type(temp.link) != TailNode:
            if temp.link.data == item:
                return count
            
            else:
                count += 1
                temp = temp.link
               
        return count

    
def find(root, item):
    """(ElementNode, object) -> bool or ElementNode.
    Return True if the root contains the item, else return the predecessor for
    the item 
    """
    
    # Suppose the string representation for a root looks like the following
    # -> 1 -> 2 -> 3 -> 
    # if called find(root, 2.5)
    # The return value will be ElementNode(2, ElementNode(3, ... 
    
    new_node = ElementNode(item)
    temp = root.link
    if type(temp) != TailNode:
        if temp is None:
            return False
        
        else:
            if type(temp.link) == TailNode:
                if temp == new_node:
                    return True
                
            while type(temp.link) != TailNode:
                if temp == new_node or temp.link == new_node:
                    return True
                
                elif temp < new_node and temp.link < new_node:
                    temp = temp.link
        
                else:
                    return temp
                
            return temp
        
    return root
         

def get_level_helper(head):
    """(HeadNode) -> int
    Return the number of heads rooted at this HeadNode. If there is no HeadNode
    rooted at head, return 0.
    """
    #the helper function which couting number of levels does skiplist have
    count = 0
    
    if head is None:
        return 0
    
    elif not head.down:
        return 0
    
    else:
        count += 1
        count += get_level_helper(head.down)
        
    return count 


def set_index(root):
    '''(HeadNode) -> NoneType
    Set the index of the bottom level
    '''
    temp = root
    count = -1
    a = True
    while temp.down:
        temp = temp.down
    while temp and a:
        #set temp.link is tailnode, then tailnode's index is temp's index
        #plus 1
        if type(temp) == TailNode:
            temp.index = (count + 1)
            a = False
        #set index from '-1', and plus 1 for next node
        else:
            temp.index = count
            count += 1
            temp = temp.link

            
def get_index(root):
    '''(Object) -> int
    Return the index of current Node.
    '''
    #going to bottom level and return root's index
    temp = root
    
    while temp.down:
        temp = temp.down
        
    return temp.index


def get_max_index(root):
    """(object) -> int
    """
    
    temp = root.head.down
    
    while temp.down:
        temp = temp.down
    
    while type(temp) != TailNode:
        temp = temp.link
    
    return temp.index - 1  # The index of the TailNode - 1.
      

#The following class is taken from official_skiplist.py by Francois Pitt.
class _SkipIter(object):  # "private" class because name starts with _
    """An iterator (allowing the use of for-loops) for skip lists.
    """

    def __init__(self, start):
        """(_SkipIter, _SkipNode) -> NoneType
        Initialize this iterator with node start, a header node that does not
        store an actual skip list element.
        """
        self.current = start

    def __iter__(self):
        """(_SkipIter) -> _SkipIter
        Return this iterator, as required for iterator objects.
        """
        return self

    def __next__(self):
        """(_SkipIter) -> object
        Return the next item for this iterator, if there is one. Raises
        StopIteration if this is none.
        """
        if not self.current.down:
            raise StopIteration()
        self.current = self.current.down
        
        return self.current              
    
    
class _SkipIterHead(object):  # Iterator used in class Headnode()
                              # Code modified based on class _SkipIter(object)
                              # by Francois Pitt. 
    
    """ An iterator (allowing the use of for-loops) for headNodes.
    """

    def __init__(self, start):
        """(_SkipIter, _SkipNode) -> NoneType
        Initialize this iterator with node start, a header node that does not
        store an actual skip list element.
        """
        self.current = start

    def __iter__(self):
        """(_SkipIter) -> _SkipIter
        Return this iterator, as required for iterator objects.
        """
        return self

    def __next__(self):
        """(_SkipIter) -> object
        Return the next item for this iterator, if there is one. Raises
        StopIteration if this is none.
        """
        if type(self.current) == TailNode:  # Stop the for-loop once reaches
                                            # a TailNode. 
            raise StopIteration()
        
        elif not self.current.link:
            raise StopIteration()
        
        self.current = self.current.link
        
        return self.current

    
