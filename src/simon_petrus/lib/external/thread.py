# Performing multithreading that can return the function's return value/result
# - Most comments have been truncated from the original GitHub repo in order to
#   reduce file size and declutter the code outlook
# - The logging is disabled
# SOURCE: https://github.com/shailshouryya/save-thread-result

# MIT License
#
# Copyright (c) 2023 Shail Shouryya
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import threading

class _runOverrideThreadWithResult(threading.Thread):
    
    def run(self):
        '''
        Method representing the thread's activity that is overriden to
        save the result of a thread (if the thread completes) in the
        `result` attribute of the instance.

        This is the only change to the functionality of the `run` method.
        This method still invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the `args` and `kwargs` arguments, respectively.
        '''
        
        # uses the try/finally blocks for consistency with the CPython implementation:
        # https://github.com/python/cpython/blob/89ac665891dec1988bedec2ce9b2c4d016502a49/Lib/threading.py#L987
        try:
            if self._target is not None:
                self.result = self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs

ThreadWithResult = _runOverrideThreadWithResult
