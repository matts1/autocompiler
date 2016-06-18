class ErrorReporter(object):
    def __init__(self, stage: str):
        self.num_errors = 0
        self.stage = stage

    def report(self, message: str, fatal: bool=False):
        print(message)
        self.num_errors += 1
        if fatal: self.stop_on_err()

    def stop_on_err(self):
        if self.num_errors > 0:
            print('Compilation failed')
            exit(1)
        else:
            print(self.stage, 'complete')