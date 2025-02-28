class HRGenericBase:
    def __init__(self):
        self.M = {r: {"assigned": None} for r in self.residents} | {
            h: {"assigned": set()} for h in self.hospitals
        }
        self.full_hospitals = set()
        self.all_stable_matchings = []

        # This lets us order residents in the stable matching by number.
        # We cannot use 'sorted' without this key because that uses lexial order.
        self.resident_order_comparator = lambda r: int(r[1:])

    def hospital_is_full(self, h):
        return self.hospitals[h]["capacity"] == len(self.M[h]["assigned"])

    def save_matching(self):
        stable_matching = {"resident_sided": {}, "hospital_sided": {}}
        for resident in self.residents:
            if self.M[resident]["assigned"] is None:
                stable_matching["resident_sided"][resident] = ""
            else:
                stable_matching["resident_sided"][resident] = self.M[resident][
                    "assigned"
                ]
        for hospital in self.hospitals:
            stable_matching["hospital_sided"][hospital] = sorted(
                self.M[hospital]["assigned"], key=self.resident_order_comparator
            )
        self.minmax_matchings.append(stable_matching)

    def has_stability(self) -> bool:
        # Link to problem description
        raise NotImplementedError("Enumerators need to link to a stability definition.")

    def resident_trial_order(self, resident) -> str:
        # generator for an order of hosptials in preference list
        raise NotImplementedError("Enumerators need to describe the order of matching.")

    def hospital_trial_order(self, hospital) -> str:
        # generator for an order of hosptials in preference list
        raise NotImplementedError("Enumerators need to describe the order of matching.")
