from eventloop_tracer import ELTracer
from google.appengine.ext import ndb

@ndb.tasklet
def child_1_async():
    if False: yield None # generator func
    raise ndb.Return()
  
@ndb.tasklet
def child_2_async():
    '''qry = model.Person.query()
    ress =  yield qry.fetch_async()  # RPC call func
    for res in ress:
        print res.name'''
    if False: yield
    raise ndb.Return()

@ndb.tasklet
def test_parent_async():
    yield child_1_async()
    yield child_2_async()
    raise ndb.Return(None)
  
@ndb.tasklet
def test_parent_parallel_async():
    futs = [test_parent_async(), test_parent_async()]
    yield futs
    raise ndb.Return(None)

@ELTracer()  
def test_parent():
    test_parent_async().get_result()

@ELTracer() 
def test_parent_parallel_yield():
  test_parent_parallel_async().get_result()

print("Executing single Future object yield")
test_parent()

print("Executing parallel Future objects yield")
test_parent_parallel_yield()
  
