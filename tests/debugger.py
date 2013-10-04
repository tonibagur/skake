import sys

raise "The debugger must not be active!"

'''Exemple d'us funció _init
      def _init_pieces(self):
          for i,v in enumerate(self.b):
              self.pieces[color(v)].add(i)
              self.pieces[v].add(i)
              import tests.debugger
              tests.debugger.predicates.append(lambda:63 not in self.pieces[True])
              tests.debugger.predicates.append(lambda:40 not in self.pieces[13])
'''
predicates=[]

def trace_it(frame,event,arg):
    for p in predicates:
        if p():
            print "line:",frame.f_lineno
            co=frame.f_code
            print "file:",co.co_filename
            import pdb
            pdb.set_trace()  
    return trace_it

sys.settrace(trace_it)