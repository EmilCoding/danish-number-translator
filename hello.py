from flask import Flask, render_template, request
from number import NumberTooBig, get_number_name_danish
from typing import Literal

app = Flask('Danish number translator')


@app.route("/", methods=["GET", "POST"])
def index():
    value = ""
    result = ""
    error = ""
    seperator = "space"
    et_before_hundred = True
    et_before_thusind = True
    og_between_large_powers = False
    conjugate_large_power = True

    if request.method == "POST":
        value = handle_raw_input(request.form.get("number", ""))
        seperator = request.form.get("seperator", "space")
        et_before_hundred = request.form.get("et_before_hundred", "yes") == "yes"
        et_before_thusind = request.form.get("et_before_thusind", "yes") == "yes"
        og_between_large_powers = request.form.get("og_between_large_powers", "no") == "yes"
        conjugate_large_power = request.form.get("conjugate_large_power", "yes") == "yes"

        if not value:
            error = "Please enter a positive integer."
        else:
            try:
                if value < 0:
                    raise ValueError('Negative')
                result = get_number_name_danish(
                    value,
                    seperator=get_separator(seperator),
                    et_before_hundred=et_before_hundred,
                    et_before_thusind=et_before_thusind,
                    og_between_large_powers=og_between_large_powers,
                    conjugate_large_power=conjugate_large_power,
                )
            except ValueError:
                error = "Please enter a valid positive integer."
            except NumberTooBig:
                error = "That number is too large. Enter a smaller positive integer."

    return render_template(
        "index.html",
        value=value,
        result=result,
        error=error,
        seperator=seperator,
        et_before_hundred=et_before_hundred,
        et_before_thusind=et_before_thusind,
        og_between_large_powers=og_between_large_powers,
        conjugate_large_power=conjugate_large_power,
    )


def handle_raw_input(raw: str) -> None | int:
    try:
        value = int(raw.strip())
    except ValueError:
        return None
    return value


def get_separator(signature: str) -> Literal["", " ", "-"]:
    match signature.lower():
        case "none":
            return ""
        case "space":
            return " "
        case "hyphen":
            return "-"
        case _:
            raise ValueError(f"Unknown seperator: {signature}")


if __name__ == "__main__":
    app.run(debug=True)
