const BASE_URL = "http://127.0.0.1:5000";

async function registerOrg() {
    const name = document.getElementById("orgName").value;

    try {
        const res = await fetch(BASE_URL + "/orgs", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: name })
        });

        if (!res.ok) throw new Error("Failed");

        alert("Organization Registered!");
    } catch (err) {
        console.error(err);
        alert("Error registering org");
    }
}

async function submitCTI() {
    const data = document.getElementById("ctiData").value;

    await fetch(BASE_URL + "/cti", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
       body: JSON.stringify({ cti_data: data })
    });

    alert("CTI Submitted!");
}

async function getCTI() {
    const response = await fetch(BASE_URL + "/cti");
    const data = await response.json();

    const list = document.getElementById("ctiList");
    list.innerHTML = "";

    data.forEach(item => {
        const li = document.createElement("li");
        li.textContent = "ID: " + item.id + " | Hash: " + item.hash;
        list.appendChild(li);
    });
}

async function rateCTI() {
    const id = document.getElementById("ctiId").value;
    const score = document.getElementById("score").value;

    await fetch(BASE_URL + "/rate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ctiId: id, score: score })
    });

    alert("Rating Submitted!");
}

async function getReputation() {
    const id = document.getElementById("repOrgId").value;

    const response = await fetch(BASE_URL + "/reputation/" + id);
    const data = await response.json();

    document.getElementById("repResult").innerText =
        "Reputation Score: " + data.reputation;
}
