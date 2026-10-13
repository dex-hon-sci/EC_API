from typing import Protocol, Iterator
import math
import random

class SourceTape(Protocol):
    def __init__(self, seed:int, s: int, scale: float, *args: float):...
    def update_params(self, *args: float) -> None:...
    def replay(self) -> Iterator[int]: ...


class GBMTape(SourceTape):
    # Geometric Brownian Motion
    def __init__(self, seed: int, s: int, scale: float, mu: float, sigma:float):
        self._seed: int = seed
        self._start_s: int = s
        self.scale: float = scale
        self.params: dict[str, float] = {'mu': mu, 'sigma': sigma}
    
        self.R = random.Random(self._seed)
        
    def _next_num(self, s_t) -> float:
        # \(dS(t)=\mu S(t)\,dt+\sigma S(t)\,dW(t)\)
        # the close form solution
        dt = 1   
        Z = self.R.gauss(0,1)
        s_t *= math.exp((self.params['mu'] - 0.5*self.params['sigma']**2)*dt + self.params['sigma']*math.sqrt(dt)*Z)
        return s_t
   
    def update_params(self, new_mu: float, new_sigma:float) -> None:
        self.params['mu'] = new_mu
        self.params['sigma'] = new_sigma
        
    def replay(self) -> Iterator[int]:
        s_t = self._start_s*self.scale
        while True:
            s_t = self._next_num(s_t)
            yield int(s_t)
    
        