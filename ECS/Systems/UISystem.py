from ECS.Components import EditTextComponent


def process(ui: dict, events: list):
    for event in events:
        match event["type"]:
            case "click":
                if event["action"] == "edit_text":
                    ui[event["id"]][EditTextComponent].editing = True

                print(event["action"])
