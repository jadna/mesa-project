from dataclasses import dataclass, field


@dataclass
class Route:
    time_min: int
    volume: int
    capacity: int
    betha: float = 4
    alpha: float = 2
    queue_exit: dict = (field(default_factory=lambda:{}))
    

    def time_out(self, step=0) -> float:

        time_out = step + self.time_min * (1 + (self.alpha*(self.volume/self.capacity)**self.betha))
        print(f"Time Out: {time_out}")
        return time_out


def main():
    #time_min, volume, capacity
    route = Route(1, 5, 7)
    route.time_out()


if __name__ == "__main__":
    main()
