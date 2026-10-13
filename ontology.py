from owlready2 import (get_ontology, Thing, ObjectProperty,
                       DataProperty, FunctionalProperty)

onto = get_ontology("http://wellness-coach.example/onto.owl")

with onto:
    # ---- Classes: the kinds of things in our world ----
    class Metric(Thing):
        pass

    class Action(Thing):
        pass

    # ---- Properties: facts we can state about them ----
    class improves(ObjectProperty):          # Action -> Metric
        domain = [Action]
        range = [Metric]

    class advice(DataProperty, FunctionalProperty):
        domain = [Action]
        range = [str]

    class time_cost_min(DataProperty, FunctionalProperty):
        domain = [Action]
        range = [int]

    class effort(DataProperty, FunctionalProperty):
        domain = [Action]
        range = [str]

    class day_type(DataProperty, FunctionalProperty):   # weekday / weekend / any
        domain = [Action]
        range = [str]

    class needs_anchor(DataProperty, FunctionalProperty):
        domain = [Action]
        range = [bool]

    class increases_intensity(DataProperty, FunctionalProperty):
        domain = [Action]
        range = [bool]

    # ---- Metrics: what the data can measure ----
    weeknight_sleep = Metric("weeknight_sleep")
    sleep_swing = Metric("sleep_swing")        # weekend sleep minus weeknight sleep
    daily_steps = Metric("daily_steps")
    weekday_steps = Metric("weekday_steps")
    weekend_steps = Metric("weekend_steps")

    # ---- Helper to add one allowed action ----
    def add(code, text, metrics, minutes, effort_level, day,
            anchor=False, intense=False):
        a = Action(code)
        a.advice = text
        a.improves = metrics
        a.time_cost_min = minutes
        a.effort = effort_level
        a.day_type = day
        a.needs_anchor = anchor
        a.increases_intensity = intense

    # ---- The allowed actions (the ONLY advice the app can give) ----
    add("A01", "Move your weeknight bedtime about 15 minutes earlier.",
        [weeknight_sleep], 0, "low", "weekday")
    add("A02", "Start winding down 20 minutes before your usual weeknight bedtime: screens down, lights low.",
        [weeknight_sleep], 20, "low", "weekday")
    add("A03", "Keep your weekend wake-up within about an hour of your weekday wake-up.",
        [sleep_swing], 0, "low", "weekend")
    add("A04", "Add 20 minutes of sleep to a few weeknights instead of one big weekend lie-in.",
        [weeknight_sleep, sleep_swing], 0, "low", "weekday")
    add("A05", "Extend a walk you already take by 5 to 10 minutes.",
        [daily_steps, weekday_steps], 10, "low", "weekday", anchor=True)
    add("A06", "Take a 10-minute walk right after a meal you already eat at a regular time.",
        [daily_steps], 10, "low", "any")
    add("A07", "Take phone calls or listen to a podcast while walking.",
        [daily_steps], 10, "low", "any")
    add("A08", "Pick one weekend slot, even 15 minutes, and pair a walk with something you already do, like errands or coffee.",
        [weekend_steps], 15, "low", "weekend")
    add("A09", "Walk or take the stairs for one short trip you would normally drive or take the elevator for.",
        [daily_steps], 5, "low", "any")
    add("A10", "Add a brisk-pace stretch to a walk you already take.",
        [daily_steps], 10, "moderate", "any", anchor=True, intense=True)


def get_actions():
    """Return every action as a plain Python dict."""
    out = []
    for a in sorted(Action.instances(), key=lambda x: x.name):
        out.append({
            "id": a.name,
            "advice": a.advice,
            "improves": [m.name for m in a.improves],
            "time_cost_min": a.time_cost_min,
            "effort": a.effort,
            "day_type": a.day_type,
            "needs_anchor": a.needs_anchor,
            "increases_intensity": a.increases_intensity,
        })
    return out


if __name__ == "__main__":
    for act in get_actions():
        print(act["id"], act["improves"], act["day_type"], "-", act["advice"])
    onto.save(file="wellness.owl")
    print("Saved wellness.owl")

    