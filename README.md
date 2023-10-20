# google_appengine_extensions

This involves some of the google_appengine related helper functions, that can be used for observability of function call ...etc.

1) Eventloop Tracer:
    @ELTracer decorator can be added to the top level method M1. 
    If this method M1 contains any asynchronous method calls, these asynchronous method's insertion and execution in the event loop will be logged.

  Ex:
  
    @ndb.tasklet
    def child_1_async():
        if False: yield None # generator func
        raise ndb.Return()
    
    @ndb.tasklet
    def child_2_async():
        qry = model.Person.query()
        ress =  yield qry.fetch_async() # RPC call func
        for res in ress:
            print res.name
        raise ndb.Return()
    
    @ndb.tasklet
    def test_parent_async():
        yield child_1_async()
        yield child_2_async()
        raise ndb.Return(None)

    @ELTracer()  
    def test_parent():
        test_parent_async().get_result()

    This will print all activity in the event loop

    SAMPLE OUTPUT:
    ----Added to queue: tasklet test_parent_async(final_main_script:115)
    $$$$$$$$ QUEUE: ['tasklet test_parent_async(final_main_script:115)'] $$$$$$$$
    ---executing: tasklet test_parent_async(final_main_script:115)
    $$$$$$$$ QUEUE: [] $$$$$$$$
    ----Added to queue: tasklet child_1_async(final_main_script:98)
    $$$$$$$$ QUEUE: ['tasklet child_1_async(final_main_script:98)'] $$$$$$$$
    ---executing: tasklet child_1_async(final_main_script:98)
    $$$$$$$$ QUEUE: [] $$$$$$$$
    ----Added to queue: on_future_completion running after: tasklet child_1_async(final_main_script:98)
    $$$$$$$$ QUEUE: ['on_future_completion running after: tasklet child_1_async(final_main_script:98)'] $$$$$$$$
    .
    .
    ,



    
    
