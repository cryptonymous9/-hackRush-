function add_tablet() {
    var w = document.getElementById('transition_container');
    var val = (parseInt(w.lastElementChild.getAttribute('name')) + 1).toString();
    var a = document.createElement("div");
    a.setAttribute('name', val);
    a.setAttribute('id', "tablet_" + val);
    a.classList.add("form-inline", "mb-3");
    var state = document.createElement("input");
    state.type = "text";
    state.placeholder = "Tablet/Drug Name";
    state.name = "tablet" + val;
    state.classList.add("form-control");
    a.appendChild(state);
    var sp = document.createElement("span");
    sp.innerText = " - ";
    sp.classList.add("ml-2", "mr-2");
    a.appendChild(sp);
    var next_state = document.createElement("input");
    next_state.type = "text";
    next_state.placeholder = "Dosage";
    next_state.name = "dosage" + val;
    next_state.classList.add("form-control");
    a.appendChild(next_state);
    var spa = document.createElement("span");
    spa.innerText = " - ";
    spa.classList.add("ml-2", "mr-2");
    a.appendChild(spa);
    var input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Quantity";
    input.name = "quantity" + val;
    input.classList.add("form-control");
    a.appendChild(input);
    var cancel = document.createElement("button");
    cancel.type = "button";
    cancel.innerText = "Delete";
    cancel.setAttribute('name', "tablet_" + val);
    cancel.setAttribute("onclick", "cancel('" + cancel.name + "')");
    cancel.classList.add("btn", "btn-danger", "form-control", "ml-2");
    a.appendChild(cancel);
    a.align = 'center';
    w.appendChild(a);
}

function cancel(argument) {
    var a = "";
    console.log(argument);
    a = "tablet_" + argument.charAt(7);
    a.toString();
    var element = document.getElementById(a);
    element.remove();
}
