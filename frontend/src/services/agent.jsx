async function stepAgents(time) {
    const res = await fetch('http://localhost:8000/step', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: time,
            type: 'message'
        }),
    })
    const data = await res.json();
    return data;
}

async function getAgents() {
    const res = await fetch('http://localhost:8000/agents');
    const data = await res.json();
    return data;
}

async function addContext(message) {
    const res = await fetch('http://localhost:8000/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message,
        }),
    });
    const data = await res.json();
    return data;
}

export { stepAgents, getAgents, addContext };