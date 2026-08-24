"""Flask web app entry point for the Danish number translator.

This module defines the web UI and form handling logic for converting
integer input into Danish number names using the core translator in
``danishnumbers.number``.
"""
from typing import Literal
from flask import Flask, render_template, request
from danishnumbers.number import NumberTooBig, get_name


app = Flask('Danish number translator')


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the main page and handle number translation form submissions.

    On GET requests, the form is shown with default options. On POST requests,
    the submitted number and formatting options are validated and passed to
    ``get_number_name_danish``. Any validation or conversion errors are
    returned to the template as an error message.

    Returns:
        str: Rendered HTML for the index page.
    """
    value = ""
    result = ""
    error = ""
    seperator = "space"
    et_before_hundrede = True
    et_before_tusinde = True

    if request.method == "POST":
        value = handle_raw_input(request.form.get("number", ""))
        seperator = request.form.get("seperator", "space")
        et_before_hundrede = request.form.get("et_before_hundrede") == "yes"
        et_before_tusinde = request.form.get("et_before_tusinde") == "yes"

        if value is None:
            error = "Please enter a non-negative integer."
        elif value < 0:
            error = "Please enter a valid non-negative integer."
        else:
            try:
                result = get_name(
                    value,
                    seperator=get_separator(seperator),
                    et_before_hundrede=et_before_hundrede,
                    et_before_tusinde=et_before_tusinde,
                )
            except NumberTooBig:
                error = "That number is too large. Enter a smaller non-negative integer."

    return render_template(
        "index.html",
        value=value,
        result=result,
        error=error,
        seperator=seperator,
        et_before_hundrede=et_before_hundrede,
        et_before_tusinde=et_before_tusinde,
    )


def handle_raw_input(raw: str) -> None | int:
    """Parse raw form input into an integer.

    Args:
        raw (str): Raw user input from the HTML form.

    Returns:
        int | None: Parsed integer value, or None if parsing fails.
    """
    try:
        value = int(raw.strip())
    except ValueError:
        return None
    return value


def get_separator(signature: str) -> Literal["", " ", "-"]:
    """Convert a separator option name to its literal string value.

    Args:
        signature (str): One of ``none``, ``space``, or ``hyphen``.

    Returns:
        str: The separator string used to join Danish word parts.

    Raises:
        ValueError: If the signature is not a recognized separator option.
    """
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
    app.run(debug=False)
