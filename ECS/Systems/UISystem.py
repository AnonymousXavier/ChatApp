from ECS.Components import EditTextComponent


def process(ui: dict, events: list):
    for event in events:
        match event["type"]:
            case "click":
                ui[event["id"]][EditTextComponent].editing = True
