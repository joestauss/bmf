from time import sleep

class PatientThreadManager:
    def __init__( self, threads):
        self.threads = threads

    def __call__(self, VERBOSE=False):
        if VERBOSE:
            self.threads = tqdm(self.threads)
            threads.set_description( "Starting threads...")
        for thread in threads:
            thread.start()
            sleep(0.1)
        if VERBOSE:
            self.threads = tqdm(self.threads)
            n = len( self.threads)
            i = 0
        for thread in threads:
            if VERBOSE:
                i = i + 1
                threads.set_description( "Waiting for thread {i} of {n}")
            thread.join()
