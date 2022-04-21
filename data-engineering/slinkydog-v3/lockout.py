import os

### Configurable Parameters ###

_lock_file = "py.lock"

### Program Lockout Mechanism ###

lock_file = _lock_file

def lock(verbose = False):
    try:
        open(lock_file, "w").close()
    except:
        raise RuntimeError("Lockout File Could Not Be Created.")
    if verbose: print("Lockout File Created.")
    return None
    
def unlock(verbose = False):
    if os.path.exists(lock_file):
        os.remove(lock_file)
        if verbose: print("Lockout File Removed.")
    else:
        if verbose: print("No Lockout File Found.")
    return None

def islocked(hault=False, verbose=False):
    if os.path.exists(lock_file):
        if verbose: print("WARNING: Lockout found.")
        if hault: raise RuntimeError("Program is locked out to prevent execution.")  #Stop program by erroring out
        return True
    else:
        if verbose: print("No lockout found.")
        return False
    return None
