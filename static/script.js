const samples = {
    basic: `safe p;
safe roksi;
p = 10;
roksi = p + 5;
ebas roksi;`,

    input: `safe p;
sah p;
ebas p;`,

    math: `safe x;
x = (2 + 3) * 4;
ebas x;`,

    error: `safe p;
roksi = p + 5;
ebas roksi;`
};

function extractInputVariables(code) {
    const matches = [...code.matchAll(/\bsah\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;/g)];
    return matches.map(match => match[1]);
}

function generateInputFields() {
    const code = document.getElementById("code").value;
    const inputFieldsContainer = document.getElementById("input-fields");
    const inputArea = document.getElementById("input-area");

    const variables = extractInputVariables(code);
    inputFieldsContainer.innerHTML = "";

    if (variables.length === 0) {
        inputArea.style.display = "none";
        return;
    }

    inputArea.style.display = "block";

    variables.forEach((variable, index) => {
        const wrapper = document.createElement("div");
        wrapper.className = "input-field-group";

        const label = document.createElement("label");
        label.textContent = `${variable}`;
        label.setAttribute("for", `input-${index}`);

        const input = document.createElement("input");
        input.type = "number";
        input.id = `input-${index}`;
        input.className = "program-input";
        input.placeholder = `Enter integer for ${variable}`;

        wrapper.appendChild(label);
        wrapper.appendChild(input);
        inputFieldsContainer.appendChild(wrapper);
    });
}

function loadSample(type) {
    document.getElementById("code").value = samples[type];
    document.getElementById("output").className = "output-neutral";
}

function runCode() {
    const code = document.getElementById("code").value;
    const output = document.getElementById("output");
    const variables = extractInputVariables(code);

    let inputs = [];
    for (let i = 0; i < variables.length; i++) {
        const value = document.getElementById(`input-${i}`)?.value ?? "";

        if (value.trim() === "") {
            output.innerText = `Execution failed.\n\nMissing input for '${variables[i]}'.`;
            return;
        }

        inputs.push(value);
    }

    output.innerText = "Running...";

    fetch("/run", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ code, inputs })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            output.className = "output-success";
            output.innerText = "Execution successful.\n\n" + data.output;
        } else {
            output.className = "output-error";
            output.innerText = "Execution failed.\n\n" + data.output;
        }
    })
    .catch(err => {
        output.innerText = "Execution failed.\n\nError: " + err;
    });
}

window.onload = generateInputFields;