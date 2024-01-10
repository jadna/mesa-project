from dataclasses import dataclass, field
import math


@dataclass
class Route:
    name: str
    time_min: int
    volume: int
    capacity: int
    betha: float = 4
    alpha: float = 2
    queue_exit: dict = (field(default_factory=lambda:{}))
    
    def reset(self):
        self.queue_exit = {}

    def time_out(self, step=0) -> float:

        time_out = step + self.time_min * (1 + (self.alpha*(self.volume/self.capacity)**self.betha))
        print(f"Time Out: {math.ceil(time_out)}")
        return math.ceil(time_out)

    def release_volume(self):
        self.volume -= 1
        

    def step(self, current_step):
        if current_step in self.queue_exit.keys():
            for id, event in self.queue_exit[current_step]:
                event()
            
            print(f"Release agent #{id} in {current_step} from {self.name}")

def main():
    #time_min, volume, capacity
    route = Route(1, 5, 7)
    route.time_out()


if __name__ == "__main__":
    main()
